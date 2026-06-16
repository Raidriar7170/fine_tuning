## 1. Readiness

- [x] 1.1 Verify repo state, active OpenSpec status, source policy artifact, prior form-fill remediation artifacts, and current recommendation.
- [x] 1.2 Run an Explorer pass to identify existing helper, report, CLI, test, and public-safety patterns for coverage assessment.

## 2. Coverage Assessment

- [x] 2.1 Add tests first for the confirmation-marker coverage assessment, including source artifact identity, coverage counts, represented field labels, unsupported changes, and claim boundaries.
- [x] 2.2 Implement deterministic coverage assessment from committed policy and form-fill remediation artifacts.
- [x] 2.3 Add a CLI/report entry point that writes JSON, Markdown, and manifest artifacts under `reports/public-sample/`.
- [x] 2.4 Generate the current confirmation-marker coverage artifacts.

## 3. Reporting And Validation

- [x] 3.1 Generate `docs/human-briefs/2026-06-16-assess-form-fill-confirmation-marker-coverage.html`.
- [x] 3.2 Run focused tests, full tests, ruff, OpenSpec strict validation, leak scan, and `git diff --check`. Dataset building and DPO pair checks are not applicable because this phase does not change data or DPO generation.
- [x] 3.3 Run a Reviewer pass and fix in-scope Must Fix items.
- [x] 3.4 Archive the OpenSpec change after tasks complete and validations pass.
