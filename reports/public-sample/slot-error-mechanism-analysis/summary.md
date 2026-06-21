# Slot Error Mechanism Analysis

- Decision label: `MIXED_SLOT_REPRESENTATION_REQUIRED`
- Sample count: 414
- Gold slot events: 471
- Prediction slot events: 942
- Exact source-copyable gold slots: 48.83%
- Normalized source-copyable gold slots: 1.70%
- Typed-derivable gold slots: 0.00%
- Generation-required gold slots: 49.47%
- Unsupported-analysis gold slots: 0.00%
- Prediction source-supported rate: 51.80%
- Prediction unsupported-by-source rate: 32.17%
- Source-support breakdowns: summary JSON includes gold rates by split/task/route/slot path and predicted-value rates by split/run role/task/route/slot path.
- Partial-span heuristic: NFKC/casefold/compact text, then substring match or unique-character overlap threshold `max(2, min(unique_folded_value_chars, 4))`; diagnostic only.
- Control/Treatment movement: persistent=70, recovered=10, regressed=12, net=-2
- Boundary: recovered metric-reproduced raw inputs only; `prediction_contract` is the analysis authority.
- Alias policy: diagnostic only; aliases do not repair strict matches.
- Claims: no training, no prediction rerun, no evaluator relaxation, no schema/runtime change.
- Recommended next change: `design-hybrid-slot-representation-v1`
