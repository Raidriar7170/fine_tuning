from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from voice2task.io import read_json, read_jsonl, write_jsonl
from voice2task.schemas import (
    PRIVATE_IP_RE,
    PRIVATE_PATH_RE,
    ROUTES,
    SECRET_RE,
    TASK_TYPES,
    BrowserTaskContract,
    SFTDatasetRow,
    ValidationError,
    as_contract,
)


@dataclass(frozen=True)
class EvaluationResult:
    metrics: dict[str, float]
    failure_slices: dict[str, dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {"metrics": dict(self.metrics), "failure_slices": self.failure_slices}


@dataclass(frozen=True)
class ExecutionSmokeResult:
    enabled: bool
    passed: int
    failed: int
    target: str | None
    notes: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "enabled": self.enabled,
            "passed": self.passed,
            "failed": self.failed,
            "target": self.target,
            "notes": self.notes,
        }


def _sanitize_id(value: str) -> str:
    sanitized = _sanitize_public_summary(value)
    sanitized = re.sub(r"[^A-Za-z0-9_.-]", "_", sanitized)
    return sanitized[:80]


def _prediction_to_contract(value: Any) -> BrowserTaskContract | None:
    try:
        if isinstance(value, str):
            parsed = json.loads(value)
        else:
            parsed = value
        if not isinstance(parsed, dict):
            return None
        return as_contract(parsed)
    except (json.JSONDecodeError, ValidationError, TypeError):
        return None


def _slot_f1(gold: dict[str, Any], predicted: dict[str, Any]) -> float:
    gold_items = {(str(key), str(value)) for key, value in gold.items()}
    predicted_items = {(str(key), str(value)) for key, value in predicted.items()}
    if not gold_items and not predicted_items:
        return 1.0
    if not gold_items or not predicted_items:
        return 0.0
    true_positive = len(gold_items & predicted_items)
    precision = true_positive / len(predicted_items)
    recall = true_positive / len(gold_items)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def _add_failure(failure_slices: dict[str, dict[str, Any]], category: str, row_id: str) -> None:
    entry = failure_slices.setdefault(category, {"count": 0, "examples": []})
    entry["count"] += 1
    if len(entry["examples"]) < 5:
        entry["examples"].append(_sanitize_id(row_id))


def evaluate_predictions(rows: list[SFTDatasetRow], predictions: dict[str, Any]) -> EvaluationResult:
    total = max(len(rows), 1)
    valid = 0
    task_type_matches = 0
    route_matches = 0
    confirmation_matches = 0
    exact_matches = 0
    slot_scores: list[float] = []
    safety_tp = safety_fp = safety_fn = 0
    failure_slices: dict[str, dict[str, Any]] = {
        category: {"count": 0, "examples": []}
        for category in ("schema", "task_type", "route", "safety", "confirmation", "slot", "unknown")
    }

    for row in rows:
        gold = as_contract(row.target_contract)
        predicted = _prediction_to_contract(predictions.get(row.id))
        if predicted is None:
            _add_failure(failure_slices, "schema", row.id)
            slot_scores.append(0.0)
            continue
        valid += 1
        if predicted.task_type == gold.task_type:
            task_type_matches += 1
        else:
            _add_failure(failure_slices, "task_type", row.id)
        if predicted.route == gold.route:
            route_matches += 1
        else:
            _add_failure(failure_slices, "route", row.id)
        if predicted.confirmation_required == gold.confirmation_required:
            confirmation_matches += 1
        else:
            _add_failure(failure_slices, "confirmation", row.id)

        predicted_safe_stop = not bool(predicted.safety["allow"])
        gold_safe_stop = not bool(gold.safety["allow"])
        if predicted_safe_stop and gold_safe_stop:
            safety_tp += 1
        elif predicted_safe_stop and not gold_safe_stop:
            safety_fp += 1
            _add_failure(failure_slices, "safety", row.id)
        elif not predicted_safe_stop and gold_safe_stop:
            safety_fn += 1
            _add_failure(failure_slices, "safety", row.id)

        slot_score = _slot_f1(gold.slots, predicted.slots)
        slot_scores.append(slot_score)
        if slot_score < 1.0:
            _add_failure(failure_slices, "slot", row.id)
        if predicted.to_dict() == gold.to_dict():
            exact_matches += 1

    safety_precision = 1.0 if safety_tp + safety_fp == 0 else safety_tp / (safety_tp + safety_fp)
    safety_recall = 1.0 if safety_tp + safety_fn == 0 else safety_tp / (safety_tp + safety_fn)
    metrics = {
        "json_valid_rate": valid / total,
        "task_type_accuracy": task_type_matches / total,
        "route_accuracy": route_matches / total,
        "safety_precision": safety_precision,
        "safety_recall": safety_recall,
        "safety_predicted_stop_support": float(safety_tp + safety_fp),
        "safety_gold_stop_support": float(safety_tp + safety_fn),
        "confirmation_accuracy": confirmation_matches / total,
        "slot_f1": sum(slot_scores) / total,
        "contract_exact_match": exact_matches / total,
    }
    return EvaluationResult(metrics=metrics, failure_slices=failure_slices)


