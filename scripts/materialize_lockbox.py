from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from voice2task.io import read_jsonl, write_json
from voice2task.lockbox import compute_lockbox_manifest_hash, compute_lockbox_row_hash


def _without_content_hash(row: dict[str, Any]) -> dict[str, Any]:
    payload = dict(row)
    payload.pop("content_hash", None)
    return payload


def _write_jsonl_preserving_key_order(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")


def _timestamp(value: str | None) -> str:
    if value:
        return value
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _source_category(row: dict[str, Any]) -> str:
    source = row.get("source")
    if isinstance(source, dict):
        category = source.get("category")
        if isinstance(category, str) and category.strip():
            return category.strip()
    return "<missing>"


def materialize_lockbox(
    *,
    draft_path: Path,
    lockbox_path: Path,
    manifest_path: Path,
    manifest_id: str,
    schema_version: str,
    created_at: str,
    frozen_at: str,
) -> dict[str, Any]:
    draft_rows = read_jsonl(draft_path)
    lockbox_rows: list[dict[str, Any]] = []
    content_hashes: list[str] = []

    for line_number, row in enumerate(draft_rows, start=1):
        materialized_row = dict(row)
        materialized_row["content_hash"] = compute_lockbox_row_hash(row)
        if _without_content_hash(row) != _without_content_hash(materialized_row):
            row_id = row.get("row_id", f"<line-{line_number}>")
            raise ValueError(f"{row_id}: materialization changed non-content_hash fields")
        lockbox_rows.append(materialized_row)
        content_hashes.append(str(materialized_row["content_hash"]))

    lockbox_hash = compute_lockbox_manifest_hash(content_hashes)
    provenance_summary = dict(sorted(Counter(_source_category(row) for row in draft_rows).items()))
    family_ids = {
        family_id.strip()
        for row in draft_rows
        if isinstance((family_id := row.get("semantic_family_id")), str) and family_id.strip()
    }
    manifest: dict[str, Any] = {
        "manifest_id": manifest_id,
        "schema_version": schema_version,
        "created_at": created_at,
        "frozen_at": frozen_at,
        "frozen": True,
        "row_count": len(lockbox_rows),
        "family_count": len(family_ids),
        "provenance_summary": provenance_summary,
        "content_hashes": content_hashes,
        "lockbox_hash": lockbox_hash,
        "dataset_sha256": lockbox_hash,
    }

    _write_jsonl_preserving_key_order(lockbox_path, lockbox_rows)
    write_json(manifest_path, manifest)
    return {
        "ok": True,
        "draft_path": draft_path.as_posix(),
        "lockbox_path": lockbox_path.as_posix(),
        "manifest_path": manifest_path.as_posix(),
        "row_count": len(lockbox_rows),
        "family_count": len(family_ids),
        "lockbox_hash": lockbox_hash,
        "provenance_summary": provenance_summary,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Materialize a reviewed lockbox draft without changing row content.")
    parser.add_argument("--draft", type=Path, required=True)
    parser.add_argument("--lockbox", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--manifest-id", default=None)
    parser.add_argument("--schema-version", default="lockbox.v1")
    parser.add_argument("--created-at", default=None)
    parser.add_argument("--frozen-at", default=None)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    frozen_at = _timestamp(args.frozen_at)
    created_at = _timestamp(args.created_at or frozen_at)
    manifest_id = args.manifest_id or f"lockbox-v1-{frozen_at.replace('-', '').replace(':', '')}"
    payload = materialize_lockbox(
        draft_path=args.draft,
        lockbox_path=args.lockbox,
        manifest_path=args.manifest,
        manifest_id=manifest_id,
        schema_version=args.schema_version,
        created_at=created_at,
        frozen_at=frozen_at,
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
