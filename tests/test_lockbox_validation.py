import json
from pathlib import Path

from voice2task.cli import data as data_cli
from voice2task.lockbox import compute_lockbox_manifest_hash, compute_lockbox_row_hash, validate_lockbox


def _contract(query: str = "天气") -> dict[str, object]:
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


def _lockbox_row(
    row_id: str,
    *,
    input_text: str | None = None,
    semantic_family_id: str | None = None,
    derived_from: list[str] | None = None,
    analysis_seen: bool = False,
    provenance: dict[str, object] | None = None,
    content_hash: str | None = None,
) -> dict[str, object]:
    row = {
        "row_id": row_id,
        "semantic_family_id": semantic_family_id or f"lockbox-family-{row_id}",
        "input_text": input_text or f"请搜索{row_id}天气",
        "gold_contract": _contract(row_id),
        "source": {"category": "new_lockbox_authoring", "provenance": provenance or {"authoring_batch": "unit-test"}},
        "derived_from": derived_from or [],
        "analysis_seen": analysis_seen,
    }
    row["content_hash"] = content_hash or compute_lockbox_row_hash(row)
    return row


def _reference_row(
    row_id: str,
    *,
    input_text: str,
    split: str = "train",
    source_id: str | None = None,
) -> dict[str, object]:
    return {
        "id": row_id,
        "split": split,
        "input_text": input_text,
        "target_contract": _contract(row_id),
        "provenance": {"source_id": source_id or row_id, "public_safe": True},
    }


def _write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    payload = "\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows) + "\n"
    path.write_text(payload, encoding="utf-8")


def _manifest(rows: list[dict[str, object]], *, frozen: bool = True) -> dict[str, object]:
    content_hashes = [str(row["content_hash"]) for row in rows]
    lockbox_hash = compute_lockbox_manifest_hash(content_hashes)
    return {
        "manifest_id": "lockbox-unit-test",
        "schema_version": "lockbox.v1",
        "created_at": "2026-06-26T00:00:00Z",
        "frozen_at": "2026-06-26T00:00:00Z",
        "frozen": frozen,
        "row_count": len(rows),
        "family_count": len({str(row["semantic_family_id"]) for row in rows}),
        "provenance_summary": {"new_lockbox_authoring": len(rows)},
        "content_hashes": content_hashes,
        "lockbox_hash": lockbox_hash,
        "dataset_sha256": lockbox_hash,
    }


def test_clean_lockbox_passes_with_frozen_manifest_and_disjoint_inputs(tmp_path: Path) -> None:
    lockbox_rows = [_lockbox_row("lb-1"), _lockbox_row("lb-2")]
    train_path = tmp_path / "train.jsonl"
    analysis_path = tmp_path / "analysis.jsonl"
    lockbox_path = tmp_path / "lockbox.jsonl"
    manifest_path = tmp_path / "manifest.json"
    _write_jsonl(lockbox_path, lockbox_rows)
    _write_jsonl(train_path, [_reference_row("train-1", input_text="训练样本")])
    _write_jsonl(analysis_path, [_reference_row("analysis-1", input_text="分析样本", split="dev")])
    manifest_path.write_text(json.dumps(_manifest(lockbox_rows), ensure_ascii=False), encoding="utf-8")

    result = validate_lockbox(
        lockbox_path=lockbox_path,
        manifest_path=manifest_path,
        train_paths=[train_path],
        analysis_paths=[analysis_path],
    )

    assert result.ok is True
    assert result.failures == []
    assert result.counts == {"lockbox_rows": 2, "train_rows": 1, "analysis_rows": 1}
    assert result.manifest["frozen"] is True


