from pathlib import Path

import pytest

from voice2task.dpo import summarize_dpo_slices, validate_dpo_pair, validate_dpo_pairs_file
from voice2task.io import write_jsonl
from voice2task.schemas import BrowserTaskContract, DPOPair, ValidationError


def _contract(
    task_type: str = "search",
    route: str = "search_web",
    confirmation_required: bool = False,
    query: str = "酒店",
    slots: dict[str, str] | None = None,
    safety_reason: str = "public_readonly",
) -> BrowserTaskContract:
    return BrowserTaskContract(
        task_type=task_type,
        route=route,
        safety={"allow": True, "reason": safety_reason},
        confirmation_required=confirmation_required,
        slots=slots or {"query": query},
        normalized_command=f"搜索{query}",
    )


def test_validate_dpo_pairs_file_rejects_weak_pairs(tmp_path: Path) -> None:
    weak = {
        "id": "weak-1",
        "split": "train",
        "input_text": "搜酒店",
        "chosen_contract": _contract().to_dict(),
        "rejected_contract": _contract().to_dict(),
        "rejection_reason": "wrong_route",
        "provenance": {"source_id": "seed-1", "public_safe": True},
    }
    path = tmp_path / "weak.jsonl"
    write_jsonl(path, [weak])

    with pytest.raises(ValidationError, match="weak_pair"):
        validate_dpo_pairs_file(path)


def test_validate_dpo_pairs_file_rejects_mislabeled_wrong_route_pair(tmp_path: Path) -> None:
    mislabeled = {
        "id": "bad-route-label",
        "split": "train",
        "input_text": "搜酒店",
        "chosen_contract": _contract(route="search_web").to_dict(),
        "rejected_contract": _contract(route="search_web", confirmation_required=True).to_dict(),
        "rejection_reason": "wrong_route",
        "provenance": {"source_id": "seed-1", "public_safe": True},
    }
    path = tmp_path / "mislabeled.jsonl"
    write_jsonl(path, [mislabeled])

    with pytest.raises(ValidationError, match="wrong_route"):
        validate_dpo_pairs_file(path)


def test_validate_dpo_pair_rejects_mislabeled_wrong_task_type_pair() -> None:
    pair = DPOPair(
        id="bad-task-type-label",
        split="train",
        input_text="搜酒店",
        chosen_contract=_contract(task_type="search"),
        rejected_contract=_contract(task_type="search", safety_reason="wrong_task_type"),
        rejection_reason="wrong_task_type",
        provenance={"source_id": "seed-1", "public_safe": True},
    )

    with pytest.raises(ValidationError, match="wrong_task_type"):
        validate_dpo_pair(pair)


def test_dpo_slice_summary_counts_rejection_categories() -> None:
    pairs = [
        DPOPair(
            id="route-1",
            split="train",
            input_text="搜酒店",
            chosen_contract=_contract(),
            rejected_contract=_contract(route="open_url"),
            rejection_reason="wrong_route",
            provenance={"source_id": "seed-1", "public_safe": True},
        ),
        DPOPair(
            id="confirm-1",
            split="train",
            input_text="搜酒店",
            chosen_contract=_contract(confirmation_required=True),
            rejected_contract=_contract(confirmation_required=False),
            rejection_reason="missing_confirmation",
            provenance={"source_id": "seed-2", "public_safe": True},
        ),
    ]

    summary = summarize_dpo_slices(pairs)

    assert summary["route"]["count"] == 1
    assert summary["confirmation"]["count"] == 1
    assert summary["aggregate"]["total_pairs"] == 2


def test_validate_dpo_pair_accepts_decomposed_search_slot_negative() -> None:
    pair = DPOPair(
        id="search-decomposed-slots",
        split="train",
        input_text="查北京明天天气",
        chosen_contract=_contract(query="北京明天天气"),
        rejected_contract=_contract(
            slots={"city": "北京", "date": "明天", "topic": ""},
            safety_reason="decomposed_search_slots",
        ),
        rejection_reason="decomposed_search_slots",
        provenance={"source_id": "seed-search-weather", "public_safe": True},
    )

    validate_dpo_pair(pair)

    summary = summarize_dpo_slices([pair])
    assert summary["slot"]["count"] == 1
    assert summary["aggregate"]["rejection_categories"] == {"decomposed_search_slots": 1}


