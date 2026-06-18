import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

import pytest

from voice2task import dataset as dataset_module
from voice2task.cli import data as data_cli
from voice2task.io import read_json, read_jsonl
from voice2task.leak_scan import scan_paths
from voice2task.reports import write_scaled_clarify_slot_boundary_candidate_materialization_report

REPO_ROOT = Path(__file__).resolve().parents[1]
DESIGN_PATH = (
    REPO_ROOT
    / "reports"
    / "public-sample"
    / "scaled-clarify-slot-boundary-candidate-design"
    / "scaled_clarify_slot_boundary_candidate_design.json"
)
PUBLIC_SAMPLE_PATHS = [
    REPO_ROOT / "data" / "public-samples" / "seed_traces.jsonl",
    REPO_ROOT / "data" / "public-samples" / "sft_public_sample.jsonl",
    REPO_ROOT / "data" / "public-samples" / "dpo_public_sample.jsonl",
    REPO_ROOT / "data" / "public-samples" / "manifest_public_sample.json",
]
MATERIALIZATION_DIR = (
    REPO_ROOT
    / "reports"
    / "public-sample"
    / "scaled-clarify-slot-boundary-candidate-materialization"
)
CANDIDATE_SEED_PATH = REPO_ROOT / "data" / "public-samples" / "scaled_clarify_slot_boundary_seed_candidates.jsonl"
THEME_IDS = {
    "clarify_search_or_extract_ambiguity",
    "clarify_navigation_or_form_fill_ambiguity",
    "clarify_pronoun_or_context_missing",
}


def _materializer() -> Any:
    assert hasattr(dataset_module, "materialize_scaled_clarify_slot_boundary_candidates")
    return dataset_module.materialize_scaled_clarify_slot_boundary_candidates


def _sha256_by_path(paths: list[Path]) -> dict[Path, str]:
    return {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}


def _assert_clarify_candidate_payload(
    seed_rows: list[dict[str, Any]],
    sft_rows: list[dict[str, Any]],
) -> None:
    assert len(seed_rows) == 9
    assert len(sft_rows) == 27
    assert Counter(row["split"] for row in seed_rows) == {"dev": 3, "test": 3, "train": 3}
    assert Counter(row["split"] for row in sft_rows) == {"dev": 9, "test": 9, "train": 9}

    seed_ids = [row["id"] for row in seed_rows]
    sft_ids = [row["id"] for row in sft_rows]
    assert len(seed_ids) == len(set(seed_ids))
    assert len(sft_ids) == len(set(sft_ids))
    assert set(Counter(row["provenance"]["source_id"] for row in sft_rows).values()) == {3}

    assert Counter(row["provenance"]["candidate_theme_id"] for row in seed_rows) == {
        theme_id: 3 for theme_id in THEME_IDS
    }
    assert all(row["provenance"]["source_mode"] == "scaled_clarify_slot_boundary_candidate_seed" for row in seed_rows)
    assert all(row["provenance"]["candidate_status"] == "standalone_not_formal_public_sample" for row in seed_rows)
    assert all(row["provenance"]["source_manifest_id"] == "public-sample-20260617T152259Z" for row in seed_rows)
    assert all(row["provenance"]["public_safe"] is True for row in seed_rows)

    for row in seed_rows:
        contract = row["target_contract"]
        assert contract["contract_version"] == "v1"
        assert contract["language"] == "zh-CN"
        assert contract["task_type"] == "clarify"
        assert contract["route"] == "clarify"
        assert contract["confirmation_required"] is True
        assert contract["safety"] == {"allow": True, "reason": "ambiguous_request"}
        assert isinstance(contract["slots"]["ambiguity"], str)
        assert contract["slots"]["ambiguity"].strip()
        assert row["input_text"] not in row["augmentations"]
        assert len(row["augmentations"]) == 2


def _read_design() -> dict[str, Any]:
    return read_json(DESIGN_PATH)


