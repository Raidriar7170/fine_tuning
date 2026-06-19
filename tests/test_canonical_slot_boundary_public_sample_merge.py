import json
from collections import Counter
from pathlib import Path

import pytest

from voice2task.cli import data as data_cli
from voice2task.dataset import (
    build_public_sample_dataset,
    canonical_slot_boundary_public_sample_merge_evidence,
    merge_canonical_slot_boundary_candidates_into_public_sample,
)
from voice2task.io import read_json, read_jsonl, write_jsonl
from voice2task.leak_scan import scan_paths
from voice2task.reports import write_canonical_slot_boundary_public_sample_merge_report
from voice2task.validation import validate_dataset_artifacts

REPO_ROOT = Path(__file__).resolve().parents[1]
PUBLIC_SAMPLE_DIR = REPO_ROOT / "data" / "public-samples"
CANONICAL_CANDIDATE_SEED = PUBLIC_SAMPLE_DIR / "canonical_slot_boundary_seed_candidates.jsonl"
MERGE_EVIDENCE_DIR = (
    REPO_ROOT / "reports" / "public-sample" / "canonical-slot-boundary-formal-merge"
)

EXPECTED_CANONICAL_IDS = {row["id"] for row in read_jsonl(CANONICAL_CANDIDATE_SEED)}
PRE_MERGE_COUNTS = {"dpo_pairs": 2046, "seed_rows": 240, "sft_rows": 675}
EXPECTED_COUNTS = {"dpo_pairs": 2100, "seed_rows": 247, "sft_rows": 696}
EXPECTED_SPLITS = {"dev": 207, "test": 207, "train": 282}
EXPECTED_SEED_SPLITS = {"dev": 0, "test": 0, "train": 7}
EXPECTED_CLASS_COUNTS = {"slot_key_aliases": 3, "slot_value_boundaries": 4}
EXPECTED_DPO_DELTAS = {
    "blocked_payment_action_drift": 0,
    "clarify_action_drift": 0,
    "decomposed_search_slots": 0,
    "extract_extra_particle_wording": 0,
    "extract_generic_price_wording": 0,
    "extract_listed_price_wording": 0,
    "extract_query_slot": 1,
    "extract_search_fallback": 1,
    "form_confirmation_drift": 0,
    "malformed_schema": 7,
    "missing_confirmation": 1,
    "missing_slot": 7,
    "navigate_canonical_url_drift": 2,
    "underspecified_request": 7,
    "unsafe_allowance": 7,
    "wrong_route": 7,
    "wrong_slot": 7,
    "wrong_task_type": 7,
}


def _copy_current_public_sample_without_canonical_candidates(tmp_path: Path) -> Path:
    public_dir = tmp_path / "public-samples"
    public_dir.mkdir()
    seed_rows = [
        row
        for row in read_jsonl(PUBLIC_SAMPLE_DIR / "seed_traces.jsonl")
        if row["id"] not in EXPECTED_CANONICAL_IDS
    ]
    write_jsonl(public_dir / "seed_traces.jsonl", seed_rows)
    build_public_sample_dataset(seed_path=public_dir / "seed_traces.jsonl", output_dir=public_dir)
    return public_dir


def _assert_manifest_has_canonical_merge_summary(manifest_payload: dict) -> None:
    assert manifest_payload["counts"] == EXPECTED_COUNTS
    assert manifest_payload["split_counts"] == EXPECTED_SPLITS
    source_summary = manifest_payload["source_summary"]
    assert source_summary["canonical_slot_boundary_candidate_seed_rows"] == 7
    assert source_summary["canonical_slot_boundary_candidate_sft_rows"] == 21
    assert source_summary["canonical_slot_boundary_candidates_formal_public_sample"] is True
    assert source_summary["canonical_slot_boundary_seed_split_counts"] == EXPECTED_SEED_SPLITS
    assert source_summary["canonical_slot_boundary_candidate_class_counts"] == EXPECTED_CLASS_COUNTS
    assert source_summary["comparison_boundary_changed"] is True


