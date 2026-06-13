from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from voice2task.io import read_jsonl, write_json, write_jsonl
from voice2task.schemas import (
    BrowserTaskContract,
    DatasetManifest,
    DPOPair,
    SFTDatasetRow,
    as_contract,
    validate_public_record,
)

HARD_NEGATIVE_CATEGORIES = [
    "wrong_task_type",
    "wrong_route",
    "unsafe_allowance",
    "missing_confirmation",
    "missing_slot",
    "wrong_slot",
    "decomposed_search_slots",
    "extract_search_fallback",
    "extract_query_slot",
    "extract_generic_price_wording",
    "extract_listed_price_wording",
    "extract_extra_particle_wording",
    "clarify_action_drift",
    "blocked_payment_action_drift",
    "form_confirmation_drift",
    "navigate_canonical_url_drift",
    "underspecified_request",
    "malformed_schema",
]

EXTRACT_PRICE_CANONICAL_TARGET = "商品价格"
EXTRACT_PRICE_CANONICAL_NORMALIZED_COMMAND = "提取页面商品价格"


def _now_id(prefix: str) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{prefix}-{stamp}"


def _read_seed_rows(seed_path: Path) -> list[dict[str, Any]]:
    raw_rows = read_jsonl(seed_path)
    for row in raw_rows:
        as_contract(row["target_contract"])
    return raw_rows


def _compact_query_phrase(value: str) -> str:
    return "".join(value.split())


def _canonical_public_search_target(contract: BrowserTaskContract | dict[str, Any]) -> BrowserTaskContract:
    target = as_contract(contract)
    if not (
        target.task_type == "search"
        and target.route == "search_web"
        and bool(target.safety.get("allow")) is True
        and target.safety.get("reason") == "public_readonly"
        and target.confirmation_required is False
    ):
        return target

    normalized_suffix = ""
    if target.normalized_command.startswith("搜索"):
        normalized_suffix = _compact_query_phrase(target.normalized_command.removeprefix("搜索"))
    query_value = target.slots.get("query")
    if normalized_suffix:
        compact_query = normalized_suffix
    elif isinstance(query_value, str):
        compact_query = _compact_query_phrase(query_value)
    else:
        compact_query = ""
    if not compact_query:
        return target

    return _replace_contract(
        target,
        slots={"query": compact_query},
        normalized_command=f"搜索{compact_query}",
    )


def _base_row(seed: dict[str, Any], public_safe: bool) -> SFTDatasetRow:
    target_contract = seed["target_contract"]
    if public_safe:
        target_contract = _canonical_public_search_target(target_contract)
    provenance = {
        "source_id": seed["id"],
        "source_mode": "sanitized_seed",
        "public_safe": public_safe,
        "augmentation": "original",
    }
    return SFTDatasetRow(
        id=seed["id"],
        split=seed["split"],
        input_text=seed["input_text"],
        target_contract=target_contract,
        provenance=provenance,
    )


def expand_sft_rows(seed_rows: list[dict[str, Any]], public_safe: bool) -> list[SFTDatasetRow]:
    rows: list[SFTDatasetRow] = []
    for seed in seed_rows:
        base = _base_row(seed, public_safe=public_safe)
        rows.append(base)
        for index, paraphrase in enumerate(seed.get("augmentations", []), start=1):
            rows.append(
                SFTDatasetRow(
                    id=f"{seed['id']}-aug-{index}",
                    split=seed["split"],
                    input_text=paraphrase,
                    target_contract=base.target_contract,
                    provenance={
                        "source_id": seed["id"],
                        "source_mode": "schema_preserving_augmentation",
                        "public_safe": public_safe,
                        "augmentation": f"paraphrase-{index}",
                    },
                )
            )
    return rows


def _replace_contract(contract: BrowserTaskContract, **updates: Any) -> BrowserTaskContract:
    data = contract.to_dict()
    data.update(updates)
    return BrowserTaskContract.from_dict(data)


def _decomposed_weather_slots(query: str) -> dict[str, str] | None:
    compact = _compact_query_phrase(query)
    if not compact.endswith("天气"):
        return None
    stem = compact.removesuffix("天气")
    for date in ("今天", "明天", "后天"):
        if stem.endswith(date):
            city = stem[: -len(date)]
            if city:
                return {"city": city, "date": date, "topic": ""}
    return None


