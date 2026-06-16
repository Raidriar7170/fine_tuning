import json
from pathlib import Path

from voice2task.cli import eval as eval_cli
from voice2task.io import read_json
from voice2task.leak_scan import scan_paths

REPO_ROOT = Path(__file__).resolve().parents[1]
SAFETY_DIAGNOSIS = (
    REPO_ROOT
    / "reports"
    / "public-sample"
    / "sft-v3-safety-regression-diagnosis"
    / "sft_v3_safety_regression_diagnosis.json"
)
PUBLIC_MANIFEST = REPO_ROOT / "data" / "public-samples" / "manifest_public_sample.json"
EVIDENCE_DIR = REPO_ROOT / "reports" / "public-sample" / "blocked-payment-safety-repair-candidate-design"


def _design_cli_args(output_dir: Path) -> list[str]:
    return [
        "design-blocked-payment-safety-repair-candidates",
        "--safety-diagnosis",
        SAFETY_DIAGNOSIS.as_posix(),
        "--public-manifest",
        PUBLIC_MANIFEST.as_posix(),
        "--output",
        output_dir.as_posix(),
    ]


def test_blocked_payment_safety_repair_candidate_design_cli_writes_design_only_evidence(
    tmp_path: Path,
    capsys,  # type: ignore[no-untyped-def]
) -> None:
    output_dir = tmp_path / "blocked-payment-safety-repair-candidate-design"

    assert eval_cli.main(_design_cli_args(output_dir)) == 0

    cli_output = json.loads(capsys.readouterr().out)
    assert cli_output["ok"] is True
    design = read_json(output_dir / "blocked_payment_safety_repair_candidate_design.json")
    manifest = read_json(output_dir / "manifest.json")
    markdown = (output_dir / "blocked_payment_safety_repair_candidate_design.md").read_text(encoding="utf-8")

    assert design["evidence_kind"] == "blocked_payment_safety_repair_candidate_design"
    assert design["dataset_manifest_id"] == "public-sample-20260616T074315Z"
    assert design["summary"]["candidate_count"] == 2
    assert design["summary"]["source_row_count"] == 4
    assert design["summary"]["formal_public_sample_modified"] is False
    assert design["summary"]["candidate_seed_rows_materialized"] is False
    assert design["summary"]["dpo_pairs_generated"] is False
    assert design["aggregates"]["source_classification_counts"] == {"persistent_miss": 3, "regressed": 1}
    assert design["aggregates"]["accepted_target_task_type_counts"] == {"blocked": 2}
    assert design["aggregates"]["accepted_target_route_counts"] == {"deny": 2}
    assert manifest["artifact_policy"]["design_only"] is True
    assert manifest["artifact_policy"]["training_run"] is False
    assert manifest["artifact_policy"]["prediction_run"] is False
    assert "does not materialize seed rows" in markdown
    assert scan_paths([output_dir]).ok is True


def test_current_blocked_payment_safety_repair_candidate_design_preserves_candidate_boundaries() -> None:
    design = read_json(EVIDENCE_DIR / "blocked_payment_safety_repair_candidate_design.json")
    manifest = read_json(EVIDENCE_DIR / "manifest.json")
    report = (EVIDENCE_DIR / "blocked_payment_safety_repair_candidate_design.md").read_text(encoding="utf-8")

    assert design["design_mode"] == "public_safe_design_only_no_materialization"
    assert design["summary"]["recommended_next_step"] == (
        "materialize_blocked_payment_safety_repair_candidates_after_review"
    )
    assert design["summary"]["source_row_ids"] == [
        "family-blocked_payment-dev-1",
        "family-blocked_payment-dev-1-aug-1",
        "family-blocked_payment-dev-1-aug-2",
        "family-blocked_payment-dev-2-aug-2",
    ]

    candidates = {candidate["repair_family"]: candidate for candidate in design["candidates"]}
    assert set(candidates) == {"refund_confirmation_or_processing", "subscription_charge_confirmation"}
    assert candidates["refund_confirmation_or_processing"]["source_row_count"] == 3
    assert candidates["refund_confirmation_or_processing"]["source_classification_counts"] == {
        "persistent_miss": 2,
        "regressed": 1,
    }
    assert candidates["subscription_charge_confirmation"]["source_row_count"] == 1
    assert candidates["subscription_charge_confirmation"]["source_classification_counts"] == {
        "persistent_miss": 1
    }
    for candidate in candidates.values():
        assert candidate["accepted_target_contract_sketch"]["task_type"] == "blocked"
        assert candidate["accepted_target_contract_sketch"]["route"] == "deny"
        assert candidate["accepted_target_contract_sketch"]["safety"] == {
            "allow": False,
            "reason": "unsafe_payment",
        }
        drift_routes = {drift["route"] for drift in candidate["rejected_drift_sketches"]}
        assert drift_routes <= {"clarify", "fill_form"}

    execution_scope = design["execution_scope"]
    claims = design["claims"]
    assert execution_scope["design_only"] is True
    assert execution_scope["formal_public_sample_modified"] is False
    assert execution_scope["candidate_seed_rows_materialized"] is False
    assert execution_scope["dpo_pairs_generated"] is False
    assert execution_scope["training_run"] is False
    assert execution_scope["prediction_run"] is False
    assert claims["candidate_design_only"] is True
    assert claims["model_quality_claim"] is False
    assert claims["safety_improvement_claim"] is False
    assert manifest["artifact_policy"]["checkpoint_release"] is False
    assert "Candidate seed rows materialized: `False`" in report
    assert scan_paths([EVIDENCE_DIR]).ok is True
