import json
import sys
import types
from pathlib import Path
from typing import Any

from voice2task import training
from voice2task.evaluation import evaluate_predictions, load_predictions
from voice2task.leak_scan import scan_paths
from voice2task.reports import write_prediction_evidence_pack
from voice2task.schemas import SFTDatasetRow
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
    assert dry_run["formatting_policy"]["prediction_prompt"] == "shared_contract_chat_template"

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


def test_sft_prediction_metadata_sanitizes_private_base_model_without_public_id(tmp_path: Path) -> None:
    manifest = _write_manifest(tmp_path)
    private_config = tmp_path / "private-config.json"
    private_config.write_text(
        json.dumps(
            {
                "base_model": "/mnt/data/" + "minghongsun/voice2task-post-training/models/model",
                "model_source": "modelscope",
                "allow_private_prediction": True,
                "adapter_path": "/mnt/data/" + "minghongsun/voice2task-post-training/runs/run/adapter",
                "prediction_split": "all",
            }
        ),
        encoding="utf-8",
    )

    metadata = run_sft_prediction_export(private_config, manifest, tmp_path / "predictions.jsonl", dry_run=True)
    metadata_text = json.dumps(metadata, ensure_ascii=False, sort_keys=True)

    assert metadata["base_model"] == "<private_base_model>"
    assert "/mnt/data/" not in metadata_text


class _FakeInputIds:
    shape = (1, 0)


class _FakeInputs(dict[str, Any]):
    def to(self, device: str) -> "_FakeInputs":
        return self


class _FakeTokenizer:
    eos_token_id = 0

    def __call__(self, prompt: str, *, return_tensors: str) -> _FakeInputs:
        return _FakeInputs({"input_ids": _FakeInputIds()})

    def apply_chat_template(
        self,
        messages: list[dict[str, str]],
        *,
        tokenize: bool,
        add_generation_prompt: bool,
    ) -> str:
        return "<chat-prompt>"

    def decode(self, new_tokens: list[int], *, skip_special_tokens: bool) -> str:
        return "模型输出不是 JSON，但需要保留为失败证据 /mnt/data/minghongsun/private/model"


class _FakeJsonPathTokenizer(_FakeTokenizer):
    def decode(self, new_tokens: list[int], *, skip_special_tokens: bool) -> str:
        return json.dumps(
            {
                "task_type": "search",
                "route": "search_web",
                "safety": {"allow": True, "reason": "read from /mnt/data/minghongsun/private/run"},
                "confirmation_required": False,
                "slots": {"query": "机票"},
                "normalized_command": "搜索机票",
                "language": "zh-CN",
                "contract_version": "v1",
            },
            ensure_ascii=False,
        )


class _FakeModel:
    device = "cpu"

    def eval(self) -> None:
        return None

    def generate(self, **kwargs: Any) -> list[list[int]]:
        return [[101, 102]]


class _FakeNoGrad:
    def __enter__(self) -> None:
        return None

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        return None


def test_real_sft_prediction_preserves_non_json_decoded_output(
    monkeypatch: Any,
    tmp_path: Path,
) -> None:
    output = tmp_path / "trained_predictions.jsonl"
    row = SFTDatasetRow(
        id="sft-test-1",
        split="test",
        input_text="帮我搜索机票",
        target_contract=_contract("机票"),
        provenance={"source_id": "sft-test-1", "public_safe": True},
    )
    torch_module = types.ModuleType("torch")
    torch_module.float16 = "float16"
    torch_module.float32 = "float32"
    torch_module.cuda = types.SimpleNamespace(is_available=lambda: False)
    torch_module.no_grad = lambda: _FakeNoGrad()
    peft_module = types.ModuleType("peft")
    peft_module.PeftModel = types.SimpleNamespace(from_pretrained=lambda model, adapter_path: model)
    transformers_module = types.ModuleType("transformers")
    transformers_module.AutoTokenizer = types.SimpleNamespace(from_pretrained=lambda *args, **kwargs: _FakeTokenizer())
    transformers_module.AutoModelForCausalLM = types.SimpleNamespace(
        from_pretrained=lambda *args, **kwargs: _FakeModel()
    )
    monkeypatch.setitem(sys.modules, "torch", torch_module)
    monkeypatch.setitem(sys.modules, "peft", peft_module)
    monkeypatch.setitem(sys.modules, "transformers", transformers_module)

    count = training._run_real_sft_prediction(
        {"base_model": "Qwen/Qwen2.5-0.5B-Instruct", "adapter_path": (tmp_path / "adapter").as_posix()},
        [row],
        output,
    )

    record = json.loads(output.read_text(encoding="utf-8"))
    result = evaluate_predictions([row], load_predictions(output))

    assert count == 1
    assert record["prediction"] == "模型输出不是 JSON，但需要保留为失败证据 <private_path>"
    assert "/mnt/data/" not in json.dumps(record, ensure_ascii=False)
    assert result.metrics["json_valid_rate"] == 0.0
    assert result.failure_slices["schema"]["count"] == 1


