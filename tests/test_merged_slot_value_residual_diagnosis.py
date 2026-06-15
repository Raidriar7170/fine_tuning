import json
from pathlib import Path

import pytest

from voice2task.cli import eval as eval_cli
from voice2task.evaluation import diagnose_merged_slot_value_residuals
from voice2task.io import write_json
from voice2task.leak_scan import scan_paths
from voice2task.reports import write_merged_slot_value_residual_report
from voice2task.schemas import SFTDatasetRow


def _contract(
    *,
    task_type: str = "form_fill",
    route: str = "fill_form",
    slots: dict[str, str] | None = None,
    normalized_command: str = "填写邮箱并确认",
) -> dict[str, object]:
    return {
        "task_type": task_type,
        "route": route,
        "safety": {"allow": True, "reason": "requires_confirmation"},
        "confirmation_required": True,
        "slots": slots if slots is not None else {"field": "邮箱"},
        "normalized_command": normalized_command,
        "language": "zh-CN",
        "contract_version": "v1",
    }


def _row(row_id: str, split: str, target_contract: dict[str, object]) -> SFTDatasetRow:
    return SFTDatasetRow(
        id=row_id,
        split=split,
        input_text=f"public sample {row_id}",
        target_contract=target_contract,
        provenance={"source_id": row_id.rsplit("-", 1)[0], "public_safe": True},
    )


def _source_manifest() -> dict[str, object]:
    return {
        "evidence_kind": "a100_merged_slot_value_heldout_eval",
        "dataset_manifest_id": "public-sample-test",
        "base_model": "Qwen/Qwen2.5-7B-Instruct",
        "split_results": {
            "dev": {
                "contract_exact_match": 0.5,
                "slot_f1": 0.5,
                "slot_f1_soft": 1.0,
                "json_valid_rate": 1.0,
                "task_type_accuracy": 1.0,
                "route_accuracy": 1.0,
                "confirmation_accuracy": 1.0,
                "safety_precision": 1.0,
                "safety_recall": 1.0,
                "residual_row_count": 1,
            },
            "test": {
                "contract_exact_match": 0.8333333333333334,
                "slot_f1": 1.0,
                "slot_f1_soft": 1.0,
                "json_valid_rate": 1.0,
                "task_type_accuracy": 1.0,
                "route_accuracy": 1.0,
                "confirmation_accuracy": 1.0,
                "safety_precision": 1.0,
                "safety_recall": 1.0,
                "residual_row_count": 1,
            },
        },
    }


def test_merged_slot_value_residual_diagnostic_classifies_strict_remaining_mismatches() -> None:
    form_gold = _contract()
    open_gold = _contract(
        task_type="navigate",
        route="open_url",
        slots={"url": "https://example.com"},
        normalized_command="打开示例网站",
    )
    rows_by_split = {
        "dev": [_row("seed-form-email-dev", "dev", form_gold)],
        "test": [_row("seed-open-example-test", "test", open_gold)],
    }
    predictions_by_split = {
        "dev": {"seed-form-email-dev": {**form_gold, "slots": {"field": "email"}}},
        "test": {"seed-open-example-test": {**open_gold, "normalized_command": "访问示例网站"}},
    }

    diagnosis = diagnose_merged_slot_value_residuals(
        merged_manifest=_source_manifest(),
        rows_by_split=rows_by_split,
        predictions_by_split=predictions_by_split,
    )

    assert diagnosis["evidence_kind"] == "merged_slot_value_residual_diagnosis"
    assert diagnosis["diagnostic_mode"] == "public_safe_no_training_no_prediction_no_metric_change"
    assert diagnosis["source_merged_eval"]["evidence_kind"] == "a100_merged_slot_value_heldout_eval"
    assert diagnosis["summary"]["strict_contract_exact_match"] == {
        "dev": 0.5,
        "test": 0.8333333333333334,
    }
    assert diagnosis["summary"]["strict_slot_f1"] == {"dev": 0.5, "test": 1.0}
    assert diagnosis["summary"]["soft_slot_f1"] == {"dev": 1.0, "test": 1.0}
    assert diagnosis["summary"]["soft_slot_f1_primary_metric"] is False
    assert diagnosis["summary"]["residual_row_count"] == 2
    assert diagnosis["summary"]["residual_field_counts"] == {"normalized_command": 1, "slots": 1}
    assert diagnosis["summary"]["source_count_consistency"]["ok"] is True
    assert diagnosis["summary"]["source_count_consistency"]["by_split"] == {
        "dev": {"computed": 1, "expected": 1, "ok": True},
        "test": {"computed": 1, "expected": 1, "ok": True},
    }
    assert diagnosis["summary"]["residual_category_counts"] == {
        "normalized_command_strict_string_mismatch": 1,
        "slot_value_strict_mismatch_soft_match": 1,
    }
    assert diagnosis["summary"]["recommended_next_step"] == "review_residual_buckets_before_data_or_training_change"

    residuals = {(entry["split"], entry["row_id"], entry["field_path"]): entry for entry in diagnosis["residuals"]}
    assert residuals[("dev", "seed-form-email-dev", "slots")]["category"] == (
        "slot_value_strict_mismatch_soft_match"
    )
    assert residuals[("test", "seed-open-example-test", "normalized_command")]["category"] == (
        "normalized_command_strict_string_mismatch"
    )
    assert diagnosis["execution_scope"]["training_run"] is False
    assert diagnosis["execution_scope"]["prediction_run"] is False
    assert diagnosis["execution_scope"]["evaluator_metric_change"] is False
    assert diagnosis["claims"]["held_out_recovery_claim"] is False
    assert diagnosis["claims"]["semantic_equivalence_primary_metric"] is False


