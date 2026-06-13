from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from voice2task.io import read_jsonl
from voice2task.schemas import DPOPair, ValidationError, as_contract

REJECTION_SLICE = {
    "wrong_task_type": "task_type",
    "wrong_route": "route",
    "unsafe_allowance": "safety",
    "missing_confirmation": "confirmation",
    "missing_slot": "slot",
    "wrong_slot": "slot",
    "decomposed_search_slots": "slot",
    "extract_search_fallback": "task_type",
    "extract_query_slot": "slot",
    "extract_generic_price_wording": "slot",
    "extract_listed_price_wording": "slot",
    "extract_extra_particle_wording": "normalized_command",
    "underspecified_request": "underspecified",
    "malformed_schema": "schema",
}

EXTRACT_PRICE_CANONICAL_TARGET = "商品价格"
EXTRACT_PRICE_CANONICAL_NORMALIZED_COMMAND = "提取页面商品价格"


def _require_canonical_extract_price_chosen(pair: DPOPair, chosen: dict[str, Any], label: str) -> None:
    if not (
        chosen.get("task_type") == "extract"
        and chosen.get("route") == "extract_page"
        and chosen.get("safety", {}).get("allow") is True
        and chosen.get("safety", {}).get("reason") == "public_readonly"
        and chosen.get("slots", {}).get("target") == EXTRACT_PRICE_CANONICAL_TARGET
        and chosen.get("normalized_command") == EXTRACT_PRICE_CANONICAL_NORMALIZED_COMMAND
    ):
        raise ValidationError(
            f"{label}: {pair.id} chosen must be the canonical public-safe extract-price contract"
        )


