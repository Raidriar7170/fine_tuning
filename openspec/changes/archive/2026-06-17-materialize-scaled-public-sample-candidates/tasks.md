## 1. Candidate Materialization

- [x] 1.1 Add deterministic scaled public-sample candidate templates and accounting helpers.
- [x] 1.2 Add a materializer that writes standalone candidate seed rows, SFT sidecars, JSON evidence, Markdown evidence, and manifest files without touching formal public sample files.
- [x] 1.3 Add CLI support for `materialize-scaled-public-sample-candidates`.

## 2. Evidence And Documentation

- [x] 2.1 Generate committed standalone candidate seed rows and evidence under the scaled candidate report directory.
- [x] 2.2 Update `CONTEXT.md` and `reports/final_status.md` to point at the new materialization evidence while preserving strict metric boundaries.
- [x] 2.3 Add a concise Chinese Human Brief HTML for this phase.

## 3. Validation

- [x] 3.1 Add focused tests for candidate counts, split accounting, standalone-only boundaries, and formal public sample overwrite rejection.
- [x] 3.2 Run focused tests, full tests, ruff, public dataset validation, DPO check, OpenSpec strict validation, leak scan, and `git diff --check`.
- [x] 3.3 Perform Reviewer self-review/fix pass and archive the OpenSpec change after validation succeeds.
