from __future__ import annotations

import json
from pathlib import Path

from voice2task.copy_shadow_policy_v2_freeze import (
    DECISION_FREEZE_READY,
    EXPECTED_FROZEN_SCOPE_STATUSES,
    run_copy_shadow_policy_v2_freeze,
    write_copy_shadow_policy_v2_freeze_report,
)
from voice2task.io import read_json
from voice2task.leak_scan import scan_paths

REPO_ROOT = Path(__file__).resolve().parents[1]
FREEZE_DIR = REPO_ROOT / "reports/public-sample/copy-shadow-policy-v2-freeze"
FROZEN_POLICY_PATH = REPO_ROOT / "configs/copy-backed-scope-policy-v2.frozen.json"
PROPOSED_POLICY_PATH = REPO_ROOT / "configs/copy-backed-scope-policy-v2.proposed.json"
DESIGN_DIR = REPO_ROOT / "reports/public-sample/copy-shadow-scope-policy-v2-design"


def test_freeze_recomputes_policy_v2_reference_without_mutating_proposal() -> None:
    before_proposed = PROPOSED_POLICY_PATH.read_text(encoding="utf-8")

    result = run_copy_shadow_policy_v2_freeze(REPO_ROOT)

    assert PROPOSED_POLICY_PATH.read_text(encoding="utf-8") == before_proposed
    assert result["summary"]["decision_label"] == DECISION_FREEZE_READY
    assert result["summary"]["recommended_next_change"] == (
        "design-and-materialize-naturalistic-copy-shadow-challenge-v2"
    )
    assert result["summary"]["frozen_policy_path"] == "configs/copy-backed-scope-policy-v2.frozen.json"
    assert result["summary"]["policy_v1_modified"] is False
    assert result["summary"]["proposed_policy_modified"] is False
    assert result["summary"]["runtime_behavior_modified"] is False
    assert result["summary"]["naturalistic_challenge_v2_created"] is False
    assert result["summary"]["scope_status_counts"] == {
        "INSUFFICIENT_EVIDENCE": 2,
        "PROPOSE_DISABLE": 1,
    }
    assert result["frozen_policy"]["status"] == "frozen_reference"
    assert result["frozen_policy"]["active"] is False
    assert result["frozen_policy"]["runtime_loaded"] is False
    assert result["frozen_policy"]["enforcement_enabled"] is False
    assert result["frozen_policy"]["source_proposal_hash"] == result["input_audit"]["source_hashes"][
        "configs/copy-backed-scope-policy-v2.proposed.json"
    ]
    assert {
        scope: row["final_status"] for scope, row in result["frozen_policy"]["scopes"].items()
    } == EXPECTED_FROZEN_SCOPE_STATUSES
    assert all(row["reviewer_required"] is True for row in result["frozen_policy"]["scopes"].values())
    assert all(row["execution_eligible"] is False for row in result["frozen_policy"]["scopes"].values())


def test_freeze_writer_emits_bounded_public_safe_bundle(tmp_path: Path) -> None:
    output_dir = tmp_path / "freeze"
    frozen_policy_path = tmp_path / "copy-backed-scope-policy-v2.frozen.json"
    output_dir.mkdir()
    (output_dir / "summary.json").write_text("{}\n", encoding="utf-8")

    result = write_copy_shadow_policy_v2_freeze_report(
        REPO_ROOT,
        output_dir=output_dir,
        frozen_policy_path=frozen_policy_path,
    )

    assert result["summary"]["decision_label"] == DECISION_FREEZE_READY
    assert sorted(path.name for path in output_dir.iterdir()) == [
        "freeze-input-audit.json",
        "frozen-scope-decisions.json",
        "recommended-next-change.md",
        "summary.json",
        "summary.md",
    ]
    frozen = json.loads(frozen_policy_path.read_text(encoding="utf-8"))
    assert frozen["status"] == "frozen_reference"
    assert frozen["active"] is False
    assert frozen["runtime_loaded"] is False
    assert frozen["enforcement_enabled"] is False
    assert frozen["recommended_next_change"] == "design-and-materialize-naturalistic-copy-shadow-challenge-v2"
    assert scan_paths([output_dir, frozen_policy_path]).ok


