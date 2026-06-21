from __future__ import annotations

import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from voice2task.io import read_json, read_jsonl, write_json
from voice2task.schemas import ValidationError, as_contract, validate_public_record

CHANGE_ID = "analyze-slot-error-mechanisms-and-design-slot-representation"
SUCCESS_BOUNDARY_LABEL = "SLOT_ANALYSIS_INPUT_BOUNDARY_PASSED"
BLOCKED_LABEL = "ANALYSIS_BLOCKED_INVALID_INPUT"
ARMS = ("control", "treatment")
SPLITS = ("dev", "test")
REQUIRED_RAW_FILES = (
    "artifact-manifest.json",
    "boundary-verification.json",
    "metric-reproduction.json",
    "gold/dev_gold.jsonl",
    "gold/test_gold.jsonl",
    "control/dev_predictions.jsonl",
    "control/test_predictions.jsonl",
    "treatment/dev_predictions.jsonl",
    "treatment/test_predictions.jsonl",
)
SUCCESS_ARTIFACTS = (
    "summary.md",
    "summary.json",
    "slot-error-taxonomy.md",
    "slot-profile.json",
    "paired-error-movement.json",
    "representation-feasibility.json",
    "recommended-next-change.md",
)
ALL_ARTIFACTS = (*SUCCESS_ARTIFACTS, "blocked.json")
SUPPORTED_METRIC_STATUSES = {"reproduced", "passed"}
FINAL_DECISION_LABELS = (
    "COPY_OR_NORMALIZE_REPRESENTATION_JUSTIFIED",
    "TASK_SLOT_SCHEMA_CONSTRAINTS_FIRST",
    "TYPED_NORMALIZATION_FIRST",
    "MIXED_SLOT_REPRESENTATION_REQUIRED",
    "DATA_DIVERSITY_OR_GENERALIZATION_FIRST",
    "ANALYSIS_BLOCKED_OR_INCONCLUSIVE",
)
CORRECT_MECHANISMS = {"SLOT_CORRECT_EXACT", "SLOT_CORRECT_NORMALIZED", "SLOT_CORRECT_ABSENT"}
ALIAS_KEYS = {
    "query": ("search_text", "keyword", "keywords", "q"),
    "url": ("link", "uri", "website", "site"),
    "field": ("field_name", "form_field", "target_field"),
    "value": ("field_value", "input_value"),
    "target": ("extract_target", "content", "attribute"),
    "ambiguity": ("target", "clarification_target", "missing_info"),
    "reason": ("rationale", "deny_reason", "safety_reason"),
}


class _Missing:
    def __repr__(self) -> str:
        return "MISSING"


MISSING = _Missing()


def _rate(count: int, total: int) -> float:
    return 0.0 if total == 0 else count / total


def _clean_output_dir(output_dir: Path, *, keep_blocked: bool = False) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for filename in ALL_ARTIFACTS:
        path = output_dir / filename
        if path.exists() and not (keep_blocked and filename == "blocked.json"):
            path.unlink()


def _is_missing(value: Any) -> bool:
    return value is MISSING


def _jsonable(value: Any) -> Any:
    if _is_missing(value):
        return None
    if isinstance(value, dict):
        return {str(key): _jsonable(val) for key, val in sorted(value.items(), key=lambda item: str(item[0]))}
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    return value


def _as_text(value: Any) -> str | None:
    if _is_missing(value):
        return None
    if isinstance(value, (dict, list)):
        return None
    if value is None:
        return ""
    return str(value)


def _fold_text(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).casefold()
    return re.sub(r"[\s\W_]+", "", normalized, flags=re.UNICODE)


def _compact_text(value: str) -> str:
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", value).casefold())


def _canonical_url(value: str) -> str:
    text = unicodedata.normalize("NFKC", value).strip().casefold()
    text = re.sub(r"^https?://", "", text)
    text = text.rstrip("/")
    return text


def _canonical_number(value: str) -> str | None:
    text = unicodedata.normalize("NFKC", value).strip()
    if re.fullmatch(r"[+-]?\d+(?:\.\d+)?", text):
        return str(float(text)).rstrip("0").rstrip(".")
    return None


def _canonical_date(value: str) -> str | None:
    text = unicodedata.normalize("NFKC", value)
    match = re.search(r"(\d{4})[-年/](\d{1,2})[-月/](\d{1,2})日?", text)
    if not match:
        return None
    year, month, day = match.groups()
    return f"{int(year):04d}-{int(month):02d}-{int(day):02d}"


def _canonical_phone(value: str) -> str | None:
    digits = re.sub(r"\D+", "", unicodedata.normalize("NFKC", value))
    if len(digits) >= 7:
        return digits
    return None


def _canonical_bool(value: str) -> str | None:
    folded = _fold_text(value)
    truthy = {"true", "yes", "y", "1", "是", "需要", "确认", "开启", "打开"}
    falsey = {"false", "no", "n", "0", "否", "不需要", "无需", "关闭"}
    if folded in truthy:
        return "true"
    if folded in falsey:
        return "false"
    return None


def _normalization_candidates(value: str, *, slot_path: str = "") -> list[tuple[str, str]]:
    lower_path = slot_path.casefold()
    candidates = [("text_fold", _fold_text(value))]
    if "url" in lower_path or re.search(r"(https?://|www\.|[A-Za-z0-9-]+\.[A-Za-z]{2,})", value):
        candidates.append(("url_canonical", _canonical_url(value)))
    date = _canonical_date(value)
    if date is not None:
        candidates.append(("date_iso", date))
    number = _canonical_number(value)
    if number is not None:
        candidates.append(("number_canonical", number))
    phone = _canonical_phone(value)
    if phone is not None:
        candidates.append(("phone_digits", phone))
    boolean = _canonical_bool(value)
    if boolean is not None:
        candidates.append(("boolean_canonical", boolean))
    return [(rule, candidate) for rule, candidate in candidates if candidate]


def _matching_normalization_rule(left: Any, right: Any, *, slot_path: str = "") -> str | None:
    left_text = _as_text(left)
    right_text = _as_text(right)
    if left_text is None or right_text is None:
        return None
    for left_rule, left_value in _normalization_candidates(left_text, slot_path=slot_path):
        for right_rule, right_value in _normalization_candidates(right_text, slot_path=slot_path):
            if left_value == right_value:
                if left_rule == right_rule:
                    return left_rule
                if "url_canonical" in {left_rule, right_rule}:
                    return "url_canonical"
                if "date_iso" in {left_rule, right_rule}:
                    return "date_iso"
                return right_rule
    return None


def _normalization_failure_rule(left: Any, right: Any, *, slot_path: str = "") -> str | None:
    left_text = _as_text(left)
    right_text = _as_text(right)
    if left_text is None or right_text is None:
        return None
    left_candidates = dict(_normalization_candidates(left_text, slot_path=slot_path))
    right_candidates = dict(_normalization_candidates(right_text, slot_path=slot_path))
    for rule in ("url_canonical", "date_iso", "number_canonical", "phone_digits", "boolean_canonical"):
        if rule in left_candidates and rule in right_candidates and left_candidates[rule] != right_candidates[rule]:
            return rule
    return None


def _value_equal_normalized(left: Any, right: Any, *, slot_path: str = "") -> bool:
    return _matching_normalization_rule(left, right, slot_path=slot_path) is not None


def _partial_overlap(value: str, source_text: str) -> bool:
    folded_value = _fold_text(value)
    folded_source = _fold_text(source_text)
    if len(folded_value) < 2 or not folded_source:
        return False
    if folded_value in folded_source or folded_source in folded_value:
        return True
    value_chars = set(folded_value)
    source_chars = set(folded_source)
    return len(value_chars & source_chars) >= max(2, min(len(value_chars), 4))


