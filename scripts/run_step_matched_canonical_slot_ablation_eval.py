from __future__ import annotations

import argparse
import hashlib
import json
import random
import subprocess
from collections import defaultdict
from pathlib import Path
from typing import Any

from step_matched_canonical_slot_ablation_report import (
    DECISION_LABELS,
    EVIDENCE_ROOT,
    PRIMARY_METRICS,
    REQUIRED_METRICS,
    assert_public_safe_text,
    decide_pilot_gate,
)

from voice2task.evaluation import evaluate_predictions, load_predictions
from voice2task.io import read_json, write_json
from voice2task.layered_evaluation import (
    _executable_contract_pass,
    _prediction_to_contract,
    evaluate_layered_predictions,
    normalize_slot_key,
    normalize_slot_value,
)
from voice2task.schemas import SFTDatasetRow, as_contract

CONTROL_REF = "c25a09874ae10c052364aaf5bfa55ee45b819e9a"
TREATMENT_REF = "115d060823ca6e90c2f9a3de37fc41eb7a08fa85"
PHASE = "run-step-matched-canonical-slot-ablation"
BOOTSTRAP_SEED = 7170
BOOTSTRAP_RESAMPLES = 2000


def _git_show_json(ref: str, path: str) -> dict[str, Any]:
    return json.loads(subprocess.check_output(["git", "show", f"{ref}:{path}"]))


def _git_show_jsonl(ref: str, path: str) -> list[dict[str, Any]]:
    data = subprocess.check_output(["git", "show", f"{ref}:{path}"]).decode("utf-8")
    return [json.loads(line) for line in data.splitlines() if line.strip()]


def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _write_public_json(path: Path, payload: Any) -> None:
    assert_public_safe_text(_canonical_json(payload))
    write_json(path, payload)


def _write_public_text(path: Path, text: str) -> None:
    assert_public_safe_text(text)
    path.write_text(text, encoding="utf-8")


def _hash_strings(values: list[str]) -> str:
    digest = hashlib.sha256()
    for value in values:
        digest.update(value.encode("utf-8"))
        digest.update(b"\n")
    return digest.hexdigest()


def _rows_by_split(records: list[dict[str, Any]], split: str) -> list[dict[str, Any]]:
    return [record for record in records if record.get("split") == split]


def _boundary_for_split(control_rows: list[dict[str, Any]], treatment_rows: list[dict[str, Any]]) -> dict[str, Any]:
    control_ids = [str(row["id"]) for row in control_rows]
    treatment_ids = [str(row["id"]) for row in treatment_rows]
    control_inputs = [str(row.get("input_text", "")) for row in control_rows]
    treatment_inputs = [str(row.get("input_text", "")) for row in treatment_rows]
    control_gold = [_canonical_json(row["target_contract"]) for row in control_rows]
    treatment_gold = [_canonical_json(row["target_contract"]) for row in treatment_rows]
    equal = control_ids == treatment_ids and control_inputs == treatment_inputs and control_gold == treatment_gold
    return {
        "control_count": len(control_rows),
        "treatment_count": len(treatment_rows),
        "row_order_equal": control_ids == treatment_ids,
        "input_text_equal": control_inputs == treatment_inputs,
        "gold_contracts_equal": control_gold == treatment_gold,
        "row_id_order_hash": {
            "control": _hash_strings(control_ids),
            "treatment": _hash_strings(treatment_ids),
        },
        "input_content_hash": {
            "control": _hash_strings(control_inputs),
            "treatment": _hash_strings(treatment_inputs),
        },
        "gold_contract_hash": {
            "control": _hash_strings(control_gold),
            "treatment": _hash_strings(treatment_gold),
        },
        "equal": equal,
        "mismatch_examples": [] if equal else _mismatch_examples(control_rows, treatment_rows),
    }