def _extract_contract(
    slots: dict[str, str] | None = None,
    task_type: str = "extract",
    normalized_command: str = "提取页面商品价格",
) -> BrowserTaskContract:
    return BrowserTaskContract(
        task_type=task_type,
        route="extract_page",
        safety={"allow": True, "reason": "public_readonly"},
        confirmation_required=False,
        slots=slots or {"target": "商品价格"},
        normalized_command=normalized_command,
    )


def test_validate_dpo_pair_accepts_extract_price_hard_negatives() -> None:
    search_fallback = DPOPair(
        id="extract-search-fallback",
        split="train",
        input_text="帮我看看这个东西现在卖多少钱",
        chosen_contract=_extract_contract(),
        rejected_contract=_contract(
            task_type="search",
            route="search_web",
            query="商品价格",
            safety_reason="extract_search_fallback",
        ),
        rejection_reason="extract_search_fallback",
        provenance={"source_id": "seed-extract-price", "public_safe": True},
    )
    query_slot = DPOPair(
        id="extract-query-slot",
        split="train",
        input_text="把页面上标价找出来",
        chosen_contract=_extract_contract(),
        rejected_contract=_extract_contract(slots={"query": "商品价格", "page_url": ""}),
        rejection_reason="extract_query_slot",
        provenance={"source_id": "seed-extract-price", "public_safe": True},
    )

    validate_dpo_pair(search_fallback)
    validate_dpo_pair(query_slot)

    summary = summarize_dpo_slices([search_fallback, query_slot])
    assert summary["task_type"]["count"] == 1
    assert summary["slot"]["count"] == 1
    assert summary["aggregate"]["rejection_categories"] == {
        "extract_query_slot": 1,
        "extract_search_fallback": 1,
    }


def test_validate_dpo_pair_accepts_extract_price_canonical_wording_hard_negatives() -> None:
    generic_wording = DPOPair(
        id="extract-generic-price-wording",
        split="train",
        input_text="帮我看看这个东西现在卖多少钱",
        chosen_contract=_extract_contract(),
        rejected_contract=_extract_contract(slots={"target": "价格"}, normalized_command="页面价格"),
        rejection_reason="extract_generic_price_wording",
        provenance={"source_id": "seed-extract-price", "public_safe": True},
    )
    listed_wording = DPOPair(
        id="extract-listed-price-wording",
        split="train",
        input_text="把页面上标价找出来",
        chosen_contract=_extract_contract(),
        rejected_contract=_extract_contract(slots={"target": "标价"}, normalized_command="提取页面标价"),
        rejection_reason="extract_listed_price_wording",
        provenance={"source_id": "seed-extract-price", "public_safe": True},
    )
    extra_particle = DPOPair(
        id="extract-extra-particle-wording",
        split="train",
        input_text="帮我提取这个页面上的商品价格",
        chosen_contract=_extract_contract(),
        rejected_contract=_extract_contract(normalized_command="提取页面上的商品价格"),
        rejection_reason="extract_extra_particle_wording",
        provenance={"source_id": "seed-extract-price", "public_safe": True},
    )

    validate_dpo_pair(generic_wording)
    validate_dpo_pair(listed_wording)
    validate_dpo_pair(extra_particle)

    summary = summarize_dpo_slices([generic_wording, listed_wording, extra_particle])
    assert summary["slot"]["count"] == 2
    assert summary["normalized_command"]["count"] == 1
    assert summary["aggregate"]["rejection_categories"] == {
        "extract_extra_particle_wording": 1,
        "extract_generic_price_wording": 1,
        "extract_listed_price_wording": 1,
    }


