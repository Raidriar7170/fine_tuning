import json
from pathlib import Path

from voice2task import evaluation, reports
from voice2task.cli import eval as eval_cli
from voice2task.evaluation import (
    evaluate_predictions,
    prompt_fixture_predictions,
    rule_baseline_predictions,
    run_execution_smoke,
)
from voice2task.io import write_jsonl
from voice2task.reports import write_metrics_report
from voice2task.schemas import BrowserTaskContract, SFTDatasetRow


def _row(row_id: str, route: str, query: str) -> SFTDatasetRow:
    return SFTDatasetRow(
        id=row_id,
        split="test",
        input_text=f"帮我搜索{query}",
        target_contract=BrowserTaskContract(
            task_type="search",
            route=route,
            safety={"allow": True, "reason": "public_readonly"},
            confirmation_required=False,
            slots={"query": query},
            normalized_command=f"搜索{query}",
        ),
        provenance={"source_id": row_id, "public_safe": True},
    )


def test_evaluator_computes_contract_metrics_and_failure_slices() -> None:
    rows = [_row("gold-1", "search_web", "机票"), _row("gold-2", "search_web", "酒店")]
    predictions = {
        "gold-1": rows[0].target_contract.to_dict(),
        "gold-2": {
            **rows[1].target_contract.to_dict(),
            "route": "open_url",
            "slots": {"query": "民宿"},
        },
    }

    result = evaluate_predictions(rows, predictions)

    assert result.metrics["json_valid_rate"] == 1.0
    assert result.metrics["task_type_accuracy"] == 1.0
    assert result.metrics["route_accuracy"] == 0.5
    assert result.metrics["slot_f1"] < 1.0
    assert result.metrics["contract_exact_match"] == 0.5
    assert result.failure_slices["route"]["count"] == 1
    assert result.failure_slices["slot"]["examples"] == ["gold-2"]


def test_evaluator_rejects_predictions_missing_required_contract_fields() -> None:
    rows = [_row("gold-1", "search_web", "天气")]
    incomplete_prediction = {
        "task_type": "search",
        "route": "search_web",
        "safety": {"allow": True, "reason": "public_readonly"},
        "normalized_command": "搜索天气",
    }

    result = evaluate_predictions(rows, {"gold-1": incomplete_prediction})

    assert result.metrics["json_valid_rate"] == 0.0
    assert result.failure_slices["schema"]["count"] == 1


