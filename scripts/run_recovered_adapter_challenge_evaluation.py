from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
from collections import defaultdict
from collections.abc import Callable, Mapping
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from voice2task.copy_backed_shadow_interface import (
    build_evaluation_audits,
    count_provenance_false_accepts,
    load_scope_policy,
    online_sidecar_has_no_gold_fields,
    stable_hash,
    validate_scope_policy,
)
from voice2task.evaluation import evaluate_predictions, load_predictions
from voice2task.io import read_json, read_jsonl, write_json, write_jsonl
from voice2task.leak_scan import scan_paths
from voice2task.schemas import PRIVATE_IP_RE, SECRET_RE, as_contract, canonical_contract_json
from voice2task.training import run_sft_prediction_export

CHANGE_ID = "recover-and-run-frozen-adapter-challenge-evaluation"
CHALLENGE_ID = "copy-shadow-template-disjoint-challenge-v1"
CHALLENGE_VERSION = "copy-shadow-template-disjoint-challenge-v1"
DEFAULT_CHALLENGE_PATH = Path("data/public-samples/copy-shadow-template-disjoint-challenge-v1.jsonl")
DEFAULT_POLICY_PATH = Path("configs/copy-backed-scope-policy-v1.json")
DEFAULT_CHALLENGE_REPORT_DIR = Path("reports/public-sample/copy-shadow-template-disjoint-challenge-v1")
DEFAULT_OUTPUT_DIR = DEFAULT_CHALLENGE_REPORT_DIR / "adapter-evaluation"
EXPECTED_CHALLENGE_HASH = "12eccdd54b2c89f1127ec23f18d7179e1ebaacb1a644ae5ca1a14b3309f11324"
EXPECTED_POLICY_HASH = "5dc14efb8ded13dc048ddb067c7c63a1a62b6c03896950e861303973d505cbc7"
EXPECTED_ROW_COUNT = 120
CANONICAL_HOOK_PATH = "voice2task.training.run_sft_prediction_export -> copy_backed_shadow"
EVALUATION_AUDITS_FILENAME = "evaluation-audits.jsonl"

DECISION_BOUNDARY_MISMATCH = "CHALLENGE_EVALUATION_BLOCKED_BOUNDARY_MISMATCH"
DECISION_ADAPTER_UNAVAILABLE = "CHALLENGE_EVALUATION_BLOCKED_ADAPTER_UNAVAILABLE"
DECISION_ADAPTER_IDENTITY = "CHALLENGE_EVALUATION_BLOCKED_ADAPTER_IDENTITY"
DECISION_OBSERVE_ONLY = "CHALLENGE_V1_VERIFIER_VALIDATED_OBSERVE_ONLY"
DECISION_HOOK_UNSAFE = "CHALLENGE_V1_HOOK_UNSAFE_OR_INVALID"

HIGH_RISK_FALSE_TRUST_KEYS = (
    "duplicate_source_false_trust_count",
    "source_absent_false_trust_count",
    "normalization_collision_false_trust_count",
    "partial_span_false_trust_count",
    "out_of_scope_action_false_trust_count",
)

EXPECTED_ADAPTERS: dict[str, dict[str, str]] = {
    "control": {
        "run_id": "step-matched-canonical-slot-ablation-20260620T000000Z:control",
        "manifest_id": "public-sample-20260617T152259Z",
        "adapter_config_hash": "462d4897a7b4051ad20d7c322fadaaaf51c5e2fe4908c751de6a669360f60bc8",
        "adapter_model_hash": "27aaffc10f39d497af08bfa35d4f914bd198dafc514798449e0e5292b56a6359",
    },
    "treatment": {
        "run_id": "step-matched-canonical-slot-ablation-20260620T000000Z:treatment",
        "manifest_id": "public-sample-20260619T090925Z",
        "adapter_config_hash": "b8ac8b6a5751315463da9e8465781b179807441f10d9a7996e773d9f418ef868",
        "adapter_model_hash": "a23c54e7c157de2dd80c88777ac752272803096f7e9a19aa69669d13c8eb9238",
    },
}

ENV_OVERRIDE_PATH = "RECOVERED_ADAPTER_CHALLENGE_OVERRIDE_JSON"
ENV_ADAPTER_PATHS = {
    "control": (
        "RECOVERED_ADAPTER_CHALLENGE_CONTROL_ADAPTER_PATH",
        "RECOVERED_CHALLENGE_CONTROL_ADAPTER_PATH",
    ),
    "treatment": (
        "RECOVERED_ADAPTER_CHALLENGE_TREATMENT_ADAPTER_PATH",
        "RECOVERED_CHALLENGE_TREATMENT_ADAPTER_PATH",
    ),
}

PRIVATE_PATH_RE = re.compile(r"(/(?:mnt/data|Users|root|tmp|private)/[^\s\"')]+)")


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _sanitize_string(value: str) -> str:
    sanitized = PRIVATE_PATH_RE.sub("<private_path>", value)
    sanitized = PRIVATE_IP_RE.sub("<private_ip>", sanitized)
    return SECRET_RE.sub("<secret>", sanitized)


def _sanitize_value(value: Any) -> Any:
    if isinstance(value, str):
        return _sanitize_string(value)
    if isinstance(value, dict):
        return {str(_sanitize_value(key)): _sanitize_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_sanitize_value(item) for item in value]
    return value


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _active_change_boundary(repo_root: Path, expected_active_change: str) -> dict[str, Any]:
    archive_matches = sorted(
        path.name
        for path in (repo_root / "openspec/changes/archive").glob(f"*-{expected_active_change}")
        if path.is_dir()
    )
    try:
        completed = subprocess.run(
            ["openspec", "list", "--json"],
            cwd=repo_root,
            env={**os.environ, "OPENSPEC_TELEMETRY": "0"},
            check=False,
            text=True,
            capture_output=True,
            timeout=20,
        )
    except (OSError, subprocess.TimeoutExpired):
        change_dir = repo_root / "openspec/changes" / expected_active_change
        archived = bool(archive_matches)
        ok = change_dir.exists() or archived
        return {
            "ok": ok,
            "method": "filesystem_fallback",
            "active_changes": [expected_active_change] if change_dir.exists() else [],
            "archived_changes": archive_matches,
            "blocking_reasons": [] if ok else ["expected_change_missing"],
        }
    raw = completed.stdout.strip()
    json_start = raw.find("{")
    if completed.returncode != 0 or json_start < 0:
        return {
            "ok": False,
            "method": "openspec_list",
            "active_changes": [],
            "blocking_reasons": ["openspec_list_failed"],
        }
    payload = json.loads(raw[json_start:])
    changes = payload.get("changes", [])
    active = [
        str(change.get("name"))
        for change in changes
        if isinstance(change, dict) and str(change.get("status", "")) != "archived"
    ]
    blocking: list[str] = []
    conflicts = sorted(name for name in active if name != expected_active_change)
    if expected_active_change not in active and not archive_matches:
        blocking.append("expected_change_missing")
    if conflicts:
        blocking.append("conflicting_active_changes")
    return {
        "ok": not blocking,
        "method": "openspec_list",
        "active_changes": sorted(active),
        "archived_changes": archive_matches,
        "expected_active_change": expected_active_change,
        "conflicting_active_changes": conflicts,
        "blocking_reasons": blocking,
    }


