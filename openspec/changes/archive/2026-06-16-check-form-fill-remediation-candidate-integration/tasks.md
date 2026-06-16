## 1. OpenSpec And Integration Logic

- [x] 1.1 Add an OpenSpec spec delta for preview-only `form_fill` candidate integration checks.
- [x] 1.2 Add fail-closed candidate seed validation for the 9 reviewed standalone rows.
- [x] 1.3 Add a preview build function that writes preview seed/SFT/DPO/manifest artifacts under reports without modifying formal public sample files.

## 2. Reporting, CLI, And Evidence

- [x] 2.1 Add a public-safe integration check report writer for JSON, Markdown, and manifest outputs.
- [x] 2.2 Add a `voice2task-data check-form-fill-remediation-candidate-integration` CLI command.
- [x] 2.3 Generate committed preview/evidence artifacts under `reports/public-sample/form-fill-remediation-candidate-integration-preview/`.
- [x] 2.4 Generate a concise Chinese Human Brief HTML for the phase.

## 3. Validation And Closeout

- [x] 3.1 Add focused tests for preview counts, candidate DPO preview counts, CLI output, committed evidence, and public-sample immutability.
- [x] 3.2 Run focused tests, full tests, ruff, OpenSpec strict validation, leak scan, and `git diff --check`.
- [x] 3.3 Archive the OpenSpec change after tasks complete.
