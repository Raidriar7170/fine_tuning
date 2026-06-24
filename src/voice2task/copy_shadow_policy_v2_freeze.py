from __future__ import annotations

import hashlib
from collections import Counter
from pathlib import Path
from typing import Any

from voice2task.copy_shadow_false_trust_diagnosis import EXPECTED_CHALLENGE_HASH, EXPECTED_POLICY_HASH
from voice2task.copy_shadow_scope_policy_design import (
    DECISION_SCOPE_REDUCTION_READY,
    GATE_VERSION,
    RECOMMENDED_SCOPE_REDUCTION_NEXT_CHANGE,
)
from voice2task.io import read_json, write_json

CHANGE_ID = "review-and-freeze-copy-shadow-policy-v2-before-naturalistic-challenge"
EVIDENCE_KIND = "copy_shadow_policy_v2_freeze"
DEFAULT_DESIGN_DIR = Path("reports/public-sample/copy-shadow-scope-policy-v2-design")
DEFAULT_FREEZE_DIR = Path("reports/public-sample/copy-shadow-policy-v2-freeze")
DEFAULT_PROPOSED_POLICY_PATH = Path("configs/copy-backed-scope-policy-v2.proposed.json")
DEFAULT_FROZEN_POLICY_PATH = Path("configs/copy-backed-scope-policy-v2.frozen.json")

DECISION_FREEZE_READY = "POLICY_V2_FROZEN_INACTIVE_REFERENCE_READY_FOR_NATURALISTIC_CHALLENGE_DESIGN"
DECISION_FREEZE_BLOCKED = "POLICY_V2_FREEZE_BLOCKED"
RECOMMENDED_NEXT_CHANGE = "design-and-materialize-naturalistic-copy-shadow-challenge-v2"

EXPECTED_FROZEN_SCOPE_STATUSES = {
    "extract:extract_page:target": "INSUFFICIENT_EVIDENCE",
    "form_fill:fill_form:field": "PROPOSE_DISABLE",
    "search:search_web:query": "INSUFFICIENT_EVIDENCE",
}
ALLOWED_REPORT_FILENAMES = {
    "summary.md",
    "summary.json",
    "freeze-input-audit.json",
    "frozen-scope-decisions.json",
    "recommended-next-change.md",
    "blocked.json",
}


def run_copy_shadow_policy_v2_freeze(
    repo_root: Path,
    *,
    proposed_policy_path: Path | None = None,
    design_dir: Path | None = None,
    frozen_policy_path: Path | None = None,
) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    proposed_policy_path = _resolve_repo_path(repo_root, proposed_policy_path or DEFAULT_PROPOSED_POLICY_PATH)
    design_dir = _resolve_repo_path(repo_root, design_dir or DEFAULT_DESIGN_DIR)
    frozen_policy_path = _resolve_repo_path(repo_root, frozen_policy_path or DEFAULT_FROZEN_POLICY_PATH)

    audit = _validate_freeze_inputs(repo_root, proposed_policy_path=proposed_policy_path, design_dir=design_dir)
    if not audit["ok"]:
        return {
            "summary": _blocked_summary(audit),
            "input_audit": audit,
            "frozen_policy": None,
            "frozen_scope_decisions": {},
        }

    proposed = read_json(proposed_policy_path)
    design_summary = read_json(design_dir / "summary.json")
    frozen_scope_decisions = _frozen_scope_decisions(proposed)
    frozen_policy = _frozen_policy(
        proposed=proposed,
        design_summary=design_summary,
        audit=audit,
        frozen_policy_path=_repo_relative(repo_root, frozen_policy_path),
        frozen_scope_decisions=frozen_scope_decisions,
    )
    summary = _summary(
        audit=audit,
        design_summary=design_summary,
        frozen_policy_path=_repo_relative(repo_root, frozen_policy_path),
        frozen_scope_decisions=frozen_scope_decisions,
    )
    return {
        "summary": summary,
        "input_audit": audit,
        "frozen_policy": frozen_policy,
        "frozen_scope_decisions": frozen_scope_decisions,
    }