def _decomposed_search_slots_negative(contract: BrowserTaskContract) -> BrowserTaskContract | None:
    if not (
        contract.task_type == "search"
        and contract.route == "search_web"
        and bool(contract.safety.get("allow")) is True
        and contract.safety.get("reason") == "public_readonly"
        and contract.confirmation_required is False
    ):
        return None
    query = contract.slots.get("query")
    if not isinstance(query, str):
        return None
    decomposed_slots = _decomposed_weather_slots(query)
    if decomposed_slots is None:
        return None
    return _replace_contract(
        contract,
        slots=decomposed_slots,
        safety={**contract.safety, "reason": "decomposed_search_slots"},
    )


def _public_extract_target(contract: BrowserTaskContract) -> str | None:
    if not (
        contract.task_type == "extract"
        and contract.route == "extract_page"
        and bool(contract.safety.get("allow")) is True
        and contract.safety.get("reason") == "public_readonly"
        and contract.confirmation_required is False
    ):
        return None
    target = contract.slots.get("target")
    if not isinstance(target, str) or not target:
        return None
    return target


def _extract_search_fallback_negative(contract: BrowserTaskContract) -> BrowserTaskContract | None:
    target = _public_extract_target(contract)
    if target is None:
        return None
    return _replace_contract(
        contract,
        task_type="search",
        route="search_web",
        slots={"query": target},
        normalized_command=f"搜索{target}",
        safety={**contract.safety, "reason": "extract_search_fallback"},
    )


def _extract_query_slot_negative(contract: BrowserTaskContract) -> BrowserTaskContract | None:
    target = _public_extract_target(contract)
    if target is None:
        return None
    return _replace_contract(
        contract,
        slots={"query": target, "page_url": ""},
        safety={**contract.safety, "reason": "extract_query_slot"},
    )


def _public_extract_price_canonical_contract(contract: BrowserTaskContract) -> bool:
    return (
        _public_extract_target(contract) == EXTRACT_PRICE_CANONICAL_TARGET
        and contract.normalized_command == EXTRACT_PRICE_CANONICAL_NORMALIZED_COMMAND
    )


def _extract_generic_price_wording_negative(contract: BrowserTaskContract) -> BrowserTaskContract | None:
    if not _public_extract_price_canonical_contract(contract):
        return None
    return _replace_contract(
        contract,
        slots={"target": "价格"},
        normalized_command="页面价格",
        safety={**contract.safety, "reason": "extract_generic_price_wording"},
    )


def _extract_listed_price_wording_negative(contract: BrowserTaskContract) -> BrowserTaskContract | None:
    if not _public_extract_price_canonical_contract(contract):
        return None
    return _replace_contract(
        contract,
        slots={"target": "标价"},
        normalized_command="提取页面标价",
        safety={**contract.safety, "reason": "extract_listed_price_wording"},
    )


def _extract_extra_particle_wording_negative(contract: BrowserTaskContract) -> BrowserTaskContract | None:
    if not _public_extract_price_canonical_contract(contract):
        return None
    return _replace_contract(
        contract,
        normalized_command="提取页面上的商品价格",
        safety={**contract.safety, "reason": "extract_extra_particle_wording"},
    )


def _public_clarify_contract(contract: BrowserTaskContract) -> bool:
    return (
        contract.task_type == "clarify"
        and contract.route == "clarify"
        and bool(contract.safety.get("allow")) is True
        and contract.safety.get("reason") == "ambiguous_request"
        and contract.confirmation_required is True
        and isinstance(contract.slots.get("ambiguity"), str)
    )


def _clarify_action_drift_negative(contract: BrowserTaskContract) -> BrowserTaskContract | None:
    if not _public_clarify_contract(contract):
        return None
    return _replace_contract(
        contract,
        task_type="search",
        route="search_web",
        safety={"allow": True, "reason": "public_readonly"},
        confirmation_required=False,
        slots={"query": "公开信息"},
        normalized_command="搜索公开信息",
    )


def _public_blocked_payment_contract(contract: BrowserTaskContract) -> bool:
    return (
        contract.task_type == "blocked"
        and contract.route == "deny"
        and bool(contract.safety.get("allow")) is False
        and contract.safety.get("reason") == "unsafe_payment"
        and contract.confirmation_required is True
        and contract.slots.get("reason") == "payment_requires_user_control"
    )


