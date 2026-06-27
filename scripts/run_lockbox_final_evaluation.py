from __future__ import annotations

import argparse
import gc
import hashlib
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from voice2task.evaluation import evaluate_predictions
from voice2task.formatting import (
    FORMATTING_POLICY,
    PredictionInput,
    format_schema_retry_prompt_text,
    format_sft_prediction_prompt,
)
from voice2task.io import read_json, read_jsonl, write_json, write_jsonl
from voice2task.schemas import SFTDatasetRow, as_contract
from voice2task.training import (
    _build_schema_guard,
    _decode_prediction_attempt,
    _extract_strict_json_object,
    _schema_guard_status,
    _schema_retry_prompt,
)

EXPECTED_LOCKBOX_HASH = "06114cf3ad6029930284af5f2245fb2c4a8174fd35c6a1107f4c73482b555b33"
EXPECTED_ADAPTER_SHA256 = "d7722c2c11b08a848f4c3bb46c9088a26121e231fbaf18f8fb55eab7f3becfac"
PROMPT_POLICY = "unified_gold_free_v1"
EVALUATOR_VERSION = "strict_contract_ladder_existing"
BASE_ARM = "base_qwen25_7b_instruct_unified_prompt"
FINAL_ARM = "final_sft_adapter_unified_prompt"
PUBLIC_METRIC_KEYS = (
    "json_parse_rate",
    "strict_schema_valid_rate",
    "semantic_contract_valid_rate",
    "contract_exact_match",
    "slot_f1",
    "slot_f1_soft",
    "task_type_accuracy",
    "route_accuracy",
    "confirmation_accuracy",
    "safety_precision",
    "safety_recall",
    "safety_tp",
    "safety_fp",
    "safety_fn",
    "safety_predicted_positive_support",
    "safety_gold_positive_support",
)


@dataclass(frozen=True)
class ArmConfig:
    arm_id: str
    public_name: str
    adapter_path: Path | None


