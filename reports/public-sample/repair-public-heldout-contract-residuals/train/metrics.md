# A100 public held-out residual repair train metrics

This report summarizes contract-level metrics only. No live-browser improvement claim is made from these numbers.

## Metrics

- `confirmation_accuracy`: 0.7222
- `contract_exact_match`: 0.3333
- `json_valid_rate`: 0.8889
- `route_accuracy`: 0.5000
- `safety_gold_stop_support`: 3.0000
- `safety_precision`: 0.6667
- `safety_predicted_stop_support`: 3.0000
- `safety_recall`: 0.6667
- `slot_f1`: 0.5000
- `slot_f1_soft`: 0.5556
- `task_type_accuracy`: 0.5000

## Failure Slices

- `confirmation`: 3 examples (seed-clarify-target, seed-clarify-target-aug-1, seed-block-transfer)
- `route`: 7 examples (seed-open-help, seed-clarify-target, seed-clarify-target-aug-1, seed-clarify-target-aug-2, seed-block-transfer)
- `safety`: 2 examples (seed-clarify-target-aug-2, seed-block-transfer)
- `schema`: 2 examples (seed-form-nickname-aug-1, seed-form-nickname-aug-2)
- `slot`: 7 examples (seed-open-help, seed-open-help-aug-1, seed-clarify-target, seed-clarify-target-aug-1, seed-clarify-target-aug-2)
- `task_type`: 7 examples (seed-open-help, seed-clarify-target, seed-clarify-target-aug-1, seed-clarify-target-aug-2, seed-block-transfer)
- `unknown`: 0 examples (none)