def _mismatch_examples(
    control_rows: list[dict[str, Any]],
    treatment_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    examples: list[dict[str, Any]] = []
    for index, (control, treatment) in enumerate(zip(control_rows, treatment_rows, strict=False)):
        if (
            control.get("id") != treatment.get("id")
            or control.get("input_text") != treatment.get("input_text")
            or control.get("target_contract") != treatment.get("target_contract")
        ):
            examples.append(
                {
                    "index": index,
                    "control_id": control.get("id"),
                    "treatment_id": treatment.get("id"),
                    "id_equal": control.get("id") == treatment.get("id"),
                    "input_equal": control.get("input_text") == treatment.get("input_text"),
                    "gold_equal": control.get("target_contract") == treatment.get("target_contract"),
                }
            )
        if len(examples) >= 20:
            break
    if len(control_rows) != len(treatment_rows):
        examples.append({"count_mismatch": [len(control_rows), len(treatment_rows)]})
    return examples


def write_boundary_verification(output_dir: Path) -> tuple[dict[str, Any], list[SFTDatasetRow]]:
    control_manifest = _git_show_json(CONTROL_REF, "data/public-samples/manifest_public_sample.json")
    treatment_manifest = _git_show_json(TREATMENT_REF, "data/public-samples/manifest_public_sample.json")
    control_records = _git_show_jsonl(CONTROL_REF, "data/public-samples/sft_public_sample.jsonl")
    treatment_records = _git_show_jsonl(TREATMENT_REF, "data/public-samples/sft_public_sample.jsonl")
    split_results = {
        split: _boundary_for_split(_rows_by_split(control_records, split), _rows_by_split(treatment_records, split))
        for split in ("dev", "test")
    }
    train_counts = {
        "control": len(_rows_by_split(control_records, "train")),
        "treatment": len(_rows_by_split(treatment_records, "train")),
    }
    heldout_equal = all(payload["equal"] for payload in split_results.values())
    payload = {
        "phase": PHASE,
        "status": "passed" if heldout_equal else "blocked",
        "comparison_method": "git_snapshot_content_hashes_by_split",
        "control": {
            "ref": CONTROL_REF,
            "manifest_id": control_manifest["manifest_id"],
            "train_sft_rows": train_counts["control"],
        },
        "treatment": {
            "ref": TREATMENT_REF,
            "manifest_id": treatment_manifest["manifest_id"],
            "train_sft_rows": train_counts["treatment"],
        },
        "splits": split_results,
        "dev_test_gold_boundary_identical": heldout_equal,
        "causal_training_allowed": heldout_equal,
        "train_only_delta_sft_rows": train_counts["treatment"] - train_counts["control"],
        "interpretation": (
            "dev/test sample ids, order, inputs, and gold contracts are identical"
            if heldout_equal
            else "held-out boundary mismatch; causal training must stop"
        ),
    }
    _write_public_json(output_dir / "boundary-verification.json", payload)
    return payload, [SFTDatasetRow(**record) for record in treatment_records]


def _metric_bundle(rows: list[SFTDatasetRow], predictions: dict[str, Any]) -> dict[str, Any]:
    strict = evaluate_predictions(rows, predictions)
    layered = evaluate_layered_predictions(rows, predictions)
    strict_metrics = strict.metrics
    layered_metrics = layered["metrics"]
    metrics = {
        "contract_exact_match_strict": layered_metrics["contract_exact_match_strict"],
        "strict_slot_f1": strict_metrics["slot_f1"],
        "slot_value_exact_f1": layered_metrics["slot_value_exact_f1"],
        "slot_value_normalized_f1": layered_metrics["slot_value_normalized_f1"],
        "executable_contract_pass_rate": layered_metrics["executable_contract_pass_rate"],
        "schema_validity": layered_metrics["schema_validity"],
        "json_valid_rate": strict_metrics["json_valid_rate"],
        "route_accuracy": layered_metrics["route_accuracy"],
        "task_type_accuracy": layered_metrics["task_type_accuracy"],
        "safety_recall": strict_metrics["safety_recall"],
        "unsafe_false_negative_rate": layered_metrics["unsafe_false_negative_rate"],
        "unsafe_false_positive_rate": layered_metrics["unsafe_false_positive_rate"],
        "requires_confirmation_accuracy": layered_metrics["requires_confirmation_accuracy"],
        "refusal_or_clarify_accuracy": layered_metrics["refusal_or_clarify_accuracy"],
    }
    layered_public = {key: value for key, value in layered.items() if key != "claims"}
    return {"metrics": metrics, "strict_metrics": strict_metrics, "layered": layered_public}


def _slot_items(slots: dict[str, Any], *, normalized: bool) -> set[tuple[str, str]]:
    if normalized:
        return {(normalize_slot_key(key), normalize_slot_value(value)) for key, value in slots.items()}
    return {(str(key), str(value)) for key, value in slots.items()}


def _row_slot_f1(gold_slots: dict[str, Any], predicted_slots: dict[str, Any], *, normalized: bool) -> float:
    gold_items = _slot_items(gold_slots, normalized=normalized)
    pred_items = _slot_items(predicted_slots, normalized=normalized)
    if not gold_items and not pred_items:
        return 1.0
    if not gold_items or not pred_items:
        return 0.0
    tp = len(gold_items & pred_items)
    precision = tp / len(pred_items)
    recall = tp / len(gold_items)
    return 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)


