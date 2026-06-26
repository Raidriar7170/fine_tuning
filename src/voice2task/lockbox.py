from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from voice2task.io import read_json, read_jsonl
from voice2task.schemas import as_contract

Failure = dict[str, Any]
FORBIDDEN_SOURCE_CATEGORIES = {"train", "training", "remediation", "analysis"}


@dataclass(frozen=True)
class LockboxValidationResult:
    ok: bool
    failures: list[Failure]
    counts: dict[str, int]
    manifest: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "failures": self.failures,
            "counts": self.counts,
            "manifest": self.manifest,
        }


def normalize_input_text(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).casefold()
    return "".join(
        char
        for char in normalized
        if not char.isspace() and not unicodedata.category(char).startswith(("P", "S"))
    )


def compute_lockbox_row_hash(row: dict[str, Any]) -> str:
    payload = dict(row)
    payload.pop("content_hash", None)
    if "gold_contract" in payload:
        payload["gold_contract"] = as_contract(payload["gold_contract"]).to_dict()
    if isinstance(payload.get("derived_from"), list):
        payload["derived_from"] = _canonical_ancestry(payload["derived_from"])
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def compute_lockbox_manifest_hash(content_hashes: list[str]) -> str:
    canonical = json.dumps(content_hashes, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def validate_lockbox(
    *,
    lockbox_path: Path,
    manifest_path: Path,
    train_paths: list[Path] | None = None,
    analysis_paths: list[Path] | None = None,
    require_family_disjointness: bool = False,
) -> LockboxValidationResult:
    failures: list[Failure] = []
    train_paths = train_paths or []
    analysis_paths = analysis_paths or []
    lockbox_rows = read_jsonl(lockbox_path)
    manifest = read_json(manifest_path)
    train_rows = _read_reference_rows(train_paths)
    analysis_rows = _read_reference_rows(analysis_paths)

    reference_rows = [
        *(_reference_record(row, "train") for row in train_rows),
        *(_reference_record(row, "analysis") for row in analysis_rows),
    ]
    reference_exact_inputs = _index_reference_values(reference_rows, "input_text")
    reference_normalized_inputs = _index_reference_values(reference_rows, "normalized_input_text")
    reference_family_ids = _index_reference_values(reference_rows, "semantic_family_id")
    forbidden_ancestor_ids = _forbidden_ancestor_ids(reference_rows)

    row_ids: dict[str, int] = {}
    content_hashes: dict[str, int] = {}
    computed_hashes: list[str] = []

    for index, row in enumerate(lockbox_rows, start=1):
        row_id = _string_field(row, "row_id")
        if row_id is None:
            failures.append(_failure("missing_required_field", "<missing-row-id>", "row_id is required"))
            row_id = f"<row-{index}>"
        _validate_required_row_fields(row, row_id, failures)

        if row_id in row_ids:
            failures.append(
                _failure("duplicate_row_id", row_id, "lockbox row_id must be unique", first_line=row_ids[row_id])
            )
        else:
            row_ids[row_id] = index

        expected_hash = _safe_compute_row_hash(row, row_id, failures)
        if expected_hash is not None:
            computed_hashes.append(expected_hash)
        declared_hash = _string_field(row, "content_hash")
        if declared_hash is None:
            failures.append(_failure("missing_required_field", row_id, "content_hash is required"))
        else:
            if declared_hash in content_hashes:
                failures.append(
                    _failure(
                        "duplicate_content_hash",
                        row_id,
                        "lockbox content_hash must be unique",
                        first_line=content_hashes[declared_hash],
                    )
                )
            else:
                content_hashes[declared_hash] = index
            if expected_hash is not None and declared_hash != expected_hash:
                failures.append(
                    _failure(
                        "content_hash_mismatch",
                        row_id,
                        "declared content_hash does not match deterministic row hash",
                        expected=expected_hash,
                        observed=declared_hash,
                    )
                )

        input_text = _string_field(row, "input_text")
        if input_text is not None:
            _check_overlap(
                failures,
                category="exact_input_text_overlap",
                row_id=row_id,
                value=input_text,
                references=reference_exact_inputs,
            )
            normalized_input = normalize_input_text(input_text)
            _check_overlap(
                failures,
                category="normalized_input_text_overlap",
                row_id=row_id,
                value=normalized_input,
                references=reference_normalized_inputs,
            )

        family_id = _semantic_family_id(row)
        if require_family_disjointness and family_id:
            _check_overlap(
                failures,
                category="semantic_family_overlap",
                row_id=row_id,
                value=family_id,
                references=reference_family_ids,
            )

        ancestry = row.get("derived_from")
        if isinstance(ancestry, list):
            forbidden_matches = sorted(
                {
                    ancestor
                    for ancestor in _flatten_ancestry(ancestry)
                    if _is_forbidden_ancestor(ancestor, forbidden_ancestor_ids)
                }
            )
            for ancestor in forbidden_matches:
                failures.append(
                    _failure(
                        "forbidden_ancestry",
                        row_id,
                        "lockbox ancestry must not reach train or remediation rows",
                        ancestor=ancestor,
                    )
                )

    _validate_manifest(manifest, computed_hashes, len(lockbox_rows), failures)

    counts = {
        "lockbox_rows": len(lockbox_rows),
        "train_rows": len(train_rows),
        "analysis_rows": len(analysis_rows),
    }
    return LockboxValidationResult(
        ok=not failures,
        failures=failures,
        counts=counts,
        manifest={
            "path": manifest_path.as_posix(),
            "manifest_id": manifest.get("manifest_id"),
            "frozen": manifest.get("frozen"),
            "row_count": manifest.get("row_count"),
            "lockbox_hash": manifest.get("lockbox_hash", manifest.get("lockbox_sha256")),
        },
    )


def _read_reference_rows(paths: list[Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in paths:
        rows.extend(read_jsonl(path))
    return rows


def _reference_record(row: dict[str, Any], source: str) -> dict[str, str]:
    input_text = str(row.get("input_text", ""))
    return {
        "source": source,
        "row_id": _record_id(row),
        "lineage_ids": "\n".join(sorted(_lineage_ids(row))),
        "input_text": input_text,
        "normalized_input_text": normalize_input_text(input_text),
        "semantic_family_id": _semantic_family_id(row),
    }


def _record_id(row: dict[str, Any]) -> str:
    row_id = row.get("row_id", row.get("id"))
    if isinstance(row_id, str) and row_id:
        return row_id
    return "<unknown>"


def _semantic_family_id(row: dict[str, Any]) -> str:
    value = row.get("semantic_family_id")
    if isinstance(value, str) and value.strip():
        return value
    provenance = row.get("provenance")
    if isinstance(provenance, dict):
        for key in (
            "semantic_family_id",
            "family_id",
            "candidate_family",
            "source_family_id",
        ):
            nested_value = provenance.get(key)
            if isinstance(nested_value, str) and nested_value.strip():
                return nested_value
    return ""


def _index_reference_values(rows: list[dict[str, str]], field_name: str) -> dict[str, list[dict[str, str]]]:
    indexed: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        value = row.get(field_name, "")
        if value:
            indexed.setdefault(value, []).append(row)
    return indexed


def _forbidden_ancestor_ids(reference_rows: list[dict[str, str]]) -> set[str]:
    forbidden: set[str] = set()
    for row in reference_rows:
        if row["source"] != "train":
            continue
        if row["row_id"]:
            forbidden.add(row["row_id"])
        forbidden.update(identifier for identifier in row["lineage_ids"].splitlines() if identifier)
    return forbidden


def _string_field(row: dict[str, Any], field_name: str) -> str | None:
    value = row.get(field_name)
    if isinstance(value, str) and value.strip():
        return value
    return None


def _validate_required_row_fields(row: dict[str, Any], row_id: str, failures: list[Failure]) -> None:
    required_string_fields = ("semantic_family_id", "input_text")
    for field_name in required_string_fields:
        if _string_field(row, field_name) is None:
            failures.append(_failure("missing_required_field", row_id, f"{field_name} is required"))
    if "gold_contract" not in row:
        failures.append(_failure("missing_required_field", row_id, "gold_contract is required"))
    if not isinstance(row.get("derived_from"), list):
        failures.append(_failure("missing_required_field", row_id, "derived_from must be a list"))
    if not isinstance(row.get("analysis_seen"), bool):
        failures.append(_failure("missing_required_field", row_id, "analysis_seen must be a boolean"))
    elif row["analysis_seen"] is True:
        failures.append(_failure("analysis_seen_violation", row_id, "final lockbox rows must set analysis_seen=false"))

    source = row.get("source")
    if not isinstance(source, dict):
        failures.append(_failure("missing_provenance", row_id, "source must contain category and provenance"))
        return
    category = source.get("category")
    provenance = source.get("provenance")
    if not isinstance(category, str) or not category.strip():
        failures.append(_failure("missing_provenance", row_id, "source.category is required"))
    elif category.strip().casefold() in FORBIDDEN_SOURCE_CATEGORIES:
        failures.append(
            _failure(
                "forbidden_source_category",
                row_id,
                "lockbox row source.category must not be train, analysis, or remediation",
                source_category=category,
            )
        )
    if not isinstance(provenance, dict) or not provenance:
        failures.append(_failure("missing_provenance", row_id, "source.provenance must be a non-empty object"))


def _safe_compute_row_hash(row: dict[str, Any], row_id: str, failures: list[Failure]) -> str | None:
    try:
        return compute_lockbox_row_hash(row)
    except Exception as exc:  # noqa: BLE001 - validation must report all row failures as JSON.
        failures.append(_failure(type(exc).__name__, row_id, str(exc)))
        return None


def _check_overlap(
    failures: list[Failure],
    *,
    category: str,
    row_id: str,
    value: str,
    references: dict[str, list[dict[str, str]]],
) -> None:
    for reference in references.get(value, []):
        failures.append(
            _failure(
                category,
                row_id,
                f"{category} with {reference['source']} data",
                reference_row_id=reference["row_id"],
                reference_source=reference["source"],
            )
        )


def _flatten_ancestry(ancestry: list[Any]) -> list[str]:
    values: list[str] = []
    for item in ancestry:
        if isinstance(item, str):
            values.append(item)
        elif isinstance(item, dict):
            for key in (
                "row_id",
                "id",
                "source_id",
                "source_case_id",
                "source_candidate_id",
                "source_row_id",
                "category",
                "source_category",
                "provenance_category",
            ):
                value = item.get(key)
                if isinstance(value, str) and value:
                    values.append(value)
            provenance = item.get("provenance")
            if isinstance(provenance, dict):
                for key in ("source_id", "source_case_id", "source_candidate_id", "source_row_id"):
                    value = provenance.get(key)
                    if isinstance(value, str) and value:
                        values.append(value)
            nested = item.get("derived_from")
            if isinstance(nested, list):
                values.extend(_flatten_ancestry(nested))
    return values


def _lineage_ids(row: dict[str, Any]) -> set[str]:
    identifiers = {_record_id(row)}
    provenance = row.get("provenance")
    if isinstance(provenance, dict):
        for key in (
            "source_id",
            "source_case_id",
            "source_candidate_id",
            "source_row_id",
            "source_family_id",
            "candidate_family",
        ):
            value = provenance.get(key)
            if isinstance(value, str) and value:
                identifiers.add(value)
        for key in ("source_row_ids", "source_ids", "derived_from"):
            values = provenance.get(key)
            if isinstance(values, list):
                identifiers.update(value for value in values if isinstance(value, str) and value)
    return identifiers


def _canonical_ancestry(ancestry: list[Any]) -> list[Any]:
    return sorted(ancestry, key=lambda value: json.dumps(value, ensure_ascii=False, sort_keys=True))


def _is_forbidden_ancestor(ancestor: str, forbidden_train_ids: set[str]) -> bool:
    lowered = ancestor.strip().casefold()
    return (
        ancestor in forbidden_train_ids
        or lowered in FORBIDDEN_SOURCE_CATEGORIES
        or bool(re.search(r"\b(train|training|remediation)\b", lowered))
    )


def _validate_manifest(
    manifest: dict[str, Any],
    computed_hashes: list[str],
    row_count: int,
    failures: list[Failure],
) -> None:
    manifest_id = str(manifest.get("manifest_id", "manifest"))
    if manifest.get("frozen") is not True:
        failures.append(_failure("manifest_not_frozen", manifest_id, "final lockbox manifest must set frozen=true"))
    if manifest.get("row_count") != row_count:
        failures.append(
            _failure(
                "manifest_count_mismatch",
                manifest_id,
                "manifest row_count must match lockbox row count",
                expected=row_count,
                observed=manifest.get("row_count"),
            )
        )
    manifest_hashes = manifest.get("content_hashes")
    observed_lockbox_hash = manifest.get("lockbox_hash", manifest.get("lockbox_sha256"))
    if manifest_hashes is None and observed_lockbox_hash is None:
        failures.append(
            _failure(
                "manifest_hash_mismatch",
                manifest_id,
                "manifest must declare content_hashes or lockbox_hash",
            )
        )
    if manifest_hashes is not None and manifest_hashes != computed_hashes:
        failures.append(
            _failure(
                "manifest_hash_mismatch",
                manifest_id,
                "manifest content_hashes must match deterministic lockbox row hashes in row order",
            )
        )
    expected_lockbox_hash = compute_lockbox_manifest_hash(computed_hashes)
    if observed_lockbox_hash is not None and observed_lockbox_hash != expected_lockbox_hash:
        failures.append(
            _failure(
                "manifest_hash_mismatch",
                manifest_id,
                "manifest lockbox_hash must match deterministic hash over row content hashes",
                expected=expected_lockbox_hash,
                observed=observed_lockbox_hash,
            )
        )


def _failure(category: str, row_id: str, message: str, **details: Any) -> Failure:
    payload: Failure = {
        "category": category,
        "row_id": row_id,
        "message": message,
    }
    payload.update(details)
    return payload