_REQUIRED_CONTRACT_FIELDS = {
    "task_type",
    "route",
    "safety",
    "confirmation_required",
    "slots",
    "normalized_command",
    "language",
    "contract_version",
}


def _sanitize_public_summary(text: str) -> str:
    sanitized = PRIVATE_PATH_RE.sub("<private_path>", text)
    sanitized = PRIVATE_IP_RE.sub("<private_ip>", sanitized)
    return SECRET_RE.sub("<secret>", sanitized)


def _observed_value_summary(value: Any) -> str:
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return "empty string"
        return _sanitize_public_summary(f"string({len(value)}): {text[:80]}")
    if isinstance(value, dict):
        if not value:
            return "empty object"
        keys = ", ".join(sorted(str(key) for key in value.keys())[:8])
        return _sanitize_public_summary(f"object with keys: {keys}")
    if isinstance(value, list):
        return _sanitize_public_summary(f"array with {len(value)} item(s)")
    if value is None:
        return "null"
    return _sanitize_public_summary(f"{type(value).__name__}: {str(value)[:80]}")


def _alignment_value_summary(value: Any, *, missing: bool = False) -> str:
    if missing:
        return "missing"
    return _observed_value_summary(value)


def _issue(
    *,
    row_id: str,
    field_path: str,
    issue_category: str,
    observed_value: Any,
    expected_constraint: str,
) -> dict[str, str]:
    return {
        "row_id": _sanitize_id(row_id),
        "field_path": field_path,
        "issue_category": issue_category,
        "observed_value_summary": _observed_value_summary(observed_value),
        "expected_constraint": expected_constraint,
    }


_ALIGNMENT_FIELD_PATHS = (
    "task_type",
    "route",
    "safety.allow",
    "safety.reason",
    "confirmation_required",
    "slots",
    "normalized_command",
    "language",
    "contract_version",
)


_MISSING = object()


def _field_value(value: dict[str, Any], field_path: str) -> Any:
    current: Any = value
    for part in field_path.split("."):
        if not isinstance(current, dict) or part not in current:
            return _MISSING
        current = current[part]
    return current


def _alignment_mismatch(
    *,
    row_id: str,
    field_path: str,
    gold_value: Any,
    prediction_value: Any,
) -> dict[str, str]:
    gold_missing = gold_value is _MISSING
    prediction_missing = prediction_value is _MISSING
    if prediction_missing:
        mismatch_category = "missing_prediction_field"
    elif gold_missing:
        mismatch_category = "missing_gold_field"
    elif type(gold_value) is not type(prediction_value):
        mismatch_category = "type_mismatch"
    else:
        mismatch_category = "value_mismatch"
    return {
        "row_id": _sanitize_id(row_id),
        "field_path": field_path,
        "mismatch_category": mismatch_category,
        "gold_value_summary": _alignment_value_summary(gold_value, missing=gold_missing),
        "prediction_value_summary": _alignment_value_summary(prediction_value, missing=prediction_missing),
    }