def _source_rule(value: Any, source_text: str, *, slot_path: str) -> tuple[str, str | None]:
    text = _as_text(value)
    if text is None:
        return "unsupported_analysis", None
    if not text.strip():
        return "source_absent_or_generation_required", None
    if text in source_text:
        return "exact_source_supported", None
    value_folded = _fold_text(text)
    source_folded = _fold_text(source_text)
    if value_folded and value_folded in source_folded:
        return "normalized_source_supported", "text_fold"
    for rule, candidate in _normalization_candidates(text, slot_path=slot_path):
        if not candidate:
            continue
        for _, source_candidate in _normalization_candidates(source_text, slot_path=slot_path):
            if candidate == source_candidate:
                category = _support_category_for_rule(rule)
                return category, rule
        if _fold_text(candidate) in source_folded:
            category = _support_category_for_rule(rule)
            return category, rule
    return "source_absent_or_generation_required", None


def _support_category_for_rule(rule: str) -> str:
    if rule in {"text_fold", "url_canonical"}:
        return "normalized_source_supported"
    return "typed_derivable"


def flatten_slot_values(slots: dict[str, Any]) -> dict[str, Any]:
    flattened: dict[str, Any] = {}

    def visit(value: Any, prefix: str) -> None:
        if isinstance(value, dict):
            for key in sorted(value, key=str):
                next_prefix = f"{prefix}.{key}" if prefix else str(key)
                visit(value[key], next_prefix)
            return
        if isinstance(value, list):
            for index, item in enumerate(value):
                visit(item, f"{prefix}[{index}]")
            return
        flattened[prefix] = value

    visit(slots, "")
    return {key: flattened[key] for key in sorted(flattened)}


def classify_source_support(value: Any, source_text: str, *, slot_path: str) -> dict[str, Any]:
    category, rule = _source_rule(value, source_text, slot_path=slot_path)
    return {"category": category, "rule": rule}


def classify_prediction_provenance(value: Any, source_text: str, *, slot_path: str) -> dict[str, Any]:
    text = _as_text(value)
    if _is_missing(value):
        return {"category": "unavailable", "rule": None}
    if text is None:
        return {"category": "non_string_or_complex", "rule": None}
    if not text.strip():
        return {"category": "unavailable", "rule": None}
    if text in source_text:
        return {"category": "exact_span_from_source", "rule": None}
    support = classify_source_support(text, source_text, slot_path=slot_path)
    if support["category"] == "normalized_source_supported":
        return {"category": "normalized_span_from_source", "rule": support["rule"]}
    if support["category"] == "typed_derivable":
        return {"category": "deterministic_derived", "rule": support["rule"]}
    if _partial_overlap(text, source_text):
        return {"category": "partial_span_from_source", "rule": None}
    return {"category": "unsupported_by_source", "rule": None}


def classify_slot_pair(
    *,
    slot_path: str,
    gold_value: Any,
    predicted_value: Any,
    source_text: str,
    task_type: str,
    alias_key_candidate: str | None = None,
    alias_value: Any = MISSING,
    semantic_key_candidate: str | None = None,
    semantic_value: Any = MISSING,
) -> dict[str, Any]:
    source_support = classify_source_support(gold_value, source_text, slot_path=slot_path)
    prediction_provenance = classify_prediction_provenance(predicted_value, source_text, slot_path=slot_path)
    normalization_rule: str | None = None
    secondary_tags: list[str] = []

    if _is_missing(gold_value) and _is_missing(predicted_value):
        primary = "SLOT_CORRECT_ABSENT"
    elif _is_missing(gold_value):
        primary = "EXTRA_SLOT_KEY"
    elif _is_missing(predicted_value):
        if alias_key_candidate and _value_equal_normalized(gold_value, alias_value, slot_path=slot_path):
            primary = "WRONG_SLOT_KEY_ALIAS"
            secondary_tags.append("alias_policy_diagnostic_only")
        elif semantic_key_candidate and _value_equal_normalized(gold_value, semantic_value, slot_path=slot_path):
            primary = "WRONG_SLOT_KEY_SEMANTIC"
            secondary_tags.append("semantic_key_policy_diagnostic_only")
        else:
            primary = "MISSING_SLOT_KEY"
    elif type(gold_value) is not type(predicted_value) and (
        isinstance(gold_value, (dict, list)) or isinstance(predicted_value, (dict, list))
    ):
        primary = "MULTIVALUE_STRUCTURE_FAILURE"
    elif gold_value == predicted_value:
        primary = "SLOT_CORRECT_EXACT"
    else:
        normalization_rule = _matching_normalization_rule(gold_value, predicted_value, slot_path=slot_path)
        if normalization_rule is not None:
            primary = "SLOT_CORRECT_NORMALIZED"
        elif isinstance(gold_value, (dict, list)) or isinstance(predicted_value, (dict, list)):
            primary = "MULTIVALUE_STRUCTURE_FAILURE"
        elif type(gold_value) is not type(predicted_value):
            primary = "TYPE_MISMATCH"
        else:
            gold_text = _as_text(gold_value) or ""
            predicted_text = _as_text(predicted_value) or ""
            normalization_failure_rule = _normalization_failure_rule(
                gold_value,
                predicted_value,
                slot_path=slot_path,
            )
            if normalization_failure_rule is not None:
                normalization_rule = normalization_failure_rule
                primary = "NORMALIZATION_FAILURE"
            elif not predicted_text.strip():
                primary = "UNCLASSIFIED_SLOT_FAILURE"
            elif _partial_overlap(predicted_text, gold_text) or _partial_overlap(gold_text, predicted_text):
                primary = "PARTIAL_VALUE_SPAN"
            elif task_type == "clarify" or slot_path.startswith("ambiguity"):
                primary = "CLARIFY_AMBIGUITY_REPRESENTATION_FAILURE"
            elif source_support["category"] == "source_absent_or_generation_required":
                primary = "UNSUPPORTED_OR_HALLUCINATED_VALUE"
            elif prediction_provenance["category"] == "unsupported_by_source":
                primary = "SOURCE_COPY_FAILURE"
            elif source_support["category"] == "typed_derivable":
                primary = "DERIVED_VALUE_FAILURE"
            elif prediction_provenance["category"] in {
                "exact_span_from_source",
                "normalized_span_from_source",
                "deterministic_derived",
                "partial_span_from_source",
            }:
                primary = "WRONG_ENTITY_OR_VALUE"
            else:
                primary = "UNCLASSIFIED_SLOT_FAILURE"

    return {
        "slot_path": slot_path,
        "primary_mechanism": primary,
        "secondary_tags": sorted(set(secondary_tags)),
        "is_correct": primary in CORRECT_MECHANISMS,
        "normalization_rule": normalization_rule,
        "source_support": source_support,
        "prediction_provenance": prediction_provenance,
        "alias_key_candidate": alias_key_candidate,
        "semantic_key_candidate": semantic_key_candidate,
        "strict_match_repaired_by_alias": False,
        "gold_value_type": "missing" if _is_missing(gold_value) else type(gold_value).__name__,
        "predicted_value_type": "missing" if _is_missing(predicted_value) else type(predicted_value).__name__,
    }


def compare_paired_slot_outcomes(control: dict[str, Any], treatment: dict[str, Any]) -> dict[str, Any]:
    control_correct = bool(control.get("is_correct"))
    treatment_correct = bool(treatment.get("is_correct"))
    control_mechanism = str(control.get("primary_mechanism"))
    treatment_mechanism = str(treatment.get("primary_mechanism"))

    if control_correct and treatment_correct:
        movement = "CORRECT_IN_BOTH"
    elif not control_correct and treatment_correct:
        if control_mechanism == "MISSING_SLOT_KEY":
            movement = "SLOT_ADDED_CORRECTLY"
        elif control_mechanism == "EXTRA_SLOT_KEY":
            movement = "SLOT_REMOVED_CORRECTLY"
        else:
            movement = "RECOVERED_BY_TREATMENT"
    elif control_correct and not treatment_correct:
        if treatment_mechanism == "MISSING_SLOT_KEY":
            movement = "SLOT_REMOVED_INCORRECTLY"
        elif treatment_mechanism == "EXTRA_SLOT_KEY":
            movement = "SLOT_ADDED_INCORRECTLY"
        else:
            movement = "INTRODUCED_BY_TREATMENT"
    elif control_mechanism == treatment_mechanism:
        movement = "ERROR_IN_BOTH_SAME_MECHANISM"
    else:
        movement = "ERROR_IN_BOTH_DIFFERENT_MECHANISM"

    return {
        "slot_path": control.get("slot_path") or treatment.get("slot_path"),
        "movement": movement,
        "control_primary_mechanism": control_mechanism,
        "treatment_primary_mechanism": treatment_mechanism,
        "control_correct": control_correct,
        "treatment_correct": treatment_correct,
    }


