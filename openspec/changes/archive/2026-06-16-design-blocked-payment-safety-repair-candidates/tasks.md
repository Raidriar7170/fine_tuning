## 1. Inputs And Boundary

- [x] 1.1 Validate OpenSpec status, local git status, and source diagnosis paths.
- [x] 1.2 Load `reports/public-sample/sft-v3-safety-regression-diagnosis/` and current public manifest.
- [x] 1.3 Confirm this phase is design-only: no dataset mutation, prediction generation, training, A100 execution, evaluator change, or release claim.

## 2. Candidate Design Evidence

- [x] 2.1 Implement or run a reproducible local design pass that derives `blocked_payment` repair candidates from regressed and persistent-miss rows.
- [x] 2.2 For each candidate, record source row ids, repair family, safety pattern, accepted `blocked/deny` target sketch, rejected drift sketches, and suggested public-safe utterance templates.
- [x] 2.3 Aggregate candidate coverage by source classification, repair family, target task type, route, and safety reason.
- [x] 2.4 Write public-safe JSON and Markdown design evidence under `reports/public-sample/`.

## 3. Project Visibility

- [x] 3.1 Refresh `CONTEXT.md` and `reports/final_status.md` if the design changes the recommended next bounded phase.
- [x] 3.2 Generate a concise Chinese Human Brief for the design phase.

## 4. Validation And Archive

- [x] 4.1 Add or update focused tests for candidate shape, public-safe boundaries, and non-claim flags.
- [x] 4.2 Run focused tests, full tests, ruff, OpenSpec strict validation, public data validation, DPO pair count check, leak scan, and `git diff --check`.
- [x] 4.3 Review the diff for overclaiming, private-path leakage, and unrelated changes.
- [x] 4.4 Archive the OpenSpec change if validation passes.
