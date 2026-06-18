import json
from pathlib import Path
from typing import Any

from voice2task.cli import eval as eval_cli
from voice2task.evaluation import design_scaled_clarify_slot_boundary_candidates
from voice2task.io import read_json
from voice2task.leak_scan import scan_paths
from voice2task.reports import write_scaled_clarify_slot_boundary_candidate_design_report

REPO_ROOT = Path(__file__).resolve().parents[1]
TARGET_SELECTION_DIR = (
    REPO_ROOT / "reports" / "public-sample" / "scaled-residual-remediation-target-selection"
)
SCALED_CLUSTER_DIR = (
    REPO_ROOT / "reports" / "public-sample" / "scaled-current-123-adapter-residual-cluster-inspection"
)
DESIGN_DIR = (
    REPO_ROOT / "reports" / "public-sample" / "scaled-clarify-slot-boundary-candidate-design"
)
ARCHIVED_CHANGE_DIR = (
    REPO_ROOT
    / "openspec"
    / "changes"
    / "archive"
    / "2026-06-18-design-scaled-clarify-slot-boundary-candidates"
)
HUMAN_BRIEF = (
    REPO_ROOT
    / "docs"
    / "human-briefs"
    / "2026-06-18-design-scaled-clarify-slot-boundary-candidates.html"
)


def _target_selection() -> dict[str, Any]:
    return read_json(TARGET_SELECTION_DIR / "scaled_residual_remediation_target_selection.json")


def _source_clusters() -> dict[str, Any]:
    return read_json(SCALED_CLUSTER_DIR / "formal_heldout_residual_cluster_inspection.json")


def test_scaled_clarify_candidate_design_derives_three_bounded_themes() -> None:
    design = design_scaled_clarify_slot_boundary_candidates(
        target_selection=_target_selection(),
        residual_cluster_inspection=_source_clusters(),
        target_selection_artifact=(
            "reports/public-sample/scaled-residual-remediation-target-selection/"
            "scaled_residual_remediation_target_selection.json"
        ),
        cluster_inspection_artifact=(
            "reports/public-sample/scaled-current-123-adapter-residual-cluster-inspection/"
            "formal_heldout_residual_cluster_inspection.json"
        ),
    )

    assert design["evidence_kind"] == "scaled_clarify_slot_boundary_candidate_design"
    assert design["design_status"] == "candidate_design_only_no_data_no_training_no_metric_change"
    assert design["source_manifest_id"] == "public-sample-20260617T152259Z"
    assert design["summary"]["selected_target"] == "clarify"
    assert design["summary"]["selected_task_family"] == (
        "clarify|clarify|ambiguous_request|confirm:true|slots:ambiguity"
    )
    assert design["summary"]["selected_field_path"] == "slots"
    assert design["summary"]["selected_residual_row_count"] == 78
    assert design["summary"]["selected_residual_field_count"] == 78
    assert design["summary"]["source_family_count"] == 28
    assert design["summary"]["source_family_incidence_total"] == 78
    assert design["summary"]["represented_source_family_incidence_total"] == 78
    assert design["summary"]["candidate_theme_ids"] == [
        "clarify_search_or_extract_ambiguity",
        "clarify_navigation_or_form_fill_ambiguity",
        "clarify_pronoun_or_context_missing",
    ]
    assert design["summary"]["recommended_next_change"] == (
        "materialize-scaled-clarify-slot-boundary-candidates"
    )

    consistency = design["source_count_consistency"]
    assert consistency["selected_cluster_matches_source_cluster"] is True
    assert consistency["themes_cover_all_source_families"] is True
    assert consistency["themes_cover_all_source_family_incidence"] is True

    represented_family_ids = {
        family_id
        for theme in design["candidate_themes"]
        for family_id in theme["source_family_ids"]
    }
    assert len(design["candidate_themes"]) == 3
    assert len(represented_family_ids) == 28
    assert sum(theme["source_family_incidence_total"] for theme in design["candidate_themes"]) == 78
    for theme in design["candidate_themes"]:
        target = theme["accepted_target_sketch"]
        assert target["task_type"] == "clarify"
        assert target["route"] == "clarify"
        assert target["safety"] == {"allow": True, "reason": "ambiguous_request"}
        assert target["confirmation_required"] is True
        assert target["slots"]["ambiguity"]
        drift_pairs = {
            (drift["task_type"], drift["route"]) for drift in theme["rejected_drift_sketches"]
        }
        assert drift_pairs == {
            ("search", "search_web"),
            ("navigate", "open_url"),
            ("form_fill", "fill_form"),
            ("blocked", "deny"),
        }

    assert design["metric_authority"]["contract_exact_match_primary_metric"] is True
    assert design["metric_authority"]["strict_slot_f1_primary_metric"] is True
    assert design["metric_authority"]["slot_f1_soft_diagnostic_only"] is True
    assert design["metric_authority"]["semantic_equivalence_primary_metric"] is False
    assert design["execution_scope"]["public_seed_rows_modified"] is False
    assert design["execution_scope"]["sft_rows_generated"] is False
    assert design["execution_scope"]["dpo_pairs_generated"] is False
    assert design["execution_scope"]["manifest_rebuild"] is False
    assert design["execution_scope"]["a100_job"] is False
    assert design["execution_scope"]["training_run"] is False
    assert design["execution_scope"]["prediction_run"] is False
    assert design["execution_scope"]["prompt_change"] is False
    assert design["execution_scope"]["evaluator_metric_change"] is False
    assert design["claims"]["candidate_design_only"] is True
    assert design["claims"]["model_recovery_claim"] is False
    assert design["claims"]["held_out_recovery_claim"] is False
    assert design["claims"]["soft_slot_f1_primary_metric"] is False


