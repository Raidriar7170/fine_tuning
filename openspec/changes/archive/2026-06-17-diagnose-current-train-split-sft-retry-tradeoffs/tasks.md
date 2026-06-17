## 1. Evidence Inputs

- [x] 1.1 Verify the current retry and current-manifest baseline evidence packs exist and share manifest `public-sample-20260616T165835Z`.
- [x] 1.2 Load dev/test gold, predictions, metrics, and sidecars from committed public-safe evidence only.
- [x] 1.3 Confirm the phase does not require training, prediction generation, dataset mutation, prompt changes, or evaluator changes.

## 2. Diagnosis Output

- [x] 2.1 Generate a public-safe trade-off diagnosis report comparing baseline and retry row-level outcomes.
- [x] 2.2 Summarize recoveries, regressions, persistent failures, and unchanged successes by split and outcome family.
- [x] 2.3 Identify the strongest next bounded recommendation without overclaiming model recovery.

## 3. Status Surfaces

- [x] 3.1 Refresh `CONTEXT.md` with the diagnosis result and strict claim boundaries.
- [x] 3.2 Refresh `reports/final_status.md` with the diagnosis result and next-stage recommendation.
- [x] 3.3 Generate a concise Chinese Human Brief under `docs/human-briefs/`.

## 4. Validation And Archive

- [x] 4.1 Add or update focused tests for the diagnosis report shape and committed evidence.
- [x] 4.2 Run full tests, ruff, OpenSpec strict validation, leak scan, manifest/count checks, and `git diff --check`.
- [x] 4.3 Review the diff for overclaiming, private-path leakage, and unrelated changes.
- [x] 4.4 Archive the OpenSpec change, then stage/commit/push under the guarded auto-integration policy.
