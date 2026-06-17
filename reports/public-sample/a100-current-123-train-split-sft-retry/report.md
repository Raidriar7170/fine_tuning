# Voice2Task current train split SFT retry

Status: training completed for one bounded private A100 current-train-split SFT retry, followed by dev/test prediction-only strict evaluation.

## Scope

- Dataset manifest: `public-sample-20260617T045941Z`
- Source adapter runtime: `a100-current-train-split-sft-retry`
- Training status: `training_completed`
- Training rows used: `123`
- Overall interpretation: `current_train_split_sft_retry_no_strict_exact_recovery`

## Split Results

| split | rows | contract_exact_match | slot_f1 | slot_f1_soft | safety_recall | json_valid_rate | residual rows |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dev | 69 | 0.4348 | 0.5580 | 0.8332 | 1.0000 | 1.0000 | 39 |
| test | 69 | 0.3768 | 0.5459 | 0.7950 | 1.0000 | 1.0000 | 43 |

## Current Baseline Comparison

- Direct comparison valid: `False`
- Baseline manifest: `public-sample-20260616T165835Z`
- Baseline source adapter runtime: `a100-current-train-split-sft-retry`
- Strict exact delta: `{'dev': 0.0, 'test': -0.02898550724637683}`
- Strict slot F1 delta: `{'dev': -0.021739130434782594, 'test': 0.007246376811594235}`
- Safety recall delta: `{'dev': 0.0, 'test': 0.0}`
- Delta values are context only, not a clean improvement/regression comparison, when direct comparison is `False`.

## Boundary

- Strict `contract_exact_match` and strict `slot_f1` remain primary.
- `slot_f1_soft` is diagnostic only.
- Predictions are not repaired, replaced, normalized, or re-scored.
- This report does not release a checkpoint or adapter and does not claim production readiness, private-corpus generalization, public full-corpus release, or live-browser benchmark improvement.
