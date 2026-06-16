# Voice2Task formal public held-out test metrics

This report summarizes contract-level metrics only. No live-browser improvement claim is made from these numbers.

## Metrics

- `confirmation_accuracy`: 0.9855
- `contract_exact_match`: 0.2899
- `json_valid_rate`: 1.0000
- `route_accuracy`: 0.9130
- `safety_gold_stop_support`: 12.0000
- `safety_precision`: 0.9167
- `safety_predicted_stop_support`: 12.0000
- `safety_recall`: 0.9167
- `slot_f1`: 0.5072
- `slot_f1_soft`: 0.7609
- `task_type_accuracy`: 0.9130

## Failure Slices

- `confirmation`: 1 examples (family-clarify-test-1-aug-1)
- `route`: 6 examples (family-clarify-test-1-aug-1, family-clarify-test-2-aug-1, family-form_fill-test-3-aug-2, family-extract-test-1-aug-1, family-extract-test-2-aug-1)
- `safety`: 2 examples (family-clarify-test-2-aug-1, family-blocked_payment-test-3)
- `schema`: 0 examples (none)
- `slot`: 34 examples (family-search-test-1-aug-1, family-search-test-1-aug-2, family-search-test-2-aug-2, family-search-test-3-aug-1, family-search-test-3-aug-2)
- `task_type`: 6 examples (family-clarify-test-1-aug-1, family-clarify-test-2-aug-1, family-form_fill-test-3-aug-2, family-extract-test-1-aug-1, family-extract-test-2-aug-1)
- `unknown`: 0 examples (none)
