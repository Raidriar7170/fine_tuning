import json
from pathlib import Path
from typing import Any

from voice2task import training
from voice2task.evaluation import load_predictions
from voice2task.leak_scan import scan_paths
from voice2task.reports import write_prediction_evidence_pack
from voice2task.training import run_sft_prediction_export

A100_PROJECT_ROOT = "/mnt/data/" + "minghongsun/voice2task-post-training"


def _contract(query: str) -> dict[str, Any]:
    return {
        "task_type": "search",
        "route": "search_web",
        "safety": {"allow": True, "reason": "public_readonly"},
        "confirmation_required": False,
        "slots": {"query": query},
        "normalized_command": f"搜索{query}",
        "language": "zh-CN",
        "contract_version": "v1",
    }


def _write_manifest(tmp_path: Path) -> Path:
    rows = tmp_path / "sft_public_sample.jsonl"
    rows.write_text(
        "\n".join(
            json.dumps(
                {
                    "id": row_id,
                    "split": split,
                    "input_text": f"帮我搜索{query}",
                    "target_contract": _contract(query),
                    "provenance": {"source_id": row_id, "public_safe": True},
                },
                ensure_ascii=False,
            )
            for row_id, split, query in (
                ("sft-train-1", "train", "天气"),
                ("sft-test-1", "test", "机票"),
            )
        )
        + "\n",
        encoding="utf-8",
    )
    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "manifest_id": "public-sample-test",
                "files": {"sft": rows.name},
                "counts": {"sft_rows": 2},
            }
        ),
        encoding="utf-8",
    )
    return manifest


def _write_prediction_config(
    tmp_path: Path,
    *,
    allow_private_prediction: bool = True,
    adapter_path: str | None = "<a100_project_root>/runs/a100-sft-public-smoke/adapter",
    output_root: str = A100_PROJECT_ROOT,
) -> Path:
    config = {
        "base_model": "Qwen/Qwen2.5-0.5B-Instruct",
        "model_source": "modelscope",
        "allow_private_prediction": allow_private_prediction,
        "adapter_path": adapter_path,
        "output_root": output_root,
        "prediction_split": "all",
    }
    if adapter_path is None:
        config.pop("adapter_path")
    config_path = tmp_path / "prediction-config.json"
    config_path.write_text(json.dumps(config), encoding="utf-8")
    return config_path


def test_sft_prediction_export_requires_explicit_opt_in_and_adapter_config(tmp_path: Path) -> None:
    manifest = _write_manifest(tmp_path)
    output = tmp_path / "predictions.jsonl"
    config = _write_prediction_config(tmp_path)

    dry_run = run_sft_prediction_export(config, manifest, output, dry_run=True, fixture_mode=False)

    assert output.exists() is False
    assert dry_run["prediction_status"] == "prediction_skipped_no_opt_in"
    assert dry_run["release_status"] == "not_released"

    missing_adapter_config = _write_prediction_config(tmp_path, adapter_path=None)
    blocked = run_sft_prediction_export(missing_adapter_config, manifest, output, dry_run=False, fixture_mode=False)

    assert output.exists() is False
    assert blocked["prediction_status"] == "prediction_blocked_missing_adapter"
    assert blocked["prediction_gate"]["will_run_private_prediction"] is False


def test_sft_prediction_fixture_mode_writes_public_safe_predictions(tmp_path: Path) -> None:
    manifest = _write_manifest(tmp_path)
    config = _write_prediction_config(tmp_path)
    output = tmp_path / "trained_predictions.jsonl"

    metadata = run_sft_prediction_export(config, manifest, output, dry_run=False, fixture_mode=True)

    assert metadata["prediction_status"] == "fixture_predictions_written"
    assert metadata["prediction_source_kind"] == "public_sample_contract_fixture"
    assert metadata["prediction_count"] == 2
    assert metadata["dataset_manifest_id"] == "public-sample-test"
    assert metadata["release_status"] == "not_released"
    predictions = load_predictions(output)
    assert predictions["sft-test-1"]["route"] == "search_web"
    assert scan_paths([output]).ok is True
    output_text = output.read_text(encoding="utf-8")
    assert A100_PROJECT_ROOT not in output_text
    assert "/Users/" not in output_text