def _is_unsafe_false_negative(gold: Any, pred: Any) -> bool:
    gold_unsafe = not bool(gold.safety.get("allow")) or bool(gold.confirmation_required)
    pred_stops = not bool(pred.safety.get("allow")) or bool(pred.confirmation_required)
    return gold_unsafe and not pred_stops


def _is_unsafe_false_positive(gold: Any, pred: Any) -> bool:
    gold_safe = bool(gold.safety.get("allow")) and not bool(gold.confirmation_required)
    pred_stops = not bool(pred.safety.get("allow")) or bool(pred.confirmation_required)
    return gold_safe and pred_stops


def _row_status(row: SFTDatasetRow, prediction: Any) -> dict[str, Any]:
    gold = as_contract(row.target_contract)
    pred = _prediction_to_contract(prediction)
    if pred is None:
        return {
            "schema_valid": False,
            "exact": False,
            "executable": False,
            "slot_exact": False,
            "slot_value_exact_f1": 0.0,
            "slot_value_normalized_f1": 0.0,
            "safety_correct": False,
            "unsafe_false_negative": False,
            "unsafe_false_positive": False,
            "confirmation_correct": False,
            "route_correct": False,
            "task_type_correct": False,
            "family": _family(gold),
        }
    return {
        "schema_valid": True,
        "exact": pred.to_dict() == gold.to_dict(),
        "executable": _executable_contract_pass(gold, pred),
        "slot_exact": pred.slots == gold.slots,
        "slot_value_exact_f1": _row_slot_f1(gold.slots, pred.slots, normalized=False),
        "slot_value_normalized_f1": _row_slot_f1(gold.slots, pred.slots, normalized=True),
        "safety_correct": pred.safety.get("allow") == gold.safety.get("allow"),
        "unsafe_false_negative": _is_unsafe_false_negative(gold, pred),
        "unsafe_false_positive": _is_unsafe_false_positive(gold, pred),
        "confirmation_correct": pred.confirmation_required == gold.confirmation_required,
        "route_correct": pred.route == gold.route,
        "task_type_correct": pred.task_type == gold.task_type,
        "family": _family(gold),
    }


def _family(gold: Any) -> str:
    slot_keys = ",".join(sorted(str(key) for key in gold.slots)) or "none"
    return (
        f"{gold.task_type}|{gold.route}|{gold.safety.get('reason')}|"
        f"confirm:{str(gold.confirmation_required).lower()}|slots:{slot_keys}"
    )


def _rate(values: list[bool | float]) -> float:
    return sum(float(value) for value in values) / len(values) if values else 0.0


def _training_summary(
    *,
    arm: str,
    config: dict[str, Any],
    metadata: dict[str, Any],
    previous_budget: dict[str, Any],
) -> dict[str, Any]:
    budget = metadata.get("training_budget") if isinstance(metadata.get("training_budget"), dict) else {}
    summary = {
        "phase": PHASE,
        "arm": arm,
        "training_status": metadata.get("training_status"),
        "training_manifest_id": config["dataset_manifest_id"],
        "train_sft_rows": metadata.get("training_rows_used", config["expected_train_sft_rows"]),
        "base_model_public_id": config["base_model"],
        "lora": config["lora"],
        "learning_rate": config["learning_rate"],
        "configured_max_steps": config["max_steps"],
        "observed_optimizer_steps": budget.get("observed_optimizer_steps"),
        "effective_batch_size": budget.get("effective_batch_size"),
        "scheduler_step_count": config["scheduler_step_count"],
        "theoretical_examples_seen": budget.get("theoretical_examples_seen"),
        "target_tokens_seen": budget.get("target_tokens_seen_estimate"),
        "target_tokens_seen_status": budget.get("target_tokens_seen_status"),
        "seed": config["seed"],
        "trainer": config["trainer"],
        "previous_control_step_budget": previous_budget,
        "step_matched_not_token_matched": True,
        "adapter_release_status": "not_released",
        "checkpoint_release_status": "not_released",
        "raw_private_paths_copied_to_git": False,
        "sanitized_for_public_evidence": True,
    }
    return summary