def test_lockbox_fails_duplicate_row_id(tmp_path: Path) -> None:
    rows = [_lockbox_row("duplicate"), _lockbox_row("duplicate", input_text="另一个输入")]
    lockbox_path = tmp_path / "lockbox.jsonl"
    manifest_path = tmp_path / "manifest.json"
    _write_jsonl(lockbox_path, rows)
    manifest_path.write_text(json.dumps(_manifest(rows), ensure_ascii=False), encoding="utf-8")

    result = validate_lockbox(lockbox_path=lockbox_path, manifest_path=manifest_path)

    assert result.ok is False
    assert {failure["category"] for failure in result.failures} == {"duplicate_row_id"}


def test_lockbox_fails_when_row_id_overlaps_train_id(tmp_path: Path) -> None:
    rows = [_lockbox_row("train-1", input_text="全新锁盒输入一")]
    train_path = tmp_path / "train.jsonl"
    lockbox_path = tmp_path / "lockbox.jsonl"
    manifest_path = tmp_path / "manifest.json"
    _write_jsonl(lockbox_path, rows)
    _write_jsonl(train_path, [_reference_row("train-1", input_text="训练输入")])
    manifest_path.write_text(json.dumps(_manifest(rows), ensure_ascii=False), encoding="utf-8")

    result = validate_lockbox(lockbox_path=lockbox_path, manifest_path=manifest_path, train_paths=[train_path])

    assert result.ok is False
    assert any(failure["category"] == "row_id_overlap" for failure in result.failures)


def test_lockbox_fails_when_row_id_overlaps_analysis_id(tmp_path: Path) -> None:
    rows = [_lockbox_row("analysis-1", input_text="全新锁盒输入二")]
    analysis_path = tmp_path / "analysis.jsonl"
    lockbox_path = tmp_path / "lockbox.jsonl"
    manifest_path = tmp_path / "manifest.json"
    _write_jsonl(lockbox_path, rows)
    _write_jsonl(analysis_path, [_reference_row("analysis-1", input_text="分析输入", split="dev")])
    manifest_path.write_text(json.dumps(_manifest(rows), ensure_ascii=False), encoding="utf-8")

    result = validate_lockbox(lockbox_path=lockbox_path, manifest_path=manifest_path, analysis_paths=[analysis_path])

    assert result.ok is False
    assert any(failure["category"] == "row_id_overlap" for failure in result.failures)


def test_lockbox_fails_when_row_id_overlaps_train_row_id(tmp_path: Path) -> None:
    rows = [_lockbox_row("train-row-1", input_text="全新锁盒输入三")]
    train_path = tmp_path / "train.jsonl"
    lockbox_path = tmp_path / "lockbox.jsonl"
    manifest_path = tmp_path / "manifest.json"
    _write_jsonl(lockbox_path, rows)
    _write_jsonl(
        train_path,
        [{**_reference_row("train-id-1", input_text="训练输入"), "row_id": "train-row-1"}],
    )
    manifest_path.write_text(json.dumps(_manifest(rows), ensure_ascii=False), encoding="utf-8")

    result = validate_lockbox(lockbox_path=lockbox_path, manifest_path=manifest_path, train_paths=[train_path])

    assert result.ok is False
    assert any(failure["category"] == "row_id_overlap" for failure in result.failures)


def test_lockbox_fails_when_row_id_overlaps_analysis_row_id(tmp_path: Path) -> None:
    rows = [_lockbox_row("analysis-row-1", input_text="全新锁盒输入四")]
    analysis_path = tmp_path / "analysis.jsonl"
    lockbox_path = tmp_path / "lockbox.jsonl"
    manifest_path = tmp_path / "manifest.json"
    _write_jsonl(lockbox_path, rows)
    _write_jsonl(
        analysis_path,
        [{**_reference_row("analysis-id-1", input_text="分析输入", split="dev"), "row_id": "analysis-row-1"}],
    )
    manifest_path.write_text(json.dumps(_manifest(rows), ensure_ascii=False), encoding="utf-8")

    result = validate_lockbox(lockbox_path=lockbox_path, manifest_path=manifest_path, analysis_paths=[analysis_path])

    assert result.ok is False
    assert any(failure["category"] == "row_id_overlap" for failure in result.failures)