def diagnose_alignment_mismatches(rows: list[SFTDatasetRow], predictions: dict[str, Any]) -> dict[str, Any]:
    diagnostics_rows: list[dict[str, Any]] = []
    field_mismatch_counts: dict[str, int] = {}
    category_counts: dict[str, int] = {}
    schema_invalid_prediction_count = 0

    for row in rows:
        gold = as_contract(row.target_contract).to_dict()
        raw_prediction = predictions.get(row.id)
        parsed_prediction = raw_prediction
        if isinstance(raw_prediction, str):
            try:
                parsed_prediction = json.loads(raw_prediction)
            except json.JSONDecodeError:
                parsed_prediction = None
        if _prediction_to_contract(raw_prediction) is None:
            schema_invalid_prediction_count += 1

        prediction_object = parsed_prediction if isinstance(parsed_prediction, dict) else {}
        mismatches: list[dict[str, str]] = []
        for field_path in _ALIGNMENT_FIELD_PATHS:
            gold_value = _field_value(gold, field_path)
            prediction_value = _field_value(prediction_object, field_path)
            if gold_value == prediction_value:
                continue
            mismatch = _alignment_mismatch(
                row_id=row.id,
                field_path=field_path,
                gold_value=gold_value,
                prediction_value=prediction_value,
            )
            mismatches.append(mismatch)
            field_mismatch_counts[field_path] = field_mismatch_counts.get(field_path, 0) + 1
            category = mismatch["mismatch_category"]
            category_counts[category] = category_counts.get(category, 0) + 1
        if mismatches:
            diagnostics_rows.append({"row_id": _sanitize_id(row.id), "mismatches": mismatches})

    return {
        "diagnostic_kind": "browser_task_contract_alignment_mismatch",
        "summary": {
            "gold_row_count": len(rows),
            "prediction_count": len(predictions),
            "row_mismatch_count": len(diagnostics_rows),
            "schema_invalid_prediction_count": schema_invalid_prediction_count,
            "field_mismatch_counts": dict(sorted(field_mismatch_counts.items())),
            "mismatch_category_counts": dict(sorted(category_counts.items())),
        },
        "rows": diagnostics_rows,
        "claims": {
            "invalid_predictions_remain_invalid": True,
            "field_level_public_sample_evidence_only": True,
            "checkpoint_release": False,
            "adapter_release": False,
            "production_readiness_claim": False,
            "full_private_corpus_claim": False,
            "live_browser_benchmark_claim": False,
        },
    }


