## 1. OpenSpec And Merge Logic

- [x] 1.1 Add formal provenance conversion for reviewed `form_fill` remediation candidates.
- [x] 1.2 Add a formal merge function that validates exactly the reviewed train-only candidates, rejects duplicates, rewrites the formal public seed, and rebuilds public SFT/DPO/manifest artifacts.
- [x] 1.3 Extend public manifest source summary with form-fill remediation candidate counts, affected source case groups, and formal-merge status while preserving existing slot-value and family-stratified metadata.

## 2. CLI, Reports, And Evidence

- [x] 2.1 Add a `voice2task-data merge-form-fill-remediation-candidates` CLI command.
- [x] 2.2 Add JSON/Markdown/manifest merge evidence under `reports/public-sample/form-fill-remediation-public-sample-merge/`.
- [x] 2.3 Rebuild committed formal public sample seed/SFT/DPO/manifest artifacts with the 9 merged candidates.
- [x] 2.4 Generate a concise Chinese Human Brief HTML for the phase.

## 3. Validation And Closeout

- [x] 3.1 Add focused tests for merge counts, provenance, DPO deltas, CLI output, duplicate rejection, committed evidence, and updated preview fixtures.
- [x] 3.2 Run focused tests, formal public sample validation, DPO check, full tests, ruff, OpenSpec strict validation, leak scan, and `git diff --check`.
- [x] 3.3 Run a Reviewer pass and fix in-scope Must Fix items.
- [x] 3.4 Archive the OpenSpec change after tasks complete.
