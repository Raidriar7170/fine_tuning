## 1. Discovery And TDD

- [x] 1.1 Inspect the current prediction prompt and schema-retry prompt construction paths, including metadata and prompt snapshot propagation.
- [x] 1.2 Add failing focused tests for retry template boundary metadata, prompt clauses, prompt snapshot propagation, and strict wrapped-fragment rejection.

## 2. Local Implementation

- [x] 2.1 Implement the minimal retry template/decoding-boundary metadata and prompt clauses without changing strict parsing, evaluator metrics, decoding parameters, or prediction repair behavior.
- [x] 2.2 Run focused tests and confirm RED-to-GREEN behavior.

## 3. Evidence And Human Brief

- [x] 3.1 Generate a public-safe local evidence pack under `reports/public-sample/retry-template-decoding-boundary/` with manifest, summary JSON/Markdown, and leak-scan results.
- [x] 3.2 Generate a concise Chinese Human Brief with validation results, source links, limitations, non-claims, and recommended next step.

## 4. Validation And Review

- [x] 4.1 Run focused tests, full test suite, lint/type checks, public data validation, DPO pair checks, public-leak scans, `git diff --check`, and `openspec validate --all --strict`.
- [x] 4.2 Complete Reviewer pass, fix Must Fix items only, archive the OpenSpec change, generate post-archive/final leak-scan sidecars, rerun validation, and commit the phase under guarded auto integration.