def validate_dpo_pair(pair: DPOPair) -> None:
    chosen = as_contract(pair.chosen_contract).to_dict()
    rejected = pair.rejected_contract_dict()
    if chosen == rejected:
        raise ValidationError(f"weak_pair: {pair.id} chosen and rejected contracts are identical")
    if pair.rejection_reason == "wrong_task_type" and chosen.get("task_type") == rejected.get("task_type"):
        raise ValidationError(f"wrong_task_type: {pair.id} rejected contract must change task_type")
    if pair.rejection_reason == "wrong_route" and chosen.get("route") == rejected.get("route"):
        raise ValidationError(f"wrong_route: {pair.id} rejected contract must change route")
    if pair.rejection_reason == "unsafe_allowance" and chosen.get("safety", {}).get("allow") == rejected.get(
        "safety", {}
    ).get("allow"):
        raise ValidationError(f"unsafe_allowance: {pair.id} rejected contract must change safety.allow")
    if pair.rejection_reason == "missing_confirmation":
        if chosen.get("confirmation_required") is not True or rejected.get("confirmation_required") is not False:
            raise ValidationError(
                f"missing_confirmation: {pair.id} chosen must require confirmation and rejected must omit it"
            )
    if pair.rejection_reason == "missing_slot" and len(rejected.get("slots", {})) >= len(chosen.get("slots", {})):
        raise ValidationError(f"missing_slot: {pair.id} rejected contract must remove a slot")
    if pair.rejection_reason == "wrong_slot" and chosen.get("slots") == rejected.get("slots"):
        raise ValidationError(f"wrong_slot: {pair.id} rejected contract must alter slots")
    if pair.rejection_reason == "decomposed_search_slots":
        chosen_slots = chosen.get("slots", {})
        rejected_slots = rejected.get("slots", {})
        if not (
            chosen.get("task_type") == "search"
            and chosen.get("route") == "search_web"
            and chosen.get("safety", {}).get("allow") is True
            and chosen.get("safety", {}).get("reason") == "public_readonly"
            and rejected.get("task_type") == "search"
            and rejected.get("route") == "search_web"
            and rejected.get("safety", {}).get("allow") is True
        ):
            raise ValidationError(
                f"decomposed_search_slots: {pair.id} must be a public-readonly search/search_web contract"
            )
        if set(chosen_slots) != {"query"} or set(rejected_slots) != {"city", "date", "topic"}:
            raise ValidationError(
                f"decomposed_search_slots: {pair.id} rejected contract must replace query with city/date/topic slots"
            )
    if pair.rejection_reason == "extract_search_fallback":
        if not (
            chosen.get("task_type") == "extract"
            and chosen.get("route") == "extract_page"
            and chosen.get("safety", {}).get("allow") is True
            and chosen.get("safety", {}).get("reason") == "public_readonly"
            and "target" in chosen.get("slots", {})
        ):
            raise ValidationError(
                f"extract_search_fallback: {pair.id} chosen must be a public-readonly extract/extract_page contract"
            )
        if rejected.get("task_type") != "search" or rejected.get("route") != "search_web":
            raise ValidationError(
                f"extract_search_fallback: {pair.id} rejected contract must be search/search_web"
            )
    if pair.rejection_reason == "extract_query_slot":
        chosen_slots = chosen.get("slots", {})
        rejected_slots = rejected.get("slots", {})
        if not (
            chosen.get("task_type") == "extract"
            and chosen.get("route") == "extract_page"
            and chosen.get("safety", {}).get("allow") is True
            and chosen.get("safety", {}).get("reason") == "public_readonly"
            and "target" in chosen_slots
        ):
            raise ValidationError(
                f"extract_query_slot: {pair.id} chosen must be a public-readonly extract/extract_page contract"
            )
        if "target" in rejected_slots or not ({"query", "page_url"} & set(rejected_slots)):
            raise ValidationError(
                f"extract_query_slot: {pair.id} rejected contract must use query/page_url slots without target"
            )
    if pair.rejection_reason == "extract_generic_price_wording":
        _require_canonical_extract_price_chosen(pair, chosen, "extract_generic_price_wording")
        if chosen.get("slots") == rejected.get("slots") and chosen.get("normalized_command") == rejected.get(
            "normalized_command"
        ):
            raise ValidationError(
                f"extract_generic_price_wording: {pair.id} rejected contract must differ from canonical wording"
            )
        rejected_target = rejected.get("slots", {}).get("target")
        rejected_command = rejected.get("normalized_command")
        if rejected_target != "价格" and rejected_command != "页面价格":
            raise ValidationError(
                f"extract_generic_price_wording: {pair.id} rejected contract must use generic 价格 wording"
            )
    if pair.rejection_reason == "extract_listed_price_wording":
        _require_canonical_extract_price_chosen(pair, chosen, "extract_listed_price_wording")
        rejected_target = rejected.get("slots", {}).get("target")
        rejected_command = str(rejected.get("normalized_command", ""))
        if rejected_target != "标价" and "标价" not in rejected_command:
            raise ValidationError(
                f"extract_listed_price_wording: {pair.id} rejected contract must use 标价 wording"
            )
    if pair.rejection_reason == "extract_extra_particle_wording":
        _require_canonical_extract_price_chosen(pair, chosen, "extract_extra_particle_wording")
        rejected_slots = rejected.get("slots", {})
        if rejected_slots.get("target") != EXTRACT_PRICE_CANONICAL_TARGET:
            raise ValidationError(
                f"extract_extra_particle_wording: {pair.id} rejected contract must preserve target 商品价格"
            )
        if rejected.get("normalized_command") == EXTRACT_PRICE_CANONICAL_NORMALIZED_COMMAND:
            raise ValidationError(
                f"extract_extra_particle_wording: {pair.id} rejected contract must change normalized_command"
            )
    if pair.rejection_reason == "underspecified_request" and rejected.get("route") != "clarify":
        raise ValidationError(f"underspecified_request: {pair.id} rejected contract must route to clarify")
    if pair.rejection_reason == "malformed_schema" and "route" in rejected:
        raise ValidationError(f"malformed_schema: {pair.id} rejected contract must violate required schema")


def validate_dpo_pairs_file(path: Path) -> list[DPOPair]:
    pairs: list[DPOPair] = []
    for record in read_jsonl(path):
        pair = DPOPair(**record)
        validate_dpo_pair(pair)
        pairs.append(pair)
    return pairs


def summarize_dpo_slices(pairs: list[DPOPair]) -> dict[str, Any]:
    category_counts = Counter(pair.rejection_reason for pair in pairs)
    slice_counts: Counter[str] = Counter(REJECTION_SLICE[pair.rejection_reason] for pair in pairs)
    summary: dict[str, Any] = {
        "aggregate": {
            "total_pairs": len(pairs),
            "rejection_categories": dict(sorted(category_counts.items())),
        }
    }
    for slice_name in (
        "task_type",
        "route",
        "safety",
        "confirmation",
        "slot",
        "normalized_command",
        "schema",
        "underspecified",
    ):
        examples = [pair.id for pair in pairs if REJECTION_SLICE[pair.rejection_reason] == slice_name][:5]
        summary[slice_name] = {"count": slice_counts.get(slice_name, 0), "examples": examples}
    return summary