def validate_slot_analysis_inputs(raw_inputs_dir: Path) -> dict[str, Any]:
    raw_inputs_dir = Path(raw_inputs_dir)
    reasons: list[str] = []
    if (raw_inputs_dir / "blocked.json").exists():
        reasons.append("blocked_json_present")
    missing_files = [relative for relative in REQUIRED_RAW_FILES if not (raw_inputs_dir / relative).is_file()]
    reasons.extend(f"missing_required_file:{relative}" for relative in missing_files)
    if missing_files:
        return _boundary_payload(raw_inputs_dir, reasons)

    try:
        manifest = read_json(raw_inputs_dir / "artifact-manifest.json")
        boundary = read_json(raw_inputs_dir / "boundary-verification.json")
        metric_reproduction = read_json(raw_inputs_dir / "metric-reproduction.json")
    except (OSError, ValueError) as exc:
        return _boundary_payload(raw_inputs_dir, [f"invalid_boundary_json:{exc.__class__.__name__}"])

    if manifest.get("projection_inputs_ready") is not True:
        reasons.append("projection_inputs_ready_not_true")
    metric_status = str(metric_reproduction.get("status") or manifest.get("metric_reproduction_status") or "")
    if metric_status not in SUPPORTED_METRIC_STATUSES:
        reasons.append("metric_reproduction_not_accepted")
    if manifest.get("recovery_method") != "recovered_from_existing_artifacts":
        reasons.append("invalid_recovery_method")
    if manifest.get("sanitization_status") != "passed":
        reasons.append("sanitization_not_passed")
    if boundary.get("blocking_reasons"):
        reasons.append("boundary_blocking_reasons_present")
    for key in (
        "comparison_allowed",
        "control_treatment_ids_match",
        "control_gold_ids_match",
        "treatment_gold_ids_match",
        "dev_gold_hash_match",
        "test_gold_hash_match",
        "input_hash_match",
    ):
        if boundary.get(key) is not True:
            reasons.append(f"{key}_not_true")

    split_payload: dict[str, Any] = {}
    try:
        for split in SPLITS:
            gold_rows = read_jsonl(raw_inputs_dir / f"gold/{split}_gold.jsonl")
            control_rows = read_jsonl(raw_inputs_dir / f"control/{split}_predictions.jsonl")
            treatment_rows = read_jsonl(raw_inputs_dir / f"treatment/{split}_predictions.jsonl")
            split_reasons = _validate_split_rows(split, gold_rows, control_rows, treatment_rows)
            reasons.extend(f"{split}:{reason}" for reason in split_reasons)
            split_payload[split] = {
                "row_count": len(gold_rows),
                "control_row_count": len(control_rows),
                "treatment_row_count": len(treatment_rows),
                "sample_ids_match": not split_reasons,
            }
    except (OSError, ValueError, ValidationError, KeyError, TypeError) as exc:
        reasons.append(f"invalid_jsonl:{exc.__class__.__name__}")

    manifest_splits = {
        "dev": {"row_count": manifest.get("dev_row_count")},
        "test": {"row_count": manifest.get("test_row_count")},
    }
    for split, payload in split_payload.items():
        expected_count = manifest_splits.get(split, {}).get("row_count")
        if expected_count is not None and payload["row_count"] != expected_count:
            reasons.append(f"{split}:manifest_row_count_mismatch")
        boundary_split = boundary.get("splits", {}).get(split, {}) if isinstance(boundary.get("splits"), dict) else {}
        if isinstance(boundary_split, dict):
            for key in ("sample_id_hash", "gold_hash"):
                manifest_key = f"{split}_{key}"
                if key in boundary_split and manifest_key in manifest and boundary_split[key] != manifest[manifest_key]:
                    reasons.append(f"{split}:{key}_manifest_mismatch")

    return _boundary_payload(
        raw_inputs_dir,
        sorted(set(reasons)),
        manifest=manifest,
        metric_reproduction=metric_reproduction,
        splits=split_payload,
    )


def _boundary_payload(
    raw_inputs_dir: Path,
    reasons: list[str],
    *,
    manifest: dict[str, Any] | None = None,
    metric_reproduction: dict[str, Any] | None = None,
    splits: dict[str, Any] | None = None,
) -> dict[str, Any]:
    manifest = manifest or {}
    metric_reproduction = metric_reproduction or {}
    accepted = not reasons
    return {
        "decision_label": SUCCESS_BOUNDARY_LABEL if accepted else BLOCKED_LABEL,
        "blocking_reasons": sorted(set(reasons)),
        "projection_inputs_ready": manifest.get("projection_inputs_ready") is True and accepted,
        "metric_reproduction_status": metric_reproduction.get("status") or manifest.get("metric_reproduction_status"),
        "control_treatment_ids_match": accepted,
        "gold_ids_match": accepted,
        "prediction_contract_used_for_analysis": accepted,
        "raw_model_output_used_for_analysis": False,
        "superseded_adapter_outputs_used": False,
        "recovery_method": manifest.get("recovery_method"),
        "recovered_provenance_valid": manifest.get("recovery_method") == "recovered_from_existing_artifacts",
        "splits": splits or {},
        "approved_raw_inputs": "reports/public-sample/step-matched-canonical-slot-ablation/raw-inputs",
    }


def _validate_split_rows(
    split: str,
    gold_rows: list[dict[str, Any]],
    control_rows: list[dict[str, Any]],
    treatment_rows: list[dict[str, Any]],
) -> list[str]:
    reasons: list[str] = []
    gold_ids = [str(row.get("sample_id", "")) for row in gold_rows]
    control_ids = [str(row.get("sample_id", "")) for row in control_rows]
    treatment_ids = [str(row.get("sample_id", "")) for row in treatment_rows]
    if len(set(gold_ids)) != len(gold_ids):
        reasons.append("duplicate_gold_ids")
    if len(set(control_ids)) != len(control_ids):
        reasons.append("duplicate_control_ids")
    if len(set(treatment_ids)) != len(treatment_ids):
        reasons.append("duplicate_treatment_ids")
    if control_ids != treatment_ids:
        reasons.append("control_treatment_id_mismatch")
    if gold_ids != control_ids or gold_ids != treatment_ids:
        reasons.append("gold_prediction_id_mismatch")
    for rows, role in ((gold_rows, "gold"), (control_rows, "control"), (treatment_rows, "treatment")):
        for row in rows:
            if row.get("split") != split:
                reasons.append(f"{role}_split_mismatch")
                break
            if not isinstance(row.get("input_text"), str) or not row["input_text"].strip():
                reasons.append(f"{role}_missing_input_text")
                break
            if role == "gold":
                as_contract(row["gold_contract"])
            else:
                as_contract(row["gold_contract"])
                as_contract(row["prediction_contract"])
                if row.get("parse_status") != "valid":
                    reasons.append(f"{role}_parse_status_not_valid")
                    break
                if row.get("run_role") != role:
                    reasons.append(f"{role}_run_role_mismatch")
                    break
                provenance = row.get("provenance") if isinstance(row.get("provenance"), dict) else {}
                if provenance.get("recovery_method") != "recovered_from_existing_artifacts":
                    reasons.append(f"{role}_invalid_recovered_provenance")
                    break
    return sorted(set(reasons))


