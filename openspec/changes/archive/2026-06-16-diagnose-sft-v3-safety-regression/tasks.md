## 1. Diagnosis Inputs

- [x] 1.1 Validate OpenSpec status, local git status, and source evidence paths.
- [x] 1.2 Load current formal public manifest, baseline dev/test gold and predictions, and SFT v3 retry dev/test gold and predictions.

## 2. Safety Regression Evidence

- [x] 2.1 Implement or run a reproducible local diagnosis that computes safety confusion counts per split and run.
- [x] 2.2 Classify matched rows as `regressed`, `recovered`, `persistent_miss`, `stable_correct`, or `unchanged_non_stop`.
- [x] 2.3 Aggregate classifications by split, task family, task type, route, and gold stop support.
- [x] 2.4 Write public-safe JSON and Markdown diagnosis evidence under `reports/public-sample/`.

## 3. Project Visibility

- [x] 3.1 Refresh `CONTEXT.md` and `reports/final_status.md` if the diagnosis changes the recommended next bounded phase.
- [x] 3.2 Generate a concise Chinese Human Brief for the diagnosis phase.

## 4. Validation And Archive

- [x] 4.1 Add or update focused tests for the diagnosis evidence shape and non-claim boundaries.
- [x] 4.2 Run focused tests, full tests, ruff, OpenSpec strict validation, public data validation, DPO pair count check, leak scan, and `git diff --check`.
- [x] 4.3 Review the diff for overclaiming, private-path leakage, and unrelated changes.
- [x] 4.4 Archive the OpenSpec change if validation passes.
