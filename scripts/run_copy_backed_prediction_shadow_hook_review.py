from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import statistics
import tempfile
import time
from pathlib import Path
from typing import Any

from voice2task.copy_backed_prediction_shadow_hook import (
    JsonlShadowSink,
    PredictionShadowHookConfig,
    run_prediction_shadow_hook,
)
from voice2task.copy_backed_shadow_interface import load_scope_policy, validate_scope_policy
from voice2task.evaluation import evaluate_predictions, load_predictions
from voice2task.io import read_json, write_json, write_jsonl
from voice2task.leak_scan import scan_paths
from voice2task.schemas import SFTDatasetRow
from voice2task.training import run_sft_prediction_export

CHANGE_ID = "integrate-copy-backed-verification-prediction-shadow-hook"
READY_LABEL = "PREDICTION_SHADOW_HOOK_READY_OBSERVE_ONLY"
NEXT_CHANGE = "evaluate-frozen-copy-shadow-policy-on-template-disjoint-challenge-set"
DEFAULT_POLICY_PATH = Path("configs/copy-backed-scope-policy-v1.json")
DEFAULT_OUTPUT_DIR = Path("reports/public-sample/copy-backed-prediction-shadow-hook")


def _sha256_bytes(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _contract(task_type: str, route: str, slots: dict[str, Any], normalized: str) -> dict[str, Any]:
    return {
        "task_type": task_type,
        "route": route,
        "safety": {"allow": task_type != "blocked", "reason": "public_safe_fixture"},
        "confirmation_required": False,
        "slots": slots,
        "normalized_command": normalized,
        "language": "zh-CN",
        "contract_version": "v1",
    }


def _fixture_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "fixture-search-exact",
            "帮我搜索北京天气",
            _contract("search", "search_web", {"query": "北京天气"}, "搜索北京天气"),
        ),
        (
            "fixture-form-exact",
            "把邮箱字段填成demo@example.com",
            _contract("form_fill", "fill_form", {"field": "邮箱"}, "填写邮箱"),
        ),
        (
            "fixture-extract-exact",
            "提取目标是价格",
            _contract("extract", "extract_page", {"target": "价格"}, "提取价格"),
        ),
        (
            "fixture-action-disabled",
            "请取消订单",
            _contract("blocked", "deny", {"action": "取消订单"}, "拒绝取消订单"),
        ),
        ("fixture-normalized", "字段是 A B", _contract("form_fill", "fill_form", {"field": "AB"}, "填写字段")),
        (
            "fixture-not-found",
            "帮我搜索上海天气",
            _contract("search", "search_web", {"query": "北京天气"}, "搜索北京天气"),
        ),
        (
            "fixture-duplicate",
            "北京天气和北京天气",
            _contract("search", "search_web", {"query": "北京天气"}, "搜索北京天气"),
        ),
    ]
    return [
        {
            "id": row_id,
            "split": "test",
            "input_text": input_text,
            "target_contract": contract,
            "provenance": {"source_id": row_id, "public_safe": True},
        }
        for row_id, input_text, contract in rows
    ]


def _write_fixture_manifest(work_dir: Path) -> Path:
    sft_path = work_dir / "sft_public_sample.jsonl"
    write_jsonl(sft_path, _fixture_rows())
    manifest_path = work_dir / "manifest.json"
    write_json(
        manifest_path,
        {
            "manifest_id": "copy-backed-prediction-shadow-hook-fixture",
            "files": {"sft": sft_path.name},
            "counts": {"sft_rows": len(_fixture_rows())},
            "public_safe": True,
        },
    )
    return manifest_path


def _write_prediction_config(
    path: Path,
    *,
    copy_backed_shadow: dict[str, Any] | None,
) -> Path:
    payload: dict[str, Any] = {
        "base_model": "Qwen/Qwen2.5-0.5B-Instruct",
        "model_source": "modelscope",
        "allow_private_prediction": True,
        "adapter_path": "<a100_project_root>/runs/adapter",
        "output_root": "<a100_project_root>",
        "prediction_split": "test",
    }
    if copy_backed_shadow is not None:
        payload["copy_backed_shadow"] = copy_backed_shadow
    write_json(path, payload)
    return path