def audit_frozen_boundary(
    repo_root: Path,
    *,
    expected_challenge_hash: str = EXPECTED_CHALLENGE_HASH,
    expected_policy_hash: str = EXPECTED_POLICY_HASH,
    expected_active_change: str = CHANGE_ID,
) -> dict[str, Any]:
    challenge_path = repo_root / DEFAULT_CHALLENGE_PATH
    policy_path = repo_root / DEFAULT_POLICY_PATH
    manifest_path = repo_root / DEFAULT_CHALLENGE_REPORT_DIR / "challenge-manifest.json"
    template_audit_path = repo_root / DEFAULT_CHALLENGE_REPORT_DIR / "template-disjoint-audit.json"

    rows = read_jsonl(challenge_path)
    manifest = read_json(manifest_path)
    template_audit = read_json(template_audit_path)
    policy = load_scope_policy(policy_path)
    policy_validation = validate_scope_policy(policy)
    challenge_hash = stable_hash(rows)
    gold_hash = stable_hash(
        [
            {
                "challenge_id": row.get("challenge_id"),
                "gold_hash": row.get("gold_hash"),
                "gold_contract_hash": stable_hash(canonical_contract_json(row.get("gold_contract", {}))),
            }
            for row in rows
        ]
    )
    active_boundary = _active_change_boundary(repo_root, expected_active_change)
    blocking: list[str] = []
    if challenge_hash != expected_challenge_hash:
        blocking.append("challenge_hash_mismatch")
    if manifest.get("challenge_hash") != challenge_hash:
        blocking.append("challenge_manifest_hash_mismatch")
    if len(rows) != EXPECTED_ROW_COUNT:
        blocking.append("challenge_row_count_mismatch")
    if any(row.get("challenge_version") != CHALLENGE_VERSION for row in rows):
        blocking.append("challenge_version_mismatch")
    if any(row.get("public_safe") is not True for row in rows):
        blocking.append("challenge_public_safe_mismatch")
    if template_audit.get("accepted") is not True:
        blocking.append("template_disjoint_audit_not_accepted")
    if policy_validation.get("ok") is not True:
        blocking.append("policy_validation_failed")
    if policy_validation.get("computed_policy_hash") != expected_policy_hash:
        blocking.append("policy_hash_mismatch")
    if policy_validation.get("policy_hash") != expected_policy_hash:
        blocking.append("policy_declared_hash_mismatch")
    if policy_validation.get("action_enabled") is not False:
        blocking.append("action_enabled_mismatch")
    if policy_validation.get("normalized_trusted") is not False:
        blocking.append("normalized_trusted_mismatch")
    if active_boundary.get("ok") is not True:
        blocking.extend(f"active_change:{reason}" for reason in active_boundary.get("blocking_reasons", []))
    return {
        "audit_kind": "recovered_adapter_challenge_boundary_audit",
        "ok": not blocking,
        "blocking_reasons": blocking,
        "challenge_id": CHALLENGE_ID,
        "challenge_version": CHALLENGE_VERSION,
        "challenge_hash": challenge_hash,
        "challenge_manifest_hash": manifest.get("challenge_hash"),
        "expected_challenge_hash": expected_challenge_hash,
        "row_count": len(rows),
        "expected_row_count": EXPECTED_ROW_COUNT,
        "gold_hash": gold_hash,
        "policy_hash": policy_validation.get("computed_policy_hash"),
        "expected_policy_hash": expected_policy_hash,
        "policy_validation": policy_validation,
        "template_disjoint_audit": {
            "accepted": template_audit.get("accepted"),
            "row_count": template_audit.get("row_count"),
            "overlap_counts": template_audit.get("overlap_counts"),
        },
        "active_change_boundary": active_boundary,
    }


def _path_value_is_unresolved(value: str) -> bool:
    stripped = value.strip()
    return not stripped or "<" in stripped or ">" in stripped or stripped.startswith("$")