def test_lockbox_fails_exact_text_overlap_with_train_data(tmp_path: Path) -> None:
    rows = [_lockbox_row("lb-1", input_text="帮我搜索北京天气")]
    train_path = tmp_path / "train.jsonl"
    lockbox_path = tmp_path / "lockbox.jsonl"
    manifest_path = tmp_path / "manifest.json"
    _write_jsonl(lockbox_path, rows)
    _write_jsonl(train_path, [_reference_row("train-1", input_text="帮我搜索北京天气")])
    manifest_path.write_text(json.dumps(_manifest(rows), ensure_ascii=False), encoding="utf-8")

    result = validate_lockbox(lockbox_path=lockbox_path, manifest_path=manifest_path, train_paths=[train_path])

    assert result.ok is False
    assert any(failure["category"] == "exact_input_text_overlap" for failure in result.failures)


def test_lockbox_fails_normalized_text_overlap_with_analysis_data(tmp_path: Path) -> None:
    rows = [_lockbox_row("lb-1", input_text="帮 我 搜 索 北京 天气")]
    analysis_path = tmp_path / "analysis.jsonl"
    lockbox_path = tmp_path / "lockbox.jsonl"
    manifest_path = tmp_path / "manifest.json"
    _write_jsonl(lockbox_path, rows)
    _write_jsonl(analysis_path, [_reference_row("analysis-1", input_text="帮我搜索北京天气", split="dev")])
    manifest_path.write_text(json.dumps(_manifest(rows), ensure_ascii=False), encoding="utf-8")

    result = validate_lockbox(lockbox_path=lockbox_path, manifest_path=manifest_path, analysis_paths=[analysis_path])

    assert result.ok is False
    assert any(failure["category"] == "normalized_input_text_overlap" for failure in result.failures)


def test_lockbox_fails_semantic_family_overlap_when_required(tmp_path: Path) -> None:
    rows = [_lockbox_row("lb-1", semantic_family_id="family-search-weather")]
    train_path = tmp_path / "train.jsonl"
    lockbox_path = tmp_path / "lockbox.jsonl"
    manifest_path = tmp_path / "manifest.json"
    _write_jsonl(lockbox_path, rows)
    _write_jsonl(
        train_path,
        [
            {
                **_reference_row("train-1", input_text="训练输入"),
                "semantic_family_id": "family-search-weather",
            }
        ],
    )
    manifest_path.write_text(json.dumps(_manifest(rows), ensure_ascii=False), encoding="utf-8")

    result = validate_lockbox(
        lockbox_path=lockbox_path,
        manifest_path=manifest_path,
        train_paths=[train_path],
        require_family_disjointness=True,
    )

    assert result.ok is False
    assert any(failure["category"] == "semantic_family_overlap" for failure in result.failures)


def test_lockbox_fails_forbidden_ancestry_to_train_or_remediation_rows(tmp_path: Path) -> None:
    rows = [_lockbox_row("lb-1", derived_from=["train-1", "remediation:case-7"])]
    train_path = tmp_path / "train.jsonl"
    lockbox_path = tmp_path / "lockbox.jsonl"
    manifest_path = tmp_path / "manifest.json"
    _write_jsonl(lockbox_path, rows)
    _write_jsonl(train_path, [_reference_row("train-1", input_text="训练输入")])
    manifest_path.write_text(json.dumps(_manifest(rows), ensure_ascii=False), encoding="utf-8")

    result = validate_lockbox(lockbox_path=lockbox_path, manifest_path=manifest_path, train_paths=[train_path])

    assert result.ok is False
    categories = {failure["category"] for failure in result.failures}
    assert "forbidden_ancestry" in categories


