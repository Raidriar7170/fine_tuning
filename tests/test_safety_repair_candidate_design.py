import json
from pathlib import Path

import pytest

from voice2task.cli import eval as eval_cli
from voice2task.evaluation import design_safety_repair_candidates
from voice2task.io import read_json, read_jsonl
from voice2task.leak_scan import scan_paths

REPO_ROOT = Path(__file__).resolve().parents[1]
TARGET_SELECTION = REPO_ROOT / "reports" / "public-sample" / "remediation-target-selection" / "summary.json"
LAYERED_DEV = REPO_ROOT / "reports" / "public-sample" / "layered-eval" / "dev" / "metrics.json"
LAYERED_TEST = REPO_ROOT / "reports" / "public-sample" / "layered-eval" / "test" / "metrics.json"
RESIDUAL_SUMMARY = REPO_ROOT / "reports" / "public-sample" / "residual-diagnosis" / "summary.json"
TEST_GOLD = (
    REPO_ROOT
    / "reports"
    / "public-sample"
    / "a100-scaled-public-sample-current-123-adapter-prediction-baseline-after-a100-recovery"
    / "test"
    / "test_gold.jsonl"
)
TEST_PREDICTIONS = TEST_GOLD.with_name("predictions.jsonl")
EVIDENCE_DIR = REPO_ROOT / "reports" / "public-sample" / "safety-repair-candidate-design"


def _design_cli_args(output_dir: Path) -> list[str]:
    return [
        "design-safety-repair-candidates",
        "--target-selection",
        TARGET_SELECTION.as_posix(),
        "--layered-eval-dev",
        LAYERED_DEV.as_posix(),
        "--layered-eval-test",
        LAYERED_TEST.as_posix(),
        "--residual-diagnosis",
        RESIDUAL_SUMMARY.as_posix(),
        "--test-gold",
        TEST_GOLD.as_posix(),
        "--test-predictions",
        TEST_PREDICTIONS.as_posix(),
        "--output",
        output_dir.as_posix(),
    ]


def test_safety_repair_candidate_design_cli_writes_design_only_evidence(
    tmp_path: Path,
    capsys,  # type: ignore[no-untyped-def]
) -> None:
    output_dir = tmp_path / "safety-repair-candidate-design"

    assert eval_cli.main(_design_cli_args(output_dir)) == 0

    cli_output = json.loads(capsys.readouterr().out)
    assert cli_output["ok"] is True
    design = read_json(output_dir / "safety_repair_candidate_design.json")
    manifest = read_json(output_dir / "manifest.json")
    markdown = (output_dir / "safety_repair_candidate_design.md").read_text(encoding="utf-8")

    assert design["evidence_kind"] == "safety_repair_candidate_design"
    assert design["design_mode"] == "public_safe_design_only_no_materialization"
    assert design["dataset_manifest_id"] == "public-sample-20260617T152259Z"
    assert design["summary"]["unsafe_false_negative_count"] == 1
    assert design["summary"]["unsafe_false_negative_example_count"] == 1
    assert design["summary"]["unsafe_false_negative_example_count_matches_layered_count"] is True
    assert design["summary"]["unsafe_false_negative_row_ids"] == ["family-clarify-test-1-aug-1"]
    assert design["summary"]["candidate_count"] == 3
    assert design["summary"]["recommended_next_step"] == "review_safety_repair_candidates_before_materialization"
    assert design["aggregates"]["safety_related_residual_counts"] == {
        "confirmation": 6,
        "refusal_or_clarify": 9,
        "risk_level": 10,
        "unsafe_false_negative": 1,
    }

    candidates = {candidate["repair_family"]: candidate for candidate in design["candidates"]}
    assert set(candidates) == {
        "clarify_confirmation_preservation",
        "confirmation_required_boundary",
        "unsafe_action_denial_boundary",
    }
    clarify_candidate = candidates["clarify_confirmation_preservation"]
    assert clarify_candidate["accepted_target_contract_sketch"] == {
        "confirmation_required": True,
        "route": "clarify",
        "safety": {"allow": True, "reason": "ambiguous_request"},
        "task_type": "clarify",
    }
    assert clarify_candidate["source_row_ids"] == ["family-clarify-test-1-aug-1"]
    assert clarify_candidate["rejected_drift_sketches"] == [
        {
            "confirmation_required": False,
            "route": "search_web",
            "safety": {"allow": True, "reason": "information_request"},
            "task_type": "search",
        }
    ]
    for candidate in candidates.values():
        assert candidate["intended_later_action"] == "review_before_seed_materialization"
        assert candidate["suggested_public_utterance_template_descriptors"]
        assert candidate["evidence_rationale"]

    execution_scope = design["execution_scope"]
    claims = design["claims"]
    assert execution_scope["design_only"] is True
    assert execution_scope["candidate_seed_rows_materialized"] is False
    assert execution_scope["formal_public_sample_modified"] is False
    assert execution_scope["training_run"] is False
    assert execution_scope["prediction_run"] is False
    assert execution_scope["evaluator_relaxation"] is False
    assert claims["candidate_design_only"] is True
    assert claims["safety_improvement_claim"] is False
    assert claims["model_quality_claim"] is False
    assert manifest["artifact_policy"]["design_only"] is True
    assert manifest["artifact_policy"]["candidate_seed_rows_materialized"] is False
    assert manifest["summary"]["unsafe_false_negative_example_count_matches_layered_count"] is True
    assert manifest["diagnostic_artifacts"]["design"].endswith("safety_repair_candidate_design.json")
    assert "does not materialize seed rows" in markdown
    assert scan_paths([output_dir]).ok is True


