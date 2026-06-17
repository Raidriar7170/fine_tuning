## 1. Input Boundary

- [x] 1.1 Confirm the active manifest is `public-sample-20260617T045941Z` with 102 seeds / 261 SFT rows / 881 DPO pairs and split counts 123 / 69 / 69.
- [x] 1.2 Confirm latest model evidence remains bound to `public-sample-20260616T165835Z` and must not be reinterpreted as current-manifest evidence.
- [x] 1.3 Confirm the phase does not run A100 training, prediction generation, DPO, prompt changes, evaluator changes, adapter release, checkpoint release, or private corpus publication.

## 2. Readiness Evidence

- [x] 2.1 Run the current train split SFT retry dry-run against the public manifest and target config.
- [x] 2.2 Generate a public-safe readiness evidence pack in a new manifest-specific output directory.
- [x] 2.3 Ensure evidence records all 123 selected train rows and identifies form-fill repair, blocked-payment repair, and current-retry confirmation-preservation train rows.
- [x] 2.4 Ensure evidence states prediction configs require a paired adapter trained for `public-sample-20260617T045941Z` before prediction-only metrics can be interpreted as current-manifest model evidence.

## 3. Status Surfaces

- [x] 3.1 Refresh `CONTEXT.md` with current-123 readiness evidence and next bounded recommendation.
- [x] 3.2 Refresh `reports/final_status.md` with the readiness boundary and non-claim posture.
- [x] 3.3 Generate a concise Chinese Human Brief under `docs/human-briefs/`.

## 4. Validation And Archive

- [x] 4.1 Run focused readiness tests or add focused coverage if the existing report cannot express current-retry row counts.
- [x] 4.2 Run full tests, ruff, OpenSpec strict validation, public data/DPO checks, leak scan, and `git diff --check`.
- [x] 4.3 Review the diff for overclaiming, private-path leakage, stale manifest comparisons, and out-of-scope training/prediction claims.
- [x] 4.4 Archive the OpenSpec change, then stage/commit/push under the guarded auto-integration policy.