def test_lockbox_fails_forbidden_ancestry_to_train_provenance_source_id(tmp_path: Path) -> None:
    rows = [_lockbox_row("lb-1", derived_from=[{"source_id": "source-alpha-1"}])]
    train_path = tmp_path / "train.jsonl"
    lockbox_path = tmp_path / "lockbox.jsonl"
    manifest_path = tmp_path / "manifest.json"
    _write_jsonl(lockbox_path, rows)
    _write_jsonl(
        train_path,
        [_reference_row("train-row-1", input_text="训练输入", source_id="source-alpha-1")],
    )
    manifest_path.write_text(json.dumps(_manifest(rows), ensure_ascii=False), encoding="utf-8")

    result = validate_lockbox(lockbox_path=lockbox_path, manifest_path=manifest_path, train_paths=[train_path])

    assert result.ok is False
    assert any(failure["category"] == "forbidden_ancestry" for failure in result.failures)


def test_lockbox_fails_forbidden_ancestry_to_analysis_row_id(tmp_path: Path) -> None:
    rows = [_lockbox_row("lb-1", derived_from=["analysis-1"])]
    analysis_path = tmp_path / "analysis.jsonl"
    lockbox_path = tmp_path / "lockbox.jsonl"
    manifest_path = tmp_path / "manifest.json"
    _write_jsonl(lockbox_path, rows)
    _write_jsonl(analysis_path, [_reference_row("analysis-1", input_text="分析输入", split="dev")])
    manifest_path.write_text(json.dumps(_manifest(rows), ensure_ascii=False), encoding="utf-8")

    result = validate_lockbox(lockbox_path=lockbox_path, manifest_path=manifest_path, analysis_paths=[analysis_path])

    assert result.ok is False
    assert any(failure["category"] == "forbidden_ancestry" for failure in result.failures)


def test_lockbox_fails_forbidden_ancestry_to_analysis_provenance_source_id(tmp_path: Path) -> None:
    rows = [_lockbox_row("lb-1", derived_from=[{"source_id": "analysis-source-1"}])]
    analysis_path = tmp_path / "analysis.jsonl"
    lockbox_path = tmp_path / "lockbox.jsonl"
    manifest_path = tmp_path / "manifest.json"
    _write_jsonl(lockbox_path, rows)
    _write_jsonl(
        analysis_path,
        [_reference_row("analysis-row-1", input_text="分析输入", split="dev", source_id="analysis-source-1")],
    )
    manifest_path.write_text(json.dumps(_manifest(rows), ensure_ascii=False), encoding="utf-8")

    result = validate_lockbox(lockbox_path=lockbox_path, manifest_path=manifest_path, analysis_paths=[analysis_path])

    assert result.ok is False
    assert any(failure["category"] == "forbidden_ancestry" for failure in result.failures)


def test_lockbox_fails_forbidden_ancestry_to_nested_train_provenance_source_id(tmp_path: Path) -> None:
    rows = [_lockbox_row("lb-1", derived_from=[{"provenance": {"source_id": "source-alpha-1"}}])]
    train_path = tmp_path / "train.jsonl"
    lockbox_path = tmp_path / "lockbox.jsonl"
    manifest_path = tmp_path / "manifest.json"
    _write_jsonl(lockbox_path, rows)
    _write_jsonl(
        train_path,
        [_reference_row("train-row-1", input_text="训练输入", source_id="source-alpha-1")],
    )
    manifest_path.write_text(json.dumps(_manifest(rows), ensure_ascii=False), encoding="utf-8")

    result = validate_lockbox(lockbox_path=lockbox_path, manifest_path=manifest_path, train_paths=[train_path])

    assert result.ok is False
    assert any(failure["category"] == "forbidden_ancestry" for failure in result.failures)


def test_lockbox_fails_forbidden_ancestry_to_top_level_train_source_row_id(tmp_path: Path) -> None:
    rows = [_lockbox_row("lb-1", derived_from=[{"source_row_id": "train-row-1"}])]
    train_path = tmp_path / "train.jsonl"
    lockbox_path = tmp_path / "lockbox.jsonl"
    manifest_path = tmp_path / "manifest.json"
    _write_jsonl(lockbox_path, rows)
    _write_jsonl(train_path, [_reference_row("train-row-1", input_text="训练输入")])
    manifest_path.write_text(json.dumps(_manifest(rows), ensure_ascii=False), encoding="utf-8")

    result = validate_lockbox(lockbox_path=lockbox_path, manifest_path=manifest_path, train_paths=[train_path])

    assert result.ok is False
    assert any(failure["category"] == "forbidden_ancestry" for failure in result.failures)