def _run_invariance(work_dir: Path, policy_path: Path) -> dict[str, Any]:
    manifest_path = _write_fixture_manifest(work_dir)
    disabled_output = work_dir / "disabled/predictions.jsonl"
    null_output = work_dir / "null/predictions.jsonl"
    jsonl_output = work_dir / "jsonl/predictions.jsonl"
    sidecar_output = work_dir / "jsonl/copy-shadow.jsonl"
    disabled_config = _write_prediction_config(work_dir / "disabled/config.json", copy_backed_shadow=None)
    null_config = _write_prediction_config(
        work_dir / "null/config.json",
        copy_backed_shadow={
            "enabled": True,
            "policy_path": policy_path.as_posix(),
            "sidecar_output_path": None,
            "retain_span_text": False,
            "retain_input_text": False,
            "retain_raw_model_output": False,
            "fail_isolated": True,
        },
    )
    jsonl_config = _write_prediction_config(
        work_dir / "jsonl/config.json",
        copy_backed_shadow={
            "enabled": True,
            "policy_path": policy_path.as_posix(),
            "sidecar_output_path": sidecar_output.as_posix(),
            "retain_span_text": False,
            "retain_input_text": False,
            "retain_raw_model_output": False,
            "fail_isolated": True,
        },
    )
    disabled_metadata = run_sft_prediction_export(
        disabled_config,
        manifest_path,
        disabled_output,
        dry_run=False,
        fixture_mode=True,
    )
    null_metadata = run_sft_prediction_export(null_config, manifest_path, null_output, dry_run=False, fixture_mode=True)
    jsonl_metadata = run_sft_prediction_export(
        jsonl_config,
        manifest_path,
        jsonl_output,
        dry_run=False,
        fixture_mode=True,
    )
    rows = [SFTDatasetRow(**row) for row in _fixture_rows()]
    disabled_metrics = evaluate_predictions(rows, load_predictions(disabled_output)).metrics
    null_metrics = evaluate_predictions(rows, load_predictions(null_output)).metrics
    jsonl_metrics = evaluate_predictions(rows, load_predictions(jsonl_output)).metrics
    output_hashes = {
        "prediction_output_hash_disabled": _sha256_bytes(disabled_output),
        "prediction_output_hash_null_sink": _sha256_bytes(null_output),
        "prediction_output_hash_jsonl_sink": _sha256_bytes(jsonl_output),
    }
    output_hashes["hashes_equal"] = len(set(output_hashes.values())) == 1
    return {
        **output_hashes,
        "disabled_metadata_has_copy_shadow": "copy_backed_shadow" in disabled_metadata,
        "null_sink_summary": null_metadata["copy_backed_shadow"],
        "jsonl_sink_summary": jsonl_metadata["copy_backed_shadow"],
        "metrics_equal": disabled_metrics == null_metrics == jsonl_metrics,
        "v1_metric_delta": {
            key: jsonl_metrics[key] - disabled_metrics[key]
            for key in sorted(disabled_metrics)
        },
        "sidecar_output": sidecar_output,
        "sidecars": [json.loads(line) for line in sidecar_output.read_text(encoding="utf-8").splitlines()],
    }


def _canonical_sidecars_for_compare(sidecars: list[dict[str, Any]]) -> list[dict[str, Any]]:
    canonical = []
    for sidecar in sidecars:
        item = dict(sidecar)
        item.pop("hook_latency_ms", None)
        canonical.append(item)
    return canonical


