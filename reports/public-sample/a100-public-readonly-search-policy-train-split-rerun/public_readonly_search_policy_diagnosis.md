# Public-readonly search policy train-split diagnosis

Status: A100 prediction-only rerun produced raw public-readonly field evidence, but strict Browser Task Contract validity regressed to `0/3` because every final prediction remained schema-invalid.

## Strict Metrics

- `json_valid_rate`: `0.0000`
- `contract_exact_match`: `0.0000`
- `task_type_accuracy`: `0.0000`
- `route_accuracy`: `0.0000`
- `confirmation_accuracy`: `0.0000`
- `slot_f1`: `0.0000`

## Raw Text Field Observations

- Raw `route=search_web`: `3/3`
- Raw `safety.reason=public_readonly`: `3/3`
- Raw `confirmation_required=false`: `3/3`
- Raw `slots.query` present: `3/3`
- Raw `task_type=search`: `0/3`
- Raw `task_type=search_web` route-alias: `3/3`
- Normalized-command exact strings from raw text: `2/3`

## Boundary

This diagnosis performs no normalization, no semantic-equivalence scoring, no slot normalization, no prediction repair, and no re-score. Strict metrics remain the evaluator result above.
No training, checkpoint release, adapter release, production-readiness claim, held-out generalization claim, model-quality claim, or live-browser benchmark improvement claim is made.
