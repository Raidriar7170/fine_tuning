from __future__ import annotations

import json
from pathlib import Path

import pytest

from voice2task.schemas import BrowserTaskContract, canonical_contract_json

REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_INPUTS = REPO_ROOT / "reports/public-sample/step-matched-canonical-slot-ablation/raw-inputs"


def _contract(
    *,
    task_type: str = "search",
    route: str = "search_web",
    slots: dict[str, object] | None = None,
    normalized_command: str = "搜索北京明天天气",
    allow: bool = True,
    reason: str = "public_readonly",
    confirmation_required: bool = False,
    language: str = "zh-CN",
    contract_version: str = "v1",
) -> dict[str, object]:
    return {
        "task_type": task_type,
        "route": route,
        "safety": {"allow": allow, "reason": reason},
        "confirmation_required": confirmation_required,
        "slots": slots or {"query": "北京明天天气"},
        "normalized_command": normalized_command,
        "language": language,
        "contract_version": contract_version,
    }


def test_core_projection_contains_only_v1_core_fields_and_is_immutable() -> None:
    from voice2task.contract_core_v2 import (
        ContractCoreV2Error,
        project_v1_to_core_v2,
        validate_contract_core_v2,
    )

    original = _contract(slots={"query": "北京明天天气"})
    snapshot = json.loads(json.dumps(original, ensure_ascii=False))

    core = project_v1_to_core_v2(original)

    assert core.to_dict() == {
        "task_type": "search",
        "route": "search_web",
        "safety": {"allow": True, "reason": "public_readonly"},
        "confirmation_required": False,
        "slots": {"query": "北京明天天气"},
    }
    assert set(core.to_dict()) == {"task_type", "route", "safety", "confirmation_required", "slots"}
    assert "normalized_command" not in core.to_dict()
    assert "language" not in core.to_dict()
    assert "contract_version" not in core.to_dict()
    assert original == snapshot
    with pytest.raises(TypeError):
        core.slots["query"] = "上海天气"
    with pytest.raises(ContractCoreV2Error):
        validate_contract_core_v2({**core.to_dict(), "allowed_actions": ["click"]})
    with pytest.raises(ContractCoreV2Error):
        validate_contract_core_v2({**core.to_dict(), "safety": {"allow": True, "reason": "x", "extra": "kept"}})
    with pytest.raises(ContractCoreV2Error):
        project_v1_to_core_v2({**original, "normalized_command": ""})


def test_preserve_legacy_roundtrip_keeps_v1_canonical_json_and_internal_metadata_only() -> None:
    from voice2task.contract_core_v2 import (
        build_v1_compatible_envelope,
        compare_v1_roundtrip,
        extract_v1_envelope_metadata,
        project_v1_to_core_v2,
        roundtrip_v1_through_core,
    )

    original = _contract(
        task_type="form_fill",
        route="fill_form",
        slots={"field": "邮箱", "value": "qa@example.com"},
        normalized_command="填写邮箱并确认",
        reason="requires_confirmation",
        confirmation_required=True,
    )

    metadata = extract_v1_envelope_metadata(original)
    core = project_v1_to_core_v2(original)
    rebuilt = build_v1_compatible_envelope(core, metadata=metadata, mode="preserve_legacy")
    comparison = compare_v1_roundtrip(original, rebuilt)

    assert metadata.to_dict() == {
        "language": "zh-CN",
        "contract_version": "v1",
        "normalized_command": "填写邮箱并确认",
        "normalized_command_provenance": "legacy_preserved",
    }
    assert isinstance(rebuilt, BrowserTaskContract)
    assert canonical_contract_json(rebuilt) == canonical_contract_json(original)
    assert "normalized_command_provenance" not in rebuilt.to_dict()
    assert comparison["roundtrip_exact"] is True
    assert comparison["safety_preserved"] is True
    assert comparison["confirmation_preserved"] is True
    assert comparison["slots_preserved"] is True
    assert canonical_contract_json(roundtrip_v1_through_core(original)) == canonical_contract_json(original)


