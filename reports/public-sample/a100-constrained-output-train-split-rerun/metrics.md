# A100 Constrained-Output Train-Split Metrics

This report summarizes contract-level train-split metrics only. `json_valid_rate` means schema-valid Browser Task Contract rate, not raw JSON parseability. No held-out generalization, release, production-readiness, adapter release, checkpoint release, A100 model recovery, or live-browser improvement claim is made from these numbers.

## Evidence Context

- `generalization_claim`: `False`
- `model_quality_evidence`: `False`
- `overfit_diagnostic`: `True`
- `prediction_source_kind`: `private_a100_adapter`
- `prediction_split`: `train`
- `training_rows_used`: `3`
- `schema_retry_enabled`: `True`
- `strict_retry_interpretation`: `whole_string_json_only_parser_for_raw_and_retry_attempts`
- `canonical_json_one_shot_visible`: `True`
- `whole_object_boundary_visible`: `True`
- `raw_attempt_schema_valid_count`: `0`
- `retry_attempt_schema_valid_count`: `0`
- `validated_output_schema_valid_count`: `0`
- `retry_fragment_objects_rejected_count`: `3`
- `train_internal_recovery_observed`: `False`
- `baseline_validated_output_schema_valid_count`: `0`

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
