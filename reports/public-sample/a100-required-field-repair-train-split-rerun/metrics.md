# A100 Required-Field Repair Train-Split Metrics

This report summarizes contract-level train-split metrics only. `json_valid_rate` means schema-valid Browser Task Contract rate, not raw JSON parseability. No held-out generalization, release, production-readiness, or live-browser improvement claim is made from these numbers.

## Evidence Context

- `assistant_only_objective_inspected`: `True`
- `assistant_tokens_carry_loss`: `True`
- `generalization_claim`: `False`
- `model_quality_evidence`: `False`
- `overfit_diagnostic`: `True`
- `prediction_source_kind`: `private_a100_adapter`
- `prediction_split`: `train`
- `prompt_tokens_masked`: `True`
- `raw_attempt_schema_valid_count`: `0`
- `required_field_checklist_visible`: `True`
- `required_field_skeleton_visible`: `True`
- `retry_attempt_schema_valid_count`: `0`
- `schema_retry_enabled`: `True`
- `train_internal_recovery_observed`: `False`
- `validated_output_schema_valid_count`: `0`

## Metrics

- `confirmation_accuracy`: 0.0000
- `contract_exact_match`: 0.0000
- `json_valid_rate`: 0.0000
- `route_accuracy`: 0.0000
- `safety_gold_stop_support`: 0.0000
- `safety_precision`: 1.0000
- `safety_predicted_stop_support`: 0.0000
- `safety_recall`: 1.0000
- `slot_f1`: 0.0000
- `task_type_accuracy`: 0.0000

## Failure Slices

- `confirmation`: 0 examples (none)
- `route`: 0 examples (none)
- `safety`: 0 examples (none)
- `schema`: 3 examples (seed-search-weather, seed-search-weather-aug-1, seed-search-weather-aug-2)
- `slot`: 0 examples (none)
- `task_type`: 0 examples (none)
- `unknown`: 0 examples (none)