def test_lockbox_fails_forbidden_training_category_in_ancestry(tmp_path: Path) -> None:
    rows = [_lockbox_row("lb-1", derived_from=[{"category": "training"}])]
    lockbox_path = tmp_path / "lockbox.jsonl"
    manifest_path = tmp_path / "manifest.json"
    _write_jsonl(lockbox_path, rows)
    manifest_path.write_text(json.dumps(_manifest(rows), ensure_ascii=False), encoding="utf-8")

    result = validate_lockbox(lockbox_path=lockbox_path, manifest_path=manifest_path)

    assert result.ok is False
    assert any(failure["category"] == "forbidden_ancestry" for failure in result.failures)


def test_lockbox_fails_when_final_row_was_analysis_seen(tmp_path: Path) -> None:
    rows = [_lockbox_row("lb-1", analysis_seen=True)]
    lockbox_path = tmp_path / "lockbox.jsonl"
    manifest_path = tmp_path / "manifest.json"
    _write_jsonl(lockbox_path, rows)
    manifest_path.write_text(json.dumps(_manifest(rows), ensure_ascii=False), encoding="utf-8")

    result = validate_lockbox(lockbox_path=lockbox_path, manifest_path=manifest_path)

    assert result.ok is False
    assert any(failure["category"] == "analysis_seen_violation" for failure in result.failures)


def test_lockbox_fails_for_forbidden_source_category(tmp_path: Path) -> None:
    rows = [_lockbox_row("lb-1")]
    rows[0]["source"] = {"category": "train", "provenance": {"authoring_batch": "unit-test"}}
    rows[0]["content_hash"] = compute_lockbox_row_hash(rows[0])
    lockbox_path = tmp_path / "lockbox.jsonl"
    manifest_path = tmp_path / "manifest.json"
    _write_jsonl(lockbox_path, rows)
    manifest_path.write_text(json.dumps(_manifest(rows), ensure_ascii=False), encoding="utf-8")

    result = validate_lockbox(lockbox_path=lockbox_path, manifest_path=manifest_path)

    assert result.ok is False
    assert any(failure["category"] == "forbidden_source_category" for failure in result.failures)


def test_lockbox_fails_for_normalized_forbidden_source_category(tmp_path: Path) -> None:
    rows = [_lockbox_row("lb-1")]
    rows[0]["source"] = {"category": " Train ", "provenance": {"authoring_batch": "unit-test"}}
    rows[0]["content_hash"] = compute_lockbox_row_hash(rows[0])
    lockbox_path = tmp_path / "lockbox.jsonl"
    manifest_path = tmp_path / "manifest.json"
    _write_jsonl(lockbox_path, rows)
    manifest_path.write_text(json.dumps(_manifest(rows), ensure_ascii=False), encoding="utf-8")

    result = validate_lockbox(lockbox_path=lockbox_path, manifest_path=manifest_path)

    assert result.ok is False
    assert any(failure["category"] == "forbidden_source_category" for failure in result.failures)


def test_lockbox_fails_hash_mismatch_and_duplicate_content_hash(tmp_path: Path) -> None:
    first = _lockbox_row("lb-1")
    duplicate_hash = str(first["content_hash"])
    rows = [first, _lockbox_row("lb-2", content_hash=duplicate_hash)]
    lockbox_path = tmp_path / "lockbox.jsonl"
    manifest_path = tmp_path / "manifest.json"
    _write_jsonl(lockbox_path, rows)
    manifest_path.write_text(json.dumps(_manifest(rows), ensure_ascii=False), encoding="utf-8")

    result = validate_lockbox(lockbox_path=lockbox_path, manifest_path=manifest_path)

    assert result.ok is False
    categories = {failure["category"] for failure in result.failures}
    assert "content_hash_mismatch" in categories
    assert "duplicate_content_hash" in categories


