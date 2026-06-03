from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from voice2task.evaluation import EvaluationResult
from voice2task.io import write_json


def write_metrics_report(
    result: EvaluationResult,
    output_dir: Path,
    title: str = "Voice2Task contract metrics",
) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "metrics.json"
    markdown_path = output_dir / "metrics.md"
    write_json(json_path, result.to_dict())
    lines = [
        f"# {title}",
        "",
        (
            "This report summarizes contract-level metrics only. "
            "No live-browser improvement claim is made from these numbers."
        ),
        "",
        "## Metrics",
        "",
    ]
    for name, value in sorted(result.metrics.items()):
        lines.append(f"- `{name}`: {value:.4f}")
    lines.extend(["", "## Failure Slices", ""])
    for name, entry in sorted(result.failure_slices.items()):
        examples = ", ".join(entry["examples"]) if entry["examples"] else "none"
        lines.append(f"- `{name}`: {entry['count']} examples ({examples})")
    markdown_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"json": json_path, "markdown": markdown_path}


def write_schema_diagnostics_report(
    diagnostics: dict[str, Any],
    output_dir: Path,
    title: str = "Voice2Task schema diagnostics",
) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "schema_diagnostics.json"
    markdown_path = output_dir / "schema_diagnostics.md"
    write_json(json_path, diagnostics)

    summary = diagnostics["summary"]
    lines = [
        f"# {title}",
        "",
        (
            "This diagnostic is evidence-only: invalid predictions remain invalid. "
            "It does not repair, normalize, or convert private-adapter predictions into valid contracts."
        ),
        "",
        "## Boundary",
        "",
        "- This is not a checkpoint release.",
        "- This is not an adapter release.",
        "- This makes no production-readiness claim.",
        "- This makes no full-private-corpus claim.",
        "- This is not a live-browser benchmark or benchmark-improvement claim.",
        "",
        "## Summary",
        "",
        f"- Gold rows: `{summary['gold_row_count']}`",
        f"- Predictions: `{summary['prediction_count']}`",
        f"- Invalid predictions: `{summary['invalid_prediction_count']}`",
        "",
        "## Issue Counts",
        "",
    ]
    issue_counts = summary.get("issue_counts", {})
    if issue_counts:
        for category, count in sorted(issue_counts.items()):
            lines.append(f"- `{category}`: `{count}`")
    else:
        lines.append("- none")
    lines.extend(["", "## Row Issues", ""])
    for row in diagnostics.get("rows", []):
        lines.append(f"### `{row['row_id']}`")
        lines.append("")
        for issue in row["issues"]:
            lines.append(
                "- "
                f"`{issue['field_path']}` "
                f"({issue['issue_category']}): observed {issue['observed_value_summary']}; "
                f"expected {issue['expected_constraint']}"
            )
        lines.append("")

    markdown_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return {"json": json_path, "markdown": markdown_path}


def write_alignment_diagnostics_report(
    diagnostics: dict[str, Any],
    output_dir: Path,
    title: str = "Voice2Task alignment diagnostics",
) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "alignment_diagnostics.json"
    markdown_path = output_dir / "alignment_diagnostics.md"
    write_json(json_path, diagnostics)

    summary = diagnostics["summary"]
    lines = [
        f"# {title}",
        "",
        (
            "This diagnostic is evidence-only: invalid predictions remain invalid. "
            "It reports field-level public-sample evidence only and does not repair, normalize, "
            "coerce, or replace prediction fields."
        ),
        "",
        "## Boundary",
        "",
        "- This is not a checkpoint release.",
        "- This is not an adapter release.",
        "- This makes no production-readiness claim.",
        "- This makes no full-private-corpus claim.",
        "- This is not a live-browser benchmark or benchmark-improvement claim.",
        "",
        "## Summary",
        "",
        f"- Gold rows: `{summary['gold_row_count']}`",
        f"- Predictions: `{summary['prediction_count']}`",
        f"- Rows with mismatches: `{summary['row_mismatch_count']}`",
        f"- Schema-invalid predictions: `{summary['schema_invalid_prediction_count']}`",
        "",
        "## Field Mismatch Counts",
        "",
    ]
    field_counts = summary.get("field_mismatch_counts", {})
    if field_counts:
        for field_path, count in sorted(field_counts.items()):
            lines.append(f"- `{field_path}`: `{count}`")
    else:
        lines.append("- none")
    lines.extend(["", "## Mismatch Category Counts", ""])
    category_counts = summary.get("mismatch_category_counts", {})
    if category_counts:
        for category, count in sorted(category_counts.items()):
            lines.append(f"- `{category}`: `{count}`")
    else:
        lines.append("- none")
    lines.extend(["", "## Row Mismatches", ""])
    for row in diagnostics.get("rows", []):
        lines.append(f"### `{row['row_id']}`")
        lines.append("")
        for mismatch in row["mismatches"]:
            lines.append(
                "- "
                f"`{mismatch['field_path']}` "
                f"({mismatch['mismatch_category']}): gold {mismatch['gold_value_summary']}; "
                f"prediction {mismatch['prediction_value_summary']}"
            )
        lines.append("")

    markdown_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return {"json": json_path, "markdown": markdown_path}


