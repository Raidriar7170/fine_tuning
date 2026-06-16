# Voice2Task formal public held-out dev metrics

This report summarizes contract-level metrics only. No live-browser improvement claim is made from these numbers.

## Metrics

- `confirmation_accuracy`: 0.9855
- `contract_exact_match`: 0.3043
- `json_valid_rate`: 1.0000
- `route_accuracy`: 0.8551
- `safety_gold_stop_support`: 9.0000
- `safety_precision`: 1.0000
- `safety_predicted_stop_support`: 6.0000
- `safety_recall`: 0.6667
- `slot_f1`: 0.3913
- `slot_f1_soft`: 0.7315
- `task_type_accuracy`: 0.8551

## Failure Slices

- `confirmation`: 1 examples (family-clarify-dev-1-aug-2)
- `route`: 10 examples (family-clarify-dev-1-aug-2, family-clarify-dev-3, family-clarify-dev-3-aug-1, family-clarify-dev-3-aug-2, family-extract-dev-2-aug-1)
- `safety`: 3 examples (family-blocked_payment-dev-1, family-blocked_payment-dev-1-aug-1, family-blocked_payment-dev-2-aug-2)
- `schema`: 0 examples (none)
- `slot`: 42 examples (seed-clarify-ambiguous, seed-clarify-ambiguous-aug-1, seed-clarify-ambiguous-aug-2, family-search-dev-1-aug-1, family-search-dev-2-aug-1)
- `task_type`: 10 examples (family-clarify-dev-1-aug-2, family-clarify-dev-3, family-clarify-dev-3-aug-1, family-clarify-dev-3-aug-2, family-extract-dev-2-aug-1)
- `unknown`: 0 examples (none)
