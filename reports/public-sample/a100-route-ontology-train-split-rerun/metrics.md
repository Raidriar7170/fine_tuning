# A100 route ontology train-split rerun metrics

This report summarizes contract-level metrics only. No live-browser improvement claim is made from these numbers.

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
## Evidence Context

- Prediction split: `train`
- Overfit diagnostic: `True`
- Generalization claim: `False`
- Prediction source kind: `private_a100_adapter`
- Schema repair applied: `False`
- Interpretation: train-internal route ontology evidence only; no held-out generalization claim.

## Strict Final Metrics vs Raw Route Ontology

- `route_accuracy`: `0.0000` is a strict final-contract route accuracy. It is computed only after strict Browser Task Contract validation, so schema-invalid final predictions do not receive route credit.
- raw route ontology / gold-route match: `3/3`.
- Raw route value counts: `{'search_web': 3}`.
- Route enum-valid count: `3/3`.
- Missing `confirmation_required`: `3/3`.
- Final validated schema-valid count: `0/3`.
