import json
from pathlib import Path

from voice2task.cli import eval as eval_cli
from voice2task.io import read_json
from voice2task.leak_scan import scan_paths

REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DESIGN = (
    REPO_ROOT
    / "reports"
    / "public-sample"
    / "safety-repair-candidate-design"
    / "safety_repair_candidate_design.json"
)
REVIEW_DIR = REPO_ROOT / "reports" / "public-sample" / "safety-repair-candidate-design-review"


def _review_cli_args(output_dir: Path) -> list[str]:
    return [
        "review-safety-repair-candidates-before-materialization",
        "--candidate-design",
        SOURCE_DESIGN.as_posix(),
        "--output",
        output_dir.as_posix(),
    ]


def test_safety_repair_candidate_design_review_cli_writes_review_only_evidence(
    tmp_path: Path,
    capsys,  # type: ignore[no-untyped-def]
) -> None:
    output_dir = tmp_path / "safety-repair-candidate-design-review"

    assert eval_cli.main(_review_cli_args(output_dir)) == 0

    cli_output = json.loads(capsys.readouterr().out)
    assert cli_output["ok"] is True
    review = read_json(output_dir / "safety_repair_candidate_design_review.json")
    manifest = read_json(output_dir / "manifest.json")
    markdown = (output_dir / "safety_repair_candidate_design_review.md").read_text(encoding="utf-8")

    assert review["evidence_kind"] == "safety_repair_candidate_design_review"
    assert review["review_mode"] == "public_safe_review_only_no_materialization"
    assert review["dataset_manifest_id"] == "public-sample-20260617T152259Z"
    assert review["source_candidate_design"]["artifact"].endswith("safety_repair_candidate_design.json")
    assert review["summary"] == {
        "candidate_count": 3,
        "ready_for_later_bounded_materialization_proposal": 1,
        "ready_for_later_policy_scoped_materialization_proposal": 1,
        "deferred_to_safety_policy_design": 1,
        "recommended_next_step": "propose_clarify_confirmation_safety_repair_materialization_after_review",
        "candidate_seed_rows_materialized": False,
        "formal_public_sample_modified": False,
        "dpo_pairs_generated": False,
    }

    decisions = {decision["repair_family"]: decision for decision in review["candidate_reviews"]}
    assert decisions["clarify_confirmation_preservation"]["review_status"] == (
        "ready_for_later_bounded_materialization_proposal"
    )
    assert decisions["confirmation_required_boundary"]["review_status"] == (
        "ready_for_later_policy_scoped_materialization_proposal"
    )
    assert decisions["unsafe_action_denial_boundary"]["review_status"] == "deferred_to_safety_policy_design"
    for decision in decisions.values():
        assert decision["approved_for_materialization"] is False
        assert decision["allowed_later_operation"] in {
            "bounded_open_spec_materialization_proposal_only",
            "bounded_open_spec_policy_or_materialization_proposal_only",
            "separate_safety_policy_design_before_materialization",
        }
        assert "materialize_now" in decision["blocked_operations"]
        assert "train_now" in decision["blocked_operations"]

    assert review["execution_scope"]["review_only"] is True
    assert review["execution_scope"]["candidate_seed_rows_materialized"] is False
    assert review["execution_scope"]["formal_public_sample_modified"] is False
    assert review["execution_scope"]["training_run"] is False
    assert review["execution_scope"]["prediction_run"] is False
    assert review["execution_scope"]["evaluator_relaxation"] is False
    assert review["claims"]["review_evidence_only"] is True
    assert review["claims"]["safety_improvement_claim"] is False
    assert review["claims"]["materialization_approval_claim"] is False
    assert manifest["artifact_policy"]["review_only"] is True
    assert manifest["artifact_policy"]["candidate_seed_rows_materialized"] is False
    assert "does not materialize seed rows" in markdown
    assert "not approval to mutate data" in markdown
    assert scan_paths([output_dir]).ok is True


def test_committed_safety_repair_candidate_design_review_is_public_safe_and_bounded() -> None:
    review = read_json(REVIEW_DIR / "safety_repair_candidate_design_review.json")
    manifest = read_json(REVIEW_DIR / "manifest.json")
    report = (REVIEW_DIR / "safety_repair_candidate_design_review.md").read_text(encoding="utf-8")

    assert review["source_candidate_design"] == {
        "artifact": "reports/public-sample/safety-repair-candidate-design/safety_repair_candidate_design.json",
        "candidate_count": 3,
        "dataset_manifest_id": "public-sample-20260617T152259Z",
        "evidence_kind": "safety_repair_candidate_design",
        "unsafe_false_negative_count": 1,
        "unsafe_false_negative_example_count_matches_layered_count": True,
    }
    assert review["summary"]["ready_for_later_bounded_materialization_proposal"] == 1
    assert review["summary"]["deferred_to_safety_policy_design"] == 1
    assert review["summary"]["candidate_seed_rows_materialized"] is False
    assert review["claims"]["held_out_recovery_claim"] is False
    assert review["claims"]["production_readiness_claim"] is False
    assert review["claims"]["safety_readiness_claim"] is False
    assert manifest["artifact_policy"]["evaluator_metric_change"] is False
    assert manifest["artifact_policy"]["evaluator_relaxation"] is False
    assert "approved_for_materialization" in report
    assert scan_paths([REVIEW_DIR]).ok is True
