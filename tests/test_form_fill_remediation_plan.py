import json
from pathlib import Path
from typing import Any

import pytest

from voice2task.cli import eval as eval_cli
from voice2task.evaluation import diagnose_form_fill_remediation_plan
from voice2task.io import read_json
from voice2task.leak_scan import scan_paths
from voice2task.reports import write_form_fill_remediation_plan_report

REPO_ROOT = Path(__file__).resolve().parents[1]
RESIDUAL_DIR = REPO_ROOT / "reports" / "public-sample" / "formal-heldout-residual-family-diagnosis"
SELECTION_DIR = REPO_ROOT / "reports" / "public-sample" / "formal-heldout-remediation-target-selection"
PLAN_DIR = REPO_ROOT / "reports" / "public-sample" / "form-fill-remediation-plan"


def _diagnosis() -> dict[str, Any]:
    return diagnose_form_fill_remediation_plan(
        residual_diagnosis=read_json(RESIDUAL_DIR / "formal_heldout_residual_family_diagnosis.json"),
        target_selection=read_json(SELECTION_DIR / "formal_heldout_remediation_target_selection.json"),
    )


def test_form_fill_remediation_plan_classifies_current_selected_residuals() -> None:
    diagnosis = _diagnosis()

    assert diagnosis["evidence_kind"] == "formal_heldout_form_fill_remediation_plan"
    assert diagnosis["remediation_status"] == "plan_only_no_data_no_training_no_metric_change"
    assert diagnosis["summary"]["target"] == "form_fill"
    assert diagnosis["summary"]["residual_row_count"] == 29
    assert diagnosis["summary"]["residual_field_count"] == 49
    assert diagnosis["summary"]["bucket_field_counts"] == {
        "clarify_boundary_confusion": 8,
        "confirmation_marker_missing_or_reordered": 23,
        "field_name_specificity_drift": 18,
    }
    assert diagnosis["summary"]["bucket_row_counts"] == {
        "clarify_boundary_confusion": 2,
        "confirmation_marker_missing_or_reordered": 23,
        "field_name_specificity_drift": 16,
    }
    assert diagnosis["summary"]["count_consistency"] == {
        "expected_residual_rows": 29,
        "computed_residual_rows": 29,
        "expected_residual_fields": 49,
        "computed_residual_fields": 49,
        "ok": True,
    }
    assert diagnosis["summary"]["recommended_strategy"] == (
        "prompt_policy_clarification_plus_targeted_public_safe_case_design"
    )
    assert diagnosis["summary"]["training_recommended_now"] is False
    assert diagnosis["summary"]["dpo_recommended_now"] is False
    assert diagnosis["execution_scope"]["new_data_generated"] is False
    assert diagnosis["execution_scope"]["a100_job"] is False
    assert diagnosis["claims"]["held_out_recovery_claim"] is False


def test_form_fill_remediation_plan_rejects_non_form_fill_selection() -> None:
    residual_diagnosis = read_json(RESIDUAL_DIR / "formal_heldout_residual_family_diagnosis.json")
    target_selection = read_json(SELECTION_DIR / "formal_heldout_remediation_target_selection.json")
    target_selection["summary"]["selected_target"] = "clarify"

    with pytest.raises(ValueError, match="must select form_fill"):
        diagnose_form_fill_remediation_plan(
            residual_diagnosis=residual_diagnosis,
            target_selection=target_selection,
        )


def test_form_fill_remediation_plan_cli_writes_public_safe_report(tmp_path: Path, capsys: Any) -> None:
    output_dir = tmp_path / "form-fill-remediation-plan"

    assert (
        eval_cli.main(
            [
                "diagnose-form-fill-remediation-plan",
                "--residual-diagnosis",
                (RESIDUAL_DIR / "formal_heldout_residual_family_diagnosis.json").as_posix(),
                "--target-selection",
                (SELECTION_DIR / "formal_heldout_remediation_target_selection.json").as_posix(),
                "--output",
                output_dir.as_posix(),
            ]
        )
        == 0
    )

    cli_output = json.loads(capsys.readouterr().out)
    json_path = output_dir / "form_fill_remediation_plan.json"
    markdown_path = output_dir / "form_fill_remediation_plan.md"
    assert cli_output["ok"] is True
    assert cli_output["paths"]["json"] == json_path.as_posix()
    assert cli_output["paths"]["markdown"] == markdown_path.as_posix()

    diagnosis = read_json(json_path)
    markdown = markdown_path.read_text(encoding="utf-8")
    assert diagnosis["summary"]["target"] == "form_fill"
    assert "plan-only diagnosis" in markdown
    assert "does not authorize materialization, training, DPO, or evaluator changes" in markdown
    assert scan_paths([output_dir]).ok is True

    direct_paths = write_form_fill_remediation_plan_report(diagnosis, tmp_path / "direct")
    assert direct_paths["json"].exists()
    assert direct_paths["markdown"].exists()
    assert direct_paths["manifest"].exists()


def test_committed_form_fill_remediation_plan_is_bounded_and_public_safe() -> None:
    manifest = read_json(PLAN_DIR / "manifest.json")
    diagnosis = read_json(PLAN_DIR / "form_fill_remediation_plan.json")

    assert manifest["evidence_kind"] == "formal_heldout_form_fill_remediation_plan"
    assert manifest["summary"]["target"] == "form_fill"
    assert manifest["summary"]["count_consistency"]["ok"] is True
    assert manifest["summary"]["training_recommended_now"] is False
    assert manifest["summary"]["dpo_recommended_now"] is False
    assert manifest["artifact_policy"]["data_generation"] is False
    assert manifest["artifact_policy"]["training_run"] is False
    assert manifest["artifact_policy"]["a100_job"] is False
    assert diagnosis["acceptance_boundary"]["future_case_design_must_not_mutate_current_heldout_splits"] is True
    assert diagnosis["claims"]["semantic_equivalence_primary_metric"] is False
    assert scan_paths([PLAN_DIR]).ok is True