def test_real_sft_prediction_sanitizes_private_paths_inside_json_output(
    monkeypatch: Any,
    tmp_path: Path,
) -> None:
    output = tmp_path / "trained_predictions.jsonl"
    row = SFTDatasetRow(
        id="sft-test-1",
        split="test",
        input_text="帮我搜索机票",
        target_contract=_contract("机票"),
        provenance={"source_id": "sft-test-1", "public_safe": True},
    )
    torch_module = types.ModuleType("torch")
    torch_module.float16 = "float16"
    torch_module.float32 = "float32"
    torch_module.cuda = types.SimpleNamespace(is_available=lambda: False)
    torch_module.no_grad = lambda: _FakeNoGrad()
    peft_module = types.ModuleType("peft")
    peft_module.PeftModel = types.SimpleNamespace(from_pretrained=lambda model, adapter_path: model)
    transformers_module = types.ModuleType("transformers")
    transformers_module.AutoTokenizer = types.SimpleNamespace(
        from_pretrained=lambda *args, **kwargs: _FakeJsonPathTokenizer()
    )
    transformers_module.AutoModelForCausalLM = types.SimpleNamespace(
        from_pretrained=lambda *args, **kwargs: _FakeModel()
    )
    monkeypatch.setitem(sys.modules, "torch", torch_module)
    monkeypatch.setitem(sys.modules, "peft", peft_module)
    monkeypatch.setitem(sys.modules, "transformers", transformers_module)

    count = training._run_real_sft_prediction(
        {"base_model": "Qwen/Qwen2.5-0.5B-Instruct", "adapter_path": (tmp_path / "adapter").as_posix()},
        [row],
        output,
    )

    record = json.loads(output.read_text(encoding="utf-8"))
    serialized = json.dumps(record, ensure_ascii=False)

    assert count == 1
    assert record["prediction"]["safety"]["reason"] == "read from <private_path>"
    assert "/mnt/data/" not in serialized
    assert scan_paths([output]).ok is True


def test_extract_json_sanitizes_top_level_lists_strings_ips_and_secrets() -> None:
    private_path = "/" + "mnt/data/minghongsun/private/run"
    private_ip = "192." + "168.1.10"
    secret = "api_key=" + "abc12345secret"
    decoded_list = json.dumps([private_path, {"nested": f"http://{private_ip}"}], ensure_ascii=False)
    decoded_string = json.dumps(secret, ensure_ascii=False)

    parsed_list = training._extract_json_object(decoded_list)
    parsed_string = training._extract_json_object(decoded_string)

    assert parsed_list == ["<private_path>", {"nested": "http://<private_ip>"}]
    assert parsed_string == "<secret>"
    assert "/mnt/data/" not in json.dumps(parsed_list, ensure_ascii=False)
    assert private_ip not in json.dumps(parsed_list, ensure_ascii=False)
    assert "abc12345secret" not in str(parsed_string)


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


def test_invalid_private_adapter_predictions_remain_schema_failures(
    monkeypatch: Any,
    tmp_path: Path,
) -> None:
    manifest = _write_manifest(tmp_path)
    config = _write_prediction_config(tmp_path, adapter_path=(tmp_path / "adapter").as_posix())
    output = tmp_path / "trained_predictions.jsonl"

    monkeypatch.setattr(training, "_prediction_dependencies_available", lambda: True)

    def write_invalid_private_predictions(config: dict[str, Any], rows: list[Any], output_path: Path) -> int:
        output_path.write_text(
            "\n".join(
                json.dumps(
                    {
                        "id": row.id,
                        "prediction": {"task": {"description": "generic normalization output"}},
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

    monkeypatch.setattr(training, "_run_real_sft_prediction", write_invalid_private_predictions)

    metadata = run_sft_prediction_export(config, manifest, output, dry_run=False, fixture_mode=False)
    prediction_rows = load_predictions(output)
    gold_rows = [
        SFTDatasetRow(**json.loads(line))
        for line in (tmp_path / "sft_public_sample.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    result = evaluate_predictions(gold_rows, prediction_rows)

    assert metadata["prediction_source_kind"] == "private_a100_adapter"
    assert prediction_rows["sft-test-1"] == {"task": {"description": "generic normalization output"}}
    assert result.metrics["json_valid_rate"] == 0.0
    assert result.failure_slices["schema"]["count"] == 2


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


def test_contract_output_recovery_template_is_public_safe_and_bounded() -> None:
    template = Path("reports/templates/a100-sft-contract-output-recovery.md")

    text = template.read_text(encoding="utf-8")

    assert "json_valid_rate=0.0000" in text
    assert "12 schema failures" in text
    assert "reports/public-sample/a100-sft-post-recovery-rerun/" in text
    assert "post-rerun result: `json_valid_rate=0.0000`" in text
    assert "post-rerun controlled smoke: `0 passed / 12 failed`" in text
    assert "did not recover schema-valid Browser Task Contract output" in text
    assert "not a checkpoint release" in text
    assert "not a live-browser benchmark" in text
    assert "no production-readiness claim" in text
    assert "private_a100_adapter" in text
    assert "<a100_project_root>" in text
    assert scan_paths([template]).ok is True


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