def _assert_canonical_rows_are_formal(seed_rows: list[dict], sft_rows: list[dict]) -> None:
    seed_by_id = {row["id"]: row for row in seed_rows}
    sft_by_source = {}
    for row in sft_rows:
        sft_by_source.setdefault(row["provenance"]["source_id"], []).append(row)

    candidate_rows = read_jsonl(CANONICAL_CANDIDATE_SEED)
    assert EXPECTED_CANONICAL_IDS.issubset(seed_by_id)
    assert Counter(row["split"] for row in candidate_rows) == {"train": 7}

    for candidate in candidate_rows:
        seed = seed_by_id[candidate["id"]]
        provenance = seed["provenance"]
        assert seed["split"] == "train"
        assert provenance["candidate_status"] == "formal_public_sample"
        assert provenance["source_mode"] == "canonical_slot_boundary_formal_public_seed"
        assert provenance["merged_from_candidate_seed"] == (
            "data/public-samples/canonical_slot_boundary_seed_candidates.jsonl"
        )
        assert provenance["source_candidate_id"] == candidate["id"]
        assert provenance["eligible_source_class"] == candidate["provenance"]["eligible_source_class"]
        assert provenance["formal_public_sample_status"] == "added"

        assert len(sft_by_source[candidate["id"]]) == 3
        assert {row["split"] for row in sft_by_source[candidate["id"]]} == {"train"}
        assert all(
            row["provenance"]["candidate_status"] == "formal_public_sample"
            for row in sft_by_source[candidate["id"]]
        )


def test_merge_canonical_slot_boundary_candidates_rebuilds_formal_public_sample(
    tmp_path: Path,
) -> None:
    public_dir = _copy_current_public_sample_without_canonical_candidates(tmp_path)

    manifest = merge_canonical_slot_boundary_candidates_into_public_sample(
        candidate_seed_path=CANONICAL_CANDIDATE_SEED,
        seed_path=public_dir / "seed_traces.jsonl",
        output_dir=public_dir,
    )

    seed_rows = read_jsonl(public_dir / "seed_traces.jsonl")
    sft_rows = read_jsonl(public_dir / "sft_public_sample.jsonl")
    dpo_rows = read_jsonl(public_dir / "dpo_public_sample.jsonl")
    manifest_payload = read_json(public_dir / "manifest_public_sample.json")

    assert manifest.counts == EXPECTED_COUNTS
    assert manifest.split_counts == EXPECTED_SPLITS
    _assert_manifest_has_canonical_merge_summary(manifest_payload)
    assert len(seed_rows) == EXPECTED_COUNTS["seed_rows"]
    assert len(sft_rows) == EXPECTED_COUNTS["sft_rows"]
    assert len(dpo_rows) == EXPECTED_COUNTS["dpo_pairs"]
    _assert_canonical_rows_are_formal(seed_rows, sft_rows)

    validation = validate_dataset_artifacts(
        sft_path=public_dir / "sft_public_sample.jsonl",
        dpo_path=public_dir / "dpo_public_sample.jsonl",
        manifest_path=public_dir / "manifest_public_sample.json",
        public=True,
    )
    assert validation.ok is True
    assert scan_paths([public_dir]).ok is True


def test_merge_canonical_slot_boundary_candidates_cli_writes_evidence(
    tmp_path: Path,
    capsys,
) -> None:
    public_dir = _copy_current_public_sample_without_canonical_candidates(tmp_path)
    evidence_dir = tmp_path / "merge-evidence"

    assert (
        data_cli.main(
            [
                "merge-canonical-slot-boundary-row-level-candidates",
                "--candidate-seed",
                CANONICAL_CANDIDATE_SEED.as_posix(),
                "--seed",
                (public_dir / "seed_traces.jsonl").as_posix(),
                "--output",
                public_dir.as_posix(),
                "--evidence-output",
                evidence_dir.as_posix(),
            ]
        )
        == 0
    )

    payload = json.loads(capsys.readouterr().out)
    assert payload["ok"] is True
    assert payload["counts"] == EXPECTED_COUNTS
    assert payload["split_counts"] == EXPECTED_SPLITS
    assert payload["source_summary"]["canonical_slot_boundary_candidate_seed_rows"] == 7
    assert payload["evidence_paths"]["manifest"] == (evidence_dir / "manifest.json").as_posix()

    evidence = read_json(evidence_dir / "canonical_slot_boundary_public_sample_merge.json")
    evidence_manifest = read_json(evidence_dir / "manifest.json")
    markdown = (evidence_dir / "canonical_slot_boundary_public_sample_merge.md").read_text(
        encoding="utf-8"
    )
    assert evidence["evidence_kind"] == "canonical_slot_boundary_public_sample_merge"
    assert evidence["pre_merge_public_sample_counts"] == PRE_MERGE_COUNTS
    assert evidence["candidate_source"]["candidate_dpo_pairs"] == 54
    assert evidence["candidate_source"]["dpo_rejection_deltas"] == EXPECTED_DPO_DELTAS
    assert evidence["comparison_boundary"]["changed"] is True
    assert evidence["metric_authority"]["slot_f1_soft"] == "diagnostic_only_not_primary"
    assert evidence_manifest["formal_public_sample_counts"] == EXPECTED_COUNTS
    assert evidence_manifest["claims"]["held_out_generalization_recovered"] is False
    assert "old metrics are not directly comparable" in markdown
    assert "strict `contract_exact_match` and strict `slot_f1` remain authoritative" in markdown
    assert scan_paths([evidence_dir]).ok is True