def test_schema_diagnostics_explain_contract_like_mismatches(tmp_path: Path) -> None:
    rows = [
        _row("missing-slots", "search_web", "天气"),
        _row("bad-task-type", "search_web", "机票"),
        _row("bad-route", "search_web", "酒店"),
        _row("slots-list", "search_web", "新闻"),
        _row("empty-safety-reason", "search_web", "地图"),
        _row("non-bool-safety-allow", "search_web", "日历"),
        _row("non-bool-confirmation", "search_web", "航班"),
        _row("bad-language", "search_web", "新闻"),
        _row("bad-contract-version", "search_web", "汇率"),
        _row("empty-normalized-command", "search_web", "翻译"),
        _row("non-string-normalized-command", "search_web", "汇率"),
    ]
    base = rows[0].target_contract.to_dict()
    predictions = {
        "missing-slots": {key: value for key, value in base.items() if key != "slots"},
        "bad-task-type": {**base, "task_type": "browser_task"},
        "bad-route": {**base, "route": "search"},
        "slots-list": {**base, "slots": ["query", "新闻"]},
        "empty-safety-reason": {**base, "safety": {"allow": True, "reason": ""}},
        "non-bool-safety-allow": {**base, "safety": {"allow": "yes", "reason": "public_readonly"}},
        "non-bool-confirmation": {**base, "confirmation_required": "false"},
        "bad-language": {**base, "language": "en-US"},
        "bad-contract-version": {**base, "contract_version": "v2"},
        "empty-normalized-command": {**base, "normalized_command": " "},
        "non-string-normalized-command": {**base, "normalized_command": {"text": "搜索汇率"}},
    }

    diagnostics = evaluation.diagnose_schema_mismatches(rows, predictions)

    assert diagnostics["summary"]["invalid_prediction_count"] == 11
    issues = {
        (issue["row_id"], issue["field_path"], issue["issue_category"])
        for row in diagnostics["rows"]
        for issue in row["issues"]
    }
    assert ("missing-slots", "slots", "missing_required_field") in issues
    assert ("bad-task-type", "task_type", "invalid_enum") in issues
    assert ("bad-route", "route", "invalid_enum") in issues
    assert ("slots-list", "slots", "invalid_type") in issues
    assert ("empty-safety-reason", "safety.reason", "empty_required_string") in issues
    assert ("non-bool-safety-allow", "safety.allow", "invalid_type") in issues
    assert ("non-bool-confirmation", "confirmation_required", "invalid_type") in issues
    assert ("bad-language", "language", "invalid_literal") in issues
    assert ("bad-contract-version", "contract_version", "invalid_literal") in issues
    assert ("empty-normalized-command", "normalized_command", "empty_required_string") in issues
    assert ("non-string-normalized-command", "normalized_command", "invalid_type") in issues
    assert all("observed_value_summary" in issue for row in diagnostics["rows"] for issue in row["issues"])
    assert all("expected_constraint" in issue for row in diagnostics["rows"] for issue in row["issues"])

    paths = reports.write_schema_diagnostics_report(
        diagnostics,
        output_dir=tmp_path,
        title="Post-recovery schema diagnostics",
    )
    report = paths["markdown"].read_text(encoding="utf-8")
    assert "invalid predictions remain invalid" in report
    assert "not a checkpoint release" in report
    assert "not an adapter release" in report
    assert "no production-readiness claim" in report
    assert "no full-private-corpus claim" in report
    assert "not a live-browser benchmark" in report


def test_diagnose_schema_cli_writes_public_safe_json_and_markdown(tmp_path: Path) -> None:
    row = _row("gold-1", "search_web", "天气")
    gold = tmp_path / "gold.jsonl"
    predictions = tmp_path / "predictions.jsonl"
    output = tmp_path / "diagnostics"
    write_jsonl(gold, [row.to_dict()])
    write_jsonl(
        predictions,
        [
            {
                "id": "gold-1",
                "prediction": {
                    "task_type": "browser_task",
                    "route": "search_web",
                    "safety": {"allow": True, "reason": "public_readonly"},
                    "confirmation_required": False,
                    "slots": {"query": "天气"},
                    "normalized_command": "搜索天气",
                    "language": "zh-CN",
                    "contract_version": "v1",
                },
            }
        ],
    )

    assert (
        eval_cli.main(
            [
                "diagnose-schema",
                "--gold",
                gold.as_posix(),
                "--predictions",
                predictions.as_posix(),
                "--output",
                output.as_posix(),
            ]
        )
        == 0
    )

    diagnostics = json.loads((output / "schema_diagnostics.json").read_text(encoding="utf-8"))
    markdown = (output / "schema_diagnostics.md").read_text(encoding="utf-8")
    assert diagnostics["rows"][0]["issues"][0]["field_path"] == "task_type"
    assert diagnostics["rows"][0]["issues"][0]["issue_category"] == "invalid_enum"
    assert "invalid predictions remain invalid" in markdown


