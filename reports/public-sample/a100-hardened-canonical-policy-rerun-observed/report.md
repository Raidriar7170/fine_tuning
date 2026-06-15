# A100 hardened canonical policy rerun

Status: prediction-only hardened prompt rerun. This phase reuses the prior merged slot-value 7B adapter and does not train, repair, normalize, or re-score predictions.

## Scope

- Dataset manifest: `public-sample-20260615T040231Z`
- Rerun status: `observed`
- Source adapter runtime: `a100-merged-slot-value-heldout-eval`
- Overall interpretation: `hardened_canonical_policy_heldout_unchanged`

## Split Results

| split | rows | contract_exact_match | prior exact | delta | slot_f1 | json_valid_rate | residual rows | hardened prompt visible |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| train | 30 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 0 | True |
| dev | 6 | 0.5000 | 0.5000 | 0.0000 | 0.5000 | 1.0000 | 3 | True |
| test | 6 | 0.8333 | 0.8333 | 0.0000 | 1.0000 | 1.0000 | 1 | True |

## Boundary

- strict `contract_exact_match` remains primary.
- Train exact match, JSON-valid rate, and soft slot F1 are not model recovery claims.
- Predictions are not repaired, replaced, normalized, or re-scored.
- This is not new training, checkpoint release, adapter release, production-readiness evidence, private-corpus generalization evidence, public full-corpus release, or a live-browser benchmark claim.