def _load_arm(
    *,
    arm: str,
    rows_all: list[SFTDatasetRow],
    prediction_root: Path,
    config: dict[str, Any],
    metadata: dict[str, Any],
    output_dir: Path,
    previous_budget: dict[str, Any],
) -> dict[str, Any]:
    arm_dir = output_dir / arm
    arm_dir.mkdir(parents=True, exist_ok=True)
    _write_public_json(arm_dir / "config.json", _public_config(config))
    _write_public_json(
        arm_dir / "training-summary.json",
        _training_summary(arm=arm, config=config, metadata=metadata, previous_budget=previous_budget),
    )
    result: dict[str, Any] = {}
    for split in ("dev", "test"):
        rows = [row for row in rows_all if row.split == split]
        predictions = load_predictions(prediction_root / arm / split / "predictions.jsonl")
        bundle = _metric_bundle(rows, predictions)
        statuses = {row.id: _row_status(row, predictions.get(row.id)) for row in rows}
        payload = {
            "phase": PHASE,
            "arm": arm,
            "split": split,
            "manifest_id": config["dataset_manifest_id"],
            "prediction_count": len(predictions),
            "gold_count": len(rows),
            **bundle,
            "row_status": statuses,
            "claims": _claims(),
        }
        _write_public_json(arm_dir / f"{split}-metrics.json", payload)
        result[split] = payload
    return result


def _public_config(config: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "dataset_manifest_id",
        "dataset_split",
        "expected_train_sft_rows",
        "base_model",
        "lora",
        "learning_rate",
        "max_steps",
        "scheduler_step_count",
        "num_train_epochs",
        "per_device_train_batch_size",
        "gradient_accumulation_steps",
        "seed",
        "max_seq_length",
        "trainer",
        "step_budget",
        "step_matched_not_token_matched",
        "target_token_exposure_policy",
        "dpo_or_grpo_allowed",
    ]
    payload = {key: config[key] for key in keys if key in config}
    return payload


def _claims() -> dict[str, bool]:
    return {
        "fresh_adapter_training_performed": True,
        "sft_only": True,
        "dpo_or_grpo_run_performed": False,
        "llm_judge_used": False,
        "prediction_repair_performed": False,
        "semantic_equivalence_scoring_used": False,
        "evaluator_changed": False,
        "adapter_released": False,
        "checkpoint_released": False,
    }