def test_merged_slot_value_residual_diagnostic_fails_closed_on_source_count_mismatch() -> None:
    gold = _contract()
    with pytest.raises(ValueError, match="residual count mismatch"):
        diagnose_merged_slot_value_residuals(
            merged_manifest=_source_manifest(),
            rows_by_split={"dev": [_row("seed-form-email-dev", "dev", gold)], "test": []},
            predictions_by_split={"dev": {"seed-form-email-dev": gold}, "test": {}},
        )


def test_merged_slot_value_residual_report_is_public_safe_and_bounded(tmp_path: Path) -> None:
    dev_gold = _contract()
    test_gold = _contract(
        task_type="navigate",
        route="open_url",
        slots={"url": "https://example.com"},
        normalized_command="打开示例网站",
    )
    diagnosis = diagnose_merged_slot_value_residuals(
        merged_manifest=_source_manifest(),
        rows_by_split={
            "dev": [_row("seed-form-email-dev", "dev", dev_gold)],
            "test": [_row("seed-open-example-test", "test", test_gold)],
        },
        predictions_by_split={
            "dev": {"seed-form-email-dev": {**dev_gold, "slots": {"field": "email"}}},
            "test": {"seed-open-example-test": {**test_gold, "normalized_command": "访问示例网站"}},
        },
    )

    paths = write_merged_slot_value_residual_report(diagnosis, tmp_path)

    assert paths["json"].exists()
    assert paths["markdown"].exists()
    assert paths["manifest"].exists()

    saved = json.loads(paths["json"].read_text(encoding="utf-8"))
    manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))
    markdown = paths["markdown"].read_text(encoding="utf-8")

    assert saved["claims"]["prediction_repair_or_replacement"] is False
    assert manifest["artifact_policy"]["private_paths_omitted"] is True
    assert manifest["claims"]["soft_slot_f1_primary_metric"] is False
    assert "strict `contract_exact_match` remains primary" in markdown
    assert "Soft slot F1 is internal diagnostic-only" in markdown
    assert "not held-out recovery" in markdown
    assert scan_paths([tmp_path]).ok is True


def test_merged_slot_value_residual_cli_filters_gold_rows_by_requested_split(tmp_path: Path, capsys: object) -> None:
    dev_gold = _contract()
    test_gold = _contract(
        task_type="navigate",
        route="open_url",
        slots={"url": "https://example.com"},
        normalized_command="打开示例网站",
    )
    all_rows = [
        _row("seed-form-email-dev", "dev", dev_gold).to_dict(),
        _row("seed-open-example-test", "test", test_gold).to_dict(),
    ]
    predictions_by_path = {
        "dev_predictions.jsonl": [
            {"id": "seed-form-email-dev", "prediction": {**dev_gold, "slots": {"field": "email"}}}
        ],
        "test_predictions.jsonl": [
            {
                "id": "seed-open-example-test",
                "prediction": {**test_gold, "normalized_command": "访问示例网站"},
            }
        ],
    }
    manifest_path = tmp_path / "manifest.json"
    gold_path = tmp_path / "all_sft_rows.jsonl"
    output_dir = tmp_path / "out"
    write_json(manifest_path, _source_manifest())
    gold_path.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in all_rows) + "\n",
        encoding="utf-8",
    )
    for name, rows in predictions_by_path.items():
        (tmp_path / name).write_text(
            "\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows) + "\n",
            encoding="utf-8",
        )

    assert (
        eval_cli.main(
            [
                "diagnose-merged-slot-value-residuals",
                "--merged-manifest",
                manifest_path.as_posix(),
                "--dev-gold",
                gold_path.as_posix(),
                "--dev-predictions",
                (tmp_path / "dev_predictions.jsonl").as_posix(),
                "--test-gold",
                gold_path.as_posix(),
                "--test-predictions",
                (tmp_path / "test_predictions.jsonl").as_posix(),
                "--output",
                output_dir.as_posix(),
            ]
        )
        == 0
    )
    cli_output = json.loads(capsys.readouterr().out)
    assert cli_output["ok"] is True
    diagnosis = json.loads((output_dir / "merged_slot_value_residual_diagnosis.json").read_text(encoding="utf-8"))
    assert diagnosis["summary"]["residual_row_count"] == 2
    assert diagnosis["aggregates"]["by_split_residual_rows"] == {"dev": 1, "test": 1}
    assert scan_paths([output_dir]).ok is True


