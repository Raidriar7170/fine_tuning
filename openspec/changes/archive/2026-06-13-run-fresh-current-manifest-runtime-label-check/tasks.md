## 1. TDD And Scope Guard

- [x] 1.1 Add failing tests that require current-manifest runtime-label evidence to mark stale prior evidence as historical context only.
- [x] 1.2 Add failing tests that require the report/manifest to preserve non-claim boundaries and recommend tiny-overfit only when fresh labels are inspectable and assistant-only.

## 2. Minimal Implementation

- [x] 2.1 Reuse or minimally extend the runtime-label provenance report surface to include current-manifest freshness and next-step recommendation.
- [x] 2.2 Add any needed public-safe config/template or metadata glue for the current manifest.
- [x] 2.3 Keep committed artifacts free of raw prompts, assistant targets, private paths, host details, logs, adapters, checkpoints, caches, and model snapshots.

## 3. Runtime Evidence

- [x] 3.1 Re-check A100 occupancy before any remote runtime work and select an idle GPU explicitly if remote execution is needed.
- [x] 3.2 Run the current-manifest runtime label provenance check or record a bounded blocked/unavailable result if the real runtime path cannot execute.
- [x] 3.3 Generate `reports/public-sample/current-runtime-label-provenance-check/` with sanitized JSON, Markdown, manifest, and leak-scan artifacts.

## 4. Human Brief, Review, And Validation

- [x] 4.1 Generate `docs/human-briefs/2026-06-13-run-fresh-current-manifest-runtime-label-check.html`.
- [x] 4.2 Run focused tests, full pytest, ruff, mypy, public data validation, DPO check, OpenSpec strict validation, leak scan, and `git diff --check`.
- [x] 4.3 Perform a read-only diff/evidence review and fix any Must Fix issues inside scope.

## 5. Archive And Integration

- [x] 5.1 Archive the OpenSpec change after successful validation and rerun post-archive validation.
- [x] 5.2 Auto-stage and commit only in-scope phase files when guarded auto-integration remains safe.