def test_committed_safety_repair_candidate_design_is_public_safe_and_bounded() -> None:
    design = read_json(EVIDENCE_DIR / "safety_repair_candidate_design.json")
    manifest = read_json(EVIDENCE_DIR / "manifest.json")
    report = (EVIDENCE_DIR / "safety_repair_candidate_design.md").read_text(encoding="utf-8")

    assert design["source_artifacts"] == {
        "layered_eval_dev": "reports/public-sample/layered-eval/dev/metrics.json",
        "layered_eval_test": "reports/public-sample/layered-eval/test/metrics.json",
        "public_test_gold": (
            "reports/public-sample/"
            "a100-scaled-public-sample-current-123-adapter-prediction-baseline-after-a100-recovery/"
            "test/test_gold.jsonl"
        ),
        "public_test_predictions": (
            "reports/public-sample/"
            "a100-scaled-public-sample-current-123-adapter-prediction-baseline-after-a100-recovery/"
            "test/predictions.jsonl"
        ),
        "remediation_target_selection": "reports/public-sample/remediation-target-selection/summary.json",
        "residual_diagnosis": "reports/public-sample/residual-diagnosis/summary.json",
    }
    assert design["summary"]["unsafe_false_negative_example_count_matches_layered_count"] is True
    assert design["summary"]["candidate_count"] == 3
    assert design["summary"]["formal_public_sample_modified"] is False
    assert design["summary"]["candidate_seed_rows_materialized"] is False
    assert design["summary"]["dpo_pairs_generated"] is False
    assert design["claims"]["held_out_recovery_claim"] is False
    assert design["claims"]["production_readiness_claim"] is False
    assert design["claims"]["safety_readiness_claim"] is False
    assert manifest["artifact_policy"]["evaluator_metric_change"] is False
    assert manifest["artifact_policy"]["evaluator_relaxation"] is False
    assert "Candidate seed rows materialized: `False`" in report
    assert "Current unsafe false-negative row ids: `['family-clarify-test-1-aug-1']`" in report
    assert scan_paths([EVIDENCE_DIR]).ok is True


def test_safety_repair_candidate_design_fails_closed_when_layered_count_and_examples_diverge() -> None:
    layered_test = read_json(LAYERED_TEST)
    layered_test["summary"]["unsafe_false_negative_count"] = 2

    with pytest.raises(ValueError, match="unsafe false-negative example count"):
        design_safety_repair_candidates(
            target_selection=read_json(TARGET_SELECTION),
            layered_eval_by_split={
                "dev": read_json(LAYERED_DEV),
                "test": layered_test,
            },
            residual_diagnosis=read_json(RESIDUAL_SUMMARY),
            test_gold_rows=read_jsonl(TEST_GOLD),
            test_prediction_rows=read_jsonl(TEST_PREDICTIONS),
            source_artifacts={
                "layered_eval_dev": "reports/public-sample/layered-eval/dev/metrics.json",
                "layered_eval_test": "reports/public-sample/layered-eval/test/metrics.json",
                "public_test_gold": (
                    "reports/public-sample/"
                    "a100-scaled-public-sample-current-123-adapter-prediction-baseline-after-a100-recovery/"
                    "test/test_gold.jsonl"
                ),
                "public_test_predictions": (
                    "reports/public-sample/"
                    "a100-scaled-public-sample-current-123-adapter-prediction-baseline-after-a100-recovery/"
                    "test/predictions.jsonl"
                ),
                "remediation_target_selection": "reports/public-sample/remediation-target-selection/summary.json",
                "residual_diagnosis": "reports/public-sample/residual-diagnosis/summary.json",
            },
        )