@pytest.mark.parametrize(
    ("pair_kwargs", "message"),
    [
        (
            {
                "id": "bad-extract-search-fallback",
                "split": "train",
                "input_text": "帮我看看这个东西现在卖多少钱",
                "chosen_contract": _extract_contract(),
                "rejected_contract": _extract_contract(slots={"target": "价格"}),
                "rejection_reason": "extract_search_fallback",
                "provenance": {"source_id": "seed-extract-price", "public_safe": True},
            },
            "search/search_web",
        ),
        (
            {
                "id": "bad-extract-query-slot",
                "split": "train",
                "input_text": "把页面上标价找出来",
                "chosen_contract": _extract_contract(),
                "rejected_contract": _extract_contract(slots={"target": "价格"}),
                "rejection_reason": "extract_query_slot",
                "provenance": {"source_id": "seed-extract-price", "public_safe": True},
            },
            "query/page_url",
        ),
    ],
)
def test_validate_dpo_pair_rejects_malformed_extract_price_hard_negatives(
    pair_kwargs: dict[str, object],
    message: str,
) -> None:
    pair = DPOPair(**pair_kwargs)
    with pytest.raises(ValidationError, match=message):
        validate_dpo_pair(pair)


@pytest.mark.parametrize(
    ("pair_kwargs", "message"),
    [
        (
            {
                "id": "bad-extract-generic-price-wording",
                "split": "train",
                "input_text": "帮我看看这个东西现在卖多少钱",
                "chosen_contract": _extract_contract(),
                "rejected_contract": _extract_contract(),
                "rejection_reason": "extract_generic_price_wording",
                "provenance": {"source_id": "seed-extract-price", "public_safe": True},
            },
            "weak_pair",
        ),
        (
            {
                "id": "bad-extract-listed-price-wording",
                "split": "train",
                "input_text": "把页面上标价找出来",
                "chosen_contract": _extract_contract(),
                "rejected_contract": _extract_contract(slots={"target": "价格"}),
                "rejection_reason": "extract_listed_price_wording",
                "provenance": {"source_id": "seed-extract-price", "public_safe": True},
            },
            "标价",
        ),
        (
            {
                "id": "bad-extract-extra-particle-wording",
                "split": "train",
                "input_text": "帮我提取这个页面上的商品价格",
                "chosen_contract": _extract_contract(),
                "rejected_contract": _extract_contract(slots={"target": "价格"}, normalized_command="页面价格"),
                "rejection_reason": "extract_extra_particle_wording",
                "provenance": {"source_id": "seed-extract-price", "public_safe": True},
            },
            "preserve target",
        ),
    ],
)
def test_validate_dpo_pair_rejects_malformed_extract_price_canonical_wording_hard_negatives(
    pair_kwargs: dict[str, object],
    message: str,
) -> None:
    pair = DPOPair(**pair_kwargs)
    with pytest.raises(ValidationError, match=message):
        validate_dpo_pair(pair)


@pytest.mark.parametrize(
    ("rejected_contract", "message"),
    [
        (
            _contract(slots={"city": "北京", "date": "明天"}, safety_reason="decomposed_search_slots"),
            "replace query with city/date/topic slots",
        ),
        (
            _contract(
                slots={"query": "北京明天天气", "city": "北京", "date": "明天", "topic": ""},
                safety_reason="decomposed_search_slots",
            ),
            "replace query with city/date/topic slots",
        ),
        (
            _contract(
                route="open_url",
                slots={"city": "北京", "date": "明天", "topic": ""},
                safety_reason="decomposed_search_slots",
            ),
            "public-readonly search/search_web contract",
        ),
        (
            _contract(
                task_type="navigate",
                route="search_web",
                slots={"city": "北京", "date": "明天", "topic": ""},
                safety_reason="decomposed_search_slots",
            ),
            "public-readonly search/search_web contract",
        ),
    ],
)
def test_validate_dpo_pair_rejects_malformed_decomposed_search_slot_negative(
    rejected_contract: BrowserTaskContract,
    message: str,
) -> None:
    pair = DPOPair(
        id="bad-search-decomposed-slots",
        split="train",
        input_text="查北京明天天气",
        chosen_contract=_contract(query="北京明天天气"),
        rejected_contract=rejected_contract,
        rejection_reason="decomposed_search_slots",
        provenance={"source_id": "seed-search-weather", "public_safe": True},
    )

    with pytest.raises(ValidationError, match=message):
        validate_dpo_pair(pair)
