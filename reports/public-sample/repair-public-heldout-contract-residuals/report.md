# A100 public held-out residual repair evidence

Status: public held-out residual repair evidence with a negative result. This is not a release, not private-corpus evidence, not production-readiness evidence, and not a live-browser benchmark.

## Scope

- Base model: `Qwen/Qwen2.5-7B-Instruct`
- Dataset manifest: `public-sample-20260613T072200Z`
- Prediction source kind: `private_a100_adapter`
- Prediction splits: `train, dev, test`
- Primary held-out evidence splits: `dev, test`
- Overall interpretation: `public_heldout_residual_repair_failed`

## Split Results

| split | rows | json_valid_rate | contract_exact_match | slot_f1 | task_type_accuracy | route_accuracy | confirmation_accuracy | safety_recall | schema_invalid | alignment_mismatch_rows |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| train | 18 | 0.8889 | 0.3333 | 0.5000 | 0.5000 | 0.5000 | 0.7222 | 0.6667 | 2 | 12 |
| dev | 6 | 1.0000 | 0.0000 | 0.3333 | 0.3333 | 0.3333 | 0.5000 | 1.0000 | 0 | 6 |
| test | 6 | 1.0000 | 0.0000 | 0.1667 | 0.6667 | 0.6667 | 0.5000 | 0.3333 | 0 | 6 |

## Interpretation

The SFT-only repair phase did not recover strict public held-out contract behavior. The train repair rows also remain far from strict memorization (`contract_exact_match=0.3333`), so the result points to insufficient or misaligned learning signal rather than a narrow dev/test-only overfitting issue. The public `dev` and `test` splits are schema-valid, but both remain `contract_exact_match=0.0000` with task, route, slot, confirmation, normalized-command, and safety residuals.

## Residual Field Counts

- train: confirmation_required=3, contract_version=1, normalized_command=11, route=7, safety.allow=2, safety.reason=5, slots=8, task_type=7
- dev: confirmation_required=3, normalized_command=6, route=4, safety.reason=3, slots=4, task_type=4
- test: confirmation_required=3, normalized_command=6, route=2, safety.allow=2, safety.reason=3, slots=5, task_type=2

## Public Artifacts

- Diagnosis: `reports/public-sample/repair-public-heldout-contract-residuals/heldout_residual_repair_diagnosis.json`
- Manifest: `reports/public-sample/repair-public-heldout-contract-residuals/manifest.json`
- Train metrics: `reports/public-sample/repair-public-heldout-contract-residuals/train/metrics.json`
- Dev metrics: `reports/public-sample/repair-public-heldout-contract-residuals/dev/metrics.json`
- Test metrics: `reports/public-sample/repair-public-heldout-contract-residuals/test/metrics.json`
- Leak scan: `reports/public-sample/repair-public-heldout-contract-residuals/leak_scan_result.json`
- Human Brief: `docs/human-briefs/2026-06-13-repair-public-heldout-contract-residuals.html`

## Boundary

The evidence pack contains sanitized public-sample predictions, aggregate metrics, diagnostics, and sidecars. It does not copy raw logs, checkpoints, adapters, remote caches, private overrides, host details, SSH details, tokens, private paths, or private corpus rows into git.

## Recommended Next Step

Archive this phase as a negative public-sample repair attempt. The next bounded phase should diagnose the actual SFT learning path before another heavy run, especially assistant-label/loss masking, target-token pressure, and whether the generated DPO hard negatives need a real preference-training phase.
