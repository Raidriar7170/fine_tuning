## 1. Readiness

- [x] 1.1 Confirm the latest scaled prediction evidence exists, is observed, and targets `public-sample-20260617T152259Z`.
- [x] 1.2 Confirm the diagnosis will read existing gold/prediction artifacts only and will not launch A100, train, predict, or change evaluator semantics.

## 2. Diagnosis Evidence

- [x] 2.1 Generate residual-family diagnosis under `reports/public-sample/scaled-current-123-adapter-residual-diagnosis/`.
- [x] 2.2 Add leak-scan sidecars and a public-safe manifest/report.
- [x] 2.3 Record tiered interpretation without making it a replacement metric.

## 3. Documentation And Tests

- [x] 3.1 Update `CONTEXT.md`, `reports/final_status.md`, and a concise Chinese Human Brief.
- [x] 3.2 Add focused tests for diagnosis counts, source boundary, claims, and leak-scan status.

## 4. Validation And Archive

- [x] 4.1 Run focused tests, full pytest, ruff, `openspec validate --all --strict`, leak scans, and `git diff --check`.
- [x] 4.2 Archive the completed OpenSpec change and re-run validation affected by archive.
- [x] 4.3 Commit and push the guarded integration if the worktree is safe and validation passes.