def write_copy_shadow_policy_v2_freeze_report(
    repo_root: Path,
    *,
    output_dir: Path | None = None,
    proposed_policy_path: Path | None = None,
    design_dir: Path | None = None,
    frozen_policy_path: Path | None = None,
) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    output_dir = _resolve_repo_path(repo_root, output_dir or DEFAULT_FREEZE_DIR)
    frozen_policy_path = _resolve_repo_path(repo_root, frozen_policy_path or DEFAULT_FROZEN_POLICY_PATH)
    result = run_copy_shadow_policy_v2_freeze(
        repo_root,
        proposed_policy_path=proposed_policy_path,
        design_dir=design_dir,
        frozen_policy_path=frozen_policy_path,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    _remove_stale_report_files(output_dir)

    if result["summary"]["decision_label"] == DECISION_FREEZE_BLOCKED:
        if frozen_policy_path.exists():
            frozen_policy_path.unlink()
        write_json(output_dir / "blocked.json", _blocked_artifact(result))
        return result

    write_json(frozen_policy_path, result["frozen_policy"])
    write_json(output_dir / "summary.json", result["summary"])
    write_json(output_dir / "freeze-input-audit.json", result["input_audit"])
    write_json(output_dir / "frozen-scope-decisions.json", result["frozen_scope_decisions"])
    (output_dir / "summary.md").write_text(_summary_markdown(result), encoding="utf-8")
    (output_dir / "recommended-next-change.md").write_text(
        _recommended_next_change_markdown(result), encoding="utf-8"
    )
    return result


def _validate_freeze_inputs(repo_root: Path, *, proposed_policy_path: Path, design_dir: Path) -> dict[str, Any]:
    blocking: list[str] = []
    required_files = [
        proposed_policy_path,
        design_dir / "summary.json",
        design_dir / "scope-decisions.json",
        design_dir / "post-hardening-scope-metrics.json",
        design_dir / "taxonomy-migration.json",
        design_dir / "gate-config.json",
    ]
    for path in required_files:
        if not path.exists():
            blocking.append(f"missing:{_repo_relative(repo_root, path)}")

    if blocking:
        return _audit(blocking, source_hashes={})

    proposed = read_json(proposed_policy_path)
    design_summary = read_json(design_dir / "summary.json")
    scope_decisions = read_json(design_dir / "scope-decisions.json")
    metrics = read_json(design_dir / "post-hardening-scope-metrics.json")
    gate_config = read_json(design_dir / "gate-config.json")

    proposed_key = _repo_relative(repo_root, proposed_policy_path)
    design_summary_key = _repo_relative(repo_root, design_dir / "summary.json")
    scope_decisions_key = _repo_relative(repo_root, design_dir / "scope-decisions.json")
    metrics_key = _repo_relative(repo_root, design_dir / "post-hardening-scope-metrics.json")
    taxonomy_key = _repo_relative(repo_root, design_dir / "taxonomy-migration.json")
    gate_config_key = _repo_relative(repo_root, design_dir / "gate-config.json")
    source_hashes = {
        proposed_key: _sha256_file(proposed_policy_path),
        design_summary_key: _sha256_file(design_dir / "summary.json"),
        scope_decisions_key: _sha256_file(design_dir / "scope-decisions.json"),
        metrics_key: _sha256_file(design_dir / "post-hardening-scope-metrics.json"),
        taxonomy_key: _sha256_file(design_dir / "taxonomy-migration.json"),
        gate_config_key: _sha256_file(design_dir / "gate-config.json"),
    }

    if proposed.get("status") != "proposal":
        blocking.append("proposal_status_not_proposal")
    if (
        proposed.get("active") is not False
        or proposed.get("runtime_loaded") is not False
        or proposed.get("enforcement_enabled") is not False
    ):
        blocking.append("proposal_active_or_executable")
    if proposed.get("action_enabled") is not False or proposed.get("normalized_trusted") is not False:
        blocking.append("proposal_trust_boundary_enabled")
    if proposed.get("decision_label") != DECISION_SCOPE_REDUCTION_READY:
        blocking.append("proposal_decision_label_mismatch")
    if proposed.get("recommended_next_change") != RECOMMENDED_SCOPE_REDUCTION_NEXT_CHANGE:
        blocking.append("proposal_recommended_next_change_mismatch")
    if design_summary.get("decision_label") != DECISION_SCOPE_REDUCTION_READY:
        blocking.append("design_decision_label_mismatch")
    if design_summary.get("recommended_next_change") != RECOMMENDED_SCOPE_REDUCTION_NEXT_CHANGE:
        blocking.append("design_recommended_next_change_mismatch")
    if proposed.get("challenge_v1_hash") != EXPECTED_CHALLENGE_HASH:
        blocking.append("challenge_hash_mismatch")
    if design_summary.get("challenge_hash") != EXPECTED_CHALLENGE_HASH:
        blocking.append("design_challenge_hash_mismatch")
    if proposed.get("source_policy_v1_hash") != EXPECTED_POLICY_HASH:
        blocking.append("source_policy_v1_hash_mismatch")
    if design_summary.get("source_policy_v1_hash") != EXPECTED_POLICY_HASH:
        blocking.append("design_source_policy_v1_hash_mismatch")
    if proposed.get("decision_gate_version") != GATE_VERSION or gate_config.get("version") != GATE_VERSION:
        blocking.append("gate_version_mismatch")

    scopes = proposed.get("scopes", {})
    if set(scopes) != set(EXPECTED_FROZEN_SCOPE_STATUSES):
        blocking.append("scope_set_mismatch")
    if set(scope_decisions) != set(EXPECTED_FROZEN_SCOPE_STATUSES):
        blocking.append("scope_decision_set_mismatch")
    if set(metrics) != set(EXPECTED_FROZEN_SCOPE_STATUSES):
        blocking.append("scope_metric_set_mismatch")

    for scope, expected_status in sorted(EXPECTED_FROZEN_SCOPE_STATUSES.items()):
        proposed_scope = scopes.get(scope, {})
        decision_scope = scope_decisions.get(scope, {})
        metric_scope = metrics.get(scope, {})
        if proposed_scope.get("final_status") != expected_status:
            blocking.append(f"scope_status_mismatch:{scope}")
        if proposed_scope.get("final_status") != decision_scope.get("final_status"):
            blocking.append(f"scope_decision_drift:{scope}")
        if proposed_scope.get("original_gate_status") != decision_scope.get("original_gate_status"):
            blocking.append(f"scope_original_gate_drift:{scope}")
        if proposed_scope.get("metrics") != metric_scope:
            blocking.append(f"scope_metrics_drift:{scope}")
        if proposed_scope.get("reviewer_required") is not True or decision_scope.get("reviewer_required") is not True:
            blocking.append(f"reviewer_required_missing:{scope}")
        if (
            proposed_scope.get("execution_eligible") is not False
            or decision_scope.get("execution_eligible") is not False
        ):
            blocking.append(f"execution_eligible_not_false:{scope}")
        if int(metric_scope.get("technical_false_accept_count") or 0) != 0:
            blocking.append(f"technical_false_accept_nonzero:{scope}")
        if int(metric_scope.get("execution_eligible_count") or 0) != 0:
            blocking.append(f"execution_eligible_count_nonzero:{scope}")
        if metric_scope.get("policy_gate_deterministic") is not True:
            blocking.append(f"policy_gate_not_deterministic:{scope}")
        if metric_scope.get("attribution_mode") != "fixture_guided":
            blocking.append(f"attribution_mode_mismatch:{scope}")

    return _audit(
        blocking,
        source_hashes=source_hashes,
        source_design_decision_label=design_summary.get("decision_label"),
        source_policy_v1_hash=design_summary.get("source_policy_v1_hash"),
        challenge_v1_hash=design_summary.get("challenge_hash"),
        diagnosis_artifact_hash=proposed.get("diagnosis_artifact_hash"),
        proposed_policy_path=proposed_key,
        design_report_dir=_repo_relative(repo_root, design_dir),
    )


def _audit(
    blocking: list[str],
    *,
    source_hashes: dict[str, str],
    source_design_decision_label: Any = None,
    source_policy_v1_hash: Any = None,
    challenge_v1_hash: Any = None,
    diagnosis_artifact_hash: Any = None,
    proposed_policy_path: Any = None,
    design_report_dir: Any = None,
) -> dict[str, Any]:
    return {
        "audit_kind": "copy_shadow_policy_v2_freeze_input_audit",
        "ok": not blocking,
        "blocking_reasons": blocking,
        "source_hashes": source_hashes,
        "source_design_decision_label": source_design_decision_label,
        "source_policy_v1_hash": source_policy_v1_hash,
        "challenge_v1_hash": challenge_v1_hash,
        "diagnosis_artifact_hash": diagnosis_artifact_hash,
        "proposed_policy_path": proposed_policy_path,
        "design_report_dir": design_report_dir,
        "proposal_runtime_boundary": {
            "required_status": "proposal",
            "required_active": False,
            "required_runtime_loaded": False,
            "required_enforcement_enabled": False,
        },
    }


def _frozen_scope_decisions(proposed: dict[str, Any]) -> dict[str, dict[str, Any]]:
    decisions: dict[str, dict[str, Any]] = {}
    for scope, expected_status in sorted(EXPECTED_FROZEN_SCOPE_STATUSES.items()):
        row = proposed["scopes"][scope]
        decisions[scope] = {
            "scope_key": scope,
            "original_gate_status": row["original_gate_status"],
            "final_status": expected_status,
            "frozen_status": expected_status,
            "reviewer_required": True,
            "execution_eligible": False,
            "evidence_reference": row["evidence_reference"],
            "freeze_reason": "reviewed_policy_v2_proposal_frozen_inactive",
        }
    return decisions


def _frozen_policy(
    *,
    proposed: dict[str, Any],
    design_summary: dict[str, Any],
    audit: dict[str, Any],
    frozen_policy_path: str,
    frozen_scope_decisions: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    return {
        "policy_id": "copy-backed-scope-policy-v2-frozen",
        "policy_version": "2.0.0-frozen-reference",
        "status": "frozen_reference",
        "active": False,
        "runtime_loaded": False,
        "enforcement_enabled": False,
        "action_enabled": False,
        "normalized_trusted": False,
        "freeze_date": "2026-06-25",
        "source_proposal_path": audit["proposed_policy_path"],
        "source_proposal_hash": audit["source_hashes"][audit["proposed_policy_path"]],
        "source_design_report_dir": audit["design_report_dir"],
        "source_design_decision_label": design_summary["decision_label"],
        "source_design_hashes": {
            key: value for key, value in audit["source_hashes"].items() if key.startswith(audit["design_report_dir"])
        },
        "source_policy_v1_id": proposed["source_policy_v1_id"],
        "source_policy_v1_hash": proposed["source_policy_v1_hash"],
        "challenge_v1_hash": proposed["challenge_v1_hash"],
        "diagnosis_artifact_hash": proposed["diagnosis_artifact_hash"],
        "decision_gate_version": proposed["decision_gate_version"],
        "decision_label": DECISION_FREEZE_READY,
        "recommended_next_change": RECOMMENDED_NEXT_CHANGE,
        "frozen_policy_path": frozen_policy_path,
        "scopes": frozen_scope_decisions,
        "claims": _claims(),
    }


def _summary(
    *,
    audit: dict[str, Any],
    design_summary: dict[str, Any],
    frozen_policy_path: str,
    frozen_scope_decisions: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    status_counts = Counter(row["final_status"] for row in frozen_scope_decisions.values())
    return {
        "change_id": CHANGE_ID,
        "evidence_kind": EVIDENCE_KIND,
        "decision_label": DECISION_FREEZE_READY,
        "recommended_next_change": RECOMMENDED_NEXT_CHANGE,
        "input_boundary_ok": audit["ok"],
        "source_design_decision_label": design_summary["decision_label"],
        "source_policy_v1_hash": design_summary["source_policy_v1_hash"],
        "challenge_v1_hash": design_summary["challenge_hash"],
        "diagnosis_artifact_hash": audit["diagnosis_artifact_hash"],
        "decision_gate_version": GATE_VERSION,
        "frozen_policy_path": frozen_policy_path,
        "scope_status_counts": dict(sorted(status_counts.items())),
        "reviewer_required_scope_count": sum(1 for row in frozen_scope_decisions.values() if row["reviewer_required"]),
        "execution_eligible_count": 0,
        "technical_false_accept_count": 0,
        "policy_v1_modified": False,
        "proposed_policy_modified": False,
        "runtime_behavior_modified": False,
        "naturalistic_challenge_v2_created": False,
        "claims": _claims(),
    }


def _blocked_summary(audit: dict[str, Any]) -> dict[str, Any]:
    return {
        "change_id": CHANGE_ID,
        "evidence_kind": EVIDENCE_KIND,
        "decision_label": DECISION_FREEZE_BLOCKED,
        "recommended_next_change": None,
        "input_boundary_ok": False,
        "blocking_reasons": audit.get("blocking_reasons", []),
        "frozen_policy_emitted": False,
        "policy_v1_modified": False,
        "proposed_policy_modified": False,
        "runtime_behavior_modified": False,
        "naturalistic_challenge_v2_created": False,
        "claims": _claims(),
    }


def _blocked_artifact(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "decision": DECISION_FREEZE_BLOCKED,
        "blocking_reasons": result["input_audit"].get("blocking_reasons", []),
        "frozen_policy_emitted": False,
        "policy_v1_modified": False,
        "proposed_policy_modified": False,
        "runtime_behavior_modified": False,
        "naturalistic_challenge_v2_created": False,
    }


def _claims() -> dict[str, bool]:
    return {
        "policy_v1_modified": False,
        "proposed_policy_modified": False,
        "runtime_loaded": False,
        "runtime_enforcement_enabled": False,
        "action_enabled": False,
        "normalized_trusted_provenance_enabled": False,
        "naturalistic_challenge_v2_created": False,
        "training_run": False,
        "prediction_rerun": False,
        "challenge_modified": False,
        "evaluator_modified": False,
        "prompt_or_decoding_modified": False,
        "model_artifact_modified": False,
        "data_expansion": False,
        "model_improvement_claim": False,
        "production_readiness_claim": False,
        "safety_readiness_claim": False,
    }


def _summary_markdown(result: dict[str, Any]) -> str:
    summary = result["summary"]
    decisions = result["frozen_scope_decisions"]
    lines = [
        "# Copy-shadow Policy V2 freeze",
        "",
        f"Decision: `{summary['decision_label']}`.",
        "",
        "Frozen Policy V2 is an inactive reference only. It is not runtime loaded, not enforcement, "
        "not action eligibility, not normalized trust, not training, not data expansion, not naturalistic "
        "challenge v2, not model improvement, and not a production or safety readiness claim.",
        "",
        "## Frozen scope decisions",
        "",
    ]
    for scope, row in sorted(decisions.items()):
        lines.append(f"- `{scope}`: `{row['final_status']}`, reviewer required, execution eligible false")
    lines.extend(
        [
            "",
            "## Evidence",
            "",
            f"- Frozen policy: `{summary['frozen_policy_path']}`",
            f"- Source design decision: `{summary['source_design_decision_label']}`",
            f"- Challenge hash: `{summary['challenge_v1_hash']}`",
            f"- Policy V1 hash: `{summary['source_policy_v1_hash']}`",
            "- Runtime behavior modified: `false`",
            "",
            f"Recommended next change: `{summary['recommended_next_change']}`.",
        ]
    )
    return "\n".join(lines) + "\n"


def _recommended_next_change_markdown(result: dict[str, Any]) -> str:
    return (
        "# Recommended next change\n\n"
        f"`{result['summary']['recommended_next_change']}`\n\n"
        "Scope: design and materialize a naturalistic copy-shadow challenge v2 in a later phase only after "
        "using this inactive frozen Policy V2 reference as a boundary. Do not enable runtime enforcement, "
        "actions, normalized trusted provenance, training, prediction repair, data expansion beyond the "
        "future challenge scope, or model/executable improvement claims in this freeze phase.\n"
    )


def _remove_stale_report_files(output_dir: Path) -> None:
    for path in output_dir.iterdir():
        if path.is_file() and path.name in ALLOWED_REPORT_FILENAMES:
            path.unlink()


def _resolve_repo_path(repo_root: Path, path: Path) -> Path:
    return path if path.is_absolute() else repo_root / path


def _repo_relative(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