def _blocked_payment_action_drift_negative(contract: BrowserTaskContract) -> BrowserTaskContract | None:
    if not _public_blocked_payment_contract(contract):
        return None
    return _replace_contract(
        contract,
        task_type="search",
        route="search_web",
        safety={"allow": True, "reason": "public_readonly"},
        confirmation_required=False,
        slots={"query": "付款"},
        normalized_command="搜索付款",
    )


def _public_form_confirmation_contract(contract: BrowserTaskContract) -> str | None:
    if not (
        contract.task_type == "form_fill"
        and contract.route == "fill_form"
        and bool(contract.safety.get("allow")) is True
        and contract.safety.get("reason") == "requires_confirmation"
        and contract.confirmation_required is True
    ):
        return None
    field = contract.slots.get("field")
    return field if isinstance(field, str) and field else None


def _form_confirmation_drift_negative(contract: BrowserTaskContract) -> BrowserTaskContract | None:
    field = _public_form_confirmation_contract(contract)
    if field is None:
        return None
    return _replace_contract(
        contract,
        safety={"allow": True, "reason": "public_readonly"},
        confirmation_required=False,
        slots={"email": field},
    )


def _public_navigate_contract(contract: BrowserTaskContract) -> str | None:
    if not (
        contract.task_type == "navigate"
        and contract.route == "open_url"
        and bool(contract.safety.get("allow")) is True
        and contract.safety.get("reason") == "public_readonly"
        and contract.confirmation_required is False
    ):
        return None
    url = contract.slots.get("url")
    return url if isinstance(url, str) and url.startswith("https://") else None


def _navigate_canonical_url_drift_negative(contract: BrowserTaskContract) -> BrowserTaskContract | None:
    url = _public_navigate_contract(contract)
    if url is None:
        return None
    host = url.removeprefix("https://")
    return _replace_contract(
        contract,
        slots={"url": host},
        normalized_command=f"打开 {host}",
        safety={**contract.safety, "reason": "navigate_canonical_url_drift"},
    )


_TASK_TYPE_SWAPS: dict[str, str] = {
    "search": "navigate",
    "navigate": "search",
    "form_fill": "extract",
    "extract": "form_fill",
    "clarify": "search",
    "blocked": "navigate",
}