def _split_analysis(rows: list[SFTDatasetRow], control: dict[str, Any], treatment: dict[str, Any]) -> dict[str, Any]:
    exact_recoveries: list[dict[str, str]] = []
    exact_regressions: list[dict[str, str]] = []
    executable_recoveries: list[dict[str, str]] = []
    executable_regressions: list[dict[str, str]] = []
    slot_recoveries: list[dict[str, str]] = []
    slot_regressions: list[dict[str, str]] = []
    safety_recoveries: list[dict[str, str]] = []
    safety_regressions: list[dict[str, str]] = []
    confirmation_recoveries: list[dict[str, str]] = []
    confirmation_regressions: list[dict[str, str]] = []
    family: dict[str, dict[str, list[Any]]] = defaultdict(lambda: defaultdict(list))
    rows_out: list[dict[str, Any]] = []
    for row in rows:
        c = control["row_status"][row.id]
        t = treatment["row_status"][row.id]
        item = {"id": row.id, "family": c["family"]}
        def rec(
            metric: str,
            recoveries: list[dict[str, str]],
            regressions: list[dict[str, str]],
            control_status: dict[str, Any] = c,
            treatment_status: dict[str, Any] = t,
            row_item: dict[str, str] = item,
        ) -> None:
            if not control_status[metric] and treatment_status[metric]:
                recoveries.append(row_item)
            if control_status[metric] and not treatment_status[metric]:
                regressions.append(row_item)
        rec("exact", exact_recoveries, exact_regressions)
        rec("executable", executable_recoveries, executable_regressions)
        rec("slot_exact", slot_recoveries, slot_regressions)
        rec("safety_correct", safety_recoveries, safety_regressions)
        rec("confirmation_correct", confirmation_recoveries, confirmation_regressions)
        rows_out.append(
            {
                "id": row.id,
                "family": c["family"],
                "control": c,
                "treatment": t,
                "deltas": {
                    "exact": int(t["exact"]) - int(c["exact"]),
                    "executable": int(t["executable"]) - int(c["executable"]),
                    "slot_value_exact_f1": t["slot_value_exact_f1"] - c["slot_value_exact_f1"],
                    "slot_value_normalized_f1": t["slot_value_normalized_f1"] - c["slot_value_normalized_f1"],
                },
            }
        )
        bucket = family[c["family"]]
        for key in ["exact", "executable", "slot_exact", "route_correct", "task_type_correct"]:
            bucket[f"control_{key}"].append(c[key])
            bucket[f"treatment_{key}"].append(t[key])
        bucket["control_slot_value_exact_f1"].append(c["slot_value_exact_f1"])
        bucket["treatment_slot_value_exact_f1"].append(t["slot_value_exact_f1"])

    return {
        "rows": rows_out,
        "exact_recoveries": _examples(exact_recoveries),
        "exact_regressions": _examples(exact_regressions),
        "executable_recoveries": _examples(executable_recoveries),
        "executable_regressions": _examples(executable_regressions),
        "slot_recoveries": _examples(slot_recoveries),
        "slot_regressions": _examples(slot_regressions),
        "safety_recoveries": _examples(safety_recoveries),
        "safety_regressions": _examples(safety_regressions),
        "confirmation_recoveries": _examples(confirmation_recoveries),
        "confirmation_regressions": _examples(confirmation_regressions),
        "family_deltas": _family_deltas(family),
    }


def _examples(items: list[dict[str, str]]) -> dict[str, Any]:
    return {"count": len(items), "examples": items[:50]}


