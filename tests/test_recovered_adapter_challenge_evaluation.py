from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any

from voice2task.copy_backed_shadow_interface import generate_online_shadow_sidecar

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts/run_recovered_adapter_challenge_evaluation.py"


def _load_script() -> Any:
    spec = importlib.util.spec_from_file_location("recovered_adapter_challenge", SCRIPT_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write_adapter(root: Path, *, role: str, config: dict[str, Any] | None = None, weights: bytes = b"adapter") -> Path:
    adapter_dir = root / role
    adapter_dir.mkdir(parents=True)
    payload = {
        "base_model_name_or_path": "Qwen/Qwen2.5-0.5B-Instruct",
        "peft_type": "LORA",
        "r": 8,
        "lora_alpha": 16,
        "lora_dropout": 0.05,
        "target_modules": ["q_proj", "v_proj"],
    }
    if config:
        payload.update(config)
    (adapter_dir / "adapter_config.json").write_text(
        json.dumps(payload, ensure_ascii=False, sort_keys=True),
        encoding="utf-8",
    )
    (adapter_dir / "adapter_model.safetensors").write_bytes(weights)
    return adapter_dir


def _expected_for(control: Path, treatment: Path) -> dict[str, dict[str, str]]:
    return {
        "control": {
            "run_id": "step-matched-canonical-slot-ablation-20260620T000000Z:control",
            "manifest_id": "public-sample-20260617T152259Z",
            "adapter_config_hash": module_sha256(control / "adapter_config.json"),
            "adapter_model_hash": module_sha256(control / "adapter_model.safetensors"),
        },
        "treatment": {
            "run_id": "step-matched-canonical-slot-ablation-20260620T000000Z:treatment",
            "manifest_id": "public-sample-20260619T090925Z",
            "adapter_config_hash": module_sha256(treatment / "adapter_config.json"),
            "adapter_model_hash": module_sha256(treatment / "adapter_model.safetensors"),
        },
    }


def module_sha256(path: Path) -> str:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()


def _override_file(tmp_path: Path, *, control: str | Path | None, treatment: str | Path | None) -> Path:
    payload: dict[str, str] = {}
    if control is not None:
        payload["control_adapter_path"] = control.as_posix() if isinstance(control, Path) else control
    if treatment is not None:
        payload["treatment_adapter_path"] = treatment.as_posix() if isinstance(treatment, Path) else treatment
    path = tmp_path / "private-override.json"
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return path


def _assert_no_private_path(value: Any, *needles: str) -> None:
    serialized = json.dumps(value, ensure_ascii=False, sort_keys=True)
    assert "/mnt/data/" not in serialized
    assert "/Users/" not in serialized
    assert "/tmp/" not in serialized
    assert "/private/" not in serialized
    for needle in needles:
        assert needle not in serialized


def test_frozen_boundary_passes_with_committed_challenge_and_policy_hashes() -> None:
    module = _load_script()

    audit = module.audit_frozen_boundary(REPO_ROOT)

    assert audit["ok"] is True
    assert audit["challenge_hash"] == "12eccdd54b2c89f1127ec23f18d7179e1ebaacb1a644ae5ca1a14b3309f11324"
    assert audit["challenge_manifest_hash"] == audit["challenge_hash"]
    assert audit["row_count"] == 120
    assert audit["policy_hash"] == "5dc14efb8ded13dc048ddb067c7c63a1a62b6c03896950e861303973d505cbc7"
    assert audit["policy_validation"]["action_enabled"] is False
    assert audit["policy_validation"]["normalized_trusted"] is False
    assert audit["template_disjoint_audit"]["accepted"] is True
    assert audit["active_change_boundary"]["ok"] is True
    assert audit["gold_hash"]


def test_boundary_mismatch_writes_blocked_artifact_without_running_inference(tmp_path: Path) -> None:
    module = _load_script()
    calls: list[tuple[Any, ...]] = []

    summary = module.write_reports(
        repo_root=REPO_ROOT,
        output_dir=tmp_path / "reports",
        expected_challenge_hash="bad-hash",
        run_prediction_export=lambda *args, **kwargs: calls.append(args),
    )

    blocked = json.loads((tmp_path / "reports/blocked.json").read_text(encoding="utf-8"))
    assert summary["decision_label"] == "CHALLENGE_EVALUATION_BLOCKED_BOUNDARY_MISMATCH"
    assert blocked["decision"] == "CHALLENGE_EVALUATION_BLOCKED_BOUNDARY_MISMATCH"
    assert blocked["fabricated_predictions"] is False
    assert blocked["training_run"] is False
    assert blocked["prediction_run_attempted"] is False
    assert calls == []


def test_adapter_identity_passes_with_private_override_without_leaking_paths(tmp_path: Path) -> None:
    module = _load_script()
    control = _write_adapter(tmp_path / "adapters", role="control", weights=b"control")
    treatment = _write_adapter(tmp_path / "adapters", role="treatment", weights=b"treatment")

    audit = module.verify_adapter_identities(
        override_path=_override_file(tmp_path, control=control, treatment=treatment),
        expected_adapters=_expected_for(control, treatment),
    )

    assert audit["overall_status"] == "verified"
    assert audit["decision"] is None
    assert audit["private_override_used"] is True
    assert {item["role"]: item["identity_status"] for item in audit["adapters"]} == {
        "control": "verified",
        "treatment": "verified",
    }
    _assert_no_private_path(audit, tmp_path.as_posix())


def test_adapter_identity_mismatch_blocks_without_private_path_leak(tmp_path: Path) -> None:
    module = _load_script()
    control = _write_adapter(tmp_path / "adapters", role="control", weights=b"control")
    treatment = _write_adapter(tmp_path / "adapters", role="treatment", weights=b"treatment")
    expected = _expected_for(control, treatment)
    expected["control"]["adapter_model_hash"] = "0" * 64

    audit = module.verify_adapter_identities(
        override_path=_override_file(tmp_path, control=control, treatment=treatment),
        expected_adapters=expected,
    )

    assert audit["overall_status"] == "identity_mismatch"
    assert audit["decision"] == "CHALLENGE_EVALUATION_BLOCKED_ADAPTER_IDENTITY"
    assert any("adapter_model_hash_mismatch" in item["failures"] for item in audit["adapters"])
    _assert_no_private_path(audit, tmp_path.as_posix())


def test_adapter_unavailable_and_unresolved_override_block(tmp_path: Path) -> None:
    module = _load_script()

    unavailable = module.verify_adapter_identities(env={}, override_path=None)
    unresolved = module.verify_adapter_identities(
        env={},
        override_path=_override_file(
            tmp_path,
            control="<a100_project_root>/control",
            treatment="<a100_project_root>/treatment",
        ),
    )

    assert unavailable["overall_status"] == "unavailable"
    assert unavailable["decision"] == "CHALLENGE_EVALUATION_BLOCKED_ADAPTER_UNAVAILABLE"
    assert unresolved["overall_status"] == "unresolved_override"
    assert unresolved["decision"] == "CHALLENGE_EVALUATION_BLOCKED_ADAPTER_UNAVAILABLE"
    _assert_no_private_path(unresolved)


def test_blocked_artifact_contract_for_missing_adapters(tmp_path: Path) -> None:
    module = _load_script()

    summary = module.write_reports(repo_root=REPO_ROOT, output_dir=tmp_path / "reports", env={})

    blocked = json.loads((tmp_path / "reports/blocked.json").read_text(encoding="utf-8"))
    identity = json.loads((tmp_path / "reports/adapter-identity-audit.json").read_text(encoding="utf-8"))
    report = json.loads((tmp_path / "reports/challenge-evaluation-summary.json").read_text(encoding="utf-8"))
    assert summary["decision_label"] == "CHALLENGE_EVALUATION_BLOCKED_ADAPTER_UNAVAILABLE"
    assert blocked["decision"] == "CHALLENGE_EVALUATION_BLOCKED_ADAPTER_UNAVAILABLE"
    assert blocked["fabricated_predictions"] is False
    assert blocked["training_run"] is False
    assert blocked["challenge_modified"] is False
    assert blocked["policy_modified"] is False
    assert blocked["prediction_run_attempted"] is False
    assert identity["overall_status"] == "unavailable"
    assert report["canonical_prediction_hook_evaluated"] is False
    assert not (tmp_path / "reports/control").exists()
    _assert_no_private_path(blocked)


def test_verified_adapters_run_canonical_export_in_disabled_null_and_jsonl_modes(tmp_path: Path) -> None:
    module = _load_script()
    private_base_model = tmp_path / "private-model"
    control = _write_adapter(
        tmp_path / "adapters",
        role="control",
        config={"base_model_name_or_path": private_base_model.as_posix()},
        weights=b"control",
    )
    treatment = _write_adapter(
        tmp_path / "adapters",
        role="treatment",
        config={"base_model_name_or_path": private_base_model.as_posix()},
        weights=b"treatment",
    )
    calls: list[dict[str, Any]] = []

    def fake_export(config_path: Path, manifest_path: Path, output_path: Path, **kwargs: Any) -> dict[str, Any]:
        config = json.loads(config_path.read_text(encoding="utf-8"))
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        rows_path = manifest_path.parent / manifest["files"]["sft"]
        rows = [json.loads(line) for line in rows_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            "\n".join(
                json.dumps(
                    {
                        "id": row["id"],
                        "prediction": row["target_contract"],
                        "prediction_source_kind": "private_a100_adapter",
                        "provenance": {"public_safe": True, "source_id": row["id"]},
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                )
                for row in rows
            )
            + "\n",
            encoding="utf-8",
        )
        (output_path.parent / "prediction_metadata.json").write_text(
            json.dumps(
                {
                    "dataset_manifest_id": manifest["challenge_id"],
                    "dataset_manifest_path": "data/public-samples/manifest_public_sample.json",
                    "command_summary": {"manifest": "data/public-samples/manifest_public_sample.json"},
                },
                ensure_ascii=False,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        metadata = {
            "prediction_status": "private_adapter_predictions_written",
            "prediction_count": manifest["counts"]["sft_rows"],
            "copy_backed_shadow": None,
        }
        if "copy_backed_shadow" in config:
            sidecar = config["copy_backed_shadow"].get("sidecar_output_path")
            if sidecar:
                policy = module.load_scope_policy(Path(config["copy_backed_shadow"]["policy_path"]))
                generated_sidecars = []
                for row in rows:
                    sidecar_payload = generate_online_shadow_sidecar(
                        row["input_text"],
                        row["target_contract"],
                        request_id=row["id"],
                        scope_policy=policy,
                        retain_request_id=False,
                    )
                    for diagnostic in sidecar_payload["slot_diagnostics"]:
                        diagnostic["verification_status"] = diagnostic.pop("status")
                    generated_sidecars.append(sidecar_payload)
                Path(sidecar).write_text(
                    "\n".join(
                        json.dumps(sidecar_payload, ensure_ascii=False, sort_keys=True)
                        for sidecar_payload in generated_sidecars
                    )
                    + "\n",
                    encoding="utf-8",
                )
            metadata["copy_backed_shadow"] = {
                "enabled": True,
                "sidecar_write_status": "written" if sidecar else "disabled",
                "main_prediction_unchanged": True,
                "hook_invocation_count": len(rows),
                "hook_status_counts": {"COMPLETED": len(rows)},
                "exception_isolated_count": 0,
                "path_conflict_count": 0,
                "contract_mutated": False,
                "runtime_decision_delta_count": 0,
                "policy_drift_detected": False,
            }
        calls.append(
            {
                "config": config,
                "manifest": manifest,
                "output_path": output_path,
                "kwargs": kwargs,
            }
        )
        return metadata

    report_dir = tmp_path / "reports"
    report_dir.mkdir()
    (report_dir / "blocked.json").write_text(
        json.dumps({"decision": "CHALLENGE_EVALUATION_BLOCKED_ADAPTER_UNAVAILABLE"}),
        encoding="utf-8",
    )

    summary = module.write_reports(
        repo_root=REPO_ROOT,
        output_dir=report_dir,
        override_path=_override_file(tmp_path, control=control, treatment=treatment),
        expected_adapters=_expected_for(control, treatment),
        run_prediction_export=fake_export,
    )

    assert summary["decision_label"] == "CHALLENGE_V1_VERIFIER_VALIDATED_OBSERVE_ONLY"
    assert len(calls) == 6
    assert {call["manifest"]["counts"]["sft_rows"] for call in calls} == {120}
    assert {tuple(sorted(call["kwargs"].items())) for call in calls} == {
        (("dry_run", False), ("fixture_mode", False))
    }
    modes = [
        (call["config"]["adapter_role"], call["config"]["copy_backed_shadow"]["mode"])
        for call in calls
        if "copy_backed_shadow" in call["config"]
    ]
    assert sorted(modes) == [
        ("control", "jsonl_sink"),
        ("control", "null_sink"),
        ("treatment", "jsonl_sink"),
        ("treatment", "null_sink"),
    ]
    disabled = [call["config"] for call in calls if "copy_backed_shadow" not in call["config"]]
    assert {item["adapter_role"] for item in disabled} == {"control", "treatment"}
    assert {call["config"]["base_model"] for call in calls} == {private_base_model.as_posix()}
    assert {call["config"]["base_model_public_id"] for call in calls} == {"<private_path>"}
    report_json = json.dumps(
        json.loads((report_dir / "challenge-evaluation-summary.json").read_text()),
        ensure_ascii=False,
    )
    summary = json.loads((report_dir / "challenge-evaluation-summary.json").read_text(encoding="utf-8"))
    hook_safety = json.loads((report_dir / "hook-safety-audit.json").read_text(encoding="utf-8"))
    per_scope = json.loads((report_dir / "per-scope-metrics.json").read_text(encoding="utf-8"))
    per_condition = json.loads((report_dir / "per-condition-metrics.json").read_text(encoding="utf-8"))
    rewritten_metadata = json.loads(
        (report_dir / "control/disabled/prediction_metadata.json").read_text(encoding="utf-8")
    )
    audits = [
        json.loads(line)
        for line in (report_dir / "evaluation-audits.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    sidecars = [
        json.loads(line)
        for line in (report_dir / "control/jsonl_sink/online-copy-shadow-sidecars.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
        if line.strip()
    ]
    assert not (report_dir / "blocked.json").exists()
    assert summary["pipeline_integrity"]["prediction_output_invariance_proven"] is True
    assert summary["pipeline_integrity"]["parsed_contract_invariance_proven"] is True
    assert summary["pipeline_integrity"]["evaluator_input_invariance_proven"] is True
    assert summary["pipeline_integrity"]["v1_metric_delta_zero"] is True
    assert summary["adapter_identity_method"] == (
        "adapter_config_sha256_and_adapter_model_sha256_match_expected_public_hashes"
    )
    assert summary["evaluation_audit_count"] == 240
    assert len(audits) == 240
    assert hook_safety["online_sidecar_has_no_gold_fields"] is True
    assert hook_safety["full_input_text_retained"] is False
    assert hook_safety["span_text_retained"] is False
    assert hook_safety["raw_model_output_retained"] is False
    assert hook_safety["private_path_or_secret_detected"] is False
    assert hook_safety["normalized_trusted_count"] == 0
    assert hook_safety["action_trusted_count"] == 0
    assert hook_safety["provenance_false_accept_count"] == 0
    assert "search:search_web:query" in per_scope["roles"]["control"]
    assert "exact_unique" in per_condition["roles"]["control"]
    assert all("gold" not in json.dumps(sidecar, ensure_ascii=False).lower() for sidecar in sidecars)
    assert all("input_text" not in json.dumps(sidecar, ensure_ascii=False) for sidecar in sidecars)
    assert rewritten_metadata["dataset_manifest_path"].endswith("/adapter-evaluation/challenge-sft/manifest.json")
    assert rewritten_metadata["command_summary"]["manifest"].endswith("/adapter-evaluation/challenge-sft/manifest.json")
    assert tmp_path.as_posix() not in report_json


def test_false_trust_counts_select_hook_unsafe_decision() -> None:
    module = _load_script()
    runs = [
        {
            "adapter_role": role,
            "mode": mode,
            "prediction_status": "private_adapter_predictions_written",
            "prediction_count": 120,
            "exit_status": "completed",
            "prediction_output_hash": role,
        }
        for role in ("control", "treatment")
        for mode in ("disabled", "null_sink", "jsonl_sink")
    ]
    hook_safety = {
        "online_sidecar_has_no_gold_fields": True,
        "full_input_text_retained": False,
        "span_text_retained": False,
        "raw_model_output_retained": False,
        "private_path_or_secret_detected": False,
        "normalized_trusted_count": 0,
        "action_trusted_count": 0,
        "provenance_false_accept_count": 0,
        "invalid_output_fail_isolated_count": 0,
        "runtime_decision_delta_count": 0,
        "contract_mutation_count": 0,
    }
    metrics = {key: 0 for key in module.HIGH_RISK_FALSE_TRUST_KEYS}
    invariance = {
        "all_prediction_output_hashes_equal": True,
        "all_parsed_prediction_contracts_equal": True,
        "all_evaluator_metrics_equal": True,
        "all_v1_metric_delta_zero": True,
    }
    alignment = {
        role: {"unmatched_sidecar_count": 0, "invalid_prediction_count": 0}
        for role in ("control", "treatment")
    }

    assert (
        module._select_verified_decision(
            runs,
            hook_safety=hook_safety,
            aggregate_metrics=metrics,
            prediction_invariance=invariance,
            sidecar_alignment=alignment,
        )
        == "CHALLENGE_V1_VERIFIER_VALIDATED_OBSERVE_ONLY"
    )
    metrics["source_absent_false_trust_count"] = 1

    assert (
        module._select_verified_decision(
            runs,
            hook_safety=hook_safety,
            aggregate_metrics=metrics,
            prediction_invariance=invariance,
            sidecar_alignment=alignment,
        )
        == "CHALLENGE_V1_HOOK_UNSAFE_OR_INVALID"
    )


def test_docs_label_challenge_v1_as_verifier_adversarial_fixture() -> None:
    text = (REPO_ROOT / "docs/copy-shadow-template-disjoint-challenge.md").read_text(encoding="utf-8")

    assert "copy-shadow verifier adversarial fixture" in text
    assert "not a naturalistic language benchmark" in text
