## 1. Readiness And Remote Preflight

- [x] 1.1 Confirm local worktree is clean and current manifest is `public-sample-20260617T045941Z` with 102 seeds / 261 SFT rows / 881 DPO pairs and split counts 123 / 69 / 69.
- [x] 1.2 Confirm current-123 readiness evidence exists and records all 123 train rows plus the 21 form-fill, 4 blocked-payment, and 5 current-retry train-row groups.
- [x] 1.3 Inspect A100 GPU/process occupancy and choose one safe idle GPU with explicit `CUDA_VISIBLE_DEVICES`, or record blocked evidence if safe placement is not available.
- [x] 1.4 Create repo-external private A100 override/config files under the approved private A100 project root; do not commit private paths, host details, raw logs, adapters, checkpoints, or tokens.

## 2. Private A100 SFT Retry

- [x] 2.1 Launch exactly one bounded SFT retry using `configs/sft-a100-current-train-split-retry.json` against the current public manifest and the selected GPU.
- [x] 2.2 Record sanitized training metadata, package/runtime policy, dataset manifest id, split counts, selected GPU policy, and adapter release status without exposing private paths.
- [x] 2.3 If training fails or preflight becomes unsafe, publish a blocked/failed public-safe evidence pack without fabricating adapter metadata or metrics.

## 3. Paired Dev/Test Prediction And Strict Evaluation

- [x] 3.1 Run dev prediction with the newly trained paired adapter using the current manifest and `configs/sft-a100-current-train-split-retry-dev-prediction.json`.
- [x] 3.2 Run test prediction with the newly trained paired adapter using the current manifest and `configs/sft-a100-current-train-split-retry-test-prediction.json`.
- [x] 3.3 Evaluate dev/test predictions with the existing strict contract ladder and keep `slot_f1_soft` diagnostic-only.
- [x] 3.4 Preserve raw private outputs outside git and commit only sanitized prediction/evaluation sidecars, metrics, manifest, and report artifacts.

## 4. Public Evidence And Status Surfaces

- [x] 4.1 Publish a public-safe evidence pack under `reports/public-sample/a100-current-123-train-split-sft-retry/`.
- [x] 4.2 Update `CONTEXT.md` and `reports/final_status.md` with the current-manifest model evidence boundary, strict metrics, and non-claim posture.
- [x] 4.3 Generate a concise Chinese Human Brief under `docs/human-briefs/`.
- [x] 4.4 Ensure reports compare against prior-manifest metrics only with explicit manifest-boundary language.

## 5. Validation, Review, Archive, And Integration

- [x] 5.1 Run focused tests for the new report/evidence behavior or add focused coverage if needed.
- [x] 5.2 Run full tests, ruff, OpenSpec strict validation, public data validation, DPO pair check, leak scan, and `git diff --check`.
- [x] 5.3 Review the diff for overclaiming, private-path leakage, stale manifest comparisons, and out-of-scope DPO/GRPO/prompt/evaluator changes.
- [x] 5.4 Archive the OpenSpec change, then stage/commit/push under the guarded auto-integration policy.