def test_merged_residual_canonical_policy_evidence_is_public_safe_and_bounded() -> None:
    source_dir = Path("reports/public-sample/merged-slot-value-residual-diagnosis")
    evidence_dir = Path("reports/public-sample/merged-residual-canonical-policy")
    human_brief_path = Path("docs/human-briefs/2026-06-15-harden-merged-residual-canonical-policy.html")
    change_dirs = [
        Path("openspec/changes/harden-merged-residual-canonical-policy"),
        Path("openspec/changes/archive/2026-06-15-harden-merged-residual-canonical-policy"),
    ]
    expected_artifacts = {
        "canonical_policy_summary.json",
        "canonical_policy_summary.md",
        "manifest.json",
        "leak_scan_result.json",
    }

    assert evidence_dir.exists()
    assert expected_artifacts <= {path.name for path in evidence_dir.iterdir()}
    assert human_brief_path.exists()
    existing_change_dirs = [path for path in change_dirs if path.exists()]
    assert existing_change_dirs

    summary = json.loads((evidence_dir / "canonical_policy_summary.json").read_text(encoding="utf-8"))
    manifest = json.loads((evidence_dir / "manifest.json").read_text(encoding="utf-8"))
    report = (evidence_dir / "canonical_policy_summary.md").read_text(encoding="utf-8")
    human_brief = human_brief_path.read_text(encoding="utf-8")
    leak_scan = json.loads((evidence_dir / "leak_scan_result.json").read_text(encoding="utf-8"))
    source_diagnosis = json.loads(
        (source_dir / "merged_slot_value_residual_diagnosis.json").read_text(encoding="utf-8")
    )
    serialized = "\n".join(
        [
            json.dumps(summary, ensure_ascii=False, sort_keys=True),
            json.dumps(manifest, ensure_ascii=False, sort_keys=True),
            json.dumps(leak_scan, ensure_ascii=False, sort_keys=True),
            report,
            human_brief,
        ]
    )

    assert summary["evidence_kind"] == "merged_residual_canonical_policy_local"
    assert summary["source_prior_phase"] == source_dir.as_posix()
    assert summary["source_residual_counts"] == source_diagnosis["summary"]["residual_category_counts"]
    assert summary["targeted_residual_policy_counts"] == {
        "clarify_ambiguity_canonical_phrase": 3,
        "unsafe_payment_canonical_command": 1,
    }
    assert summary["prompt_constraints"]["clarify_ambiguity_canonical_phrase_visible"] is True
    assert summary["prompt_constraints"]["unsafe_payment_canonical_command_visible"] is True
    assert summary["claims"]["local_prompt_policy_hardening_only"] is True
    assert summary["claims"]["a100_execution_performed"] is False
    assert summary["claims"]["training_or_prediction_rerun_performed"] is False
    assert summary["claims"]["evaluator_metric_change"] is False
    assert summary["claims"]["held_out_recovery_claim"] is False

    assert manifest["evidence_kind"] == "merged_residual_canonical_policy_local"
    assert manifest["source_artifacts"]["merged_residual_diagnosis"].endswith(
        "merged_slot_value_residual_diagnosis.json"
    )
    assert manifest["diagnostic_artifacts"]["canonical_policy_summary"].endswith("canonical_policy_summary.json")
    assert manifest["diagnostic_artifacts"]["canonical_policy_report"].endswith("canonical_policy_summary.md")
    assert manifest["diagnostic_artifacts"]["leak_scan"].endswith("leak_scan_result.json")
    assert manifest["claims"]["held_out_recovery_claim"] is False

    assert leak_scan["ok"] is True
    assert leak_scan["findings"] == []
    assert "local prompt/policy hardening only" in report
    assert "No A100 execution was performed" in report
    assert "strict `contract_exact_match` remains primary" in report
    assert "pytest: `274 passed`" in report
    assert "ruff: `All checks passed!`" in report
    assert "mypy: `Success: no issues found in 16 source files`" in report
    assert "本地 prompt/policy hardening" in human_brief
    assert "不使用 A100" in human_brief
    assert "不改 evaluator metrics" in human_brief
    assert "274 passed" in human_brief
    assert "All checks passed!" in human_brief
    assert "/mnt/data/" not in serialized
    assert "/Users/" not in serialized
    assert "volcano" not in serialized
    assert scan_paths([evidence_dir, human_brief_path, *existing_change_dirs]).ok is True