def _negative_contract(contract: BrowserTaskContract, category: str) -> BrowserTaskContract | dict[str, Any]:
    if category == "wrong_task_type":
        wrong_type = _TASK_TYPE_SWAPS.get(contract.task_type, "search")
        return _replace_contract(
            contract,
            task_type=wrong_type,
            safety={**contract.safety, "reason": "wrong_task_type"},
        )
    if category == "wrong_route":
        route = "open_url" if contract.route != "open_url" else "search_web"
        return _replace_contract(contract, route=route, safety={**contract.safety, "reason": "wrong_route"})
    if category == "unsafe_allowance":
        safety = {"allow": not bool(contract.safety["allow"]), "reason": "unsafe_allowance"}
        return _replace_contract(contract, safety=safety)
    if category == "missing_confirmation":
        return _replace_contract(
            contract,
            confirmation_required=False,
            safety={**contract.safety, "reason": "missing_confirmation"},
        )
    if category == "missing_slot":
        slots = dict(contract.slots)
        if slots:
            slots.pop(next(iter(slots)))
        return _replace_contract(contract, slots=slots, safety={**contract.safety, "reason": "missing_slot"})
    if category == "wrong_slot":
        slots = dict(contract.slots)
        if slots:
            first_key = next(iter(slots))
            slots[first_key] = f"{slots[first_key]}_wrong"
        else:
            slots["missing"] = "wrong"
        return _replace_contract(contract, slots=slots, safety={**contract.safety, "reason": "wrong_slot"})
    if category == "decomposed_search_slots":
        decomposed = _decomposed_search_slots_negative(contract)
        if decomposed is None:
            raise ValueError("decomposed_search_slots applies only to compact public-readonly weather search")
        return decomposed
    if category == "extract_search_fallback":
        search_fallback = _extract_search_fallback_negative(contract)
        if search_fallback is None:
            raise ValueError("extract_search_fallback applies only to public-readonly extract_page target contracts")
        return search_fallback
    if category == "extract_query_slot":
        query_slot = _extract_query_slot_negative(contract)
        if query_slot is None:
            raise ValueError("extract_query_slot applies only to public-readonly extract_page target contracts")
        return query_slot
    if category == "extract_generic_price_wording":
        generic_price = _extract_generic_price_wording_negative(contract)
        if generic_price is None:
            raise ValueError("extract_generic_price_wording applies only to canonical public extract-price contracts")
        return generic_price
    if category == "extract_listed_price_wording":
        listed_price = _extract_listed_price_wording_negative(contract)
        if listed_price is None:
            raise ValueError("extract_listed_price_wording applies only to canonical public extract-price contracts")
        return listed_price
    if category == "extract_extra_particle_wording":
        extra_particle = _extract_extra_particle_wording_negative(contract)
        if extra_particle is None:
            raise ValueError("extract_extra_particle_wording applies only to canonical public extract-price contracts")
        return extra_particle
    if category == "clarify_action_drift":
        clarify_drift = _clarify_action_drift_negative(contract)
        if clarify_drift is None:
            raise ValueError("clarify_action_drift applies only to public ambiguous clarify contracts")
        return clarify_drift
    if category == "blocked_payment_action_drift":
        blocked_drift = _blocked_payment_action_drift_negative(contract)
        if blocked_drift is None:
            raise ValueError("blocked_payment_action_drift applies only to public unsafe payment block contracts")
        return blocked_drift
    if category == "form_confirmation_drift":
        form_drift = _form_confirmation_drift_negative(contract)
        if form_drift is None:
            raise ValueError("form_confirmation_drift applies only to confirmation-required public form contracts")
        return form_drift
    if category == "navigate_canonical_url_drift":
        navigate_drift = _navigate_canonical_url_drift_negative(contract)
        if navigate_drift is None:
            raise ValueError("navigate_canonical_url_drift applies only to public canonical navigation contracts")
        return navigate_drift
    if category == "underspecified_request":
        return _replace_contract(
            contract,
            route="clarify",
            confirmation_required=True,
            slots={},
            safety={**contract.safety, "reason": "underspecified_request"},
        )
    if category == "malformed_schema":
        malformed = contract.to_dict()
        malformed.pop("route", None)
        malformed["malformed_reason"] = "route_removed"
        return malformed
    raise ValueError(f"unknown hard-negative category: {category}")


def generate_hard_negative_pairs(rows: list[SFTDatasetRow]) -> list[DPOPair]:
    pairs: list[DPOPair] = []
    for row in rows:
        if row.provenance.get("augmentation") != "original":
            continue
        chosen = as_contract(row.target_contract)
        for category in HARD_NEGATIVE_CATEGORIES:
            if category == "missing_confirmation" and not chosen.confirmation_required:
                continue
            if category == "decomposed_search_slots":
                if row.provenance.get("public_safe") is not True or _decomposed_search_slots_negative(chosen) is None:
                    continue
            if category == "extract_search_fallback":
                if row.provenance.get("public_safe") is not True or _extract_search_fallback_negative(chosen) is None:
                    continue
            if category == "extract_query_slot":
                if row.provenance.get("public_safe") is not True or _extract_query_slot_negative(chosen) is None:
                    continue
            if category == "extract_generic_price_wording":
                if (
                    row.provenance.get("public_safe") is not True
                    or _extract_generic_price_wording_negative(chosen) is None
                ):
                    continue
            if category == "extract_listed_price_wording":
                if (
                    row.provenance.get("public_safe") is not True
                    or _extract_listed_price_wording_negative(chosen) is None
                ):
                    continue
            if category == "extract_extra_particle_wording":
                if (
                    row.provenance.get("public_safe") is not True
                    or _extract_extra_particle_wording_negative(chosen) is None
                ):
                    continue
            if category == "clarify_action_drift":
                if row.provenance.get("public_safe") is not True or _clarify_action_drift_negative(chosen) is None:
                    continue
            if category == "blocked_payment_action_drift":
                if (
                    row.provenance.get("public_safe") is not True
                    or _blocked_payment_action_drift_negative(chosen) is None
                ):
                    continue
            if category == "form_confirmation_drift":
                if row.provenance.get("public_safe") is not True or _form_confirmation_drift_negative(chosen) is None:
                    continue
            if category == "navigate_canonical_url_drift":
                if (
                    row.provenance.get("public_safe") is not True
                    or _navigate_canonical_url_drift_negative(chosen) is None
                ):
                    continue
            pairs.append(
                DPOPair(
                    id=f"{row.id}-{category}",
                    split=row.split,
                    input_text=row.input_text,
                    chosen_contract=chosen,
                    rejected_contract=_negative_contract(chosen, category),
                    rejection_reason=category,
                    provenance={
                        "source_id": row.provenance.get("source_id", row.id),
                        "source_mode": "hard_negative",
                        "public_safe": row.provenance.get("public_safe", False),
                    },
                )
            )
    return pairs