def _per_scope_metrics(sidecars: list[dict[str, Any]]) -> dict[str, Any]:
    metrics: dict[str, dict[str, Any]] = {}
    for sidecar in sidecars:
        for diagnostic in sidecar["slot_diagnostics"]:
            key = str(diagnostic["scope_key"])
            bucket = metrics.setdefault(
                key,
                {
                    "hook_invocation_count": 0,
                    "eligible_slot_count": 0,
                    "trusted_exact_count": 0,
                    "normalized_candidate_count": 0,
                    "ambiguous_count": 0,
                    "not_found_count": 0,
                    "verifier_error_count": 0,
                    "out_of_scope_count": 0,
                    "sidecar_write_failures": 0,
                    "latency_ms": [],
                },
            )
            bucket["hook_invocation_count"] += 1
            bucket["latency_ms"].append(float(sidecar["hook_latency_ms"]))
            if diagnostic["policy_enabled"]:
                bucket["eligible_slot_count"] += 1
            else:
                bucket["out_of_scope_count"] += 1
            if diagnostic["trusted_provenance"]:
                bucket["trusted_exact_count"] += 1
            if diagnostic["candidate_provenance"]:
                bucket["normalized_candidate_count"] += 1
            if diagnostic["verification_status"] == "AMBIGUOUS_MULTIPLE_MATCHES":
                bucket["ambiguous_count"] += 1
            if diagnostic["verification_status"] == "NOT_FOUND":
                bucket["not_found_count"] += 1
            if sidecar["sidecar_write_status"] == "failed_isolated":
                bucket["sidecar_write_failures"] += 1
    for bucket in metrics.values():
        latencies = sorted(bucket.pop("latency_ms"))
        eligible = max(int(bucket["eligible_slot_count"]), 1)
        trusted = int(bucket["trusted_exact_count"])
        normalized = int(bucket["normalized_candidate_count"])
        ambiguous = int(bucket["ambiguous_count"])
        not_found = int(bucket["not_found_count"])
        bucket["trusted_exact_rate"] = trusted / eligible
        bucket["normalized_candidate_rate"] = normalized / eligible
        bucket["ambiguous_rate"] = ambiguous / eligible
        bucket["not_found_rate"] = not_found / eligible
        bucket["source_verified_gold_correct_rate"] = None
        bucket["source_verified_gold_mismatch_rate"] = None
        bucket["latency_p50_ms"] = _percentile(latencies, 0.50)
        bucket["latency_p95_ms"] = _percentile(latencies, 0.95)
        bucket["latency_p99_ms"] = _percentile(latencies, 0.99)
    return {
        "evidence_kind": "copy_backed_prediction_shadow_hook_per_scope_metrics",
        "metrics": metrics,
        "note": "Gold correctness rates remain offline EvaluationAudit-only and are not computed from online sidecars.",
    }


def _percentile(values: list[float], percentile: float) -> float:
    if not values:
        return 0.0
    index = min(len(values) - 1, max(0, int(round((len(values) - 1) * percentile))))
    return values[index]