def _override_payload(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("private override must be a JSON object")
    return payload


def _override_locations(payload: dict[str, Any]) -> dict[str, str]:
    adapters = payload.get("adapters")
    locations: dict[str, str] = {}
    for role in ("control", "treatment"):
        candidates = [
            payload.get(f"{role}_adapter_path"),
            payload.get(f"{role}_path"),
        ]
        if isinstance(adapters, dict):
            item = adapters.get(role)
            if isinstance(item, dict):
                candidates.extend([item.get("adapter_path"), item.get("path")])
            else:
                candidates.append(item)
        for candidate in candidates:
            if isinstance(candidate, str) and candidate.strip():
                locations[role] = candidate
                break
    return locations


def _env_locations(env: Mapping[str, str]) -> dict[str, str]:
    locations: dict[str, str] = {}
    for role, keys in ENV_ADAPTER_PATHS.items():
        for key in keys:
            value = env.get(key)
            if value:
                locations[role] = value
                break
    return locations


def _adapter_model_path(adapter_dir: Path) -> Path | None:
    for name in ("adapter_model.safetensors", "adapter_model.bin"):
        candidate = adapter_dir / name
        if candidate.exists():
            return candidate
    return None


def _sanitized_config_fields(config: dict[str, Any]) -> dict[str, Any]:
    return _sanitize_value(
        {
            "base_model_id": config.get("base_model_name_or_path") or config.get("base_model"),
            "tokenizer_id": config.get("tokenizer_name_or_path") or config.get("base_model_name_or_path"),
            "peft_type": config.get("peft_type"),
            "lora_rank": config.get("r"),
            "lora_alpha": config.get("lora_alpha"),
            "lora_dropout": config.get("lora_dropout"),
            "target_modules": sorted(config.get("target_modules", []))
            if isinstance(config.get("target_modules"), list)
            else config.get("target_modules"),
        }
    )


def _verify_one_adapter(
    role: str,
    path_text: str | None,
    expected: dict[str, str],
) -> tuple[dict[str, Any], Path | None]:
    base = {
        "role": role,
        "run_id": expected["run_id"],
        "manifest_id": expected["manifest_id"],
        "expected_adapter_config_hash": expected["adapter_config_hash"],
        "expected_adapter_model_hash": expected["adapter_model_hash"],
        "private_path_recorded": False,
    }
    if path_text is None:
        return base | {"identity_status": "unavailable", "available": False, "failures": ["adapter_path_missing"]}, None
    if _path_value_is_unresolved(path_text):
        return (
            base
            | {
                "identity_status": "unresolved_override",
                "available": False,
                "failures": ["adapter_path_unresolved_template"],
            },
            None,
        )
    adapter_dir = Path(path_text).expanduser()
    if not adapter_dir.exists() or not adapter_dir.is_dir():
        return base | {"identity_status": "unavailable", "available": False, "failures": ["adapter_dir_missing"]}, None
    config_path = adapter_dir / "adapter_config.json"
    model_path = _adapter_model_path(adapter_dir)
    failures: list[str] = []
    config: dict[str, Any] = {}
    config_hash = None
    model_hash = None
    if not config_path.exists():
        failures.append("adapter_config_missing")
    else:
        config_hash = _sha256_file(config_path)
        try:
            config = read_json(config_path)
        except ValueError:
            failures.append("adapter_config_invalid_json")
        if config_hash != expected["adapter_config_hash"]:
            failures.append("adapter_config_hash_mismatch")
    if model_path is None:
        failures.append("adapter_model_missing")
    else:
        model_hash = _sha256_file(model_path)
        if model_hash != expected["adapter_model_hash"]:
            failures.append("adapter_model_hash_mismatch")
    status = "verified" if not failures else "identity_mismatch"
    return (
        base
        | {
            "identity_status": status,
            "available": True,
            "failures": failures,
            "adapter_config_hash": config_hash,
            "adapter_model_hash": model_hash,
            "adapter_model_filename": model_path.name if model_path is not None else None,
            "config_fields": _sanitized_config_fields(config),
        },
        adapter_dir if status == "verified" else None,
    )


def verify_adapter_identities(
    *,
    env: Mapping[str, str] | None = None,
    override_path: Path | None = None,
    expected_adapters: dict[str, dict[str, str]] | None = None,
    include_private_paths: bool = False,
) -> dict[str, Any]:
    env_mapping = os.environ if env is None else env
    expected = expected_adapters or EXPECTED_ADAPTERS
    private_override_used = False
    override_unresolved = False
    locations: dict[str, str] = {}
    override_source = override_path
    if override_source is None and env_mapping.get(ENV_OVERRIDE_PATH):
        override_source = Path(str(env_mapping[ENV_OVERRIDE_PATH]))
    if override_source is not None:
        private_override_used = True
        if _path_value_is_unresolved(override_source.as_posix()) or not override_source.exists():
            override_unresolved = True
        else:
            try:
                locations = _override_locations(_override_payload(override_source))
            except (OSError, ValueError, json.JSONDecodeError):
                override_unresolved = True
    if not locations:
        locations = _env_locations(env_mapping)
    adapters: list[dict[str, Any]] = []
    verified_paths: dict[str, Path] = {}
    if override_unresolved:
        for role in ("control", "treatment"):
            adapters.append(
                {
                    "role": role,
                    "run_id": expected[role]["run_id"],
                    "manifest_id": expected[role]["manifest_id"],
                    "identity_status": "unresolved_override",
                    "available": False,
                    "private_path_recorded": False,
                    "failures": ["private_override_unresolved"],
                }
            )
    else:
        for role in ("control", "treatment"):
            item, verified_path = _verify_one_adapter(role, locations.get(role), expected[role])
            adapters.append(item)
            if verified_path is not None:
                verified_paths[role] = verified_path
    statuses = {str(item["identity_status"]) for item in adapters}
    if "unresolved_override" in statuses:
        overall = "unresolved_override"
        decision = DECISION_ADAPTER_UNAVAILABLE
    elif "unavailable" in statuses:
        overall = "unavailable"
        decision = DECISION_ADAPTER_UNAVAILABLE
    elif "identity_mismatch" in statuses:
        overall = "identity_mismatch"
        decision = DECISION_ADAPTER_IDENTITY
    else:
        overall = "verified"
        decision = None
    audit = {
        "audit_kind": "recovered_adapter_identity_audit",
        "overall_status": overall,
        "decision": decision,
        "private_override_used": private_override_used,
        "private_override_path_recorded": False,
        "adapters": adapters,
    }
    if include_private_paths:
        audit["_verified_adapter_paths"] = {role: path.as_posix() for role, path in verified_paths.items()}
        return audit
    return _sanitize_value(audit)


def _public_identity_audit(identity: dict[str, Any]) -> dict[str, Any]:
    public = {key: value for key, value in identity.items() if key != "_verified_adapter_paths"}
    return _sanitize_value(public)


def _prepare_output_dir(output_dir: Path) -> None:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)


def _write_markdown_summary(path: Path, summary: dict[str, Any]) -> None:
    lines = [
        "# Recovered Adapter Challenge Evaluation",
        "",
        f"- Decision: `{summary['decision_label']}`",
        f"- Challenge: `{summary['challenge_id']}`",
        f"- Challenge hash: `{summary['challenge_hash']}`",
        f"- Policy hash: `{summary['policy_hash']}`",
        f"- Canonical hook path: `{summary['canonical_prediction_hook_path']}`",
        f"- Adapter identity: `{summary['adapter_identity_status']}`",
        f"- Prediction attempted: `{summary['prediction_run_attempted']}`",
        "",
        (
            "Challenge v1 is a copy-shadow verifier adversarial fixture, not a naturalistic language "
            "benchmark or ASR generalization benchmark."
        ),
        "",
    ]
    if summary.get("blocked_reason"):
        lines.append(f"Blocked reason: `{summary['blocked_reason']}`")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def _blocked_payload(decision: str, reason: str) -> dict[str, Any]:
    return {
        "decision": decision,
        "reason": reason,
        "fabricated_predictions": False,
        "training_run": False,
        "challenge_modified": False,
        "policy_modified": False,
        "prediction_run_attempted": False,
        "canonical_prediction_hook_evaluated": False,
        "private_paths_recorded": False,
    }


def _base_summary(
    boundary: dict[str, Any],
    identity: dict[str, Any],
    *,
    decision: str,
    blocked_reason: str | None,
) -> dict[str, Any]:
    return {
        "evidence_kind": "recovered_adapter_copy_shadow_template_disjoint_challenge_v1",
        "change_id": CHANGE_ID,
        "decision_label": decision,
        "blocked_reason": blocked_reason,
        "created_at": _utc_now(),
        "challenge_id": CHALLENGE_ID,
        "challenge_version": CHALLENGE_VERSION,
        "challenge_hash": boundary.get("challenge_hash"),
        "row_count": boundary.get("row_count"),
        "gold_hash": boundary.get("gold_hash"),
        "policy_hash": boundary.get("policy_hash"),
        "canonical_prediction_entrypoint": (
            "voice2task-train sft-predict / voice2task.training.run_sft_prediction_export"
        ),
        "canonical_prediction_hook_path": CANONICAL_HOOK_PATH,
        "challenge_v1_boundary": "copy-shadow verifier adversarial fixture; not a naturalistic language benchmark",
        "adapter_identity_status": identity.get("overall_status"),
        "adapter_identity_method": "adapter_config_sha256_and_adapter_model_sha256_match_expected_public_hashes",
        "adapter_identity_claim_limit": (
            "content-hash identity only; no adapter release, no checkpoint release, and no public no-overwrite claim"
        ),
        "private_override_used": bool(identity.get("private_override_used")),
        "private_paths_recorded": False,
        "canonical_prediction_hook_evaluated": False,
        "prediction_run_attempted": False,
        "prediction_runs": [],
        "cannot_claim": [
            "natural-language generalization",
            "speech or ASR generalization",
            "model quality improvement",
            "slot accuracy improvement",
            "runtime enforcement safety",
            "production readiness",
            "safety readiness",
        ],
    }