def _utc_now_id() -> str:
    return datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _deterministic_lockbox_hash(rows: list[dict[str, Any]]) -> str:
    content_hashes = [str(row.get("content_hash", "")) for row in rows]
    payload = json.dumps(content_hashes, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _validate_frozen_lockbox(
    lockbox_path: Path,
    manifest_path: Path,
    expected_hash: str,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows = read_jsonl(lockbox_path)
    manifest = read_json(manifest_path)
    row_count = len(rows)
    family_count = len({str(row.get("semantic_family_id", "")) for row in rows})
    manifest_hash = manifest.get("lockbox_hash") or manifest.get("dataset_sha256")
    computed_hash = _deterministic_lockbox_hash(rows)
    if manifest.get("frozen") is not True:
        raise ValueError("lockbox manifest is not frozen")
    if manifest.get("row_count") != row_count:
        raise ValueError(f"manifest row_count mismatch: manifest={manifest.get('row_count')} actual={row_count}")
    if manifest.get("family_count") != family_count:
        raise ValueError(
            f"manifest family_count mismatch: manifest={manifest.get('family_count')} actual={family_count}"
        )
    if manifest_hash != expected_hash:
        raise ValueError(f"manifest hash mismatch: manifest={manifest_hash} expected={expected_hash}")
    if computed_hash != expected_hash:
        raise ValueError(f"computed lockbox hash mismatch: computed={computed_hash} expected={expected_hash}")
    content_hashes = manifest.get("content_hashes")
    if content_hashes is not None and content_hashes != [row.get("content_hash") for row in rows]:
        raise ValueError("manifest content_hashes do not match row order")
    return rows, manifest


def _lockbox_rows_to_sft_rows(rows: list[dict[str, Any]]) -> list[SFTDatasetRow]:
    converted: list[SFTDatasetRow] = []
    for row in rows:
        converted.append(
            SFTDatasetRow(
                id=str(row["row_id"]),
                split="test",
                input_text=str(row["input_text"]),
                target_contract=as_contract(row["gold_contract"]),
                provenance={
                    "source_id": row["row_id"],
                    "semantic_family_id": row["semantic_family_id"],
                    "lockbox_content_hash": row["content_hash"],
                    "public_safe": True,
                },
            )
        )
    return converted


def _load_model(base_model: str, adapter_path: Path | None) -> tuple[Any, Any, Any]:
    import torch
    from peft import PeftModel  # type: ignore[import-not-found, unused-ignore]
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(base_model, trust_remote_code=True)
    dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    model: Any = AutoModelForCausalLM.from_pretrained(
        base_model,
        device_map="auto",
        torch_dtype=dtype,
        trust_remote_code=True,
    )
    if adapter_path is not None:
        model = PeftModel.from_pretrained(model, str(adapter_path))
        merge_and_unload = getattr(model, "merge_and_unload", None)
        if callable(merge_and_unload):
            model = merge_and_unload()
    model.eval()
    return model, tokenizer, torch


def _predict_rows(
    *,
    arm: ArmConfig,
    rows: list[SFTDatasetRow],
    base_model: str,
    max_new_tokens: int,
    raw_dir: Path,
) -> dict[str, Any]:
    model, tokenizer, torch_module = _load_model(base_model, arm.adapter_path)
    predictions: dict[str, Any] = {}
    raw_records: list[dict[str, Any]] = []
    try:
        for row in rows:
            prediction_input = PredictionInput.from_sft_row(row)
            prompt = format_sft_prediction_prompt(prediction_input, tokenizer=tokenizer)
            decoded, _, _ = _decode_prediction_attempt(
                model=model,
                tokenizer=tokenizer,
                prompt=prompt,
                max_new_tokens=max_new_tokens,
                torch_module=torch_module,
            )
            raw_prediction = _extract_strict_json_object(decoded)
            raw_status = _schema_guard_status(raw_prediction)
            retry_status: dict[str, Any] | None = None
            retry_prediction: Any = None
            retry_decoded: str | None = None
            retry_attempted = False
            if not raw_status["schema_valid"]:
                retry_attempted = True
                retry_instruction = _schema_retry_prompt(prediction_input, raw_prediction, raw_status)
                retry_prompt = format_schema_retry_prompt_text(retry_instruction, tokenizer=tokenizer)
                retry_decoded, _, _ = _decode_prediction_attempt(
                    model=model,
                    tokenizer=tokenizer,
                    prompt=retry_prompt,
                    max_new_tokens=max_new_tokens,
                    torch_module=torch_module,
                )
                retry_prediction = _extract_strict_json_object(retry_decoded)
                retry_status = _schema_guard_status(retry_prediction)
            schema_guard = _build_schema_guard(
                raw_status=raw_status,
                retry_enabled=True,
                retry_attempted=retry_attempted,
                retry_status=retry_status,
            )
            final_prediction = (
                retry_prediction if schema_guard["validated_output_source"] == "retry_attempt" else raw_prediction
            )
            predictions[row.id] = final_prediction
            raw_records.append(
                {
                    "id": row.id,
                    "arm": arm.arm_id,
                    "prediction": final_prediction,
                    "raw_decoded": decoded,
                    "retry_decoded": retry_decoded,
                    "schema_guard": schema_guard,
                    "prompt_policy": PROMPT_POLICY,
                }
            )
    finally:
        del model
        gc.collect()
        if hasattr(torch_module, "cuda") and torch_module.cuda.is_available():
            torch_module.cuda.empty_cache()
    write_jsonl(raw_dir / arm.arm_id / "predictions.jsonl", raw_records)
    return predictions


def public_metrics_payload(*, arm: ArmConfig, rows: list[SFTDatasetRow], predictions: dict[str, Any]) -> dict[str, Any]:
    result = evaluate_predictions(rows, predictions)
    metrics = {key: result.metrics.get(key) for key in PUBLIC_METRIC_KEYS}
    return {
        "arm": arm.public_name,
        "row_count": len(rows),
        "prompt_policy": PROMPT_POLICY,
        "evaluator_version": EVALUATOR_VERSION,
        "metrics": metrics,
        "public_report_policy": {
            "aggregate_metrics_only": True,
            "row_level_failure_analysis_included": False,
        },
    }


def comparison_payload(base_payload: dict[str, Any], final_payload: dict[str, Any]) -> dict[str, Any]:
    base_metrics = base_payload["metrics"]
    final_metrics = final_payload["metrics"]
    deltas: dict[str, float | None] = {}
    for key in PUBLIC_METRIC_KEYS:
        base_value = base_metrics.get(key)
        final_value = final_metrics.get(key)
        if isinstance(base_value, int | float) and isinstance(final_value, int | float):
            deltas[key] = float(final_value) - float(base_value)
        else:
            deltas[key] = None
    return {
        "comparison": "final_sft_minus_base",
        "row_count": base_payload["row_count"],
        "prompt_policy": PROMPT_POLICY,
        "evaluator_version": EVALUATOR_VERSION,
        "base_arm": base_payload["arm"],
        "final_arm": final_payload["arm"],
        "delta": deltas,
        "metrics": {
            "base": base_metrics,
            "final_sft": final_metrics,
        },
        "public_report_policy": {
            "aggregate_metrics_only": True,
            "row_level_failure_analysis_included": False,
            "lockbox_tuning_after_result": False,
        },
    }


def _format_metric(value: Any) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, int | float):
        return f"{float(value):.4f}"
    return str(value)


def write_comparison_markdown(path: Path, comparison: dict[str, Any]) -> None:
    base = comparison["metrics"]["base"]
    final = comparison["metrics"]["final_sft"]
    delta = comparison["delta"]
    lines = [
        "# Lockbox v1 Final Evaluation",
        "",
        "Aggregate metrics only. No row-level failure analysis is included in this public report.",
        "",
        "| Metric | Base | Final SFT | Delta |",
        "| --- | ---: | ---: | ---: |",
    ]
    for key in PUBLIC_METRIC_KEYS:
        lines.append(
            f"| `{key}` | {_format_metric(base.get(key))} | "
            f"{_format_metric(final.get(key))} | {_format_metric(delta.get(key))} |"
        )
    lines.extend(
        [
            "",
            "Claim boundary: this is a one-look frozen-lockbox result under the pre-registered prompt, "
            "decoding, schema guard, and evaluator. It does not justify post-hoc lockbox tuning.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_human_brief(path: Path, comparison: dict[str, Any]) -> None:
    exact_delta = comparison["delta"].get("contract_exact_match")
    lines = [
        "<!doctype html>",
        '<html lang="zh-CN">',
        "<head>",
        '<meta charset="utf-8">',
        "<title>Lockbox v1 Final Evaluation</title>",
        "<style>",
        "body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;"
        "margin:32px;line-height:1.55;color:#1f2937}",
        "table{border-collapse:collapse;width:100%;max-width:980px}"
        "th,td{border:1px solid #d1d5db;padding:8px;text-align:right}"
        "th:first-child,td:first-child{text-align:left}",
        ".note{max-width:980px;background:#f8fafc;border-left:4px solid #2563eb;padding:12px;margin:16px 0}",
        "code{background:#f3f4f6;padding:1px 4px;border-radius:4px}",
        "</style>",
        "</head>",
        "<body>",
        "<h1>Lockbox v1 Final Evaluation</h1>",
        (
            "<p><strong>结论：</strong>已完成一次 frozen lockbox 聚合评估；"
            f"final SFT 相对 base 的 contract_exact_match delta 为 <code>{_format_metric(exact_delta)}</code>。</p>"
        ),
        '<div class="note">公开材料只包含 aggregate metrics；没有逐行失败分析，'
        "也没有基于 lockbox 结果调参、改 prompt、改 schema 或重训。</div>",
        "<table>",
        "<thead><tr><th>Metric</th><th>Base</th><th>Final SFT</th><th>Delta</th></tr></thead>",
        "<tbody>",
    ]
    base = comparison["metrics"]["base"]
    final = comparison["metrics"]["final_sft"]
    delta = comparison["delta"]
    for key in PUBLIC_METRIC_KEYS:
        lines.append(
            f"<tr><td><code>{key}</code></td><td>{_format_metric(base.get(key))}</td>"
            f"<td>{_format_metric(final.get(key))}</td><td>{_format_metric(delta.get(key))}</td></tr>"
        )
    lines.extend(
        [
            "</tbody></table>",
            "<h2>边界</h2>",
            "<p>这是 lockbox-v1 的 one-look frozen evaluation。结果只支持该冻结数据、"
            "预注册 prompt policy、decoding policy 和 strict evaluator 下的聚合对比。</p>",
            "<p>不得据此声称生产可用、安全就绪、live browser benchmark 提升，或对 lockbox 逐条失败做后续调参。</p>",
            "</body></html>",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_run_card(
    *,
    path: Path,
    run_id: str,
    args: argparse.Namespace,
    manifest: dict[str, Any],
    rows: list[SFTDatasetRow],
) -> None:
    payload = {
        "run_id": run_id,
        "stage": "lockbox_v1_final_evaluation",
        "git_commit": args.git_commit,
        "data_freeze_commit": args.data_freeze_commit,
        "final_prep_commit": args.final_prep_commit,
        "lockbox": {
            "path": str(args.lockbox),
            "manifest_path": str(args.manifest),
            "lockbox_hash": args.expected_lockbox_hash,
            "manifest_id": manifest.get("manifest_id"),
            "row_count": len(rows),
            "family_count": manifest.get("family_count"),
            "frozen": manifest.get("frozen"),
        },
        "train_dataset": {
            "manifest_path": "data/public-samples/manifest_public_sample.json",
            "train_dataset_hash": args.train_dataset_hash,
            "policy": "existing training data only; no lockbox rows added",
        },
        "prompt_policy": PROMPT_POLICY,
        "formatting_policy": FORMATTING_POLICY,
        "base_model": {
            "public_id": args.base_model_public_id,
            "revision": args.base_model_revision,
        },
        "adapter": {
            "public_name": FINAL_ARM,
            "adapter_model_sha256": args.adapter_sha256,
            "adapter_weights_copied_to_git": False,
        },
        "sft_config": {
            "seed": args.seed,
            "trainer": "trl.SFTTrainer",
            "max_steps": 3132,
            "num_train_epochs": 12,
            "per_device_train_batch_size": 1,
            "gradient_accumulation_steps": 1,
            "learning_rate": 0.00005,
            "lora": {
                "r": 16,
                "alpha": 32,
                "dropout": 0.05,
                "target_modules": ["q_proj", "k_proj", "v_proj", "o_proj"],
            },
        },
        "decoding_config": {
            "strategy": "greedy",
            "do_sample": False,
            "max_new_tokens": args.max_new_tokens,
            "schema_guard": True,
            "schema_retry": True,
            "schema_retry_max_attempts": 1,
            "schema_repair_applied": False,
            "posthoc_prediction_repair": False,
        },
        "evaluator": {
            "version": EVALUATOR_VERSION,
            "metric_names": list(PUBLIC_METRIC_KEYS),
        },
        "arms": [BASE_ARM, FINAL_ARM],
        "output_paths": {
            "run_card_public": "reports/lockbox-v1/final-evaluation/run-card.json",
            "base_metrics_public": "reports/lockbox-v1/final-evaluation/base/metrics.json",
            "final_sft_metrics_public": "reports/lockbox-v1/final-evaluation/final-sft/metrics.json",
            "comparison_public": "reports/lockbox-v1/final-evaluation/comparison.json",
            "comparison_markdown_public": "reports/lockbox-v1/final-evaluation/comparison.md",
            "raw_predictions_private": "<private_a100_run_root>/raw/<arm>/predictions.jsonl",
        },
        "one_look_rule": {
            "final_lockbox_evaluation_run_once": True,
            "row_level_failure_analysis_public": False,
            "lockbox_tuning_after_result": False,
            "readme_rewritten": False,
            "dpo_or_grpo_started": False,
        },
    }
    write_json(path, payload)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the pre-registered lockbox v1 final evaluation once.")
    parser.add_argument("--lockbox", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--raw-dir", type=Path, required=True)
    parser.add_argument("--base-model", required=True)
    parser.add_argument("--base-model-public-id", default="Qwen/Qwen2.5-7B-Instruct")
    parser.add_argument("--base-model-revision", required=True)
    parser.add_argument("--adapter-path", type=Path, required=True)
    parser.add_argument("--adapter-sha256", default=EXPECTED_ADAPTER_SHA256)
    parser.add_argument("--expected-lockbox-hash", default=EXPECTED_LOCKBOX_HASH)
    parser.add_argument("--data-freeze-commit", default="3fb352b")
    parser.add_argument("--final-prep-commit", default="020391f")
    parser.add_argument("--git-commit", required=True)
    parser.add_argument("--train-dataset-hash", required=True)
    parser.add_argument("--max-new-tokens", type=int, default=256)
    parser.add_argument("--seed", type=int, default=7170)
    parser.add_argument("--human-brief", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.adapter_sha256 != EXPECTED_ADAPTER_SHA256:
        raise ValueError(f"adapter sha256 mismatch: {args.adapter_sha256} != {EXPECTED_ADAPTER_SHA256}")
    adapter_file = args.adapter_path / "adapter_model.safetensors"
    if _sha256_file(adapter_file) != args.adapter_sha256:
        raise ValueError("adapter_model.safetensors SHA-256 does not match pre-registered final adapter")
    lockbox_rows, manifest = _validate_frozen_lockbox(args.lockbox, args.manifest, args.expected_lockbox_hash)
    rows = _lockbox_rows_to_sft_rows(lockbox_rows)
    run_id = f"lockbox-v1-final-evaluation-{_utc_now_id()}"
    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.raw_dir.mkdir(parents=True, exist_ok=True)
    write_run_card(path=args.output_dir / "run-card.json", run_id=run_id, args=args, manifest=manifest, rows=rows)

    base_arm = ArmConfig(BASE_ARM, BASE_ARM, None)
    final_arm = ArmConfig(FINAL_ARM, FINAL_ARM, args.adapter_path)
    base_predictions = _predict_rows(
        arm=base_arm,
        rows=rows,
        base_model=args.base_model,
        max_new_tokens=args.max_new_tokens,
        raw_dir=args.raw_dir,
    )
    final_predictions = _predict_rows(
        arm=final_arm,
        rows=rows,
        base_model=args.base_model,
        max_new_tokens=args.max_new_tokens,
        raw_dir=args.raw_dir,
    )
    base_metrics = public_metrics_payload(arm=base_arm, rows=rows, predictions=base_predictions)
    final_metrics = public_metrics_payload(arm=final_arm, rows=rows, predictions=final_predictions)
    comparison = comparison_payload(base_metrics, final_metrics)
    write_json(args.output_dir / "base" / "metrics.json", base_metrics)
    write_json(args.output_dir / "final-sft" / "metrics.json", final_metrics)
    write_json(args.output_dir / "comparison.json", comparison)
    write_comparison_markdown(args.output_dir / "comparison.md", comparison)
    write_human_brief(args.human_brief, comparison)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