def test_materialize_scaled_clarify_candidates_writes_standalone_artifacts(tmp_path: Path) -> None:
    public_sample_before = _sha256_by_path(PUBLIC_SAMPLE_PATHS)
    seed_output = tmp_path / "scaled_clarify_slot_boundary_seed_candidates.jsonl"
    output_dir = tmp_path / "scaled-clarify-slot-boundary-candidate-materialization"

    paths = _materializer()(
        candidate_design_path=DESIGN_PATH,
        seed_output_path=seed_output,
        output_dir=output_dir,
    )

    assert paths["seed"] == seed_output
    assert paths["sft"] == output_dir / "sft_candidate_rows.jsonl"
    assert paths["json"] == output_dir / "scaled_clarify_slot_boundary_candidate_materialization.json"
    assert paths["markdown"] == output_dir / "scaled_clarify_slot_boundary_candidate_materialization.md"
    assert paths["manifest"] == output_dir / "manifest.json"
    assert _sha256_by_path(PUBLIC_SAMPLE_PATHS) == public_sample_before

    seed_rows = read_jsonl(seed_output)
    sft_rows = read_jsonl(paths["sft"])
    evidence = read_json(paths["json"])
    manifest = read_json(paths["manifest"])
    markdown = paths["markdown"].read_text(encoding="utf-8")

    _assert_clarify_candidate_payload(seed_rows, sft_rows)
    assert evidence["evidence_kind"] == "scaled_clarify_slot_boundary_candidate_materialization"
    assert evidence["materialization_status"] == "standalone_candidate_dataset_materialized"
    assert evidence["source_design"]["evidence_kind"] == "scaled_clarify_slot_boundary_candidate_design"
    assert evidence["source_design"]["source_manifest_id"] == "public-sample-20260617T152259Z"
    assert evidence["summary"]["source_family_count"] == 28
    assert evidence["summary"]["source_family_incidence_total"] == 78
    assert evidence["summary"]["candidate_theme_count"] == 3
    assert evidence["summary"]["candidate_seed_rows"] == 9
    assert evidence["summary"]["candidate_sft_rows"] == 27
    assert evidence["summary"]["seed_split_counts"] == {"dev": 3, "test": 3, "train": 3}
    assert evidence["summary"]["sft_split_counts"] == {"dev": 9, "test": 9, "train": 9}
    assert evidence["summary"]["candidate_theme_seed_counts"] == {theme_id: 3 for theme_id in sorted(THEME_IDS)}
    assert evidence["summary"]["formal_public_sample_modified"] is False
    assert evidence["summary"]["recommended_next_change"] == "merge-scaled-clarify-slot-boundary-candidates"
    assert evidence["execution_scope"]["standalone_candidate_data_only"] is True
    assert evidence["execution_scope"]["formal_public_sample_modified"] is False
    assert evidence["execution_scope"]["formal_dpo_rebuilt"] is False
    assert evidence["execution_scope"]["training_run"] is False
    assert evidence["execution_scope"]["prediction_run"] is False
    assert evidence["execution_scope"]["a100_execution"] is False
    assert evidence["claims"]["held_out_generalization_recovered"] is False
    assert evidence["claims"]["model_recovery_claim"] is False
    assert manifest["artifact_policy"]["candidate_data_only"] is True
    assert manifest["artifact_policy"]["standalone_only"] is True
    assert manifest["artifact_policy"]["formal_public_sample_files_modified"] is False
    assert manifest["artifact_policy"]["dpo_pairs_generated"] is False
    assert "standalone scaled clarify slot-boundary candidate" in markdown
    assert "does not merge the formal public sample" in markdown
    assert "No model-quality improvement can be inferred" in markdown
    assert scan_paths([seed_output, output_dir]).ok is True


def test_materialize_scaled_clarify_candidates_cli(tmp_path: Path, capsys: Any) -> None:
    seed_output = tmp_path / "scaled_clarify_slot_boundary_seed_candidates.jsonl"
    output_dir = tmp_path / "scaled-clarify-slot-boundary-candidate-materialization"

    assert (
        data_cli.main(
            [
                "materialize-scaled-clarify-slot-boundary-candidates",
                "--candidate-design",
                DESIGN_PATH.as_posix(),
                "--seed-output",
                seed_output.as_posix(),
                "--output",
                output_dir.as_posix(),
            ]
        )
        == 0
    )

    payload = json.loads(capsys.readouterr().out)
    assert payload["ok"] is True
    assert payload["summary"]["candidate_seed_rows"] == 9
    assert payload["summary"]["candidate_sft_rows"] == 27
    assert payload["summary"]["candidate_theme_count"] == 3
    assert payload["summary"]["source_family_incidence_total"] == 78
    assert payload["execution_scope"]["standalone_candidate_data_only"] is True
    assert payload["execution_scope"]["formal_public_sample_modified"] is False
    assert payload["paths"]["seed"] == seed_output.as_posix()
    assert payload["paths"]["manifest"] == (output_dir / "manifest.json").as_posix()