def _write_blocked(
    output_dir: Path,
    *,
    boundary: dict[str, Any],
    identity: dict[str, Any],
    decision: str,
    reason: str,
) -> dict[str, Any]:
    summary = _base_summary(boundary, identity, decision=decision, blocked_reason=reason)
    write_json(output_dir / "boundary-audit.json", _sanitize_value(boundary))
    write_json(output_dir / "adapter-identity-audit.json", _public_identity_audit(identity))
    write_json(output_dir / "blocked.json", _blocked_payload(decision, reason))
    write_json(output_dir / "challenge-evaluation-summary.json", _sanitize_value(summary))
    _write_markdown_summary(output_dir / "challenge-evaluation-summary.md", summary)
    (output_dir / "recommended-next-change.md").write_text(
        "\n".join(
            [
                "# Recommended next step",
                "",
                "Resolve identity-verifiable frozen adapter availability, then rerun the same frozen challenge.",
                "Do not train a replacement adapter, change policy, change prompts, or enable runtime enforcement.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return summary


def _challenge_sft_rows(repo_root: Path) -> list[dict[str, Any]]:
    rows = read_jsonl(repo_root / DEFAULT_CHALLENGE_PATH)
    sft_rows: list[dict[str, Any]] = []
    for row in rows:
        contract = as_contract(row["gold_contract"]).to_dict()
        sft_rows.append(
            {
                "id": str(row["challenge_id"]),
                "split": "test",
                "input_text": str(row["input_text"]),
                "target_contract": contract,
                "provenance": {
                    "public_safe": True,
                    "source_id": str(row["challenge_id"]),
                    "challenge_version": CHALLENGE_VERSION,
                    "condition_tags": row.get("condition_tags", []),
                    "input_hash": row.get("input_hash"),
                    "target_contract_hash": stable_hash(canonical_contract_json(contract)),
                },
            }
        )
    return sft_rows


def _write_challenge_sft_manifest(repo_root: Path, output_dir: Path) -> Path:
    rows = _challenge_sft_rows(repo_root)
    sft_dir = output_dir / "challenge-sft"
    sft_path = sft_dir / "sft_public_sample.jsonl"
    manifest_path = sft_dir / "manifest.json"
    write_jsonl(sft_path, rows)
    write_json(
        manifest_path,
        {
            "manifest_id": "copy-shadow-template-disjoint-challenge-v1-adapter-evaluation",
            "files": {"sft": sft_path.name},
            "counts": {"sft_rows": len(rows)},
            "public_safe": True,
            "challenge_id": CHALLENGE_ID,
            "challenge_version": CHALLENGE_VERSION,
            "challenge_hash": EXPECTED_CHALLENGE_HASH,
        },
    )
    return manifest_path


def _prediction_config(
    *,
    role: str,
    adapter_path: Path,
    adapter_audit: dict[str, Any],
    mode: str,
    policy_path: Path,
    sidecar_path: Path | None,
) -> dict[str, Any]:
    config_fields = adapter_audit.get("config_fields", {})
    base_model = "Qwen/Qwen2.5-0.5B-Instruct"
    if isinstance(config_fields, dict) and isinstance(config_fields.get("base_model_id"), str):
        base_model = str(config_fields["base_model_id"])
    if base_model == "<private_path>":
        try:
            adapter_config = read_json(adapter_path / "adapter_config.json")
        except (OSError, ValueError):
            adapter_config = {}
        runtime_base_model = adapter_config.get("base_model_name_or_path") or adapter_config.get("base_model")
        if isinstance(runtime_base_model, str) and runtime_base_model:
            base_model = runtime_base_model
    payload: dict[str, Any] = {
        "base_model": base_model,
        "base_model_public_id": _sanitize_string(base_model),
        "model_source": "modelscope",
        "allow_private_prediction": True,
        "adapter_path": adapter_path.as_posix(),
        "prediction_split": "test",
        "adapter_role": role,
        "adapter_run_id": adapter_audit["run_id"],
        "adapter_manifest_id": adapter_audit["manifest_id"],
        "max_new_tokens": 256,
    }
    if mode != "disabled":
        payload["copy_backed_shadow"] = {
            "mode": mode,
            "enabled": True,
            "policy_path": policy_path.as_posix(),
            "sidecar_output_path": None if sidecar_path is None else sidecar_path.as_posix(),
            "retain_span_text": False,
            "retain_input_text": False,
            "retain_raw_model_output": False,
            "fail_isolated": True,
        }
    return payload


def _write_private_config(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _output_hash(path: Path) -> str | None:
    return _sha256_file(path) if path.exists() else None


def _rate(numerator: int, denominator: int) -> float | None:
    return None if denominator == 0 else numerator / denominator


def _read_jsonl_if_exists(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return read_jsonl(path)


def _challenge_rows_by_id(repo_root: Path) -> dict[str, dict[str, Any]]:
    return {str(row["challenge_id"]): row for row in read_jsonl(repo_root / DEFAULT_CHALLENGE_PATH)}


def _challenge_sft_dataset_rows(repo_root: Path) -> list[Any]:
    from voice2task.schemas import SFTDatasetRow

    return [SFTDatasetRow(**row) for row in _challenge_sft_rows(repo_root)]


def _prediction_contract_hash(value: Any) -> str | None:
    try:
        return stable_hash(canonical_contract_json(as_contract(value).to_dict()))
    except (TypeError, ValueError):
        return None


def _sidecar_prediction_hash(sidecar: dict[str, Any]) -> str | None:
    value = sidecar.get("prediction_hash", sidecar.get("prediction_contract_hash"))
    return str(value) if isinstance(value, str) and value else None


def _sidecar_for_false_accept_count(sidecar: dict[str, Any]) -> dict[str, Any]:
    cloned = json.loads(json.dumps(sidecar, ensure_ascii=False))
    for diagnostic in cloned.get("slot_diagnostics", []):
        if "status" not in diagnostic and "verification_status" in diagnostic:
            diagnostic["status"] = diagnostic["verification_status"]
    return cloned


def _sidecar_json_text(sidecar: dict[str, Any]) -> str:
    return json.dumps(sidecar, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sidecar_retains_span_text(sidecar: dict[str, Any]) -> bool:
    for diagnostic in sidecar.get("slot_diagnostics", []):
        span = diagnostic.get("source_span")
        if isinstance(span, dict) and "text" in span:
            return True
    return False


def _sidecar_has_private_value(sidecar: dict[str, Any]) -> bool:
    return _sanitize_string(_sidecar_json_text(sidecar)) != _sidecar_json_text(sidecar)


def _match_jsonl_sidecars(
    *,
    challenge_rows: dict[str, dict[str, Any]],
    predictions: dict[str, Any],
    sidecars: list[dict[str, Any]],
) -> tuple[list[tuple[str, dict[str, Any]]], int, int]:
    by_key: dict[tuple[str, str], list[str]] = defaultdict(list)
    invalid_prediction_count = 0
    for row_id, prediction in predictions.items():
        row = challenge_rows.get(row_id)
        prediction_hash = _prediction_contract_hash(prediction)
        if row is None or prediction_hash is None:
            invalid_prediction_count += 1
            continue
        by_key[(str(row["input_hash"]), prediction_hash)].append(row_id)

    matched: list[tuple[str, dict[str, Any]]] = []
    unmatched_count = 0
    for sidecar in sidecars:
        prediction_hash = _sidecar_prediction_hash(sidecar)
        if prediction_hash is None:
            unmatched_count += 1
            continue
        candidates = by_key.get((str(sidecar.get("input_hash")), prediction_hash), [])
        if len(candidates) != 1:
            unmatched_count += 1
            continue
        matched.append((candidates[0], sidecar))
    return matched, unmatched_count, invalid_prediction_count


def _diagnostic_status(diagnostic: dict[str, Any]) -> str:
    return str(diagnostic.get("verification_status", diagnostic.get("status", "")))


def _condition_tags(row: dict[str, Any]) -> list[str]:
    tags = row.get("condition_tags", [])
    return [str(tag) for tag in tags if isinstance(tag, str)]


def _primary_condition(row: dict[str, Any]) -> str:
    for tag in _condition_tags(row):
        if not tag.startswith("scope:") and not tag.startswith("negative_condition:"):
            return tag
    for tag in _condition_tags(row):
        if tag.startswith("negative_condition:"):
            return tag.removeprefix("negative_condition:")
    return "unknown"


def _empty_metric_bucket() -> dict[str, Any]:
    return {
        "observed_slot_event_count": 0,
        "trusted_exact_count": 0,
        "candidate_provenance_count": 0,
        "normalized_trusted_count": 0,
        "action_trusted_count": 0,
        "duplicate_source_false_trust_count": 0,
        "source_absent_false_trust_count": 0,
        "normalization_collision_false_trust_count": 0,
        "partial_span_false_trust_count": 0,
        "out_of_scope_action_false_trust_count": 0,
        "ambiguous_count": 0,
        "not_found_count": 0,
        "out_of_scope_count": 0,
        "trusted_gold_correct_count": 0,
        "trusted_gold_mismatch_count": 0,
    }


def _finalize_metric_bucket(bucket: dict[str, Any]) -> dict[str, Any]:
    trusted = int(bucket["trusted_exact_count"])
    observed = int(bucket["observed_slot_event_count"])
    bucket = dict(bucket)
    bucket["trusted_exact_rate"] = _rate(trusted, observed)
    bucket["candidate_provenance_rate"] = _rate(int(bucket["candidate_provenance_count"]), observed)
    bucket["trusted_gold_correct_rate"] = _rate(int(bucket["trusted_gold_correct_count"]), trusted)
    bucket["trusted_gold_mismatch_rate"] = _rate(int(bucket["trusted_gold_mismatch_count"]), trusted)
    return bucket


def _add_metric_event(
    bucket: dict[str, Any],
    *,
    row: dict[str, Any],
    diagnostic: dict[str, Any],
    audit: dict[str, Any] | None,
) -> None:
    status = _diagnostic_status(diagnostic)
    trusted = bool(diagnostic.get("trusted_provenance"))
    bucket["observed_slot_event_count"] += 1
    if trusted:
        bucket["trusted_exact_count"] += 1
    if bool(diagnostic.get("candidate_provenance")):
        bucket["candidate_provenance_count"] += 1
    if trusted and status == "VERIFIED_NORMALIZED_UNIQUE":
        bucket["normalized_trusted_count"] += 1
    if trusted and diagnostic.get("slot_path") == "action":
        bucket["action_trusted_count"] += 1
    if status == "AMBIGUOUS_MULTIPLE_MATCHES":
        bucket["ambiguous_count"] += 1
    if status == "NOT_FOUND":
        bucket["not_found_count"] += 1
    if status == "OUT_OF_SCOPE":
        bucket["out_of_scope_count"] += 1
    tags = set(_condition_tags(row))
    if trusted and "duplicate_exact" in tags:
        bucket["duplicate_source_false_trust_count"] += 1
    if trusted and "source_absent" in tags:
        bucket["source_absent_false_trust_count"] += 1
    if trusted and "normalization_collision" in tags:
        bucket["normalization_collision_false_trust_count"] += 1
    if trusted and "partial_span_trap" in tags:
        bucket["partial_span_false_trust_count"] += 1
    if trusted and "out_of_scope_action" in tags:
        bucket["out_of_scope_action_false_trust_count"] += 1
    if audit is not None and trusted:
        if audit.get("gold_correct_exact") is True:
            bucket["trusted_gold_correct_count"] += 1
        else:
            bucket["trusted_gold_mismatch_count"] += 1


def _build_evaluation_audit_payload(
    *,
    repo_root: Path,
    role: str,
    output_dir: Path,
) -> dict[str, Any]:
    challenge_rows = _challenge_rows_by_id(repo_root)
    policy = load_scope_policy(repo_root / DEFAULT_POLICY_PATH)
    jsonl_dir = output_dir / role / "jsonl_sink"
    sidecar_path = jsonl_dir / "online-copy-shadow-sidecars.jsonl"
    prediction_path = jsonl_dir / "predictions.jsonl"
    predictions = load_predictions(prediction_path) if prediction_path.exists() else {}
    sidecars = _read_jsonl_if_exists(sidecar_path)
    matched, unmatched_sidecar_count, invalid_prediction_count = _match_jsonl_sidecars(
        challenge_rows=challenge_rows,
        predictions=predictions,
        sidecars=sidecars,
    )
    audits: list[dict[str, Any]] = []
    rows_for_metrics: list[tuple[dict[str, Any], dict[str, Any], dict[str, Any] | None]] = []
    false_accept_count = 0
    for row_id, sidecar in matched:
        row = challenge_rows[row_id]
        prediction = predictions.get(row_id)
        if prediction is None:
            continue
        offline_sidecar = {
            **sidecar,
            "request_id": row_id,
            "sample_id": row_id,
            "split": "test",
            "run_role": role,
            "task_type": row["task_type"],
            "route": row["route"],
        }
        row_audits = build_evaluation_audits(
            _sidecar_for_false_accept_count(offline_sidecar),
            prediction,
            row["gold_contract"],
        )
        audits.extend(row_audits)
        audits_by_slot = {str(audit["slot_path"]): audit for audit in row_audits}
        false_accept_count += count_provenance_false_accepts(
            _sidecar_for_false_accept_count(offline_sidecar),
            str(row["input_text"]),
            policy,
        )
        for diagnostic in sidecar.get("slot_diagnostics", []):
            rows_for_metrics.append((row, diagnostic, audits_by_slot.get(str(diagnostic.get("slot_path")))))

    all_bucket = _empty_metric_bucket()
    per_scope: dict[str, dict[str, Any]] = defaultdict(_empty_metric_bucket)
    per_condition: dict[str, dict[str, Any]] = defaultdict(_empty_metric_bucket)
    for row, diagnostic, audit in rows_for_metrics:
        _add_metric_event(all_bucket, row=row, diagnostic=diagnostic, audit=audit)
        _add_metric_event(per_scope[str(diagnostic.get("scope_key"))], row=row, diagnostic=diagnostic, audit=audit)
        _add_metric_event(per_condition[_primary_condition(row)], row=row, diagnostic=diagnostic, audit=audit)

    sidecar_text = "\n".join(_sidecar_json_text(sidecar) for sidecar in sidecars)
    return {
        "role": role,
        "prediction_count": len(predictions),
        "jsonl_sidecar_count": len(sidecars),
        "matched_sidecar_count": len(matched),
        "unmatched_sidecar_count": unmatched_sidecar_count,
        "invalid_prediction_count": invalid_prediction_count,
        "evaluation_audit_count": len(audits),
        "evaluation_audits": audits,
        "online_sidecar_safety": {
            "online_sidecar_has_no_gold_fields": all(
                online_sidecar_has_no_gold_fields(sidecar) for sidecar in sidecars
            ),
            "full_input_text_retained": "input_text" in sidecar_text,
            "span_text_retained": any(_sidecar_retains_span_text(sidecar) for sidecar in sidecars),
            "raw_model_output_retained": "raw_model_output" in sidecar_text,
            "private_path_or_secret_detected": any(_sidecar_has_private_value(sidecar) for sidecar in sidecars),
        },
        "provenance_false_accept_count": false_accept_count,
        "metrics": _finalize_metric_bucket(all_bucket),
        "per_scope": {key: _finalize_metric_bucket(value) for key, value in sorted(per_scope.items())},
        "per_condition": {key: _finalize_metric_bucket(value) for key, value in sorted(per_condition.items())},
    }


def _prediction_invariance_for_role(repo_root: Path, output_dir: Path, role: str) -> dict[str, Any]:
    paths = {
        mode: output_dir / role / mode / "predictions.jsonl"
        for mode in ("disabled", "null_sink", "jsonl_sink")
    }
    hashes = {mode: _output_hash(path) for mode, path in paths.items()}
    predictions = {
        mode: load_predictions(path) if path.exists() else {}
        for mode, path in paths.items()
    }
    rows = _challenge_sft_dataset_rows(repo_root)
    metrics = {
        mode: evaluate_predictions(rows, prediction).metrics
        for mode, prediction in predictions.items()
    }
    return {
        "role": role,
        "prediction_output_hashes": hashes,
        "prediction_output_hashes_equal": len(set(hashes.values())) == 1 and None not in set(hashes.values()),
        "parsed_prediction_contracts_equal": (
            predictions["disabled"] == predictions["null_sink"] == predictions["jsonl_sink"]
        ),
        "evaluator_metrics": metrics,
        "evaluator_metrics_equal": metrics["disabled"] == metrics["null_sink"] == metrics["jsonl_sink"],
        "v1_metric_delta": {
            key: metrics["jsonl_sink"].get(key, 0.0) - metrics["disabled"].get(key, 0.0)
            for key in sorted(metrics["disabled"])
        },
        "v1_metric_delta_zero": all(
            metrics["jsonl_sink"].get(key, 0.0) - metrics["disabled"].get(key, 0.0) == 0
            for key in metrics["disabled"]
        ),
    }


def _latency_from_prediction_runs(prediction_runs: list[dict[str, Any]]) -> dict[str, Any]:
    elapsed = sorted(
        float(run["elapsed_ms"])
        for run in prediction_runs
        if isinstance(run.get("elapsed_ms"), (int, float))
    )
    return {
        "benchmark_kind": "adapter_prediction_export_wall_time_not_production_slo",
        "sample_count": len(elapsed),
        "p50_ms": elapsed[len(elapsed) // 2] if elapsed else None,
        "max_ms": max(elapsed) if elapsed else None,
        "total_ms": sum(elapsed),
        "production_slo_claim": False,
    }


def _recommended_next_change_text(decision: str) -> str:
    if decision == DECISION_HOOK_UNSAFE:
        return "\n".join(
            [
                "# diagnose-copy-shadow-false-trust-before-naturalistic-v2",
                "",
                "Challenge v1 found high-risk false-trust cases in adversarial fixture conditions.",
                (
                    "Do not recommend runtime enforcement, action provenance, normalized trusted provenance, or "
                    "challenge v2 until a separate OpenSpec change diagnoses and hardens these traps."
                ),
                "",
            ]
        )
    return "\n".join(
        [
            "# design-and-materialize-naturalistic-copy-shadow-challenge-v2",
            "",
            "Challenge v1 remains observe-only verifier fixture evidence. Do not recommend runtime enforcement.",
            "",
        ]
    )


def _challenge_manifest_public_path() -> str:
    return (DEFAULT_OUTPUT_DIR / "challenge-sft/manifest.json").as_posix()


def _rewrite_prediction_metadata_files(output_dir: Path) -> None:
    public_manifest_path = _challenge_manifest_public_path()
    for metadata_path in output_dir.glob("*/*/prediction_metadata.json"):
        try:
            metadata = read_json(metadata_path)
        except (OSError, ValueError):
            continue
        metadata["dataset_manifest_path"] = public_manifest_path
        metadata["challenge_manifest_path"] = public_manifest_path
        command = metadata.get("command_summary")
        if isinstance(command, dict):
            command["manifest"] = public_manifest_path
        write_json(metadata_path, _sanitize_value(metadata))


def _aggregate_metric_counts(payloads: list[dict[str, Any]]) -> dict[str, Any]:
    total = _empty_metric_bucket()
    for payload in payloads:
        metrics = payload.get("metrics", {})
        for key in total:
            value = metrics.get(key)
            if isinstance(value, int):
                total[key] += value
    return _finalize_metric_bucket(total)


def _run_verified_predictions(
    *,
    repo_root: Path,
    output_dir: Path,
    identity: dict[str, Any],
    manifest_path: Path,
    private_work_dir: Path,
    run_prediction_export: Callable[..., dict[str, Any]],
) -> list[dict[str, Any]]:
    verified_paths = {
        role: Path(path_text)
        for role, path_text in identity.get("_verified_adapter_paths", {}).items()
        if isinstance(path_text, str)
    }
    adapter_by_role = {
        str(item["role"]): item
        for item in identity.get("adapters", [])
        if isinstance(item, dict) and item.get("identity_status") == "verified"
    }
    runs: list[dict[str, Any]] = []
    for role in ("control", "treatment"):
        adapter_path = verified_paths[role]
        adapter_audit = adapter_by_role[role]
        for mode in ("disabled", "null_sink", "jsonl_sink"):
            mode_dir = output_dir / role / mode
            output_path = mode_dir / "predictions.jsonl"
            sidecar_path = mode_dir / "online-copy-shadow-sidecars.jsonl" if mode == "jsonl_sink" else None
            config = _prediction_config(
                role=role,
                adapter_path=adapter_path,
                adapter_audit=adapter_audit,
                mode=mode,
                policy_path=repo_root / DEFAULT_POLICY_PATH,
                sidecar_path=sidecar_path,
            )
            config_path = _write_private_config(private_work_dir / role / f"{mode}-prediction-config.json", config)
            started = time.perf_counter()
            metadata = run_prediction_export(
                config_path,
                manifest_path,
                output_path,
                dry_run=False,
                fixture_mode=False,
            )
            elapsed_ms = round((time.perf_counter() - started) * 1000.0, 6)
            runs.append(
                _sanitize_value(
                    {
                        "adapter_role": role,
                        "mode": mode,
                        "prediction_status": metadata.get("prediction_status"),
                        "prediction_count": metadata.get("prediction_count"),
                        "exit_status": "completed" if metadata.get("prediction_status") else "unknown",
                        "elapsed_ms": elapsed_ms,
                        "prediction_output_hash": _output_hash(output_path),
                        "prediction_output_path": f"{role}/{mode}/predictions.jsonl",
                        "sidecar_output_path": None
                        if sidecar_path is None
                        else f"{role}/{mode}/online-copy-shadow-sidecars.jsonl",
                        "copy_backed_shadow": metadata.get("copy_backed_shadow"),
                    }
                )
            )
    return runs


def _positive_count(mapping: Mapping[str, Any], key: str) -> bool:
    value = mapping.get(key)
    return isinstance(value, int) and value > 0


def _select_verified_decision(
    prediction_runs: list[dict[str, Any]],
    *,
    hook_safety: Mapping[str, Any],
    aggregate_metrics: Mapping[str, Any],
    prediction_invariance: Mapping[str, Any],
    sidecar_alignment: Mapping[str, Mapping[str, Any]],
) -> str:
    if len(prediction_runs) != 6:
        return DECISION_HOOK_UNSAFE
    if any(run.get("prediction_status") != "private_adapter_predictions_written" for run in prediction_runs):
        return DECISION_ADAPTER_UNAVAILABLE
    if any(run.get("exit_status") != "completed" for run in prediction_runs):
        return DECISION_HOOK_UNSAFE
    if any(run.get("prediction_count") != EXPECTED_ROW_COUNT for run in prediction_runs):
        return DECISION_HOOK_UNSAFE
    for role in ("control", "treatment"):
        hashes = {
            run.get("prediction_output_hash")
            for run in prediction_runs
            if run.get("adapter_role") == role
        }
        if len(hashes) != 1 or None in hashes:
            return DECISION_HOOK_UNSAFE
    if hook_safety.get("online_sidecar_has_no_gold_fields") is not True:
        return DECISION_HOOK_UNSAFE
    for key in (
        "full_input_text_retained",
        "span_text_retained",
        "raw_model_output_retained",
        "private_path_or_secret_detected",
    ):
        if hook_safety.get(key) is True:
            return DECISION_HOOK_UNSAFE
    for key in (
        "normalized_trusted_count",
        "action_trusted_count",
        "provenance_false_accept_count",
        "invalid_output_fail_isolated_count",
        "runtime_decision_delta_count",
        "contract_mutation_count",
    ):
        if _positive_count(hook_safety, key):
            return DECISION_HOOK_UNSAFE
    if any(_positive_count(aggregate_metrics, key) for key in HIGH_RISK_FALSE_TRUST_KEYS):
        return DECISION_HOOK_UNSAFE
    for alignment in sidecar_alignment.values():
        if _positive_count(alignment, "unmatched_sidecar_count") or _positive_count(
            alignment, "invalid_prediction_count"
        ):
            return DECISION_HOOK_UNSAFE
    for key in (
        "all_prediction_output_hashes_equal",
        "all_parsed_prediction_contracts_equal",
        "all_evaluator_metrics_equal",
        "all_v1_metric_delta_zero",
    ):
        if prediction_invariance.get(key) is not True:
            return DECISION_HOOK_UNSAFE
    return DECISION_OBSERVE_ONLY


def _write_verified_summary(
    output_dir: Path,
    *,
    repo_root: Path,
    boundary: dict[str, Any],
    identity: dict[str, Any],
    prediction_runs: list[dict[str, Any]],
) -> dict[str, Any]:
    stale_blocked = output_dir / "blocked.json"
    if stale_blocked.exists():
        stale_blocked.unlink()
    audit_payloads = [
        _build_evaluation_audit_payload(repo_root=repo_root, role=role, output_dir=output_dir)
        for role in ("control", "treatment")
    ]
    invariance = {
        role: _prediction_invariance_for_role(repo_root, output_dir, role)
        for role in ("control", "treatment")
    }
    all_evaluation_audits: list[dict[str, Any]] = []
    for payload in audit_payloads:
        all_evaluation_audits.extend(payload["evaluation_audits"])
    hook_safety = {
        "audit_kind": "recovered_adapter_challenge_hook_safety",
        "online_sidecar_has_no_gold_fields": all(
            payload["online_sidecar_safety"]["online_sidecar_has_no_gold_fields"] for payload in audit_payloads
        ),
        "full_input_text_retained": any(
            payload["online_sidecar_safety"]["full_input_text_retained"] for payload in audit_payloads
        ),
        "span_text_retained": any(payload["online_sidecar_safety"]["span_text_retained"] for payload in audit_payloads),
        "raw_model_output_retained": any(
            payload["online_sidecar_safety"]["raw_model_output_retained"] for payload in audit_payloads
        ),
        "private_path_or_secret_detected": any(
            payload["online_sidecar_safety"]["private_path_or_secret_detected"] for payload in audit_payloads
        ),
        "normalized_trusted_count": sum(
            int(payload["metrics"]["normalized_trusted_count"]) for payload in audit_payloads
        ),
        "action_trusted_count": sum(int(payload["metrics"]["action_trusted_count"]) for payload in audit_payloads),
        "provenance_false_accept_count": sum(
            int(payload["provenance_false_accept_count"]) for payload in audit_payloads
        ),
        "invalid_output_fail_isolated_count": sum(
            int((run.get("copy_backed_shadow") or {}).get("exception_isolated_count", 0))
            for run in prediction_runs
            if run.get("mode") == "jsonl_sink"
        ),
        "main_prediction_unchanged_all": all(
            (run.get("copy_backed_shadow") or {}).get("main_prediction_unchanged", True) is True
            for run in prediction_runs
            if run.get("mode") != "disabled"
        ),
        "runtime_decision_delta_count": sum(
            int((run.get("copy_backed_shadow") or {}).get("runtime_decision_delta_count", 0))
            for run in prediction_runs
        ),
        "contract_mutation_count": sum(
            1
            for run in prediction_runs
            if (run.get("copy_backed_shadow") or {}).get("contract_mutated") is True
        ),
    }
    aggregate_metrics = _aggregate_metric_counts(audit_payloads)
    per_scope_metrics = {
        "metrics_kind": "recovered_adapter_challenge_per_scope_metrics",
        "roles": {payload["role"]: payload["per_scope"] for payload in audit_payloads},
    }
    per_condition_metrics = {
        "metrics_kind": "recovered_adapter_challenge_per_condition_metrics",
        "roles": {payload["role"]: payload["per_condition"] for payload in audit_payloads},
    }
    prediction_invariance = {
        "roles": invariance,
        "all_prediction_output_hashes_equal": all(
            item["prediction_output_hashes_equal"] for item in invariance.values()
        ),
        "all_parsed_prediction_contracts_equal": all(
            item["parsed_prediction_contracts_equal"] for item in invariance.values()
        ),
        "all_evaluator_metrics_equal": all(item["evaluator_metrics_equal"] for item in invariance.values()),
        "all_v1_metric_delta_zero": all(item["v1_metric_delta_zero"] for item in invariance.values()),
    }
    sidecar_alignment = {
        payload["role"]: {
            "prediction_count": payload["prediction_count"],
            "jsonl_sidecar_count": payload["jsonl_sidecar_count"],
            "matched_sidecar_count": payload["matched_sidecar_count"],
            "unmatched_sidecar_count": payload["unmatched_sidecar_count"],
            "invalid_prediction_count": payload["invalid_prediction_count"],
        }
        for payload in audit_payloads
    }
    decision = _select_verified_decision(
        prediction_runs,
        hook_safety=hook_safety,
        aggregate_metrics=aggregate_metrics,
        prediction_invariance=prediction_invariance,
        sidecar_alignment=sidecar_alignment,
    )
    summary = _base_summary(boundary, identity, decision=decision, blocked_reason=None)
    summary["canonical_prediction_hook_evaluated"] = True
    summary["prediction_run_attempted"] = True
    summary["prediction_runs"] = prediction_runs
    summary["evaluation_audit_count"] = len(all_evaluation_audits)
    summary["sidecar_alignment"] = sidecar_alignment
    summary["technical_gate_counts"] = {
        "hook_invocation_count": sum(
            int((run.get("copy_backed_shadow") or {}).get("hook_invocation_count", 0))
            for run in prediction_runs
        ),
        "sidecar_attachment_count": sum(int(payload["jsonl_sidecar_count"]) for payload in audit_payloads),
        "sidecar_unmatched_count": sum(int(payload["unmatched_sidecar_count"]) for payload in audit_payloads),
        "policy_drift_count": sum(
            1
            for run in prediction_runs
            if (run.get("copy_backed_shadow") or {}).get("policy_drift_detected") is True
        ),
        "path_conflict_count": sum(
            int((run.get("copy_backed_shadow") or {}).get("path_conflict_count", 0))
            for run in prediction_runs
        ),
        "contract_mutation_count": hook_safety["contract_mutation_count"],
        "runtime_decision_delta_count": hook_safety["runtime_decision_delta_count"],
        "prediction_output_hash_mismatch_count": sum(
            0 if item["prediction_output_hashes_equal"] else 1 for item in invariance.values()
        ),
        "provenance_false_accept_count": hook_safety["provenance_false_accept_count"],
        "action_trusted_count": hook_safety["action_trusted_count"],
        "normalized_trusted_count": hook_safety["normalized_trusted_count"],
        "invalid_output_fail_isolated_count": hook_safety["invalid_output_fail_isolated_count"],
    }
    summary["pipeline_integrity"] = {
        "prediction_output_invariance_proven": prediction_invariance["all_prediction_output_hashes_equal"],
        "parsed_contract_invariance_proven": prediction_invariance["all_parsed_prediction_contracts_equal"],
        "evaluator_input_invariance_proven": prediction_invariance["all_evaluator_metrics_equal"],
        "runtime_decision_invariance_proven": hook_safety["runtime_decision_delta_count"] == 0,
        "v1_metric_delta_zero": prediction_invariance["all_v1_metric_delta_zero"],
        "sidecar_path_invariance_proven": summary["technical_gate_counts"]["path_conflict_count"] == 0,
    }
    summary["observed_metrics"] = aggregate_metrics
    summary["output_invariance"] = {
        role: {
            "hashes_equal": invariance[role]["prediction_output_hashes_equal"],
            "parsed_prediction_contracts_equal": invariance[role]["parsed_prediction_contracts_equal"],
            "evaluator_metrics_equal": invariance[role]["evaluator_metrics_equal"],
            "v1_metric_delta_zero": invariance[role]["v1_metric_delta_zero"],
        }
        for role in ("control", "treatment")
    }
    summary["public_leak_scan_clean"] = scan_paths([output_dir]).ok
    write_json(output_dir / "boundary-audit.json", _sanitize_value(boundary))
    write_json(output_dir / "adapter-identity-audit.json", _public_identity_audit(identity))
    write_json(output_dir / "prediction-run-audit.json", _sanitize_value({"prediction_runs": prediction_runs}))
    write_json(output_dir / "hook-safety-audit.json", _sanitize_value(hook_safety))
    write_json(output_dir / "per-scope-metrics.json", _sanitize_value(per_scope_metrics))
    write_json(output_dir / "per-condition-metrics.json", _sanitize_value(per_condition_metrics))
    write_json(output_dir / "latency-benchmark.json", _sanitize_value(_latency_from_prediction_runs(prediction_runs)))
    write_jsonl(output_dir / EVALUATION_AUDITS_FILENAME, _sanitize_value(all_evaluation_audits))
    _rewrite_prediction_metadata_files(output_dir)
    write_json(output_dir / "challenge-evaluation-summary.json", _sanitize_value(summary))
    _write_markdown_summary(output_dir / "challenge-evaluation-summary.md", summary)
    (output_dir / "recommended-next-change.md").write_text(_recommended_next_change_text(decision), encoding="utf-8")
    return _sanitize_value(summary)


def write_reports(
    *,
    repo_root: Path,
    output_dir: Path,
    env: Mapping[str, str] | None = None,
    override_path: Path | None = None,
    expected_challenge_hash: str = EXPECTED_CHALLENGE_HASH,
    expected_policy_hash: str = EXPECTED_POLICY_HASH,
    expected_adapters: dict[str, dict[str, str]] | None = None,
    private_work_dir: Path | None = None,
    run_prediction_export: Callable[..., dict[str, Any]] = run_sft_prediction_export,
) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    output_dir = output_dir if output_dir.is_absolute() else repo_root / output_dir
    _prepare_output_dir(output_dir)
    boundary = audit_frozen_boundary(
        repo_root,
        expected_challenge_hash=expected_challenge_hash,
        expected_policy_hash=expected_policy_hash,
    )
    if boundary["ok"] is not True:
        identity = {
            "audit_kind": "recovered_adapter_identity_audit",
            "overall_status": "not_evaluated_boundary_mismatch",
            "decision": None,
            "private_override_used": bool(override_path),
            "private_override_path_recorded": False,
            "adapters": [],
        }
        return _write_blocked(
            output_dir,
            boundary=boundary,
            identity=identity,
            decision=DECISION_BOUNDARY_MISMATCH,
            reason="frozen_boundary_mismatch",
        )
    identity = verify_adapter_identities(
        env=env,
        override_path=override_path,
        expected_adapters=expected_adapters,
        include_private_paths=True,
    )
    if identity.get("decision"):
        return _write_blocked(
            output_dir,
            boundary=boundary,
            identity=identity,
            decision=str(identity["decision"]),
            reason=str(identity["overall_status"]),
        )
    manifest_path = _write_challenge_sft_manifest(repo_root, output_dir)
    if private_work_dir is not None:
        private_work_dir.mkdir(parents=True, exist_ok=True)
        prediction_runs = _run_verified_predictions(
            repo_root=repo_root,
            output_dir=output_dir,
            identity=identity,
            manifest_path=manifest_path,
            private_work_dir=private_work_dir,
            run_prediction_export=run_prediction_export,
        )
    else:
        with tempfile.TemporaryDirectory(prefix="recovered-adapter-challenge-") as tmp:
            prediction_runs = _run_verified_predictions(
                repo_root=repo_root,
                output_dir=output_dir,
                identity=identity,
                manifest_path=manifest_path,
                private_work_dir=Path(tmp),
                run_prediction_export=run_prediction_export,
            )
    return _write_verified_summary(
        output_dir,
        repo_root=repo_root,
        boundary=boundary,
        identity=identity,
        prediction_runs=prediction_runs,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Run recovered frozen adapter challenge evaluation.")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--override-json", type=Path, default=None)
    parser.add_argument("--private-work-dir", type=Path, default=None)
    args = parser.parse_args()
    summary = write_reports(
        repo_root=args.repo_root,
        output_dir=args.output_dir,
        override_path=args.override_json,
        private_work_dir=args.private_work_dir,
    )
    print(json.dumps({"ok": True, "decision_label": summary["decision_label"]}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