def test_merge_canonical_slot_boundary_candidates_rejects_unreviewed_rows(
    tmp_path: Path,
) -> None:
    public_dir = _copy_current_public_sample_without_canonical_candidates(tmp_path)
    candidate_rows = read_jsonl(CANONICAL_CANDIDATE_SEED)
    unreviewed = dict(candidate_rows[0])
    unreviewed["id"] = "canonical-slot-boundary-unreviewed-extra"
    write_jsonl(tmp_path / "candidate_seed_with_extra.jsonl", [*candidate_rows, unreviewed])

    with pytest.raises(ValueError, match="expected reviewed canonical slot-boundary candidate seed IDs"):
        merge_canonical_slot_boundary_candidates_into_public_sample(
            candidate_seed_path=tmp_path / "candidate_seed_with_extra.jsonl",
            seed_path=public_dir / "seed_traces.jsonl",
            output_dir=public_dir,
        )


def test_merge_canonical_slot_boundary_candidates_rejects_missing_candidate_row(
    tmp_path: Path,
) -> None:
    public_dir = _copy_current_public_sample_without_canonical_candidates(tmp_path)
    candidate_rows = read_jsonl(CANONICAL_CANDIDATE_SEED)
    write_jsonl(tmp_path / "candidate_seed_missing_row.jsonl", candidate_rows[:-1])

    with pytest.raises(ValueError, match="expected reviewed canonical slot-boundary candidate seed IDs"):
        merge_canonical_slot_boundary_candidates_into_public_sample(
            candidate_seed_path=tmp_path / "candidate_seed_missing_row.jsonl",
            seed_path=public_dir / "seed_traces.jsonl",
            output_dir=public_dir,
        )


def test_merge_canonical_slot_boundary_candidates_rejects_duplicate_candidate_row(
    tmp_path: Path,
) -> None:
    public_dir = _copy_current_public_sample_without_canonical_candidates(tmp_path)
    candidate_rows = read_jsonl(CANONICAL_CANDIDATE_SEED)
    write_jsonl(tmp_path / "candidate_seed_with_duplicate_row.jsonl", [*candidate_rows, candidate_rows[0]])

    with pytest.raises(ValueError, match="without duplicates"):
        merge_canonical_slot_boundary_candidates_into_public_sample(
            candidate_seed_path=tmp_path / "candidate_seed_with_duplicate_row.jsonl",
            seed_path=public_dir / "seed_traces.jsonl",
            output_dir=public_dir,
        )


def test_merge_canonical_slot_boundary_candidates_rejects_duplicate_formal_ids(
    tmp_path: Path,
) -> None:
    public_dir = _copy_current_public_sample_without_canonical_candidates(tmp_path)
    seed_path = public_dir / "seed_traces.jsonl"
    candidate_rows = read_jsonl(CANONICAL_CANDIDATE_SEED)
    write_jsonl(seed_path, [*read_jsonl(seed_path), candidate_rows[0]])

    with pytest.raises(ValueError, match="canonical slot-boundary candidate seed IDs already exist"):
        merge_canonical_slot_boundary_candidates_into_public_sample(
            candidate_seed_path=CANONICAL_CANDIDATE_SEED,
            seed_path=seed_path,
            output_dir=public_dir,
        )


