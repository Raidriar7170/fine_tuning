# A100 public-readonly search policy train-split rerun metrics

This report summarizes strict contract-level metrics. Raw field observations below are diagnostic only and are not metric relaxation.

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

## Metadata

- `prediction_source_kind`: `private_a100_adapter`
- `prediction_split`: `train`
- `generalization_claim`: `False`
- `strict_final_contract_metrics`: `True`
- `semantic_equivalence_scoring_performed`: `False`
- `slot_normalization_performed`: `False`
- `prediction_repair_or_rescore_performed`: `False`

## Raw Field Observation Counts

- `route=search_web`: `3/3`
- `safety.reason=public_readonly`: `3/3`
- `confirmation_required=false`: `3/3`
- `task_type=search_web` route-alias: `3/3`
- `validated_output_schema_valid`: `0/3`

## Failure Slices

- `confirmation`: 0 examples (none)
- `route`: 0 examples (none)
- `safety`: 0 examples (none)
- `schema`: 3 examples (seed-search-weather, seed-search-weather-aug-1, seed-search-weather-aug-2)
- `slot`: 0 examples (none)
- `task_type`: 0 examples (none)
- `unknown`: 0 examples (none)
