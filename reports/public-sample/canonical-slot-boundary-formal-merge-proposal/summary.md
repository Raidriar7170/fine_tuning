# Canonical Slot Boundary Formal-Merge Proposal Readiness

## Conclusion

This phase is proposal/readiness evidence only. It is not a direct formal merge
and it does not change the formal public sample.

Current readiness:
`not_ready_missing_row_level_candidate_source`.

## Source Review

- Source artifact:
  `reports/public-sample/canonical-slot-boundary-candidate-review/summary.json`
- Source evidence kind: `canonical_slot_boundary_candidate_review`
- Source review status: `review_complete_archived`
- Eligible future proposal classes from the review: 2

## Readiness Result

| item | value |
| --- | --- |
| evidence kind | `canonical_slot_boundary_formal_merge_proposal` |
| formal merge ready now | false |
| formal merge readiness | `not_ready_missing_row_level_candidate_source` |
| implemented now | false |
| formal public sample modified | false |
| required future source artifact | `data/public-samples/canonical_slot_boundary_seed_candidates.jsonl` |

No exact reviewed row-level canonical slot-boundary seed source exists in this
repository yet. Class-level review evidence is enough to plan a future bounded
data phase, but it is not enough to mutate `seed_traces.jsonl`, SFT rows, DPO
pairs, or the manifest.

## Future Merge Scope

Only these reviewed classes are eligible future formal-merge inputs:

- `slot_key_aliases`
- `slot_value_boundaries`

These classes are excluded from future formal merge in this boundary:

- `normalized_command_display_diagnostic`: diagnostic/display only; no strict
  exact change, residual rescore, semantic-equivalence claim, or prediction
  repair.
- `excluded_non_equivalence_cases`: date, city/location, product, URL host,
  price/amount, query/product, location/destination, and action/reason cases
  remain blocked or deferred non-equivalence boundaries.

## Future Acceptance Criteria

A later formal data phase must provide all of the following before any merge:

1. exact reviewed row-level candidate source;
2. public-safe validation and leak scan;
3. duplicate seed/source-id validation;
4. synchronized derived SFT rows, DPO pairs, and manifest metadata;
5. split-boundary accounting;
6. comparison-boundary warning;
7. strict `contract_exact_match` and strict `slot_f1` remain authoritative;
8. `slot_f1_soft` remains diagnostic only.

Comparison boundary: old metrics cannot be compared directly after a future
formal sample boundary change.

## Execution Boundary

No formal public sample seed traces, SFT rows, DPO pairs, manifests, splits,
source candidate artifacts, evaluator definitions, predictions, checkpoints,
adapters, A100 evidence, model configs, or postprocessor logic were changed.

No JSONL seed candidate generation, SFT/DPO row generation, manifest rebuild,
training, prediction run, A100 job, deterministic postprocessor
implementation, strict-exact relaxation, LLM judge, semantic-equivalence
scoring, prediction repair, model-quality claim, held-out recovery claim,
production-readiness claim, safety-readiness claim, or live-browser benchmark
claim is made.

## Recommended Next Bounded Step

Open a materialization phase for the exact row-level source artifact:
`data/public-samples/canonical_slot_boundary_seed_candidates.jsonl`.

Do not go directly to formal merge.

## Files

- `reports/public-sample/canonical-slot-boundary-formal-merge-proposal/summary.json`
- `reports/public-sample/canonical-slot-boundary-formal-merge-proposal/summary.md`
- `reports/public-sample/canonical-slot-boundary-formal-merge-proposal/leak_scan_result.json`
- `docs/human-briefs/2026-06-19-propose-canonical-slot-boundary-formal-merge-after-review.html`