def test_alignment_diagnostics_compare_raw_invalid_prediction_fields(tmp_path: Path) -> None:
    row = _row("gold-1", "search_web", "天气")
    prediction = {
        "task_type": "normalization",
        "route": "/search",
        "safety": {"allow": "yes", "reason": "allowed"},
        "confirmation_required": "false",
        "slots": ["query", "天气"],
        "normalized_command": "查天气",
        "language": "en-US",
        "contract_version": "v2",
    }

    diagnostics = evaluation.diagnose_alignment_mismatches([row], {"gold-1": prediction})

    assert diagnostics["diagnostic_kind"] == "browser_task_contract_alignment_mismatch"
    assert diagnostics["summary"]["gold_row_count"] == 1
    assert diagnostics["summary"]["prediction_count"] == 1
    assert diagnostics["summary"]["row_mismatch_count"] == 1
    assert diagnostics["summary"]["schema_invalid_prediction_count"] == 1
    assert diagnostics["summary"]["field_mismatch_counts"]["slots"] == 1
    assert diagnostics["claims"]["invalid_predictions_remain_invalid"] is True

    mismatches = diagnostics["rows"][0]["mismatches"]
    mismatch_paths = {mismatch["field_path"] for mismatch in mismatches}
    assert mismatch_paths == {
        "task_type",
        "route",
        "safety.allow",
        "safety.reason",
        "confirmation_required",
        "slots",
        "normalized_command",
        "language",
        "contract_version",
    }
    assert all(mismatch["row_id"] == "gold-1" for mismatch in mismatches)
    assert all("mismatch_category" in mismatch for mismatch in mismatches)
    assert all("gold_value_summary" in mismatch for mismatch in mismatches)
    assert all("prediction_value_summary" in mismatch for mismatch in mismatches)

    paths = reports.write_alignment_diagnostics_report(
        diagnostics,
        output_dir=tmp_path,
        title="Post-recovery alignment diagnostics",
    )
    report = paths["markdown"].read_text(encoding="utf-8")
    assert "invalid predictions remain invalid" in report
    assert "field-level public-sample evidence only" in report
    assert "not a checkpoint release" in report
    assert "not an adapter release" in report
    assert "no production-readiness claim" in report
    assert "no full-private-corpus claim" in report
    assert "not a live-browser benchmark" in report


def test_diagnose_alignment_cli_writes_public_safe_json_and_markdown(tmp_path: Path) -> None:
    row = _row("gold-1", "search_web", "天气")
    gold = tmp_path / "gold.jsonl"
    predictions = tmp_path / "predictions.jsonl"
    output = tmp_path / "diagnostics"
    write_jsonl(gold, [row.to_dict()])
    write_jsonl(
        predictions,
        [
            {
                "id": "gold-1",
                "prediction": {
                    "task_type": "normalization",
                    "route": "search_web",
                    "safety": {"allow": True, "reason": "public_readonly"},
                    "confirmation_required": False,
                    "slots": {"query": "天气"},
                    "normalized_command": "搜索天气",
                    "language": "zh-CN",
                    "contract_version": "v1",
                },
            }
        ],
    )

    assert (
        eval_cli.main(
            [
                "diagnose-alignment",
                "--gold",
                gold.as_posix(),
                "--predictions",
                predictions.as_posix(),
                "--output",
                output.as_posix(),
            ]
        )
        == 0
    )

    diagnostics = json.loads((output / "alignment_diagnostics.json").read_text(encoding="utf-8"))
    markdown = (output / "alignment_diagnostics.md").read_text(encoding="utf-8")
    assert diagnostics["rows"][0]["mismatches"][0]["field_path"] == "task_type"
    assert diagnostics["rows"][0]["mismatches"][0]["mismatch_category"] == "value_mismatch"
    assert "field-level public-sample evidence only" in markdown


def test_alignment_diagnostics_redact_private_row_ids_and_values(tmp_path: Path) -> None:
    private_row_id = "/Users/example/private/sk-1234567890123456"
    row = _row(private_row_id, "search_web", "天气")
    prediction = {
        **row.target_contract.to_dict(),
        "task_type": "api_key=secret1234",
        "normalized_command": "/Users/example/private/sk-1234567890123456",
    }

    diagnostics = evaluation.diagnose_alignment_mismatches([row], {private_row_id: prediction})
    paths = reports.write_alignment_diagnostics_report(diagnostics, output_dir=tmp_path)
    markdown = paths["markdown"].read_text(encoding="utf-8")
    serialized = json.dumps(diagnostics, ensure_ascii=False, sort_keys=True)

    assert "/Users/example" not in serialized
    assert "sk-1234567890123456" not in serialized
    assert "/Users/example" not in markdown
    assert "sk-1234567890123456" not in markdown
    assert "<private_path>" in serialized
    assert "<secret>" in serialized