def test_scaled_clarify_candidate_design_cli_writes_public_safe_report(
    tmp_path: Path, capsys: Any
) -> None:
    output_dir = tmp_path / "scaled-clarify-slot-boundary-candidate-design"

    assert (
        eval_cli.main(
            [
                "design-scaled-clarify-slot-boundary-candidates",
                "--target-selection",
                (TARGET_SELECTION_DIR / "scaled_residual_remediation_target_selection.json").as_posix(),
                "--residual-clusters",
                (SCALED_CLUSTER_DIR / "formal_heldout_residual_cluster_inspection.json").as_posix(),
                "--output",
                output_dir.as_posix(),
            ]
        )
        == 0
    )

    cli_output = json.loads(capsys.readouterr().out)
    json_path = output_dir / "scaled_clarify_slot_boundary_candidate_design.json"
    markdown_path = output_dir / "scaled_clarify_slot_boundary_candidate_design.md"
    assert cli_output["ok"] is True
    assert cli_output["paths"]["json"] == json_path.as_posix()
    assert cli_output["paths"]["markdown"] == markdown_path.as_posix()

    design = read_json(json_path)
    markdown = markdown_path.read_text(encoding="utf-8")
    manifest = read_json(output_dir / "manifest.json")
    assert design["summary"]["candidate_theme_count"] == 3
    assert design["summary"]["source_family_count"] == 28
    assert design["source_count_consistency"]["themes_cover_all_source_family_incidence"] is True
    assert "design evidence only" in markdown
    assert "Blocked-payment residuals remain deferred" in markdown
    assert "does not claim any model-quality improvement" in markdown
    assert manifest["artifact_policy"]["candidate_design_only"] is True
    assert manifest["artifact_policy"]["sft_rows_generated"] is False
    assert manifest["artifact_policy"]["dpo_pairs_generated"] is False
    assert manifest["artifact_policy"]["training_run"] is False
    assert manifest["artifact_policy"]["prediction_run"] is False
    assert manifest["artifact_policy"]["a100_job"] is False
    assert manifest["diagnostic_artifacts"] == {
        "design": (
            "scaled-clarify-slot-boundary-candidate-design/"
            "scaled_clarify_slot_boundary_candidate_design.json"
        ),
        "markdown": (
            "scaled-clarify-slot-boundary-candidate-design/"
            "scaled_clarify_slot_boundary_candidate_design.md"
        ),
        "manifest": "scaled-clarify-slot-boundary-candidate-design/manifest.json",
    }
    assert scan_paths([output_dir]).ok is True

    direct_paths = write_scaled_clarify_slot_boundary_candidate_design_report(
        design,
        tmp_path / "direct-scaled-clarify-design",
    )
    direct_manifest = read_json(direct_paths["manifest"])
    assert direct_manifest["diagnostic_artifacts"] == {
        "design": "direct-scaled-clarify-design/scaled_clarify_slot_boundary_candidate_design.json",
        "markdown": "direct-scaled-clarify-design/scaled_clarify_slot_boundary_candidate_design.md",
        "manifest": "direct-scaled-clarify-design/manifest.json",
    }