def _family_deltas(family: dict[str, dict[str, list[Any]]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for name, bucket in family.items():
        out.append(
            {
                "family": name,
                "count": len(bucket["control_exact"]),
                "exact_delta": _rate(bucket["treatment_exact"]) - _rate(bucket["control_exact"]),
                "executable_delta": _rate(bucket["treatment_executable"]) - _rate(bucket["control_executable"]),
                "slot_exact_delta": _rate(bucket["treatment_slot_exact"]) - _rate(bucket["control_slot_exact"]),
                "slot_value_exact_f1_delta": _rate(bucket["treatment_slot_value_exact_f1"])
                - _rate(bucket["control_slot_value_exact_f1"]),
                "route_accuracy_delta": _rate(bucket["treatment_route_correct"])
                - _rate(bucket["control_route_correct"]),
                "task_type_accuracy_delta": _rate(bucket["treatment_task_type_correct"])
                - _rate(bucket["control_task_type_correct"]),
            }
        )
    out.sort(
        key=lambda item: (abs(item["slot_value_exact_f1_delta"]) + abs(item["executable_delta"]), item["count"]),
        reverse=True,
    )
    return out


def _bootstrap(split_rows: list[dict[str, Any]]) -> dict[str, Any]:
    rng = random.Random(BOOTSTRAP_SEED)
    metrics = {
        "exact": ("exact", "binary"),
        "executable": ("executable", "binary"),
        "slot_value_exact_f1": ("slot_value_exact_f1", "score"),
        "slot_value_normalized_f1": ("slot_value_normalized_f1", "score"),
    }
    intervals: dict[str, Any] = {}
    if not split_rows:
        return intervals
    for metric, (key, kind) in metrics.items():
        samples: list[float] = []
        for _ in range(BOOTSTRAP_RESAMPLES):
            total = 0.0
            for _index in range(len(split_rows)):
                row = split_rows[rng.randrange(len(split_rows))]
                if kind == "binary":
                    total += float(row["treatment"][key]) - float(row["control"][key])
                else:
                    total += float(row["treatment"][key]) - float(row["control"][key])
            samples.append(total / len(split_rows))
        samples.sort()
        intervals[metric] = {
            "mean_delta": sum(samples) / len(samples),
            "ci95": [samples[int(0.025 * len(samples))], samples[int(0.975 * len(samples)) - 1]],
        }
    return intervals


def _comparison_markdown(comparison: dict[str, Any]) -> str:
    lines = [
        "# Step-matched canonical slot ablation comparison",
        "",
        f"- Status: `{comparison['status']}`",
        f"- Decision label: `{comparison['decision_label']}`",
        f"- Gate passed: `{comparison['pilot_gate']['passed']}`",
        f"- Recommended next step: `{comparison['recommended_next_step']}`",
        "- Scope: one fixed-seed SFT A/B; step-matched, not token-matched.",
        "- Non-goals: no DPO/GRPO, no evaluator change, no LLM judge, no prediction repair, no "
        "semantic-equivalence scoring, no public adapter/checkpoint release.",
        "",
    ]
    for split in ("dev", "test"):
        lines.extend(
            [
                f"## {split}",
                "",
                "| metric | control | treatment | delta |",
                "| --- | ---: | ---: | ---: |",
            ]
        )
        payload = comparison["splits"][split]
        for metric in REQUIRED_METRICS:
            lines.append(
                f"| `{metric}` | {payload['control_metrics'][metric]:.6f} | "
                f"{payload['treatment_metrics'][metric]:.6f} | "
                f"{payload['absolute_delta_treatment_minus_control'][metric]:+.6f} |"
            )
        lines.extend(
            [
                "",
                "Top family-level deltas:",
                "",
                "| family | count | exact | executable | slot exact F1 |",
                "| --- | ---: | ---: | ---: | ---: |",
            ]
        )
        for item in payload["top_family_level_deltas"][:8]:
            lines.append(
                f"| `{item['family']}` | {item['count']} | {item['exact_delta']:+.6f} | "
                f"{item['executable_delta']:+.6f} | {item['slot_value_exact_f1_delta']:+.6f} |"
            )
        lines.append("")
    lines.extend(["## Required Questions", ""])
    for item in comparison["required_question_answers"]:
        lines.append(f"- {item}")
    return "\n".join(lines) + "\n"


def _decision_markdown(comparison: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Step-matched canonical slot ablation decision",
            "",
            f"- Decision label: `{comparison['decision_label']}`",
            f"- Gate passed: `{comparison['pilot_gate']['passed']}`",
            f"- Recommended next step: `{comparison['recommended_next_step']}`",
            "- This is one fixed seed and is not statistical confirmation.",
            "- Do not claim public adapter/checkpoint release, production readiness, safety certification, "
            "live-browser improvement, or held-out recovery beyond observed metrics.",
            "",
        ]
    )


def run(args: argparse.Namespace) -> None:
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    boundary, rows_all = write_boundary_verification(output_dir)
    if not boundary["causal_training_allowed"]:
        raise SystemExit("boundary verification failed")

    previous_budget = {
        "source_type": "reconstructed_from_prior_control_config",
        "prior_control_train_rows": 261,
        "prior_control_num_train_epochs": 12,
        "prior_control_per_device_train_batch_size": 1,
        "prior_control_gradient_accumulation_steps": 1,
        "optimizer_steps": 3132,
    }
    control_config = read_json(args.control_config)
    treatment_config = read_json(args.treatment_config)
    control_metadata = read_json(args.control_metadata)
    treatment_metadata = read_json(args.treatment_metadata)
    results = {
        "control": _load_arm(
            arm="control",
            rows_all=rows_all,
            prediction_root=args.prediction_root,
            config=control_config,
            metadata=control_metadata,
            output_dir=output_dir,
            previous_budget=previous_budget,
        ),
        "treatment": _load_arm(
            arm="treatment",
            rows_all=rows_all,
            prediction_root=args.prediction_root,
            config=treatment_config,
            metadata=treatment_metadata,
            output_dir=output_dir,
            previous_budget=previous_budget,
        ),
    }
    paired: dict[str, Any] = {"phase": PHASE, "splits": {}}
    family_payload: dict[str, Any] = {"phase": PHASE, "splits": {}}
    bootstrap: dict[str, Any] = {
        "phase": PHASE,
        "bootstrap_seed": BOOTSTRAP_SEED,
        "resamples": BOOTSTRAP_RESAMPLES,
        "interpretation": "paired bootstrap diagnostic only; one seed is not statistical confirmation",
        "splits": {},
    }
    comparison: dict[str, Any] = {
        "phase": PHASE,
        "status": "observed",
        "decision_labels": DECISION_LABELS,
        "training_manifests": {
            "control": control_config["dataset_manifest_id"],
            "treatment": treatment_config["dataset_manifest_id"],
        },
        "step_matching": {
            "unit": "optimizer_steps",
            "max_steps": control_config["max_steps"],
            "not_token_matched": True,
            "previous_budget": previous_budget,
        },
        "primary_metrics": PRIMARY_METRICS,
        "guardrail_metrics": REQUIRED_METRICS[5:],
        "splits": {},
        "claims": _claims(),
    }
    deltas_for_gate: dict[str, dict[str, float]] = {}
    for split in ("dev", "test"):
        rows = [row for row in rows_all if row.split == split]
        split_analysis = _split_analysis(rows, results["control"][split], results["treatment"][split])
        paired["splits"][split] = {key: value for key, value in split_analysis.items() if key != "family_deltas"}
        family_payload["splits"][split] = split_analysis["family_deltas"]
        bootstrap["splits"][split] = _bootstrap(split_analysis["rows"])
        deltas = {
            metric: results["treatment"][split]["metrics"][metric] - results["control"][split]["metrics"][metric]
            for metric in REQUIRED_METRICS
        }
        deltas_for_gate[split] = deltas
        comparison["splits"][split] = {
            "control_metrics": results["control"][split]["metrics"],
            "treatment_metrics": results["treatment"][split]["metrics"],
            "absolute_delta_treatment_minus_control": deltas,
            "top_family_level_deltas": split_analysis["family_deltas"][:12],
            "exact_recoveries": split_analysis["exact_recoveries"],
            "exact_regressions": split_analysis["exact_regressions"],
            "slot_recoveries": split_analysis["slot_recoveries"],
            "slot_regressions": split_analysis["slot_regressions"],
            "safety_regressions": split_analysis["safety_regressions"],
            "confirmation_regressions": split_analysis["confirmation_regressions"],
        }
    gate = decide_pilot_gate(deltas_for_gate)
    comparison["pilot_gate"] = gate
    comparison["decision_label"] = gate["decision_label"]
    comparison["recommended_next_step"] = (
        "run_3_seed_confirmation"
        if gate["passed"]
        else "design-and-implement-contract-v2; do_not_add_candidates_or_run_dpo"
    )
    comparison["required_question_answers"] = _required_answers(comparison)
    _write_public_json(output_dir / "paired-row-analysis.json", paired)
    _write_public_json(output_dir / "family-level-deltas.json", family_payload)
    _write_public_json(output_dir / "bootstrap-analysis.json", bootstrap)
    _write_public_json(output_dir / "comparison.json", comparison)
    _write_public_text(output_dir / "comparison.md", _comparison_markdown(comparison))
    _write_public_text(output_dir / "decision.md", _decision_markdown(comparison))
    print(json.dumps({"ok": True, "decision_label": comparison["decision_label"], "gate_passed": gate["passed"]}))


def _required_answers(comparison: dict[str, Any]) -> list[str]:
    return [
        "Step-matched: yes; both arms use the same explicit max_steps and scheduler step count.",
        "Examples/tokens: examples are step-matched by optimizer updates; target token exposure is recorded but "
        "not matched.",
        "Canonical data gain: answer is limited to observed treatment-minus-control deltas in comparison.json.",
        "Search concentration: see family-level-deltas.json for concentration by family.",
        "Regressions: see paired-row-analysis.json exact/executable/slot regressions.",
        "Safety and confirmation: see safety and confirmation regression counts plus guardrail deltas.",
        f"Decision label: {comparison['decision_label']}.",
        f"Next recommendation: {comparison['recommended_next_step']}.",
        "Cannot claim: public adapter/checkpoint release, production readiness, safety certification, "
        "live-browser improvement, or held-out recovery beyond observed metrics.",
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prediction-root", type=Path, required=True)
    parser.add_argument("--control-metadata", type=Path, required=True)
    parser.add_argument("--treatment-metadata", type=Path, required=True)
    parser.add_argument(
        "--control-config",
        type=Path,
        default=Path("configs/sft-a100-step-matched-canonical-slot-control.json"),
    )
    parser.add_argument(
        "--treatment-config",
        type=Path,
        default=Path("configs/sft-a100-step-matched-canonical-slot-treatment.json"),
    )
    parser.add_argument("--output-dir", type=Path, default=EVIDENCE_ROOT)
    run(parser.parse_args())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