def test_lockbox_fails_manifest_count_hash_mismatch_and_unfrozen_manifest(tmp_path: Path) -> None:
    rows = [_lockbox_row("lb-1")]
    lockbox_path = tmp_path / "lockbox.jsonl"
    manifest_path = tmp_path / "manifest.json"
    _write_jsonl(lockbox_path, rows)
    manifest = _manifest(rows, frozen=False)
    manifest["row_count"] = 2
    manifest["content_hashes"] = ["wrong-hash"]
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")

    result = validate_lockbox(lockbox_path=lockbox_path, manifest_path=manifest_path)

    assert result.ok is False
    categories = {failure["category"] for failure in result.failures}
    assert "manifest_count_mismatch" in categories
    assert "manifest_hash_mismatch" in categories
    assert "manifest_not_frozen" in categories


def test_lockbox_fails_manifest_missing_family_count(tmp_path: Path) -> None:
    rows = [_lockbox_row("lb-1")]
    lockbox_path = tmp_path / "lockbox.jsonl"
    manifest_path = tmp_path / "manifest.json"
    _write_jsonl(lockbox_path, rows)
    manifest = _manifest(rows)
    manifest.pop("family_count")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")

    result = validate_lockbox(lockbox_path=lockbox_path, manifest_path=manifest_path)

    assert result.ok is False
    assert any(failure["category"] == "manifest_family_count_mismatch" for failure in result.failures)


def test_lockbox_fails_manifest_wrong_family_count(tmp_path: Path) -> None:
    rows = [_lockbox_row("lb-1"), _lockbox_row("lb-2", semantic_family_id="lockbox-family-lb-1")]
    lockbox_path = tmp_path / "lockbox.jsonl"
    manifest_path = tmp_path / "manifest.json"
    _write_jsonl(lockbox_path, rows)
    manifest = _manifest(rows)
    manifest["family_count"] = 2
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")

    result = validate_lockbox(lockbox_path=lockbox_path, manifest_path=manifest_path)

    assert result.ok is False
    assert any(failure["category"] == "manifest_family_count_mismatch" for failure in result.failures)


def test_lockbox_fails_manifest_missing_schema_version_or_id(tmp_path: Path) -> None:
    rows = [_lockbox_row("lb-1")]
    lockbox_path = tmp_path / "lockbox.jsonl"
    manifest_path = tmp_path / "manifest.json"
    _write_jsonl(lockbox_path, rows)
    manifest = _manifest(rows)
    manifest.pop("schema_version")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")

    result = validate_lockbox(lockbox_path=lockbox_path, manifest_path=manifest_path)

    assert result.ok is False
    assert any(failure["category"] == "manifest_schema_missing" for failure in result.failures)


def test_lockbox_fails_manifest_missing_frozen_timestamp(tmp_path: Path) -> None:
    rows = [_lockbox_row("lb-1")]
    lockbox_path = tmp_path / "lockbox.jsonl"
    manifest_path = tmp_path / "manifest.json"
    _write_jsonl(lockbox_path, rows)
    manifest = _manifest(rows)
    manifest.pop("created_at")
    manifest.pop("frozen_at")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")

    result = validate_lockbox(lockbox_path=lockbox_path, manifest_path=manifest_path)

    assert result.ok is False
    assert any(failure["category"] == "manifest_timestamp_missing" for failure in result.failures)


def test_lockbox_fails_manifest_missing_provenance_summary(tmp_path: Path) -> None:
    rows = [_lockbox_row("lb-1")]
    lockbox_path = tmp_path / "lockbox.jsonl"
    manifest_path = tmp_path / "manifest.json"
    _write_jsonl(lockbox_path, rows)
    manifest = _manifest(rows)
    manifest.pop("provenance_summary")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")

    result = validate_lockbox(lockbox_path=lockbox_path, manifest_path=manifest_path)

    assert result.ok is False
    assert any(failure["category"] == "manifest_provenance_summary_missing" for failure in result.failures)