def test_freeze_writer_does_not_delete_unrelated_files_in_output_dir(tmp_path: Path) -> None:
    output_dir = tmp_path / "freeze"
    frozen_policy_path = tmp_path / "copy-backed-scope-policy-v2.frozen.json"
    output_dir.mkdir()
    unrelated = output_dir / "EVIDENCE_INDEX.md"
    unrelated.write_text("keep me\n", encoding="utf-8")

    result = write_copy_shadow_policy_v2_freeze_report(
        REPO_ROOT,
        output_dir=output_dir,
        frozen_policy_path=frozen_policy_path,
    )

    assert result["summary"]["decision_label"] == DECISION_FREEZE_READY
    assert unrelated.read_text(encoding="utf-8") == "keep me\n"
    assert (output_dir / "summary.json").exists()


def test_freeze_blocks_drifted_or_executable_proposal_without_emitting_policy(tmp_path: Path) -> None:
    proposed = read_json(PROPOSED_POLICY_PATH)
    proposed["active"] = True
    proposed_path = tmp_path / "copy-backed-scope-policy-v2.proposed.json"
    proposed_path.write_text(json.dumps(proposed, ensure_ascii=False, indent=2), encoding="utf-8")
    frozen_policy_path = tmp_path / "copy-backed-scope-policy-v2.frozen.json"

    result = write_copy_shadow_policy_v2_freeze_report(
        REPO_ROOT,
        output_dir=tmp_path / "freeze",
        proposed_policy_path=proposed_path,
        frozen_policy_path=frozen_policy_path,
    )

    assert result["summary"]["decision_label"] == "POLICY_V2_FREEZE_BLOCKED"
    assert "proposal_active_or_executable" in result["input_audit"]["blocking_reasons"]
    assert sorted(path.name for path in (tmp_path / "freeze").iterdir()) == ["blocked.json"]
    assert not frozen_policy_path.exists()


def test_committed_freeze_artifacts_are_current_inactive_and_public_safe() -> None:
    summary = read_json(FREEZE_DIR / "summary.json")
    frozen = read_json(FROZEN_POLICY_PATH)
    design_summary = read_json(DESIGN_DIR / "summary.json")

    assert summary["decision_label"] == DECISION_FREEZE_READY
    assert summary["source_design_decision_label"] == design_summary["decision_label"]
    assert frozen["status"] == "frozen_reference"
    assert frozen["active"] is False
    assert frozen["runtime_loaded"] is False
    assert frozen["enforcement_enabled"] is False
    assert frozen["source_policy_v1_hash"] == design_summary["source_policy_v1_hash"]
    assert frozen["challenge_v1_hash"] == design_summary["challenge_hash"]
    assert {scope: row["final_status"] for scope, row in frozen["scopes"].items()} == EXPECTED_FROZEN_SCOPE_STATUSES
    assert all(row["reviewer_required"] is True for row in frozen["scopes"].values())
    assert all(row["execution_eligible"] is False for row in frozen["scopes"].values())
    assert scan_paths(
        [
            FREEZE_DIR,
            FROZEN_POLICY_PATH,
            REPO_ROOT / "docs/copy-shadow-policy-v2-freeze.md",
            REPO_ROOT
            / "docs/human-briefs"
            / "2026-06-25-review-and-freeze-copy-shadow-policy-v2-before-naturalistic-challenge.html",
        ]
    ).ok


def test_freeze_docs_preserve_runtime_and_claim_boundaries() -> None:
    text = (REPO_ROOT / "docs/copy-shadow-policy-v2-freeze.md").read_text(encoding="utf-8")

    for required in (
        "frozen_reference",
        "active=false",
        "runtime_loaded=false",
        "enforcement_enabled=false",
        "not runtime enforcement",
        "not action eligibility",
        "not normalized trust",
        "not training",
        "not naturalistic challenge v2",
        "design-and-materialize-naturalistic-copy-shadow-challenge-v2",
    ):
        assert required in text


def test_runtime_code_does_not_load_frozen_policy_v2_reference() -> None:
    runtime_paths = [
        *REPO_ROOT.glob("src/voice2task/**/*.py"),
        *REPO_ROOT.glob("scripts/*.py"),
    ]
    allowed_paths = {
        REPO_ROOT / "src/voice2task/copy_shadow_policy_v2_freeze.py",
        REPO_ROOT / "scripts/run_copy_shadow_policy_v2_freeze.py",
        REPO_ROOT / "scripts/check_current_truth_surface.py",
    }

    offenders = [
        path.relative_to(REPO_ROOT).as_posix()
        for path in runtime_paths
        if path not in allowed_paths and "copy-backed-scope-policy-v2.frozen.json" in path.read_text(encoding="utf-8")
    ]

    assert offenders == []