def test_merge_canonical_slot_boundary_candidates_rejects_non_standalone_or_unsafe_rows(
    tmp_path: Path,
) -> None:
    public_dir = _copy_current_public_sample_without_canonical_candidates(tmp_path)
    candidate_rows = json.loads(json.dumps(read_jsonl(CANONICAL_CANDIDATE_SEED), ensure_ascii=False))
    candidate_rows[0]["provenance"]["candidate_status"] = "formal_public_sample"
    write_jsonl(tmp_path / "candidate_seed_with_formal_status.jsonl", candidate_rows)

    with pytest.raises(ValueError, match="must originate from standalone status"):
        merge_canonical_slot_boundary_candidates_into_public_sample(
            candidate_seed_path=tmp_path / "candidate_seed_with_formal_status.jsonl",
            seed_path=public_dir / "seed_traces.jsonl",
            output_dir=public_dir,
        )

    candidate_rows = json.loads(json.dumps(read_jsonl(CANONICAL_CANDIDATE_SEED), ensure_ascii=False))
    candidate_rows[0]["provenance"]["public_safe"] = False
    write_jsonl(tmp_path / "candidate_seed_with_unsafe_status.jsonl", candidate_rows)

    with pytest.raises(ValueError, match="must be public_safe"):
        merge_canonical_slot_boundary_candidates_into_public_sample(
            candidate_seed_path=tmp_path / "candidate_seed_with_unsafe_status.jsonl",
            seed_path=public_dir / "seed_traces.jsonl",
            output_dir=public_dir,
        )


def test_canonical_slot_boundary_merge_report_writer_rejects_contradictory_claim(
    tmp_path: Path,
) -> None:
    public_dir = _copy_current_public_sample_without_canonical_candidates(tmp_path)
    pre_merge_manifest = read_json(public_dir / "manifest_public_sample.json")
    manifest = merge_canonical_slot_boundary_candidates_into_public_sample(
        candidate_seed_path=CANONICAL_CANDIDATE_SEED,
        seed_path=public_dir / "seed_traces.jsonl",
        output_dir=public_dir,
    )
    evidence = canonical_slot_boundary_public_sample_merge_evidence(
        manifest=manifest,
        candidate_seed_path=CANONICAL_CANDIDATE_SEED,
        pre_merge_manifest=pre_merge_manifest,
    )
    evidence["execution_scope"]["training_run"] = True

    with pytest.raises(ValueError, match="canonical slot-boundary merge report cannot claim"):
        write_canonical_slot_boundary_public_sample_merge_report(
            evidence,
            output_dir=tmp_path / "bad-report",
        )


def test_committed_formal_public_sample_contains_canonical_slot_boundary_candidates() -> None:
    manifest = read_json(PUBLIC_SAMPLE_DIR / "manifest_public_sample.json")
    seed_rows = read_jsonl(PUBLIC_SAMPLE_DIR / "seed_traces.jsonl")
    sft_rows = read_jsonl(PUBLIC_SAMPLE_DIR / "sft_public_sample.jsonl")

    _assert_manifest_has_canonical_merge_summary(manifest)
    _assert_canonical_rows_are_formal(seed_rows, sft_rows)
    assert scan_paths([PUBLIC_SAMPLE_DIR]).ok is True


def test_committed_canonical_slot_boundary_merge_evidence_is_public_safe() -> None:
    evidence = read_json(MERGE_EVIDENCE_DIR / "canonical_slot_boundary_public_sample_merge.json")
    evidence_manifest = read_json(MERGE_EVIDENCE_DIR / "manifest.json")

    assert evidence["evidence_kind"] == "canonical_slot_boundary_public_sample_merge"
    assert evidence["pre_merge_public_sample_counts"] == PRE_MERGE_COUNTS
    assert evidence["execution_scope"]["training_run"] is False
    assert evidence["execution_scope"]["prediction_run"] is False
    assert evidence["execution_scope"]["a100_execution"] is False
    assert evidence["execution_scope"]["prompt_change"] is False
    assert evidence["execution_scope"]["postprocessor_implementation"] is False
    assert evidence["execution_scope"]["evaluator_metric_change"] is False
    assert evidence["candidate_source"]["candidate_dpo_pairs"] == 54
    assert evidence_manifest["formal_public_sample_counts"] == EXPECTED_COUNTS
    assert evidence_manifest["formal_public_sample_split_counts"] == EXPECTED_SPLITS
    assert evidence_manifest["claims"]["held_out_generalization_recovered"] is False
    assert evidence_manifest["claims"]["model_quality_claim"] is False
    assert evidence_manifest["claims"]["adapter_release"] is False
    assert evidence_manifest["claims"]["checkpoint_release"] is False
    assert evidence_manifest["comparison_boundary"]["changed"] is True
    assert scan_paths([MERGE_EVIDENCE_DIR]).ok is True