def test_alignment_diagnostics_summarize_empty_objects_without_trailing_whitespace(tmp_path: Path) -> None:
    row = _row("gold-1", "search_web", "天气")
    prediction = {**row.target_contract.to_dict(), "slots": {}}

    diagnostics = evaluation.diagnose_alignment_mismatches([row], {"gold-1": prediction})
    paths = reports.write_alignment_diagnostics_report(diagnostics, output_dir=tmp_path)
    markdown = paths["markdown"].read_text(encoding="utf-8")
    slots_mismatch = diagnostics["rows"][0]["mismatches"][0]

    assert slots_mismatch["field_path"] == "slots"
    assert slots_mismatch["prediction_value_summary"] == "empty object"
    assert "prediction empty object" in markdown
    assert "prediction object with keys: " not in markdown


def test_rule_and_prompt_fixture_baselines_are_bounded(tmp_path: Path) -> None:
    rows = [_row("gold-1", "search_web", "天气")]
    predictions = rule_baseline_predictions(rows)

    assert predictions["gold-1"]["task_type"] == "search"

    fixture = tmp_path / "prompt_predictions.jsonl"
    write_jsonl(fixture, [{"id": "gold-1", "prediction": rows[0].target_contract.to_dict()}])
    prompt_predictions = prompt_fixture_predictions(rows, fixture)
    assert prompt_predictions["gold-1"]["route"] == "search_web"


def test_execution_smoke_calls_controlled_validation_command(tmp_path: Path) -> None:
    rows = [_row("gold-1", "search_web", "天气")]
    predictions = rule_baseline_predictions(rows)
    assert run_execution_smoke(rows, predictions, enabled=False).enabled is False

    validator = tmp_path / "validator.py"
    validator.write_text(
        "\n".join(
            [
                "import json, sys",
                "payload = json.load(sys.stdin)",
                "contract = payload['contract']",
                "ok = contract.get('route') == 'search_web'",
                "print(json.dumps({'ok': ok, 'reason': 'checked'}))",
            ]
        ),
        encoding="utf-8",
    )
    target = tmp_path / "validation-target.json"
    target.write_text(json.dumps({"command": ["python", str(validator)]}), encoding="utf-8")
    smoke = run_execution_smoke(rows, predictions, enabled=True, target_path=target)
    assert smoke.enabled is True
    assert smoke.passed == 1
    assert smoke.failed == 0


def test_smoke_cli_can_write_json_result(tmp_path: Path, capsys) -> None:  # type: ignore[no-untyped-def]
    rows = [_row("gold-1", "search_web", "天气")]
    gold = tmp_path / "gold.jsonl"
    predictions = tmp_path / "predictions.jsonl"
    write_jsonl(gold, [rows[0].to_dict()])
    write_jsonl(predictions, [{"id": "gold-1", "prediction": rows[0].target_contract.to_dict()}])
    target = tmp_path / "validation-target.json"
    target.write_text(json.dumps({"accepts_contracts": True}), encoding="utf-8")
    output = tmp_path / "smoke_result.json"

    assert (
        eval_cli.main(
            [
                "smoke",
                "--gold",
                gold.as_posix(),
                "--predictions",
                predictions.as_posix(),
                "--target",
                target.as_posix(),
                "--output",
                output.as_posix(),
            ]
        )
        == 0
    )

    assert capsys.readouterr().out == ""
    result = json.loads(output.read_text(encoding="utf-8"))
    assert result["passed"] == 1
    assert result["failed"] == 0


def test_write_metrics_report_outputs_json_and_markdown(tmp_path: Path) -> None:
    rows = [_row("gold-1", "search_web", "天气")]
    result = evaluate_predictions(rows, {"gold-1": rows[0].target_contract.to_dict()})

    paths = write_metrics_report(result, output_dir=tmp_path, title="Public sample metrics")

    metrics = json.loads(paths["json"].read_text(encoding="utf-8"))
    markdown = paths["markdown"].read_text(encoding="utf-8")
    assert metrics["metrics"]["contract_exact_match"] == 1.0
    assert "Public sample metrics" in markdown
    assert "live-browser improvement" in markdown