def write_prediction_evidence_pack(
    *,
    output_dir: Path,
    prediction_path: Path,
    prediction_metadata: dict[str, Any],
    metrics_path: Path,
    smoke_result: dict[str, Any],
    leak_scan_result: dict[str, Any],
) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "manifest.json"
    report_path = output_dir / "report.md"
    release_status = str(prediction_metadata.get("release_status", "not_released"))
    prediction_source_kind = str(prediction_metadata.get("prediction_source_kind", "unknown"))
    manifest = {
        "evidence_kind": "a100_sft_prediction_eval_smoke",
        "evidence_status": prediction_metadata.get("prediction_status", "unknown"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "base_model": prediction_metadata.get("base_model"),
        "model_source": prediction_metadata.get("model_source", "unknown"),
        "dataset_manifest_id": prediction_metadata.get("dataset_manifest_id"),
        "prediction_artifact_path": prediction_path.as_posix(),
        "prediction_source_kind": prediction_source_kind,
        "prediction_count": prediction_metadata.get("prediction_count"),
        "metrics_path": metrics_path.as_posix(),
        "controlled_smoke_status": smoke_result,
        "leak_scan_result": leak_scan_result,
        "release_status": release_status,
        "claims": {
            "checkpoint_release": False,
            "adapter_release": False,
            "live_browser_benchmark_claim": False,
            "production_readiness_claim": False,
        },
        "artifact_policy": {
            "raw_logs_copied_to_git": False,
            "checkpoints_or_adapters_copied_to_git": False,
            "remote_caches_copied_to_git": False,
            "private_paths_omitted": True,
        },
    }
    write_json(manifest_path, manifest)
    lines = [
        "# A100 SFT Prediction/Eval Smoke Evidence",
        "",
        (
            "Status: public-sample prediction/evaluation smoke evidence. "
            "This is not a checkpoint release and not a live-browser benchmark."
        ),
        "",
        "## Scope",
        "",
        f"- Base model: `{manifest['base_model']}`",
        f"- Model source: `{manifest['model_source']}`",
        f"- Dataset manifest: `{manifest['dataset_manifest_id']}`",
        f"- Prediction source kind: `{prediction_source_kind}`",
        f"- Release status: `{release_status}`",
        "",
        "## Interpretation",
        "",
        (
            "If `prediction_source_kind` is `public_sample_contract_fixture`, the predictions are deterministic "
            "public-sample contract fixtures used to validate the evidence pipeline. They are not private adapter "
            "model outputs and must not be presented as model-quality evidence."
        ),
        (
            "If `prediction_source_kind` is `private_a100_adapter`, the predictions came from the private A100 "
            "adapter path, but the metrics and controlled smoke results still only describe this bounded public "
            "sample. Failed schema or smoke results must be reported as failures, not hidden behind the existence "
            "of a completed training run."
        ),
        "",
        "## Public Artifacts",
        "",
        f"- Predictions: `{prediction_path.as_posix()}`",
        f"- Metrics: `{metrics_path.as_posix()}`",
        f"- Controlled smoke: `{smoke_result.get('notes', 'unknown')}`",
        f"- Leak scan ok: `{bool(leak_scan_result.get('ok'))}`",
        "",
        "## Boundary",
        "",
        (
            "The evidence pack may contain sanitized public-sample contract predictions, aggregate metrics, "
            "controlled smoke status, and leak-scan status. It does not copy raw logs, checkpoints, adapters, "
            "remote caches, private paths, host details, tokens, or private corpus rows into git."
        ),
    ]
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"manifest": manifest_path, "report": report_path}