def test_derive_display_uses_existing_renderer_ignores_legacy_command_and_fails_closed() -> None:
    from voice2task.contract_core_v2 import (
        UnsupportedRendererError,
        build_v1_compatible_envelope,
        extract_v1_envelope_metadata,
        project_v1_to_core_v2,
    )

    original = _contract(slots={"query": "上海后天机票 300 元"}, normalized_command="旧命令不应被读取")
    metadata = extract_v1_envelope_metadata(original)
    core = project_v1_to_core_v2(original)

    first = build_v1_compatible_envelope(core, metadata=metadata, mode="derive_display")
    second = build_v1_compatible_envelope(core, metadata=metadata, mode="derive_display")

    assert first == second
    assert first.to_dict()["normalized_command"] == "搜索上海后天机票 300 元"
    assert first.to_dict()["language"] == "zh-CN"
    assert first.to_dict()["contract_version"] == "v1"

    unsupported = project_v1_to_core_v2(_contract(slots={"not_query": "北京"}))
    with pytest.raises(UnsupportedRendererError):
        build_v1_compatible_envelope(unsupported, metadata=metadata, mode="derive_display")


def test_shadow_compatibility_result_reports_preservation_and_does_not_mutate_input() -> None:
    from voice2task.contract_core_v2 import check_v1_core_compatibility

    original = _contract(
        task_type="blocked",
        route="deny",
        slots={"reason": "payment_requires_user_control"},
        normalized_command="拒绝代替用户付款",
        allow=False,
        reason="unsafe_payment",
        confirmation_required=True,
    )
    snapshot = json.loads(json.dumps(original, ensure_ascii=False))

    result = check_v1_core_compatibility(original)

    assert original == snapshot
    assert result == {
        "v1_valid": True,
        "core_valid": True,
        "roundtrip_exact": True,
        "safety_preserved": True,
        "confirmation_preserved": True,
        "slots_preserved": True,
        "normalized_command_preserved": True,
        "language_preserved": True,
        "contract_version_preserved": True,
        "failure_reason": None,
    }


def test_internal_contract_v2_core_report_preserves_v1_metrics_and_writes_compact_artifacts(tmp_path: Path) -> None:
    from voice2task.contract_core_v2 import generate_internal_contract_v2_core_report
    from voice2task.leak_scan import scan_paths

    output_dir = tmp_path / "custom-core-output"

    result = generate_internal_contract_v2_core_report(repo_root=REPO_ROOT, output_dir=output_dir)

    expected_files = {
        "summary.md",
        "summary.json",
        "compatibility-matrix.json",
        "evaluator-regression.json",
        "decision.md",
    }
    assert {path.name for path in output_dir.iterdir() if path.is_file()} == expected_files
    assert result["decision_label"] in {
        "INTERNAL_V2_CORE_READY_V1_COMPATIBLE",
        "INTERNAL_V2_CORE_READY_RENDERER_PARTIAL",
    }

    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))
    matrix = json.loads((output_dir / "compatibility-matrix.json").read_text(encoding="utf-8"))
    regression = json.loads((output_dir / "evaluator-regression.json").read_text(encoding="utf-8"))

    assert summary["default_external_schema"] == "BrowserTaskContract V1"
    assert summary["training_target_changed"] is False
    assert summary["downstream_runtime_changed"] is False
    assert matrix["preserve_roundtrip_exact_rate"] == 1.0
    assert matrix["safety_preservation_rate"] == 1.0
    assert matrix["confirmation_preservation_rate"] == 1.0
    assert matrix["slots_preservation_rate"] == 1.0
    assert matrix["total_contracts_checked"] > 1000
    assert matrix["execution_smoke_fixture_covered"] is True
    assert summary["report_artifacts"]["compatibility_matrix"] == "custom-core-output/compatibility-matrix.json"
    assert summary["report_artifacts"]["evaluator_regression"] == "custom-core-output/evaluator-regression.json"
    assert regression["passed"] is True
    assert all(metric["absolute_delta"] == 0 for metric in regression["metrics"].values())
    assert scan_paths([output_dir]).ok