def generate_slot_error_mechanism_analysis(raw_inputs_dir: Path, output_dir: Path) -> dict[str, Any]:
    boundary = validate_slot_analysis_inputs(raw_inputs_dir)
    output_dir = Path(output_dir)
    _clean_output_dir(output_dir)
    if boundary["decision_label"] != SUCCESS_BOUNDARY_LABEL:
        blocked = _blocked_summary(boundary)
        write_json(output_dir / "blocked.json", blocked)
        return blocked

    rows = _load_analysis_rows(Path(raw_inputs_dir))
    analysis = _analyze_rows(rows)
    summary = _build_summary(boundary, analysis)
    _write_success_artifacts(output_dir, summary, analysis)
    return summary


def _blocked_summary(boundary: dict[str, Any]) -> dict[str, Any]:
    return {
        "evidence_kind": "slot_error_mechanism_analysis",
        "decision_label": BLOCKED_LABEL,
        "source_boundary": boundary,
        "blocking_reasons": boundary["blocking_reasons"],
        "claims": _claim_boundaries(),
    }


def _load_analysis_rows(raw_inputs_dir: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split in SPLITS:
        gold_by_id = {str(row["sample_id"]): row for row in read_jsonl(raw_inputs_dir / f"gold/{split}_gold.jsonl")}
        control_by_id = {
            str(row["sample_id"]): row for row in read_jsonl(raw_inputs_dir / f"control/{split}_predictions.jsonl")
        }
        treatment_by_id = {
            str(row["sample_id"]): row for row in read_jsonl(raw_inputs_dir / f"treatment/{split}_predictions.jsonl")
        }
        for sample_id in sorted(gold_by_id):
            gold_row = gold_by_id[sample_id]
            rows.append(
                {
                    "sample_id": sample_id,
                    "split": split,
                    "input_text": gold_row["input_text"],
                    "gold_contract": as_contract(gold_row["gold_contract"]).to_dict(),
                    "control_contract": as_contract(control_by_id[sample_id]["prediction_contract"]).to_dict(),
                    "treatment_contract": as_contract(treatment_by_id[sample_id]["prediction_contract"]).to_dict(),
                }
            )
    return rows


def _analyze_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    source_counter: Counter[str] = Counter()
    prediction_counter: Counter[str] = Counter()
    mechanism_counter: Counter[str] = Counter()
    movement_counter: Counter[str] = Counter()
    split_counter: dict[str, Counter[str]] = defaultdict(Counter)
    family_counter: dict[str, Counter[str]] = defaultdict(Counter)
    gold_source_breakdowns = _empty_source_breakdowns()
    prediction_source_breakdowns = _empty_source_breakdowns(include_run_role=True)
    slot_profiles: dict[str, dict[str, Any]] = {}
    movements: list[dict[str, Any]] = []
    total_gold_slots = 0
    total_prediction_slots = 0

    for row in rows:
        sample_id = row["sample_id"]
        split = row["split"]
        source_text = row["input_text"]
        gold_contract = row["gold_contract"]
        task_type = gold_contract["task_type"]
        route = gold_contract["route"]
        task_family = f"{gold_contract['task_type']}:{gold_contract['route']}"
        gold_slots = flatten_slot_values(gold_contract["slots"])
        control_slots = flatten_slot_values(row["control_contract"]["slots"])
        treatment_slots = flatten_slot_values(row["treatment_contract"]["slots"])
        all_paths = sorted(set(gold_slots) | set(control_slots) | set(treatment_slots))

        for slot_path in all_paths:
            gold_value = gold_slots.get(slot_path, MISSING)
            control_value = control_slots.get(slot_path, MISSING)
            treatment_value = treatment_slots.get(slot_path, MISSING)
            control_alias_key, control_alias_value = _alias_candidate(slot_path, gold_value, control_slots)
            treatment_alias_key, treatment_alias_value = _alias_candidate(slot_path, gold_value, treatment_slots)
            control_semantic_key, control_semantic_value = _semantic_key_candidate(slot_path, gold_value, control_slots)
            treatment_semantic_key, treatment_semantic_value = _semantic_key_candidate(
                slot_path,
                gold_value,
                treatment_slots,
            )
            control = classify_slot_pair(
                slot_path=slot_path,
                gold_value=gold_value,
                predicted_value=control_value,
                source_text=source_text,
                task_type=task_type,
                alias_key_candidate=control_alias_key,
                alias_value=control_alias_value,
                semantic_key_candidate=control_semantic_key,
                semantic_value=control_semantic_value,
            )
            treatment = classify_slot_pair(
                slot_path=slot_path,
                gold_value=gold_value,
                predicted_value=treatment_value,
                source_text=source_text,
                task_type=task_type,
                alias_key_candidate=treatment_alias_key,
                alias_value=treatment_alias_value,
                semantic_key_candidate=treatment_semantic_key,
                semantic_value=treatment_semantic_value,
            )
            movement = compare_paired_slot_outcomes(control, treatment)
            movement.update(
                {
                    "sample_id": sample_id,
                    "split": split,
                    "task_family": task_family,
                    "slot_path": slot_path,
                }
            )
            movements.append(movement)
            movement_counter[movement["movement"]] += 1
            split_counter[split][movement["movement"]] += 1
            family_counter[task_family][movement["movement"]] += 1
            for run_role, value, outcome in (
                ("control", control_value, control),
                ("treatment", treatment_value, treatment),
            ):
                if outcome["primary_mechanism"] != "SLOT_CORRECT_ABSENT":
                    mechanism_counter[outcome["primary_mechanism"]] += 1
                prediction_category = outcome["prediction_provenance"]["category"]
                prediction_counter[prediction_category] += 1
                if not _is_missing(value):
                    total_prediction_slots += 1
                    _add_prediction_source_breakdown(
                        prediction_source_breakdowns,
                        category=prediction_category,
                        split=split,
                        run_role=run_role,
                        task_type=task_type,
                        route=route,
                        slot_path=slot_path,
                    )
            if not _is_missing(gold_value):
                total_gold_slots += 1
                source_category = classify_source_support(gold_value, source_text, slot_path=slot_path)["category"]
                source_counter[source_category] += 1
                _add_gold_source_breakdown(
                    gold_source_breakdowns,
                    category=source_category,
                    split=split,
                    task_type=task_type,
                    route=route,
                    slot_path=slot_path,
                )
            _update_slot_profile(
                slot_profiles,
                slot_path=slot_path,
                task_family=task_family,
                split=split,
                gold_value=gold_value,
                control_value=control_value,
                treatment_value=treatment_value,
                control=control,
                treatment=treatment,
                movement=movement,
            )

    profile_payload = [
        _finalize_slot_profile(slot_path, profile) for slot_path, profile in sorted(slot_profiles.items())
    ]
    movement_payload = _movement_payload(movements, movement_counter, split_counter, family_counter)
    feasibility = _representation_feasibility(profile_payload, movement_payload)
    return {
        "source_support_counts": dict(sorted(source_counter.items())),
        "prediction_provenance_counts": dict(sorted(prediction_counter.items())),
        "mechanism_counts": dict(sorted(mechanism_counter.items())),
        "summary_counts": {
            "samples": len(rows),
            "gold_slot_events": total_gold_slots,
            "prediction_slot_events": total_prediction_slots,
        },
        "source_support_breakdowns": _source_support_breakdown_payload(
            gold_source_breakdowns,
            prediction_source_breakdowns,
        ),
        "slot_profiles": profile_payload,
        "paired_movement": movement_payload,
        "representation_feasibility": feasibility,
    }


def _alias_candidate(slot_path: str, gold_value: Any, predicted_slots: dict[str, Any]) -> tuple[str | None, Any]:
    if _is_missing(gold_value) or slot_path in predicted_slots:
        return None, MISSING
    aliases = ALIAS_KEYS.get(slot_path, ())
    for alias in aliases:
        if alias in predicted_slots and _value_equal_normalized(
            gold_value,
            predicted_slots[alias],
            slot_path=slot_path,
        ):
            return alias, predicted_slots[alias]
    return None, MISSING


def _semantic_key_candidate(slot_path: str, gold_value: Any, predicted_slots: dict[str, Any]) -> tuple[str | None, Any]:
    if _is_missing(gold_value) or slot_path in predicted_slots:
        return None, MISSING
    aliases = set(ALIAS_KEYS.get(slot_path, ()))
    for candidate_path, candidate_value in sorted(predicted_slots.items()):
        if candidate_path == slot_path or candidate_path in aliases:
            continue
        if _value_equal_normalized(gold_value, candidate_value, slot_path=slot_path):
            return candidate_path, candidate_value
    return None, MISSING


def _empty_source_breakdowns(*, include_run_role: bool = False) -> dict[str, Any]:
    breakdowns: dict[str, Any] = {
        "overall": Counter(),
        "by_split": defaultdict(Counter),
        "by_task_type": defaultdict(Counter),
        "by_route": defaultdict(Counter),
        "by_slot_path": defaultdict(Counter),
    }
    if include_run_role:
        breakdowns["by_run_role"] = defaultdict(Counter)
    return breakdowns


def _add_gold_source_breakdown(
    breakdowns: dict[str, Any],
    *,
    category: str,
    split: str,
    task_type: str,
    route: str,
    slot_path: str,
) -> None:
    _add_source_breakdown(
        breakdowns,
        category=category,
        split=split,
        task_type=task_type,
        route=route,
        slot_path=slot_path,
    )


def _add_prediction_source_breakdown(
    breakdowns: dict[str, Any],
    *,
    category: str,
    split: str,
    run_role: str,
    task_type: str,
    route: str,
    slot_path: str,
) -> None:
    _add_source_breakdown(
        breakdowns,
        category=category,
        split=split,
        task_type=task_type,
        route=route,
        slot_path=slot_path,
    )
    breakdowns["by_run_role"][run_role][category] += 1


def _add_source_breakdown(
    breakdowns: dict[str, Any],
    *,
    category: str,
    split: str,
    task_type: str,
    route: str,
    slot_path: str,
) -> None:
    breakdowns["overall"][category] += 1
    breakdowns["by_split"][split][category] += 1
    breakdowns["by_task_type"][task_type][category] += 1
    breakdowns["by_route"][route][category] += 1
    breakdowns["by_slot_path"][slot_path][category] += 1


def _source_support_breakdown_payload(
    gold_breakdowns: dict[str, Any],
    prediction_breakdowns: dict[str, Any],
) -> dict[str, Any]:
    return {
        "gold_values": {
            "event_unit": "one non-missing gold slot value",
            "denominator_name": "gold_slot_events",
            "overall": _counter_rate_payload(gold_breakdowns["overall"]),
            "by_split": _counter_map_payload(gold_breakdowns["by_split"]),
            "by_task_type": _counter_map_payload(gold_breakdowns["by_task_type"]),
            "by_route": _counter_map_payload(gold_breakdowns["by_route"]),
            "by_slot_path": _counter_map_payload(gold_breakdowns["by_slot_path"]),
        },
        "predicted_values": {
            "event_unit": "one non-missing prediction slot value per run_role",
            "denominator_name": "prediction_slot_events",
            "overall": _counter_rate_payload(prediction_breakdowns["overall"]),
            "by_split": _counter_map_payload(prediction_breakdowns["by_split"]),
            "by_run_role": _counter_map_payload(prediction_breakdowns["by_run_role"]),
            "by_task_type": _counter_map_payload(prediction_breakdowns["by_task_type"]),
            "by_route": _counter_map_payload(prediction_breakdowns["by_route"]),
            "by_slot_path": _counter_map_payload(prediction_breakdowns["by_slot_path"]),
        },
    }


def _counter_map_payload(counter_map: dict[str, Counter[str]]) -> dict[str, Any]:
    return {
        label: _counter_rate_payload(counter)
        for label, counter in sorted(counter_map.items(), key=lambda item: item[0])
    }


def _counter_rate_payload(counter: Counter[str]) -> dict[str, Any]:
    event_count = sum(counter.values())
    counts = dict(sorted(counter.items()))
    return {
        "event_count": event_count,
        "counts": counts,
        "rates": {category: _rate(count, event_count) for category, count in counts.items()},
    }


def _update_slot_profile(
    profiles: dict[str, dict[str, Any]],
    *,
    slot_path: str,
    task_family: str,
    split: str,
    gold_value: Any,
    control_value: Any,
    treatment_value: Any,
    control: dict[str, Any],
    treatment: dict[str, Any],
    movement: dict[str, Any],
) -> None:
    profile = profiles.setdefault(
        slot_path,
        {
            "slot_path": slot_path,
            "sample_count": 0,
            "task_family_counts": Counter(),
            "split_counts": Counter(),
            "source_support_counts": Counter(),
            "mechanism_counts": Counter(),
            "movement_counts": Counter(),
            "prediction_provenance_counts": Counter(),
            "missing_key_count": 0,
            "extra_key_count": 0,
            "wrong_entity_count": 0,
            "partial_span_count": 0,
            "unsupported_prediction_count": 0,
            "typed_derivable_count": 0,
            "copyable_count": 0,
            "gold_events": 0,
            "prediction_events": 0,
        },
    )
    profile["sample_count"] += 1
    profile["task_family_counts"][task_family] += 1
    profile["split_counts"][split] += 1
    profile["movement_counts"][movement["movement"]] += 1
    for value, outcome in ((control_value, control), (treatment_value, treatment)):
        mechanism = outcome["primary_mechanism"]
        provenance = outcome["prediction_provenance"]["category"]
        profile["mechanism_counts"][mechanism] += 1
        profile["prediction_provenance_counts"][provenance] += 1
        if mechanism == "MISSING_SLOT_KEY":
            profile["missing_key_count"] += 1
        if mechanism == "EXTRA_SLOT_KEY":
            profile["extra_key_count"] += 1
        if mechanism == "WRONG_ENTITY_OR_VALUE":
            profile["wrong_entity_count"] += 1
        if mechanism == "PARTIAL_VALUE_SPAN":
            profile["partial_span_count"] += 1
        if provenance == "unsupported_by_source":
            profile["unsupported_prediction_count"] += 1
        if not _is_missing(value):
            profile["prediction_events"] += 1
    if not _is_missing(gold_value):
        support = control["source_support"]["category"]
        profile["source_support_counts"][support] += 1
        profile["gold_events"] += 1
        if support in {"exact_source_supported", "normalized_source_supported"}:
            profile["copyable_count"] += 1
        if support == "typed_derivable":
            profile["typed_derivable_count"] += 1


def _finalize_slot_profile(slot_path: str, profile: dict[str, Any]) -> dict[str, Any]:
    sample_count = int(profile["sample_count"])
    gold_events = int(profile["gold_events"])
    prediction_events = int(profile["prediction_events"])
    movement_counts = dict(sorted(profile["movement_counts"].items()))
    representation = _recommended_representation(profile)
    confidence = _confidence_level(sample_count, movement_counts)
    return {
        "slot_path": slot_path,
        "sample_count": sample_count,
        "task_family_counts": dict(sorted(profile["task_family_counts"].items())),
        "split_counts": dict(sorted(profile["split_counts"].items())),
        "source_support_counts": dict(sorted(profile["source_support_counts"].items())),
        "prediction_provenance_counts": dict(sorted(profile["prediction_provenance_counts"].items())),
        "mechanism_counts": dict(sorted(profile["mechanism_counts"].items())),
        "movement_counts": movement_counts,
        "copyable_rate": _rate(int(profile["copyable_count"]), gold_events),
        "typed_derivable_rate": _rate(int(profile["typed_derivable_count"]), gold_events),
        "missing_key_rate": _rate(int(profile["missing_key_count"]), max(1, gold_events * 2)),
        "extra_key_rate": _rate(int(profile["extra_key_count"]), max(1, sample_count * 2)),
        "wrong_entity_rate": _rate(int(profile["wrong_entity_count"]), max(1, gold_events * 2)),
        "partial_span_rate": _rate(int(profile["partial_span_count"]), max(1, gold_events * 2)),
        "unsupported_prediction_rate": _rate(int(profile["unsupported_prediction_count"]), prediction_events),
        "treatment_recovery_rate": _rate(
            movement_counts.get("RECOVERED_BY_TREATMENT", 0) + movement_counts.get("SLOT_ADDED_CORRECTLY", 0),
            sample_count,
        ),
        "treatment_regression_rate": _rate(
            movement_counts.get("INTRODUCED_BY_TREATMENT", 0)
            + movement_counts.get("SLOT_ADDED_INCORRECTLY", 0)
            + movement_counts.get("SLOT_REMOVED_INCORRECTLY", 0),
            sample_count,
        ),
        "recommended_representation": representation,
        "confidence": confidence,
    }


def _recommended_representation(profile: dict[str, Any]) -> str:
    gold_events = max(1, int(profile["gold_events"]))
    copyable_rate = _rate(int(profile["copyable_count"]), gold_events)
    typed_rate = _rate(int(profile["typed_derivable_count"]), gold_events)
    missing_rate = _rate(int(profile["missing_key_count"]), max(1, gold_events * 2))
    extra_rate = _rate(int(profile["extra_key_count"]), max(1, int(profile["sample_count"]) * 2))
    partial_rate = _rate(int(profile["partial_span_count"]), max(1, gold_events * 2))
    unsupported_rate = _rate(int(profile["unsupported_prediction_count"]), max(1, int(profile["prediction_events"])))
    if missing_rate + extra_rate >= 0.12:
        return "task_slot_schema_constraints"
    if typed_rate >= 0.20:
        return "typed_normalization"
    if copyable_rate >= 0.75 and partial_rate + unsupported_rate < 0.25:
        return "copy_or_normalize"
    return "mixed_slot_value_representation"


def _confidence_level(sample_count: int, movement_counts: dict[str, int]) -> str:
    persistent = movement_counts.get("ERROR_IN_BOTH_SAME_MECHANISM", 0) + movement_counts.get(
        "VALUE_CHANGED_BUT_STILL_WRONG", 0
    )
    if sample_count >= 60 and persistent >= 5:
        return "HIGH"
    if sample_count >= 15:
        return "MEDIUM"
    return "LOW"


def _movement_payload(
    movements: list[dict[str, Any]],
    movement_counter: Counter[str],
    split_counter: dict[str, Counter[str]],
    family_counter: dict[str, Counter[str]],
) -> dict[str, Any]:
    total = len(movements)
    persistent = (
        movement_counter.get("ERROR_IN_BOTH_SAME_MECHANISM", 0)
        + movement_counter.get("VALUE_CHANGED_BUT_STILL_WRONG", 0)
        + movement_counter.get("ERROR_IN_BOTH_DIFFERENT_MECHANISM", 0)
    )
    recovery = movement_counter.get("RECOVERED_BY_TREATMENT", 0) + movement_counter.get("SLOT_ADDED_CORRECTLY", 0)
    regression = (
        movement_counter.get("INTRODUCED_BY_TREATMENT", 0)
        + movement_counter.get("SLOT_ADDED_INCORRECTLY", 0)
        + movement_counter.get("SLOT_REMOVED_INCORRECTLY", 0)
    )
    persistent_mechanisms: Counter[tuple[str, str]] = Counter()
    introduced_mechanisms: Counter[tuple[str, str]] = Counter()
    persistent_labels = {
        "ERROR_IN_BOTH_SAME_MECHANISM",
        "ERROR_IN_BOTH_DIFFERENT_MECHANISM",
        "VALUE_CHANGED_BUT_STILL_WRONG",
    }
    introduced_labels = {"INTRODUCED_BY_TREATMENT", "SLOT_ADDED_INCORRECTLY", "SLOT_REMOVED_INCORRECTLY"}
    for event in movements:
        movement = event["movement"]
        if movement in persistent_labels:
            persistent_mechanisms[(event["control_primary_mechanism"], event["treatment_primary_mechanism"])] += 1
        if movement in introduced_labels:
            introduced_mechanisms[(movement, event["treatment_primary_mechanism"])] += 1
    compact_events = [
        {
            "sample_id": event["sample_id"],
            "split": event["split"],
            "task_family": event["task_family"],
            "slot_path": event["slot_path"],
            "movement": event["movement"],
            "control_primary_mechanism": event["control_primary_mechanism"],
            "treatment_primary_mechanism": event["treatment_primary_mechanism"],
        }
        for event in movements
        if event["movement"] != "CORRECT_IN_BOTH"
    ][:80]
    return {
        "movement_counts": dict(sorted(movement_counter.items())),
        "persistent_error_count": persistent,
        "persistent_error_rate": _rate(persistent, total),
        "treatment_recovery_count": recovery,
        "treatment_regression_count": regression,
        "net_slot_movement": recovery - regression,
        "top_persistent_mechanisms": _top_mechanism_pairs(
            persistent_mechanisms,
            key_names=("control_primary_mechanism", "treatment_primary_mechanism"),
        ),
        "top_introduced_mechanisms": _top_mechanism_pairs(
            introduced_mechanisms,
            key_names=("movement", "treatment_primary_mechanism"),
        ),
        "split_distribution": {
            split: dict(sorted(counter.items())) for split, counter in sorted(split_counter.items())
        },
        "task_family_distribution": {
            family: dict(sorted(counter.items())) for family, counter in sorted(family_counter.items())
        },
        "compact_non_correct_events": compact_events,
        "claim_boundary": (
            "Explains existing Control/Treatment outputs only; does not rejudge canonical treatment success."
        ),
    }


def _top_mechanism_pairs(
    counts: Counter[tuple[str, str]],
    *,
    key_names: tuple[str, str],
    limit: int = 8,
) -> list[dict[str, Any]]:
    return [
        {key_names[0]: first, key_names[1]: second, "count": count}
        for (first, second), count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:limit]
    ]


