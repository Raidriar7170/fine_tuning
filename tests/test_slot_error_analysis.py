from __future__ import annotations

import json
from pathlib import Path

from voice2task.leak_scan import scan_paths
from voice2task.slot_error_analysis import (
    MISSING,
    classify_prediction_provenance,
    classify_slot_pair,
    classify_source_support,
    compare_paired_slot_outcomes,
    flatten_slot_values,
    generate_slot_error_mechanism_analysis,
    validate_slot_analysis_inputs,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_INPUTS = REPO_ROOT / "reports/public-sample/step-matched-canonical-slot-ablation/raw-inputs"
ANALYSIS_DIR = REPO_ROOT / "reports/public-sample/slot-error-mechanism-analysis"


def _read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def test_recovered_slot_analysis_boundary_accepts_only_metric_reproduced_inputs() -> None:
    boundary = validate_slot_analysis_inputs(RAW_INPUTS)

    assert boundary["decision_label"] == "SLOT_ANALYSIS_INPUT_BOUNDARY_PASSED"
    assert boundary["projection_inputs_ready"] is True
    assert boundary["metric_reproduction_status"] == "reproduced"
    assert boundary["control_treatment_ids_match"] is True
    assert boundary["gold_ids_match"] is True
    assert boundary["prediction_contract_used_for_analysis"] is True
    assert boundary["raw_model_output_used_for_analysis"] is False
    assert boundary["superseded_adapter_outputs_used"] is False
    assert boundary["splits"]["dev"]["row_count"] == 207
    assert boundary["splits"]["test"]["row_count"] == 207


def test_slot_flattening_and_same_path_alignment_are_stable() -> None:
    slots = {
        "query": "北京明天天气",
        "filters": {"date": "明天", "city": "北京"},
        "items": [{"name": "机票"}, {"name": "酒店"}],
    }

    assert flatten_slot_values(slots) == {
        "filters.city": "北京",
        "filters.date": "明天",
        "items[0].name": "机票",
        "items[1].name": "酒店",
        "query": "北京明天天气",
    }


def test_slot_pair_classifier_covers_exact_normalized_missing_extra_alias_and_partial_span() -> None:
    exact = classify_slot_pair(
        slot_path="query",
        gold_value="北京明天天气",
        predicted_value="北京明天天气",
        source_text="帮我搜索北京明天天气",
        task_type="search",
    )
    assert exact["primary_mechanism"] == "SLOT_CORRECT_EXACT"

    normalized = classify_slot_pair(
        slot_path="url",
        gold_value="https://example.com",
        predicted_value="Example.COM/",
        source_text="打开 example.com",
        task_type="navigate",
    )
    assert normalized["primary_mechanism"] == "SLOT_CORRECT_NORMALIZED"
    assert normalized["normalization_rule"] == "url_canonical"

    missing = classify_slot_pair(
        slot_path="field",
        gold_value="邮箱",
        predicted_value=MISSING,
        source_text="填写邮箱字段",
        task_type="form_fill",
    )
    assert missing["primary_mechanism"] == "MISSING_SLOT_KEY"

    extra = classify_slot_pair(
        slot_path="city",
        gold_value=MISSING,
        predicted_value="北京",
        source_text="搜索北京天气",
        task_type="search",
    )
    assert extra["primary_mechanism"] == "EXTRA_SLOT_KEY"

    alias = classify_slot_pair(
        slot_path="query",
        gold_value="苏州园林门票",
        predicted_value=MISSING,
        source_text="搜苏州园林门票信息",
        task_type="search",
        alias_key_candidate="search_text",
        alias_value="苏州园林门票",
    )
    assert alias["primary_mechanism"] == "WRONG_SLOT_KEY_ALIAS"
    assert alias["alias_key_candidate"] == "search_text"

    partial = classify_slot_pair(
        slot_path="query",
        gold_value="南京今天空气质量",
        predicted_value="南京空气质量",
        source_text="帮我搜南京今天空气质量",
        task_type="search",
    )
    assert partial["primary_mechanism"] == "PARTIAL_VALUE_SPAN"


def test_slot_pair_classifier_reaches_promised_taxonomy_labels_deterministically() -> None:
    semantic_key = classify_slot_pair(
        slot_path="query",
        gold_value="苏州园林门票",
        predicted_value=MISSING,
        source_text="帮我搜苏州园林门票",
        task_type="search",
        semantic_key_candidate="search_phrase",
        semantic_value="苏州园林门票",
    )
    assert semantic_key["primary_mechanism"] == "WRONG_SLOT_KEY_SEMANTIC"
    assert semantic_key["semantic_key_candidate"] == "search_phrase"

    normalization = classify_slot_pair(
        slot_path="date",
        gold_value="2026-06-21",
        predicted_value="2026-06-22",
        source_text="订 2026年6月21日 的票",
        task_type="form_fill",
    )
    assert normalization["primary_mechanism"] == "NORMALIZATION_FAILURE"
    assert normalization["normalization_rule"] == "date_iso"

    unclassified = classify_slot_pair(
        slot_path="query",
        gold_value="北京天气",
        predicted_value="",
        source_text="搜索北京天气",
        task_type="search",
    )
    assert unclassified["primary_mechanism"] == "UNCLASSIFIED_SLOT_FAILURE"


def test_source_support_prediction_provenance_and_typed_derivation_are_bounded() -> None:
    exact = classify_source_support("成都博物馆开放时间", "查成都博物馆开放时间", slot_path="query")
    assert exact["category"] == "exact_source_supported"

    normalized = classify_source_support("https://example.com", "打开 example.com", slot_path="url")
    assert normalized["category"] == "normalized_source_supported"
    assert normalized["rule"] == "url_canonical"

    typed = classify_source_support("2026-06-21", "订 2026年6月21日 的票", slot_path="date")
    assert typed["category"] == "typed_derivable"
    assert typed["rule"] == "date_iso"

    absent = classify_source_support("目标不明确，未指定具体页面", "帮我打开那个页面", slot_path="ambiguity")
    assert absent["category"] == "source_absent_or_generation_required"

    prediction = classify_prediction_provenance("北京空气", "帮我搜北京今天空气质量", slot_path="query")
    assert prediction["category"] == "partial_span_from_source"

    unsupported = classify_prediction_provenance({"nested": "value"}, "输入", slot_path="object")
    assert unsupported["category"] == "non_string_or_complex"


def test_paired_slot_outcome_labels_persistent_recovered_and_introduced_errors() -> None:
    control_wrong = classify_slot_pair(
        slot_path="query",
        gold_value="北京明天天气",
        predicted_value="上海明天天气",
        source_text="搜索北京明天天气",
        task_type="search",
    )
    treatment_right = classify_slot_pair(
        slot_path="query",
        gold_value="北京明天天气",
        predicted_value="北京明天天气",
        source_text="搜索北京明天天气",
        task_type="search",
    )
    assert compare_paired_slot_outcomes(control_wrong, treatment_right)["movement"] == "RECOVERED_BY_TREATMENT"

    introduced = compare_paired_slot_outcomes(treatment_right, control_wrong)
    assert introduced["movement"] == "INTRODUCED_BY_TREATMENT"

    persistent = compare_paired_slot_outcomes(control_wrong, control_wrong)
    assert persistent["movement"] == "ERROR_IN_BOTH_SAME_MECHANISM"

    missing = classify_slot_pair(
        slot_path="query",
        gold_value="北京明天天气",
        predicted_value=MISSING,
        source_text="搜索北京明天天气",
        task_type="search",
    )
    different_wrong = compare_paired_slot_outcomes(missing, control_wrong)
    assert different_wrong["movement"] == "ERROR_IN_BOTH_DIFFERENT_MECHANISM"


def test_report_generation_is_reproducible_public_safe_and_does_not_mutate_inputs(tmp_path: Path) -> None:
    before_manifest = (RAW_INPUTS / "artifact-manifest.json").read_bytes()
    before_prediction = (RAW_INPUTS / "control/dev_predictions.jsonl").read_bytes()

    first = generate_slot_error_mechanism_analysis(RAW_INPUTS, tmp_path / "first")
    second = generate_slot_error_mechanism_analysis(RAW_INPUTS, tmp_path / "second")

    assert first["decision_label"] in {
        "COPY_OR_NORMALIZE_REPRESENTATION_JUSTIFIED",
        "TASK_SLOT_SCHEMA_CONSTRAINTS_FIRST",
        "TYPED_NORMALIZATION_FIRST",
        "MIXED_SLOT_REPRESENTATION_REQUIRED",
        "DATA_DIVERSITY_OR_GENERALIZATION_FIRST",
        "ANALYSIS_BLOCKED_OR_INCONCLUSIVE",
    }
    assert first == second
    assert first["claims"]["training_performed"] is False
    assert first["claims"]["prediction_rerun_performed"] is False
    assert first["claims"]["evaluator_relaxation_performed"] is False
    assert first["source_boundary"]["projection_inputs_ready"] is True
    assert first["summary_metrics"]["gold_exact_or_normalized_source_copyable_rate"] >= 0
    assert first["summary_metrics"]["prediction_unsupported_by_source_rate"] >= 0
    assert first["summary_metric_denominators"]["missing_slot_key_rate"] == "mechanism_events"
    assert first["summary_metric_denominators"]["extra_slot_key_rate"] == "mechanism_events"
    assert first["heuristics"]["partial_span"]["minimum_folded_length"] == 2

    gold_breakdowns = first["source_support_breakdowns"]["gold_values"]
    assert gold_breakdowns["denominator_name"] == "gold_slot_events"
    assert set(gold_breakdowns["by_split"]) == {"dev", "test"}
    assert "search" in gold_breakdowns["by_task_type"]
    assert "search_web" in gold_breakdowns["by_route"]
    assert "query" in gold_breakdowns["by_slot_path"]

    prediction_breakdowns = first["source_support_breakdowns"]["predicted_values"]
    assert prediction_breakdowns["denominator_name"] == "prediction_slot_events"
    assert set(prediction_breakdowns["by_run_role"]) == {"control", "treatment"}
    assert set(prediction_breakdowns["by_split"]) == {"dev", "test"}
    assert "search" in prediction_breakdowns["by_task_type"]
    assert "search_web" in prediction_breakdowns["by_route"]
    assert "query" in prediction_breakdowns["by_slot_path"]

    paired = _read_json(tmp_path / "first" / "paired-error-movement.json")
    assert paired["top_persistent_mechanisms"]
    assert paired["top_introduced_mechanisms"]

    required = {
        "summary.md",
        "summary.json",
        "slot-error-taxonomy.md",
        "slot-profile.json",
        "paired-error-movement.json",
        "representation-feasibility.json",
        "recommended-next-change.md",
    }
    assert {path.name for path in (tmp_path / "first").iterdir()} == required
    assert not (tmp_path / "first" / "blocked.json").exists()
    assert scan_paths([tmp_path / "first"]).ok
    assert (RAW_INPUTS / "artifact-manifest.json").read_bytes() == before_manifest
    assert (RAW_INPUTS / "control/dev_predictions.jsonl").read_bytes() == before_prediction


def test_committed_slot_error_report_contract_is_current_public_safe_and_bounded() -> None:
    summary = _read_json(ANALYSIS_DIR / "summary.json")

    assert summary["evidence_kind"] == "slot_error_mechanism_analysis"
    assert summary["source_boundary"]["prediction_contract_used_for_analysis"] is True
    assert summary["source_boundary"]["raw_model_output_used_for_analysis"] is False
    assert summary["claims"]["training_performed"] is False
    assert summary["claims"]["prediction_repair_performed"] is False
    assert summary["claims"]["browser_task_contract_v1_changed"] is False
    assert summary["claims"]["contract_core_v2_changed"] is False
    assert summary["claims"]["slot_representation_implemented"] is False
    assert summary["source_support_breakdowns"]["gold_values"]["by_split"]
    assert summary["source_support_breakdowns"]["predicted_values"]["by_run_role"]
    assert summary["summary_metric_denominators"]["missing_slot_key_rate"] == "mechanism_events"
    assert summary["recommended_next_change"]["change_id"]
    assert scan_paths([ANALYSIS_DIR, REPO_ROOT / "docs/slot-representation.md"]).ok