@pytest.mark.parametrize(
    "protected_path",
    [
        dataset_module.FORMAL_PUBLIC_SEED_PATH,
        dataset_module.FORMAL_PUBLIC_SFT_PATH,
        dataset_module.FORMAL_PUBLIC_DPO_PATH,
        dataset_module.FORMAL_PUBLIC_MANIFEST_PATH,
    ],
)
def test_materialize_scaled_clarify_candidates_rejects_formal_public_sample_outputs(
    tmp_path: Path,
    protected_path: Path,
) -> None:
    with pytest.raises(ValueError, match="formal public sample files"):
        _materializer()(
            candidate_design_path=DESIGN_PATH,
            seed_output_path=protected_path,
            output_dir=tmp_path / "scaled-clarify-slot-boundary-candidate-materialization",
        )

    with pytest.raises(ValueError, match="formal public sample files"):
        _materializer()(
            candidate_design_path=DESIGN_PATH,
            seed_output_path=tmp_path / "scaled_clarify_slot_boundary_seed_candidates.jsonl",
            output_dir=protected_path,
        )


def test_materialize_scaled_clarify_candidates_rejects_non_clarify_design_sketch(tmp_path: Path) -> None:
    bad_design = _read_design()
    bad_design["candidate_themes"][0]["accepted_target_sketch"] = {
        "task_type": "search",
        "route": "search_web",
        "safety": {"allow": True, "reason": "safe"},
        "confirmation_required": False,
        "slots": {"query": "随便搜一下"},
    }
    bad_design_path = tmp_path / "bad_scaled_clarify_design.json"
    bad_design_path.write_text(json.dumps(bad_design, ensure_ascii=False), encoding="utf-8")

    with pytest.raises(ValueError, match="accepted target sketch"):
        _materializer()(
            candidate_design_path=bad_design_path,
            seed_output_path=tmp_path / "scaled_clarify_slot_boundary_seed_candidates.jsonl",
            output_dir=tmp_path / "scaled-clarify-slot-boundary-candidate-materialization",
        )


def test_scaled_clarify_materialization_report_rejects_unsupported_claims_before_writes(tmp_path: Path) -> None:
    seed_output = tmp_path / "scaled_clarify_slot_boundary_seed_candidates.jsonl"
    output_dir = tmp_path / "scaled-clarify-slot-boundary-candidate-materialization"
    paths = _materializer()(
        candidate_design_path=DESIGN_PATH,
        seed_output_path=seed_output,
        output_dir=output_dir,
    )
    materialization = read_json(paths["json"])
    sft_rows = read_jsonl(paths["sft"])
    materialization["execution_scope"]["training_run"] = True
    materialization["claims"]["model_recovery_claim"] = True
    rejected_output_dir = tmp_path / "rejected-report"

    with pytest.raises(ValueError, match="unsupported scope or recovery signals"):
        write_scaled_clarify_slot_boundary_candidate_materialization_report(
            materialization=materialization,
            output_dir=rejected_output_dir,
            sft_rows=sft_rows,
        )

    assert not (rejected_output_dir / "scaled_clarify_slot_boundary_candidate_materialization.json").exists()
    assert not (rejected_output_dir / "sft_candidate_rows.jsonl").exists()


def test_committed_scaled_clarify_materialization_is_standalone_and_public_safe() -> None:
    manifest = read_json(MATERIALIZATION_DIR / "manifest.json")
    evidence = read_json(MATERIALIZATION_DIR / "scaled_clarify_slot_boundary_candidate_materialization.json")
    seed_rows = read_jsonl(CANDIDATE_SEED_PATH)
    sft_rows = read_jsonl(MATERIALIZATION_DIR / "sft_candidate_rows.jsonl")
    leak_scan = read_json(MATERIALIZATION_DIR / "final_leak_scan_result.json")

    _assert_clarify_candidate_payload(seed_rows, sft_rows)
    assert manifest["evidence_kind"] == "scaled_clarify_slot_boundary_candidate_materialization"
    assert manifest["materialization_status"] == "standalone_candidate_dataset_materialized"
    assert manifest["summary"]["candidate_seed_rows"] == 9
    assert manifest["summary"]["candidate_sft_rows"] == 27
    assert manifest["summary"]["source_family_count"] == 28
    assert manifest["summary"]["source_family_incidence_total"] == 78
    assert manifest["summary"]["formal_public_sample_modified"] is False
    assert evidence["artifact_files"]["candidate_seed"] == (
        "data/public-samples/scaled_clarify_slot_boundary_seed_candidates.jsonl"
    )
    assert manifest["artifact_policy"]["formal_public_sample_files_modified"] is False
    assert manifest["artifact_policy"]["formal_sample_merge"] is False
    assert manifest["artifact_policy"]["formal_dpo_rebuilt"] is False
    assert manifest["artifact_policy"]["training_run"] is False
    assert manifest["artifact_policy"]["prediction_run"] is False
    assert manifest["artifact_policy"]["a100_execution"] is False
    assert manifest["artifact_policy"]["evaluator_metric_change"] is False
    assert manifest["artifact_policy"]["private_paths_omitted"] is True
    assert leak_scan["ok"] is True