def test_lockbox_fails_manifest_dataset_sha256_mismatch(tmp_path: Path) -> None:
    rows = [_lockbox_row("lb-1")]
    lockbox_path = tmp_path / "lockbox.jsonl"
    manifest_path = tmp_path / "manifest.json"
    _write_jsonl(lockbox_path, rows)
    manifest = _manifest(rows)
    manifest["dataset_sha256"] = "wrong-lockbox-hash"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")

    result = validate_lockbox(lockbox_path=lockbox_path, manifest_path=manifest_path)

    assert result.ok is False
    assert any(failure["category"] == "manifest_hash_mismatch" for failure in result.failures)


def test_lockbox_fails_manifest_missing_hash_declaration(tmp_path: Path) -> None:
    rows = [_lockbox_row("lb-1")]
    lockbox_path = tmp_path / "lockbox.jsonl"
    manifest_path = tmp_path / "manifest.json"
    _write_jsonl(lockbox_path, rows)
    manifest = _manifest(rows)
    manifest.pop("lockbox_hash")
    manifest.pop("dataset_sha256")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")

    result = validate_lockbox(lockbox_path=lockbox_path, manifest_path=manifest_path)

    assert result.ok is False
    assert any(failure["category"] == "manifest_hash_mismatch" for failure in result.failures)


def test_lockbox_fails_missing_provenance_fields(tmp_path: Path) -> None:
    rows = [_lockbox_row("lb-1", provenance={})]
    del rows[0]["source"]
    lockbox_path = tmp_path / "lockbox.jsonl"
    manifest_path = tmp_path / "manifest.json"
    _write_jsonl(lockbox_path, rows)
    manifest_path.write_text(json.dumps(_manifest(rows), ensure_ascii=False), encoding="utf-8")

    result = validate_lockbox(lockbox_path=lockbox_path, manifest_path=manifest_path)

    assert result.ok is False
    assert any(failure["category"] == "missing_provenance" for failure in result.failures)


def test_validate_lockbox_cli_outputs_json_and_nonzero_on_failure(tmp_path: Path, capsys) -> None:
    rows = [_lockbox_row("duplicate"), _lockbox_row("duplicate", input_text="另一个输入")]
    lockbox_path = tmp_path / "lockbox.jsonl"
    manifest_path = tmp_path / "manifest.json"
    _write_jsonl(lockbox_path, rows)
    manifest_path.write_text(json.dumps(_manifest(rows), ensure_ascii=False), encoding="utf-8")

    exit_code = data_cli.main(
        [
            "validate-lockbox",
            "--lockbox",
            lockbox_path.as_posix(),
            "--manifest",
            manifest_path.as_posix(),
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 1
    assert payload["ok"] is False
    assert payload["failures"][0]["category"] == "duplicate_row_id"


def test_validate_lockbox_cli_outputs_json_for_input_read_error(tmp_path: Path, capsys) -> None:
    missing_lockbox_path = tmp_path / "missing-lockbox.jsonl"
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps({"manifest_id": "lockbox-unit-test"}, ensure_ascii=False), encoding="utf-8")

    exit_code = data_cli.main(
        [
            "validate-lockbox",
            "--lockbox",
            missing_lockbox_path.as_posix(),
            "--manifest",
            manifest_path.as_posix(),
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 1
    assert payload["ok"] is False
    assert payload["failures"][0]["category"] == "FileNotFoundError"


def test_validate_lockbox_cli_outputs_json_for_parser_error(capsys) -> None:
    exit_code = data_cli.main(["validate-lockbox", "--lockbox", "lockbox.jsonl"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert exit_code == 2
    assert captured.err == ""
    assert payload["ok"] is False
    assert payload["failures"][0]["category"] == "ArgumentParserError"
