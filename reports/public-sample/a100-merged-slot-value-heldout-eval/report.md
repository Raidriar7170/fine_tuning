# A100 merged slot value held-out evaluation

Status: merged-candidate public-sample SFT evaluation. Train split is learnability evidence; dev/test strict exact is the primary held-out signal.

## Scope

- Dataset manifest: `public-sample-20260615T040231Z`
- Formal public sample counts: `{'dpo_pairs': 125, 'seed_rows': 14, 'sft_rows': 42}`
- Training status: `training_completed`
- Overall interpretation: `merged_slot_value_heldout_improved_partial`

## Split Results

| split | rows | contract_exact_match | slot_f1 | json_valid_rate | residual rows |
| --- | ---: | ---: | ---: | ---: | ---: |
| train | 30 | 1.0000 | 1.0000 | 1.0000 | 0 |
| dev | 6 | 0.5000 | 0.5000 | 1.0000 | 3 |
| test | 6 | 0.8333 | 1.0000 | 1.0000 | 1 |

## Comparison

- Prior targeted family coverage exact: `{'train': 1.0, 'dev': 0.16666666666666666, 'test': 0.16666666666666666}`
- Merged slot value exact: `{'train': 1.0, 'dev': 0.5, 'test': 0.8333333333333334}`
- Dev/test improved from prior targeted: `{'dev': True, 'test': True}`

## Boundary

- strict `contract_exact_match` remains primary.
- Soft slot F1 and semantic equivalence remain diagnostic-only.
- Predictions are not repaired, replaced, normalized, or re-scored.
- This is not a checkpoint release, adapter release, production-readiness claim, private-corpus generalization claim, public full-corpus release, or live-browser benchmark claim.