def test_committed_scaled_clarify_candidate_design_is_bounded_and_public_safe() -> None:
    manifest = read_json(DESIGN_DIR / "manifest.json")
    design = read_json(DESIGN_DIR / "scaled_clarify_slot_boundary_candidate_design.json")
    report = (DESIGN_DIR / "scaled_clarify_slot_boundary_candidate_design.md").read_text(
        encoding="utf-8"
    )
    leak_scan = read_json(DESIGN_DIR / "final_leak_scan_result.json")

    assert manifest["evidence_kind"] == "scaled_clarify_slot_boundary_candidate_design"
    assert manifest["design_status"] == "candidate_design_only_no_data_no_training_no_metric_change"
    assert manifest["source_manifest_id"] == "public-sample-20260617T152259Z"
    assert manifest["summary"]["candidate_theme_count"] == 3
    assert manifest["summary"]["source_family_count"] == 28
    assert manifest["summary"]["source_family_incidence_total"] == 78
    assert manifest["summary"]["represented_source_family_incidence_total"] == 78
    assert manifest["summary"]["recommended_next_change"] == (
        "materialize-scaled-clarify-slot-boundary-candidates"
    )
    assert manifest["source_count_consistency"]["selected_cluster_matches_source_cluster"] is True
    assert manifest["source_count_consistency"]["themes_cover_all_source_families"] is True
    assert manifest["source_count_consistency"]["themes_cover_all_source_family_incidence"] is True
    assert manifest["artifact_policy"]["candidate_design_only"] is True
    assert manifest["artifact_policy"]["formal_public_sample_modified"] is False
    assert manifest["artifact_policy"]["sft_rows_generated"] is False
    assert manifest["artifact_policy"]["dpo_pairs_generated"] is False
    assert manifest["artifact_policy"]["manifest_rebuild"] is False
    assert manifest["artifact_policy"]["training_run"] is False
    assert manifest["artifact_policy"]["prediction_run"] is False
    assert manifest["artifact_policy"]["a100_job"] is False
    assert manifest["artifact_policy"]["prompt_change"] is False
    assert manifest["artifact_policy"]["evaluator_metric_change"] is False
    assert manifest["diagnostic_artifacts"] == {
        "design": (
            "reports/public-sample/scaled-clarify-slot-boundary-candidate-design/"
            "scaled_clarify_slot_boundary_candidate_design.json"
        ),
        "markdown": (
            "reports/public-sample/scaled-clarify-slot-boundary-candidate-design/"
            "scaled_clarify_slot_boundary_candidate_design.md"
        ),
        "manifest": (
            "reports/public-sample/scaled-clarify-slot-boundary-candidate-design/manifest.json"
        ),
    }
    assert design["claims"]["candidate_design_only"] is True
    assert design["claims"]["model_recovery_claim"] is False
    assert design["claims"]["held_out_recovery_claim"] is False
    assert design["claims"]["soft_slot_f1_primary_metric"] is False
    assert leak_scan["ok"] is True
    assert "design evidence only" in report

    scan_targets = [DESIGN_DIR, HUMAN_BRIEF]
    if ARCHIVED_CHANGE_DIR.exists():
        scan_targets.append(ARCHIVED_CHANGE_DIR)
    assert scan_paths(scan_targets).ok is True