def _split_counts(rows: list[SFTDatasetRow]) -> dict[str, int]:
    counts = Counter(row.split for row in rows)
    return {split: counts.get(split, 0) for split in ("train", "dev", "test")}


def _rejection_counts(pairs: list[DPOPair]) -> dict[str, int]:
    counts = Counter(pair.rejection_reason for pair in pairs)
    return {category: counts.get(category, 0) for category in HARD_NEGATIVE_CATEGORIES}


def _write_manifest(path: Path, manifest: DatasetManifest) -> None:
    write_json(path, manifest.to_dict())


def build_public_sample_dataset(seed_path: Path, output_dir: Path) -> DatasetManifest:
    seed_rows = _read_seed_rows(seed_path)
    rows = expand_sft_rows(seed_rows, public_safe=True)
    pairs = generate_hard_negative_pairs(rows)
    for row in rows:
        validate_public_record(row.to_dict())
    for pair in pairs:
        validate_public_record(pair.to_dict())

    sft_path = output_dir / "sft_public_sample.jsonl"
    dpo_path = output_dir / "dpo_public_sample.jsonl"
    manifest_path = output_dir / "manifest_public_sample.json"
    write_jsonl(sft_path, [row.to_dict() for row in rows])
    write_jsonl(dpo_path, [pair.to_dict() for pair in pairs])

    manifest = DatasetManifest(
        manifest_id=_now_id("public-sample"),
        mode="public_sample",
        generated_at=datetime.now(timezone.utc).isoformat(),
        files={
            "seed": seed_path.as_posix(),
            "sft": sft_path.as_posix(),
            "dpo": dpo_path.as_posix(),
            "manifest": manifest_path.as_posix(),
        },
        counts={"seed_rows": len(seed_rows), "sft_rows": len(rows), "dpo_pairs": len(pairs)},
        split_counts=_split_counts(rows),
        dpo_rejection_counts=_rejection_counts(pairs),
        source_summary={"seed_rows": len(seed_rows), "source": "sanitized_public_seed_fixture"},
        public_safe=True,
    )
    _write_manifest(manifest_path, manifest)
    return manifest


def build_local_private_corpus(seed_trace_path: Path, output_dir: Path) -> DatasetManifest:
    seed_rows = _read_seed_rows(seed_trace_path)
    rows = expand_sft_rows(seed_rows, public_safe=False)
    pairs = generate_hard_negative_pairs(rows)

    split_files: dict[str, str] = {}
    for split in ("train", "dev", "test"):
        path = output_dir / f"{split}.jsonl"
        write_jsonl(path, [row.to_dict() for row in rows if row.split == split])
        split_files[split] = path.as_posix()
    dpo_path = output_dir / "dpo_pairs.jsonl"
    manifest_path = output_dir / "manifest_local_private.json"
    write_jsonl(dpo_path, [pair.to_dict() for pair in pairs])

    manifest = DatasetManifest(
        manifest_id=_now_id("local-private"),
        mode="local_private",
        generated_at=datetime.now(timezone.utc).isoformat(),
        files={**split_files, "dpo": dpo_path.as_posix(), "manifest": manifest_path.as_posix()},
        counts={"seed_rows": len(seed_rows), "sft_rows": len(rows), "dpo_pairs": len(pairs)},
        split_counts=_split_counts(rows),
        dpo_rejection_counts=_rejection_counts(pairs),
        source_summary={
            "seed_rows": len(seed_rows),
            "source": "configured_voice_to_browser_agent_seed_trace_path",
            "raw_rows_committed": 0,
        },
        public_safe=False,
    )
    _write_manifest(manifest_path, manifest)
    return manifest
