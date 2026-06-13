"""Validate, deduplicate, and assign splits to generated seed traces."""

from __future__ import annotations

import argparse
import json
import random
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from voice2task.schemas import BrowserTaskContract, ValidationError


def _edit_distance_ratio(a: str, b: str) -> float:
    """Normalized edit distance (0=identical, 1=completely different)."""
    if not a and not b:
        return 0.0
    max_len = max(len(a), len(b))
    if max_len == 0:
        return 0.0
    n, m = len(a), len(b)
    dp = list(range(m + 1))
    for i in range(1, n + 1):
        prev = dp[0]
        dp[0] = i
        for j in range(1, m + 1):
            temp = dp[j]
            if a[i - 1] == b[j - 1]:
                dp[j] = prev
            else:
                dp[j] = 1 + min(dp[j], dp[j - 1], prev)
            prev = temp
    return dp[m] / max_len


def validate_schema(seed: dict) -> list[str]:
    """Validate target_contract against BrowserTaskContract schema."""
    issues = []
    contract = seed.get("target_contract", {})
    try:
        BrowserTaskContract.from_dict(contract)
    except (ValidationError, KeyError, TypeError) as e:
        issues.append(f"schema: {e}")
    return issues


def validate_structure(seed: dict) -> list[str]:
    """Validate seed trace structure."""
    issues = []
    if not isinstance(seed.get("id"), str) or not seed["id"]:
        issues.append("missing id")
    if not isinstance(seed.get("input_text"), str) or not seed["input_text"].strip():
        issues.append("missing input_text")
    augs = seed.get("augmentations", [])
    if not isinstance(augs, list) or len(augs) < 2:
        issues.append(f"need >=2 augmentations, got {len(augs) if isinstance(augs, list) else 0}")
    if seed.get("split") not in ("train", "dev", "test"):
        issues.append(f"invalid split: {seed.get('split')}")
    return issues


def validate_safety_consistency(seed: dict) -> list[str]:
    """Check safety labels match task type conventions."""
    issues = []
    contract = seed.get("target_contract", {})
    task_type = contract.get("task_type")
    safety = contract.get("safety", {})

    if task_type == "blocked" and safety.get("allow") is not False:
        issues.append("blocked task must have safety.allow=false")
    if task_type in ("search", "navigate", "extract") and safety.get("allow") is False:
        issues.append(f"{task_type} task should normally have safety.allow=true")
    return issues


def deduplicate(seeds: list[dict], threshold: float = 0.3) -> tuple[list[dict], int]:
    """Remove near-duplicate seeds by input_text edit distance."""
    kept = []
    removed = 0
    seen_texts: list[str] = []

    for seed in seeds:
        text = seed["input_text"]
        is_dup = False
        for seen in seen_texts:
            if _edit_distance_ratio(text, seen) < threshold:
                is_dup = True
                break
        if is_dup:
            removed += 1
        else:
            kept.append(seed)
            seen_texts.append(text)
    return kept, removed


def reassign_splits(
    seeds: list[dict],
    train_ratio: float = 0.7,
    dev_ratio: float = 0.15,
    seed_val: int = 42,
) -> list[dict]:
    """Stratified split assignment by task_type."""
    rng = random.Random(seed_val)

    by_type: dict[str, list[dict]] = {}
    for s in seeds:
        tt = s["target_contract"]["task_type"]
        by_type.setdefault(tt, []).append(s)

    result = []
    for group in by_type.values():
        rng.shuffle(group)
        n = len(group)
        n_train = max(1, int(n * train_ratio))
        n_dev = max(1, int(n * dev_ratio))

        for i, s in enumerate(group):
            if i < n_train:
                s["split"] = "train"
            elif i < n_train + n_dev:
                s["split"] = "dev"
            else:
                s["split"] = "test"
        result.extend(group)

    return result


def main():
    parser = argparse.ArgumentParser(description="Validate and prepare generated seed traces")
    parser.add_argument("--input", required=True, help="Input JSONL (raw generated seeds)")
    parser.add_argument("--output", required=True, help="Output JSONL (validated, deduped, split-assigned)")
    parser.add_argument("--dedup-threshold", type=float, default=0.3, help="Edit distance ratio for dedup (0-1)")
    parser.add_argument("--skip-dedup", action="store_true", help="Skip deduplication")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    seeds = []
    with open(input_path, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                seeds.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"  Line {i}: JSON parse error: {e}", file=sys.stderr)

    print(f"Loaded {len(seeds)} candidate seeds")

    # Phase 1: Structure + Schema validation
    valid_seeds = []
    invalid_count = 0
    for seed in seeds:
        issues = validate_structure(seed) + validate_schema(seed) + validate_safety_consistency(seed)
        if issues:
            invalid_count += 1
            print(f"  INVALID [{seed.get('id', '?')}]: {issues}", file=sys.stderr)
        else:
            valid_seeds.append(seed)

    print(f"Schema-valid: {len(valid_seeds)}/{len(seeds)} (rejected {invalid_count})")

    # Phase 2: Deduplication
    if not args.skip_dedup:
        deduped, removed = deduplicate(valid_seeds, threshold=args.dedup_threshold)
        print(f"After dedup: {len(deduped)} (removed {removed} near-duplicates)")
    else:
        deduped = valid_seeds
        print("Dedup skipped")

    # Phase 3: Reassign splits (stratified)
    final = reassign_splits(deduped)

    # Phase 4: Summary stats
    type_counts = Counter(s["target_contract"]["task_type"] for s in final)
    split_counts = Counter(s["split"] for s in final)
    print(f"\nFinal dataset: {len(final)} seeds")
    print(f"  By task_type: {dict(sorted(type_counts.items()))}")
    print(f"  By split: {dict(sorted(split_counts.items()))}")

    # Write output
    with open(output_path, "w", encoding="utf-8") as f:
        for seed in final:
            f.write(json.dumps(seed, ensure_ascii=False) + "\n")

    print(f"\nWritten to: {output_path}")


if __name__ == "__main__":
    main()