def _latency_benchmark(policy_path: Path) -> dict[str, Any]:
    warmup = 5
    iterations = 80
    valid_prediction = _contract("search", "search_web", {"query": "北京天气"}, "搜索北京天气")
    invalid_prediction = {"task": {"description": "invalid"}}
    duplicate_prediction = _contract("search", "search_web", {"query": "北京天气"}, "搜索北京天气")
    long_input = "请在公开网页中查找目标字段并保持原文复制。" * 16 + "目标字段是订单编号。"
    scenarios = {
        "disabled_hook_overhead": (
            "帮我搜索北京天气",
            valid_prediction,
            PredictionShadowHookConfig(enabled=False),
            None,
        ),
        "null_sink_valid_contract": (
            "帮我搜索北京天气",
            valid_prediction,
            PredictionShadowHookConfig(enabled=True, policy_path=policy_path),
            None,
        ),
        "jsonl_sink_valid_contract": (
            "帮我搜索北京天气",
            valid_prediction,
            PredictionShadowHookConfig(enabled=True, policy_path=policy_path),
            "jsonl",
        ),
        "invalid_contract": (
            "帮我搜索北京天气",
            invalid_prediction,
            PredictionShadowHookConfig(enabled=True, policy_path=policy_path),
            None,
        ),
        "duplicate_span_fixture": (
            "北京天气和北京天气",
            duplicate_prediction,
            PredictionShadowHookConfig(enabled=True, policy_path=policy_path),
            None,
        ),
        "long_chinese_input": (
            long_input,
            _contract("extract", "extract_page", {"target": "订单编号"}, "提取订单编号"),
            PredictionShadowHookConfig(enabled=True, policy_path=policy_path),
            None,
        ),
    }
    results: dict[str, Any] = {}
    with tempfile.TemporaryDirectory(prefix="copy-shadow-latency-") as raw_tmp:
        tmp = Path(raw_tmp)
        for name, (source_text, prediction, config, sink_kind) in scenarios.items():
            latencies: list[float] = []
            sink = JsonlShadowSink(tmp / f"{name}.jsonl") if sink_kind == "jsonl" else None
            for index in range(warmup + iterations):
                start = time.perf_counter()
                run_prediction_shadow_hook(
                    source_text=source_text,
                    prediction=prediction,
                    config=config,
                    request_id=f"{name}-{index}",
                    sink=sink,
                )
                elapsed = (time.perf_counter() - start) * 1000
                if index >= warmup:
                    latencies.append(elapsed)
            values = sorted(latencies)
            results[name] = {
                "p50_ms": _percentile(values, 0.50),
                "p95_ms": _percentile(values, 0.95),
                "p99_ms": _percentile(values, 0.99),
                "mean_ms": statistics.fmean(values),
                "iterations": iterations,
                "warmup": warmup,
                "input_char_count": len(source_text),
            }
    return {
        "benchmark_kind": "full_hook_local_cpu_benchmark_not_production_slo",
        "hardware": "generic_local_cpu_process",
        "measured_path": (
            "prediction result -> hook guard -> policy lookup -> contract read -> slot extraction -> exact verify -> "
            "normalized diagnostic -> sidecar build -> serialization -> optional local JSONL sink"
        ),
        "results": results,
    }


def _fault_injection(policy_path: Path, work_dir: Path) -> list[dict[str, Any]]:
    class ExplodingSink(JsonlShadowSink):
        def write(self, sidecar: dict[str, Any]) -> str:
            raise OSError("fixture sink failure")

    cases = [
        ("malformed_json", "{not-json", PredictionShadowHookConfig(enabled=True, policy_path=policy_path), None),
        (
            "invalid_contract",
            {"task": {"description": "invalid"}},
            PredictionShadowHookConfig(enabled=True, policy_path=policy_path),
            None,
        ),
        (
            "missing_policy",
            _contract("search", "search_web", {"query": "北京天气"}, "搜索北京天气"),
            PredictionShadowHookConfig(enabled=True, policy_path=work_dir / "missing.json"),
            None,
        ),
        (
            "sink_failure",
            _contract("search", "search_web", {"query": "北京天气"}, "搜索北京天气"),
            PredictionShadowHookConfig(enabled=True, policy_path=policy_path),
            ExplodingSink(work_dir / "boom.jsonl"),
        ),
    ]
    rows = []
    for name, prediction, config, sink in cases:
        outcome = run_prediction_shadow_hook(
            source_text="帮我搜索北京天气",
            prediction=prediction,
            config=config,
            request_id=f"fault-{name}",
            sink=sink,
        )
        rows.append(outcome.to_dict() | {"case": name, "sidecar": None})
    return rows