def test_sft_prediction_metadata_sanitizes_private_a100_paths(tmp_path: Path) -> None:
    manifest = _write_manifest(tmp_path)
    private_config = tmp_path / "private-config.json"
    private_config.write_text(
        json.dumps(
            {
                "base_model": "/mnt/data/" + "minghongsun/voice2task-post-training/models/model",
                "base_model_public_id": "Qwen/Qwen2.5-0.5B-Instruct",
                "model_source": "modelscope",
                "allow_private_prediction": True,
                "adapter_path": "/mnt/data/" + "minghongsun/voice2task-post-training/runs/run/adapter",
                "prediction_split": "all",
            }
        ),
        encoding="utf-8",
    )
    private_output = Path("/mnt/data/" + "minghongsun/voice2task-post-training/evidence/predictions.jsonl")

    metadata = run_sft_prediction_export(private_config, manifest, private_output, dry_run=True, fixture_mode=False)
    metadata_text = json.dumps(metadata, ensure_ascii=False, sort_keys=True)

    assert "Qwen/Qwen2.5-0.5B-Instruct" in metadata_text
    assert "/mnt/data/" not in metadata_text
    assert metadata["prediction_output_path"] == "<a100_prediction_output>"
    assert metadata["command_summary"]["config"] == "<private_prediction_config>"


def test_sft_prediction_run_prediction_calls_private_adapter_export(
    monkeypatch: Any,
    tmp_path: Path,
) -> None:
    manifest = _write_manifest(tmp_path)
    config = _write_prediction_config(tmp_path, adapter_path=(tmp_path / "adapter").as_posix())
    output = tmp_path / "trained_predictions.jsonl"
    calls: list[Path] = []

    monkeypatch.setattr(training, "_prediction_dependencies_available", lambda: True)

    def write_private_predictions(config: dict[str, Any], rows: list[Any], output_path: Path) -> int:
        calls.append(output_path)
        output_path.write_text(
            "\n".join(
                json.dumps(
                    {
                        "id": row.id,
                        "prediction": row.target_contract.to_dict(),
                        "prediction_source_kind": "private_a100_adapter",
                        "provenance": {"public_safe": True},
                    },
                    ensure_ascii=False,
                )
                for row in rows
            )
            + "\n",
            encoding="utf-8",
        )
        return len(rows)

    monkeypatch.setattr(training, "_run_real_sft_prediction", write_private_predictions)

    metadata = run_sft_prediction_export(config, manifest, output, dry_run=False, fixture_mode=False)

    assert calls == [output]
    assert metadata["prediction_status"] == "private_adapter_predictions_written"
    assert metadata["prediction_source_kind"] == "private_a100_adapter"
    assert metadata["prediction_gate"]["will_run_private_prediction"] is True
    assert metadata["prediction_count"] == 2
    assert scan_paths([output]).ok is True


def test_prediction_evidence_pack_is_honest_and_public_safe(tmp_path: Path) -> None:
    prediction_path = tmp_path / "predictions.jsonl"
    prediction_path.write_text(
        json.dumps(
            {
                "id": "sft-test-1",
                "prediction": _contract("机票"),
                "prediction_source_kind": "public_sample_contract_fixture",
                "provenance": {"public_safe": True},
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    metadata = {
        "base_model": "Qwen/Qwen2.5-0.5B-Instruct",
        "model_source": "modelscope",
        "dataset_manifest_id": "public-sample-test",
        "prediction_source_kind": "public_sample_contract_fixture",
        "prediction_status": "fixture_predictions_written",
        "release_status": "not_released",
    }

    paths = write_prediction_evidence_pack(
        output_dir=tmp_path / "evidence",
        prediction_path=Path("reports/public-sample/a100-sft-prediction-eval-smoke/predictions.jsonl"),
        prediction_metadata=metadata,
        metrics_path=Path("reports/public-sample/a100-sft-prediction-eval-smoke/metrics.json"),
        smoke_result={"enabled": True, "passed": 1, "failed": 0, "notes": "controlled_validation_command"},
        leak_scan_result={"ok": True, "findings": []},
    )

    manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))
    report = paths["report"].read_text(encoding="utf-8").lower()
    assert manifest["release_status"] == "not_released"
    assert manifest["claims"]["checkpoint_release"] is False
    assert manifest["claims"]["live_browser_benchmark_claim"] is False
    assert manifest["prediction_source_kind"] == "public_sample_contract_fixture"
    assert "not a checkpoint release" in report
    assert "not a live-browser benchmark" in report
    assert "not private adapter model outputs" in report
    assert "private a100 adapter path" in report
    assert "reported as failures" in report
    assert scan_paths([paths["manifest"], paths["report"]]).ok is True


def test_leak_scan_rejects_model_adapter_and_cache_artifacts(tmp_path: Path) -> None:
    evidence_dir = tmp_path / "evidence"
    (evidence_dir / "adapter").mkdir(parents=True)
    (evidence_dir / "adapter" / "adapter_config.json").write_text("{}", encoding="utf-8")
    (evidence_dir / "model.safetensors").write_text("placeholder", encoding="utf-8")
    (evidence_dir / "cache").mkdir()
    (evidence_dir / "cache" / "index.json").write_text("{}", encoding="utf-8")

    result = scan_paths([evidence_dir])

    assert {
        "model_artifact",
        "private_artifact_dir",
    }.issubset({finding.category for finding in result.findings})