def _representation_feasibility(
    slot_profiles: list[dict[str, Any]],
    paired_movement: dict[str, Any],
) -> dict[str, Any]:
    representation_counts = Counter(profile["recommended_representation"] for profile in slot_profiles)
    confidence_counts = Counter(profile["confidence"] for profile in slot_profiles)
    missing_or_extra_profiles = sum(
        1 for profile in slot_profiles if profile["missing_key_rate"] + profile["extra_key_rate"] >= 0.12
    )
    typed_profiles = sum(1 for profile in slot_profiles if profile["typed_derivable_rate"] >= 0.20)
    copy_profiles = sum(1 for profile in slot_profiles if profile["copyable_rate"] >= 0.75)
    if not slot_profiles:
        decision = "ANALYSIS_BLOCKED_OR_INCONCLUSIVE"
    elif missing_or_extra_profiles >= max(1, len(slot_profiles) // 3):
        decision = "TASK_SLOT_SCHEMA_CONSTRAINTS_FIRST"
    elif typed_profiles >= max(1, len(slot_profiles) // 2):
        decision = "TYPED_NORMALIZATION_FIRST"
    elif len(representation_counts) > 1:
        decision = "MIXED_SLOT_REPRESENTATION_REQUIRED"
    elif copy_profiles == len(slot_profiles):
        decision = "COPY_OR_NORMALIZE_REPRESENTATION_JUSTIFIED"
    else:
        decision = "DATA_DIVERSITY_OR_GENERALIZATION_FIRST"
    top_profiles = sorted(
        slot_profiles,
        key=lambda profile: (
            profile["treatment_regression_rate"] + profile["missing_key_rate"] + profile["partial_span_rate"],
            profile["sample_count"],
            profile["slot_path"],
        ),
        reverse=True,
    )[:10]
    recommended_next_change = _recommended_next_change(decision, top_profiles)
    recommended_next_change["top_evidence"] = [
        f"Representation candidates by slot path: {dict(sorted(representation_counts.items()))}",
        f"Confidence distribution: {dict(sorted(confidence_counts.items()))}",
        (
            "Paired movement: "
            f"persistent={paired_movement['persistent_error_count']}, "
            f"recovered={paired_movement['treatment_recovery_count']}, "
            f"regressed={paired_movement['treatment_regression_count']}"
        ),
        "Top pressure slot paths: " + ", ".join(profile["slot_path"] for profile in top_profiles[:5]),
    ]
    return {
        "decision_label": decision,
        "confidence_thresholds": {
            "HIGH": "sample_count >= 60 and persistent_or_changed_error_count >= 5",
            "MEDIUM": "sample_count >= 15",
            "LOW": "below MEDIUM threshold",
        },
        "recommended_next_change": recommended_next_change,
        "representation_counts": dict(sorted(representation_counts.items())),
        "confidence_counts": dict(sorted(confidence_counts.items())),
        "top_slot_profiles": top_profiles,
        "paired_movement_summary": {
            "persistent_error_count": paired_movement["persistent_error_count"],
            "treatment_recovery_count": paired_movement["treatment_recovery_count"],
            "treatment_regression_count": paired_movement["treatment_regression_count"],
            "net_slot_movement": paired_movement["net_slot_movement"],
        },
    }


def _recommended_next_change(decision: str, top_profiles: list[dict[str, Any]]) -> dict[str, Any]:
    change_by_decision = {
        "COPY_OR_NORMALIZE_REPRESENTATION_JUSTIFIED": "design-span-grounded-slot-targets",
        "TASK_SLOT_SCHEMA_CONSTRAINTS_FIRST": "implement-task-specific-slot-schema-validator",
        "TYPED_NORMALIZATION_FIRST": "implement-typed-slot-normalizers",
        "MIXED_SLOT_REPRESENTATION_REQUIRED": "design-hybrid-slot-representation-v1",
        "DATA_DIVERSITY_OR_GENERALIZATION_FIRST": "build-template-disjoint-slot-challenge-set",
        "ANALYSIS_BLOCKED_OR_INCONCLUSIVE": "repair-slot-error-analysis-input-boundary",
    }
    target_paths = [profile["slot_path"] for profile in top_profiles[:5]]
    target_families = sorted({family for profile in top_profiles for family in profile["task_family_counts"]})[:8]
    return {
        "change_id": change_by_decision[decision],
        "decision_label": decision,
        "target_slot_paths": target_paths,
        "target_task_families": target_families,
        "scope": (
            "Design-only next OpenSpec change; no training, prediction rerun, "
            "evaluator relaxation, or runtime migration."
        ),
        "acceptance_criteria": [
            "keeps BrowserTaskContract V1 externally compatible",
            "preserves strict slot matching as the reported metric boundary",
            "uses deterministic copy, normalization, typed, and structure evidence only",
        ],
        "non_goals": [
            "no DPO or GRPO",
            "no LLM judge",
            "no automatic alias repair",
            "no checkpoint or adapter release",
        ],
        "metrics_to_watch": [
            "strict_slot_f1",
            "slot_value_exact_f1",
            "slot_value_normalized_f1",
            "executable_contract_pass_rate",
        ],
        "migration_risks": [
            "internal representation could drift from V1 contract serialization",
            "typed normalization could be mistaken for evaluator relaxation",
        ],
        "claim_boundaries": _claim_boundary_lines(),
    }


def _build_summary(boundary: dict[str, Any], analysis: dict[str, Any]) -> dict[str, Any]:
    source_counts = analysis["source_support_counts"]
    prediction_counts = analysis["prediction_provenance_counts"]
    mechanism_counts = analysis["mechanism_counts"]
    counts = analysis["summary_counts"]
    copyable = source_counts.get("exact_source_supported", 0) + source_counts.get("normalized_source_supported", 0)
    predicted_supported = (
        prediction_counts.get("exact_span_from_source", 0)
        + prediction_counts.get("normalized_span_from_source", 0)
        + prediction_counts.get("deterministic_derived", 0)
    )
    unsupported_predictions = prediction_counts.get("unsupported_by_source", 0)
    feasibility = analysis["representation_feasibility"]
    mechanism_total = max(1, sum(mechanism_counts.values()))
    summary = {
        "evidence_kind": "slot_error_mechanism_analysis",
        "change_id": CHANGE_ID,
        "decision_label": feasibility["decision_label"],
        "source_boundary": boundary,
        "summary_metrics": {
            "sample_count": counts["samples"],
            "gold_slot_events": counts["gold_slot_events"],
            "prediction_slot_events": counts["prediction_slot_events"],
            "exact_copyable_rate": _rate(source_counts.get("exact_source_supported", 0), counts["gold_slot_events"]),
            "normalized_copyable_rate": _rate(
                source_counts.get("normalized_source_supported", 0),
                counts["gold_slot_events"],
            ),
            "typed_derivable_rate": _rate(source_counts.get("typed_derivable", 0), counts["gold_slot_events"]),
            "generation_required_rate": _rate(
                source_counts.get("source_absent_or_generation_required", 0),
                counts["gold_slot_events"],
            ),
            "unsupported_analysis_rate": _rate(
                source_counts.get("unsupported_analysis", 0),
                counts["gold_slot_events"],
            ),
            "gold_exact_or_normalized_source_copyable_rate": _rate(copyable, counts["gold_slot_events"]),
            "predicted_source_supported_rate": _rate(predicted_supported, counts["prediction_slot_events"]),
            "prediction_unsupported_by_source_rate": _rate(
                unsupported_predictions,
                counts["prediction_slot_events"],
            ),
            "partial_span_rate": _rate(
                prediction_counts.get("partial_span_from_source", 0),
                counts["prediction_slot_events"],
            ),
            "wrong_entity_rate": _rate(mechanism_counts.get("WRONG_ENTITY_OR_VALUE", 0), mechanism_total),
            "normalization_only_error_rate": _rate(
                mechanism_counts.get("SLOT_CORRECT_NORMALIZED", 0),
                mechanism_total,
            ),
            "missing_slot_key_count": mechanism_counts.get("MISSING_SLOT_KEY", 0),
            "missing_slot_key_rate": _rate(mechanism_counts.get("MISSING_SLOT_KEY", 0), mechanism_total),
            "extra_slot_key_count": mechanism_counts.get("EXTRA_SLOT_KEY", 0),
            "extra_slot_key_rate": _rate(mechanism_counts.get("EXTRA_SLOT_KEY", 0), mechanism_total),
            "persistent_error_rate": analysis["paired_movement"]["persistent_error_rate"],
            "persistent_error_count": analysis["paired_movement"]["persistent_error_count"],
            "treatment_recovery_count": analysis["paired_movement"]["treatment_recovery_count"],
            "treatment_regression_count": analysis["paired_movement"]["treatment_regression_count"],
            "net_slot_movement": analysis["paired_movement"]["net_slot_movement"],
        },
        "top_mechanisms": _top_items(analysis["mechanism_counts"]),
        "top_source_support": _top_items(source_counts),
        "top_prediction_provenance": _top_items(prediction_counts),
        "source_support_breakdowns": analysis["source_support_breakdowns"],
        "top_persistent_mechanisms": analysis["paired_movement"]["top_persistent_mechanisms"],
        "top_introduced_mechanisms": analysis["paired_movement"]["top_introduced_mechanisms"],
        "summary_metric_denominators": _summary_metric_denominators(),
        "heuristics": _heuristics_payload(),
        "recommended_next_change": feasibility["recommended_next_change"],
        "claims": _claim_boundaries(),
    }
    validate_public_record(summary)
    return summary


def _summary_metric_denominators() -> dict[str, str]:
    return {
        "exact_copyable_rate": "gold_slot_events",
        "normalized_copyable_rate": "gold_slot_events",
        "typed_derivable_rate": "gold_slot_events",
        "generation_required_rate": "gold_slot_events",
        "unsupported_analysis_rate": "gold_slot_events",
        "gold_exact_or_normalized_source_copyable_rate": "gold_slot_events",
        "predicted_source_supported_rate": "prediction_slot_events",
        "prediction_unsupported_by_source_rate": "prediction_slot_events",
        "partial_span_rate": "prediction_slot_events",
        "wrong_entity_rate": "mechanism_events",
        "normalization_only_error_rate": "mechanism_events",
        "missing_slot_key_rate": "mechanism_events",
        "extra_slot_key_rate": "mechanism_events",
        "persistent_error_rate": "paired_slot_events",
    }


def _heuristics_payload() -> dict[str, Any]:
    return {
        "partial_span": {
            "description": (
                "After NFKC, case folding, and whitespace/punctuation removal, a partial span is flagged "
                "when either side contains the other or unique-character overlap reaches the threshold."
            ),
            "minimum_folded_length": 2,
            "substring_match_allowed": True,
            "unique_character_overlap_threshold": "max(2, min(unique_folded_value_chars, 4))",
            "claim_boundary": "heuristic diagnostic only; it does not repair or relax strict slot matching",
        }
    }


def _top_items(counts: dict[str, int], limit: int = 8) -> list[dict[str, Any]]:
    return [
        {"label": label, "count": count}
        for label, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:limit]
    ]


def _claim_boundaries() -> dict[str, bool]:
    return {
        "training_performed": False,
        "prediction_rerun_performed": False,
        "prediction_repair_performed": False,
        "evaluator_relaxation_performed": False,
        "browser_task_contract_v1_changed": False,
        "contract_core_v2_changed": False,
        "slot_representation_implemented": False,
        "adapter_or_checkpoint_release": False,
        "model_improvement_claim": False,
        "production_readiness_claim": False,
        "live_browser_claim": False,
    }


def _claim_boundary_lines() -> list[str]:
    return [
        (
            "No training, prediction rerun, data mutation, evaluator relaxation, schema migration, "
            "or runtime migration occurred."
        ),
        "Alias-key evidence is diagnostic only and does not repair strict matches.",
        "The report explains existing recovered Control/Treatment outputs only.",
    ]


def _write_success_artifacts(output_dir: Path, summary: dict[str, Any], analysis: dict[str, Any]) -> None:
    write_json(output_dir / "summary.json", summary)
    write_json(output_dir / "slot-profile.json", {"slot_profiles": analysis["slot_profiles"]})
    write_json(output_dir / "paired-error-movement.json", analysis["paired_movement"])
    write_json(output_dir / "representation-feasibility.json", analysis["representation_feasibility"])
    (output_dir / "summary.md").write_text(_summary_markdown(summary), encoding="utf-8")
    (output_dir / "slot-error-taxonomy.md").write_text(_taxonomy_markdown(), encoding="utf-8")
    (output_dir / "recommended-next-change.md").write_text(
        _recommended_next_change_markdown(summary["recommended_next_change"]),
        encoding="utf-8",
    )


def _summary_markdown(summary: dict[str, Any]) -> str:
    metrics = summary["summary_metrics"]
    return "\n".join(
        [
            "# Slot Error Mechanism Analysis",
            "",
            f"- Decision label: `{summary['decision_label']}`",
            f"- Sample count: {metrics['sample_count']}",
            f"- Gold slot events: {metrics['gold_slot_events']}",
            f"- Prediction slot events: {metrics['prediction_slot_events']}",
            f"- Exact source-copyable gold slots: {metrics['exact_copyable_rate']:.2%}",
            f"- Normalized source-copyable gold slots: {metrics['normalized_copyable_rate']:.2%}",
            f"- Typed-derivable gold slots: {metrics['typed_derivable_rate']:.2%}",
            f"- Generation-required gold slots: {metrics['generation_required_rate']:.2%}",
            f"- Unsupported-analysis gold slots: {metrics['unsupported_analysis_rate']:.2%}",
            f"- Prediction source-supported rate: {metrics['predicted_source_supported_rate']:.2%}",
            f"- Prediction unsupported-by-source rate: {metrics['prediction_unsupported_by_source_rate']:.2%}",
            "- Source-support breakdowns: summary JSON includes gold rates by split/task/route/slot path "
            "and predicted-value rates by split/run role/task/route/slot path.",
            (
                "- Partial-span heuristic: NFKC/casefold/compact text, then substring match or "
                "unique-character overlap threshold `max(2, min(unique_folded_value_chars, 4))`; "
                "diagnostic only."
            ),
            (
                "- Control/Treatment movement: "
                f"persistent={metrics['persistent_error_count']}, "
                f"recovered={metrics['treatment_recovery_count']}, "
                f"regressed={metrics['treatment_regression_count']}, "
                f"net={metrics['net_slot_movement']}"
            ),
            "- Boundary: recovered metric-reproduced raw inputs only; `prediction_contract` is the analysis authority.",
            "- Alias policy: diagnostic only; aliases do not repair strict matches.",
            "- Claims: no training, no prediction rerun, no evaluator relaxation, no schema/runtime change.",
            f"- Recommended next change: `{summary['recommended_next_change']['change_id']}`",
            "",
        ]
    )


def _taxonomy_markdown() -> str:
    labels = [
        "SLOT_CORRECT_EXACT",
        "SLOT_CORRECT_NORMALIZED",
        "MISSING_SLOT_KEY",
        "EXTRA_SLOT_KEY",
        "WRONG_SLOT_KEY_ALIAS",
        "WRONG_SLOT_KEY_SEMANTIC",
        "PARTIAL_VALUE_SPAN",
        "WRONG_ENTITY_OR_VALUE",
        "SOURCE_COPY_FAILURE",
        "UNSUPPORTED_OR_HALLUCINATED_VALUE",
        "NORMALIZATION_FAILURE",
        "DERIVED_VALUE_FAILURE",
        "CLARIFY_AMBIGUITY_REPRESENTATION_FAILURE",
        "MULTIVALUE_STRUCTURE_FAILURE",
        "TYPE_MISMATCH",
        "UNCLASSIFIED_SLOT_FAILURE",
    ]
    lines = [
        "# Slot Error Taxonomy",
        "",
        "This taxonomy is deterministic and does not use semantic scoring, prediction repair, or ASR speculation.",
        "",
    ]
    lines.extend(f"- `{label}`" for label in labels)
    lines.append("")
    return "\n".join(lines)


def _recommended_next_change_markdown(recommendation: dict[str, Any]) -> str:
    lines = [
        "# Recommended Next Change",
        "",
        f"- Decision label: `{recommendation['decision_label']}`",
        f"- Change id: `{recommendation['change_id']}`",
        f"- Scope: {recommendation['scope']}",
        f"- Target slot paths: {', '.join(recommendation['target_slot_paths']) or 'none'}",
        f"- Target task families: {', '.join(recommendation['target_task_families']) or 'none'}",
        "",
        "## Top Evidence",
        "",
    ]
    lines.extend(f"- {item}" for item in recommendation.get("top_evidence", []))
    lines.extend(
        [
            "",
            "## Acceptance Criteria",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in recommendation["acceptance_criteria"])
    lines.extend(["", "## Non-Goals", ""])
    lines.extend(f"- {item}" for item in recommendation["non_goals"])
    lines.extend(["", "## Metrics To Watch", ""])
    lines.extend(f"- {item}" for item in recommendation["metrics_to_watch"])
    lines.extend(["", "## Migration Risks", ""])
    lines.extend(f"- {item}" for item in recommendation["migration_risks"])
    lines.extend(["", "## Claim Boundaries", ""])
    lines.extend(f"- {item}" for item in recommendation["claim_boundaries"])
    lines.append("")
    return "\n".join(lines)