def _diagnose_contract_object(row_id: str, prediction: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    missing = sorted(_REQUIRED_CONTRACT_FIELDS - set(prediction))
    for field_name in missing:
        issues.append(
            _issue(
                row_id=row_id,
                field_path=field_name,
                issue_category="missing_required_field",
                observed_value=None,
                expected_constraint="Browser Task Contract requires this top-level field",
            )
        )

    if "task_type" in prediction and prediction["task_type"] not in TASK_TYPES:
        issues.append(
            _issue(
                row_id=row_id,
                field_path="task_type",
                issue_category="invalid_enum",
                observed_value=prediction["task_type"],
                expected_constraint=f"must be one of {sorted(TASK_TYPES)}",
            )
        )
    if "route" in prediction and prediction["route"] not in ROUTES:
        issues.append(
            _issue(
                row_id=row_id,
                field_path="route",
                issue_category="invalid_enum",
                observed_value=prediction["route"],
                expected_constraint=f"must be one of {sorted(ROUTES)}",
            )
        )
    if "safety" in prediction:
        safety = prediction["safety"]
        if not isinstance(safety, dict):
            issues.append(
                _issue(
                    row_id=row_id,
                    field_path="safety",
                    issue_category="invalid_type",
                    observed_value=safety,
                    expected_constraint="must be an object with boolean allow and non-empty string reason",
                )
            )
        else:
            if "allow" not in safety:
                issues.append(
                    _issue(
                        row_id=row_id,
                        field_path="safety.allow",
                        issue_category="missing_required_field",
                        observed_value=None,
                        expected_constraint="must be a boolean",
                    )
                )
            elif not isinstance(safety["allow"], bool):
                issues.append(
                    _issue(
                        row_id=row_id,
                        field_path="safety.allow",
                        issue_category="invalid_type",
                        observed_value=safety["allow"],
                        expected_constraint="must be a boolean",
                    )
                )
            if "reason" not in safety:
                issues.append(
                    _issue(
                        row_id=row_id,
                        field_path="safety.reason",
                        issue_category="missing_required_field",
                        observed_value=None,
                        expected_constraint="must be a non-empty string",
                    )
                )
            elif not isinstance(safety["reason"], str):
                issues.append(
                    _issue(
                        row_id=row_id,
                        field_path="safety.reason",
                        issue_category="invalid_type",
                        observed_value=safety["reason"],
                        expected_constraint="must be a non-empty string",
                    )
                )
            elif not safety["reason"].strip():
                issues.append(
                    _issue(
                        row_id=row_id,
                        field_path="safety.reason",
                        issue_category="empty_required_string",
                        observed_value=safety["reason"],
                        expected_constraint="must be a non-empty string",
                )
            )
    if "confirmation_required" in prediction and not isinstance(prediction["confirmation_required"], bool):
        issues.append(
            _issue(
                row_id=row_id,
                field_path="confirmation_required",
                issue_category="invalid_type",
                observed_value=prediction["confirmation_required"],
                expected_constraint="must be a boolean",
            )
        )
    if "slots" in prediction and not isinstance(prediction["slots"], dict):
        issues.append(
            _issue(
                row_id=row_id,
                field_path="slots",
                issue_category="invalid_type",
                observed_value=prediction["slots"],
                expected_constraint="must be an object",
            )
        )
    if "normalized_command" in prediction:
        normalized_command = prediction["normalized_command"]
        if not isinstance(normalized_command, str):
            issues.append(
                _issue(
                    row_id=row_id,
                    field_path="normalized_command",
                    issue_category="invalid_type",
                    observed_value=normalized_command,
                    expected_constraint="must be a non-empty string",
                )
            )
        elif not normalized_command.strip():
            issues.append(
                _issue(
                    row_id=row_id,
                    field_path="normalized_command",
                    issue_category="empty_required_string",
                    observed_value=normalized_command,
                    expected_constraint="must be a non-empty string",
                )
            )
    if "language" in prediction and prediction["language"] != "zh-CN":
        issues.append(
            _issue(
                row_id=row_id,
                field_path="language",
                issue_category="invalid_literal",
                observed_value=prediction["language"],
                expected_constraint="must be zh-CN",
            )
        )
    if "contract_version" in prediction and prediction["contract_version"] != "v1":
        issues.append(
            _issue(
                row_id=row_id,
                field_path="contract_version",
                issue_category="invalid_literal",
                observed_value=prediction["contract_version"],
                expected_constraint="must be v1",
            )
        )
    return issues


def diagnose_schema_mismatches(rows: list[SFTDatasetRow], predictions: dict[str, Any]) -> dict[str, Any]:
    diagnostics_rows: list[dict[str, Any]] = []
    issue_counts: dict[str, int] = {}
    invalid_prediction_count = 0

    for row in rows:
        row_id = _sanitize_id(row.id)
        raw_prediction = predictions.get(row.id)
        parsed_prediction = raw_prediction
        issues: list[dict[str, str]] = []
        if isinstance(raw_prediction, str):
            try:
                parsed_prediction = json.loads(raw_prediction)
            except json.JSONDecodeError:
                issues.append(
                    _issue(
                        row_id=row.id,
                        field_path="$",
                        issue_category="invalid_json",
                        observed_value=raw_prediction,
                        expected_constraint="prediction must be a JSON object matching Browser Task Contract",
                    )
                )
        if not issues:
            if not isinstance(parsed_prediction, dict):
                issues.append(
                    _issue(
                        row_id=row.id,
                        field_path="$",
                        issue_category="invalid_type",
                        observed_value=parsed_prediction,
                        expected_constraint="prediction must be an object matching Browser Task Contract",
                    )
                )
            elif _prediction_to_contract(parsed_prediction) is None:
                issues.extend(_diagnose_contract_object(row.id, parsed_prediction))
                if not issues:
                    issues.append(
                        _issue(
                            row_id=row.id,
                            field_path="$",
                            issue_category="schema_validation_error",
                            observed_value=parsed_prediction,
                            expected_constraint="must satisfy Browser Task Contract validator",
                        )
                    )
        if issues:
            invalid_prediction_count += 1
            for issue in issues:
                issue_counts[issue["issue_category"]] = issue_counts.get(issue["issue_category"], 0) + 1
            diagnostics_rows.append({"row_id": row_id, "issues": issues})

    return {
        "diagnostic_kind": "browser_task_contract_schema_mismatch",
        "summary": {
            "gold_row_count": len(rows),
            "prediction_count": len(predictions),
            "invalid_prediction_count": invalid_prediction_count,
            "issue_counts": dict(sorted(issue_counts.items())),
        },
        "rows": diagnostics_rows,
        "claims": {
            "invalid_predictions_remain_invalid": True,
            "checkpoint_release": False,
            "adapter_release": False,
            "production_readiness_claim": False,
            "full_private_corpus_claim": False,
            "live_browser_benchmark_claim": False,
        },
    }


def rule_baseline_predictions(rows: list[SFTDatasetRow]) -> dict[str, dict[str, Any]]:
    predictions: dict[str, dict[str, Any]] = {}
    for row in rows:
        text = row.input_text
        if any(marker in text for marker in ("搜", "搜索", "查")):
            query = text.replace("帮我", "").replace("搜索", "").replace("搜", "").replace("查一下", "").strip()
            contract = BrowserTaskContract(
                task_type="search",
                route="search_web",
                safety={"allow": True, "reason": "public_readonly"},
                confirmation_required=False,
                slots={"query": query or text},
                normalized_command=f"搜索{query or text}",
            )
        elif "打开" in text:
            contract = BrowserTaskContract(
                task_type="navigate",
                route="open_url",
                safety={"allow": True, "reason": "public_readonly"},
                confirmation_required=False,
                slots={"url": "about:blank"},
                normalized_command=text,
            )
        else:
            contract = BrowserTaskContract(
                task_type="clarify",
                route="clarify",
                safety={"allow": False, "reason": "underspecified_request"},
                confirmation_required=True,
                slots={},
                normalized_command=text,
            )
        predictions[row.id] = contract.to_dict()
    return predictions


def prompt_fixture_predictions(rows: list[SFTDatasetRow], fixture_path: Path) -> dict[str, Any]:
    expected_ids = {row.id for row in rows}
    predictions = load_predictions(fixture_path)
    missing = sorted(expected_ids - set(predictions))
    if missing:
        raise ValidationError(f"prompt_fixture_missing_predictions: {', '.join(missing)}")
    return {row_id: predictions[row_id] for row_id in sorted(expected_ids)}


def _run_validation_command(command: list[str], row: SFTDatasetRow, contract: BrowserTaskContract) -> bool:
    payload = json.dumps(
        {"id": row.id, "input_text": row.input_text, "contract": contract.to_dict()},
        ensure_ascii=False,
    )
    completed = subprocess.run(
        command,
        input=payload,
        text=True,
        capture_output=True,
        check=False,
        timeout=10,
    )
    if completed.returncode != 0:
        return False
    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError:
        return False
    return bool(result.get("ok"))


def run_execution_smoke(
    rows: list[SFTDatasetRow],
    predictions: dict[str, Any],
    enabled: bool,
    target_path: Path | None = None,
) -> ExecutionSmokeResult:
    if not enabled:
        return ExecutionSmokeResult(enabled=False, passed=0, failed=0, target=None, notes="disabled")
    if target_path is None:
        return ExecutionSmokeResult(enabled=True, passed=0, failed=len(rows), target=None, notes="target_path_missing")
    target = read_json(target_path)
    command = target.get("command")
    if isinstance(command, list) and all(isinstance(item, str) for item in command):
        passed = 0
        failed = 0
        for row in rows:
            prediction = _prediction_to_contract(predictions.get(row.id))
            if prediction is not None and _run_validation_command(command, row, prediction):
                passed += 1
            else:
                failed += 1
        return ExecutionSmokeResult(
            enabled=True,
            passed=passed,
            failed=failed,
            target=target_path.as_posix(),
            notes="controlled_validation_command",
        )
    if target.get("accepts_contracts") is not True:
        return ExecutionSmokeResult(
            enabled=True,
            passed=0,
            failed=len(rows),
            target=target_path.as_posix(),
            notes="target_does_not_accept_contracts",
        )
    passed = sum(1 for row in rows if _prediction_to_contract(predictions.get(row.id)) is not None)
    return ExecutionSmokeResult(
        enabled=True,
        passed=passed,
        failed=len(rows) - passed,
        target=target_path.as_posix(),
        notes="controlled_contract_consumer_smoke",
    )


def load_sft_rows(path: Path) -> list[SFTDatasetRow]:
    return [SFTDatasetRow(**record) for record in read_jsonl(path)]


def load_predictions(path: Path) -> dict[str, Any]:
    predictions: dict[str, Any] = {}
    for record in read_jsonl(path):
        row_id = str(record.get("id", ""))
        if "prediction" in record:
            predictions[row_id] = record["prediction"]
        elif "contract" in record:
            predictions[row_id] = record["contract"]
        else:
            predictions[row_id] = {key: value for key, value in record.items() if key != "id"}
    return predictions


def write_predictions(path: Path, predictions: dict[str, dict[str, Any]]) -> None:
    write_jsonl(path, [{"id": row_id, "prediction": prediction} for row_id, prediction in predictions.items()])