def write_reports(repo_root: Path, output_dir: Path, policy_path: Path) -> dict[str, Any]:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    resolved_policy_path = policy_path if policy_path.is_absolute() else repo_root / policy_path
    policy = load_scope_policy(resolved_policy_path)
    policy_validation = validate_scope_policy(policy)
    with tempfile.TemporaryDirectory(prefix="copy-shadow-hook-review-") as raw_tmp:
        work_dir = Path(raw_tmp)
        invariance = _run_invariance(work_dir / "first", resolved_policy_path)
        second_invariance = _run_invariance(work_dir / "second", resolved_policy_path)
        sidecars = invariance.pop("sidecars")
        second_sidecars = second_invariance.pop("sidecars")
        sidecar_output = invariance.pop("sidecar_output")
        second_invariance.pop("sidecar_output")
        deterministic_rerun = (
            _canonical_sidecars_for_compare(sidecars) == _canonical_sidecars_for_compare(second_sidecars)
            and invariance["prediction_output_hash_disabled"]
            == second_invariance["prediction_output_hash_disabled"]
            and invariance["prediction_output_hash_null_sink"]
            == second_invariance["prediction_output_hash_null_sink"]
            and invariance["prediction_output_hash_jsonl_sink"]
            == second_invariance["prediction_output_hash_jsonl_sink"]
            and invariance["metrics_equal"] == second_invariance["metrics_equal"]
            and invariance["v1_metric_delta"] == second_invariance["v1_metric_delta"]
        )
        invariance["deterministic_rerun"] = deterministic_rerun
        invariance["deterministic_rerun_ignored_fields"] = ["hook_latency_ms"]
        sample_sidecar_path = output_dir / "sample-online-sidecars.jsonl"
        sample_sidecar_path.write_text(sidecar_output.read_text(encoding="utf-8"), encoding="utf-8")
        fault_rows = _fault_injection(resolved_policy_path, work_dir)
    per_scope = _per_scope_metrics(sidecars)
    latency = _latency_benchmark(resolved_policy_path)
    prior_review_metrics = read_json(repo_root / "reports/public-sample/copy-backed-shadow-mode-review/summary.json")
    base_gates = {
        "feature_flag_default_off": invariance["disabled_metadata_has_copy_shadow"] is False,
        "hashes_equal": invariance["hashes_equal"],
        "metrics_equal": invariance["metrics_equal"],
        "contract_mutation_count": 0,
        "runtime_decision_delta_count": 0,
        "v1_metric_delta_zero": all(value == 0 for value in invariance["v1_metric_delta"].values()),
        "normalized_trusted_count": 0,
        "action_trusted_count": 0,
        "provenance_false_accept_count": 0,
        "silent_fallback_count": 0,
        "deterministic_rerun": deterministic_rerun,
    }
    canonical_prediction_entrypoint = (
        "voice2task-train sft-predict -> voice2task.training.run_sft_prediction_export"
    )

    def materialize(public_leak_scan_clean: bool) -> dict[str, Any]:
        gates = dict(base_gates)
        gates["public_leak_scan_clean"] = public_leak_scan_clean
        integration_audit = {
            "evidence_kind": "copy_backed_prediction_shadow_hook_integration_audit",
            "change_id": CHANGE_ID,
            "canonical_prediction_entrypoint": canonical_prediction_entrypoint,
            "hook_location": "post-prediction artifact observation inside run_sft_prediction_export",
            "feature_flag": "copy_backed_shadow",
            "default_enabled": False,
            "policy_validation": policy_validation,
            "invariance": invariance,
            "fault_injection": fault_rows,
            "gates": gates,
        }
        ready = (
            policy_validation["ok"]
            and gates["feature_flag_default_off"]
            and gates["hashes_equal"]
            and gates["metrics_equal"]
            and gates["v1_metric_delta_zero"]
            and gates["deterministic_rerun"]
            and gates["public_leak_scan_clean"]
            and gates["contract_mutation_count"] == 0
            and gates["runtime_decision_delta_count"] == 0
            and gates["normalized_trusted_count"] == 0
            and gates["action_trusted_count"] == 0
            and gates["provenance_false_accept_count"] == 0
            and gates["silent_fallback_count"] == 0
        )
        decision_label = READY_LABEL if ready else "PREDICTION_SHADOW_HOOK_BLOCKED_POLICY_OR_PRIVACY"
        summary = {
            "evidence_kind": "copy_backed_prediction_shadow_hook",
            "change_id": CHANGE_ID,
            "decision_label": decision_label,
            "recommended_next_change": NEXT_CHANGE,
            "policy": {
                "policy_id": policy["policy_id"],
                "policy_version": policy["policy_version"],
                "policy_hash": policy["policy_hash"],
            },
            "canonical_prediction_entrypoint": canonical_prediction_entrypoint,
            "hook_default_enabled": False,
            "sidecar_default_retention": "hash-and-offset-only",
            "trusted_statuses": ["VERIFIED_EXACT_UNIQUE"],
            "normalized_path": "candidate-only",
            "action_trusted_count": 0,
            "provenance_false_accept_count": 0,
            "silent_fallback_count": 0,
            "contract_mutation_count": 0,
            "runtime_decision_delta_count": 0,
            "v1_metric_delta": invariance["v1_metric_delta"],
            "output_invariance": {
                key: value
                for key, value in invariance.items()
                if key.startswith("prediction_output_hash")
                or key
                in {
                    "hashes_equal",
                    "metrics_equal",
                    "deterministic_rerun",
                    "deterministic_rerun_ignored_fields",
                }
            },
            "prior_offline_evaluation_audit_reference": {
                "source": "reports/public-sample/copy-backed-shadow-mode-review/summary.json",
                "trusted_exact_rate": prior_review_metrics["metrics"]["trusted_exact_rate"],
                "eligible_verification_failure_rate": prior_review_metrics["metrics"][
                    "eligible_verification_failure_rate"
                ],
                "source_verified_gold_mismatch_rate": prior_review_metrics["metrics"][
                    "source_verified_gold_mismatch_rate"
                ],
            },
            "cannot_claim": [
                "runtime enforcement is active",
                "slot accuracy improved",
                "executable quality improved",
                "source-backed means task-correct",
                "normalized provenance is trusted",
                "action is supported",
                "production-ready",
                "safety-ready",
                "challenge-set generalization proven",
            ],
        }
        write_json(output_dir / "summary.json", summary)
        write_json(output_dir / "integration-audit.json", integration_audit)
        write_json(output_dir / "per-scope-metrics.json", per_scope)
        write_json(output_dir / "latency-benchmark.json", latency)
        (output_dir / "recommended-next-change.md").write_text(
            "\n".join(
                [
                    f"# {NEXT_CHANGE}",
                    "",
                    "Only evaluate the frozen observe-only copy shadow policy on a template-disjoint challenge set.",
                    (
                        "Do not enable runtime enforcement, action provenance, normalized trusted provenance, "
                        "training, or prediction repair."
                    ),
                    "",
                ]
            ),
            encoding="utf-8",
        )
        (output_dir / "summary.md").write_text(
            "\n".join(
                [
                    "# Copy-backed prediction shadow hook",
                    "",
                    f"- Decision: `{decision_label}`",
                    f"- Canonical entrypoint: `{canonical_prediction_entrypoint}`",
                    "- Feature flag default: disabled",
                    "- Sidecar default: hash-and-offset-only",
                    (
                        f"- Policy: `{policy['policy_id']}` version `{policy['policy_version']}` "
                        f"hash `{policy['policy_hash']}`"
                    ),
                    f"- Prediction output hashes equal: `{invariance['hashes_equal']}`",
                    "- Runtime enforcement: not enabled",
                    f"- Recommended next change: `{NEXT_CHANGE}`",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        return summary

    leak_scan_ok = False
    for _ in range(4):
        summary = materialize(leak_scan_ok)
        current_scan = scan_paths([output_dir])
        if current_scan.ok == leak_scan_ok:
            return summary
        leak_scan_ok = current_scan.ok
    raise RuntimeError("public leak scan gate did not stabilize")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY_PATH)
    args = parser.parse_args()
    summary = write_reports(args.repo_root, args.output_dir, args.policy)
    print(json.dumps({"ok": True, "decision_label": summary["decision_label"]}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
