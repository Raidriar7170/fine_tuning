## 1. Readiness

- [x] 1.1 Confirm the scaled residual diagnosis exists, is leak-clean, and targets `public-sample-20260617T152259Z`.
- [x] 1.2 Confirm this phase will read committed diagnosis artifacts only and will not launch A100, train, predict, mutate data, or change evaluator semantics.

## 2. Cluster Evidence

- [x] 2.1 Generate residual-cluster inspection under `reports/public-sample/scaled-current-123-adapter-residual-cluster-inspection/`.
- [x] 2.2 Ensure cluster report artifacts record source diagnosis links, source count consistency, top clusters, and diagnosis-only claim boundaries.
- [x] 2.3 If needed, update the cluster report writer so manifest artifact paths are output-directory accurate.

## 3. Documentation And Tests

- [x] 3.1 Update `CONTEXT.md`, `reports/final_status.md`, and a concise Chinese Human Brief with the cluster-inspection result.
- [x] 3.2 Add focused tests for scaled cluster counts, source boundary, claim boundaries, output-directory manifest paths, and leak-scan status.

## 4. Validation And Archive

- [x] 4.1 Run focused tests, full pytest, ruff, `openspec validate --all --strict`, leak scans, and `git diff --check`.
- [x] 4.2 Archive the completed OpenSpec change and re-run validation affected by archive.
- [x] 4.3 Commit and push the guarded integration if the worktree is safe and validation passes.
