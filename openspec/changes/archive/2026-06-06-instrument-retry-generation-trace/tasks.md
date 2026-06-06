## 1. Setup and OpenSpec

- [x] 1.1 Run `/opsx auto` preflight: confirm clean `main`, OpenSpec-managed repo, no active changes, and no upstream push path.
- [x] 1.2 Create `instrument-retry-generation-trace` OpenSpec change.
- [x] 1.3 Validate proposal/design/spec/tasks strictly before implementation.

## 2. TDD and Implementation

- [x] 2.1 Add a failing focused test proving retry attempts write `attempt=retry_attempt` generation trace rows.
- [x] 2.2 Implement minimal retry generation trace instrumentation in `src/voice2task/training.py`.
- [x] 2.3 Preserve existing retry prompt text, decoding parameters, parser behavior, schema guard source selection, predictions, and evaluator metrics.

## 3. Evidence and Human Brief

- [x] 3.1 Generate `reports/public-sample/retry-generation-trace-instrumentation/` with instrumentation summary JSON/Markdown, manifest, and leak scans.
- [x] 3.2 Generate a concise Chinese Human Brief HTML for this phase.
- [x] 3.3 Record project-stage progress and non-claims: no A100 execution, no training, no private prediction rerun, no model recovery claim.

## 4. Validation, Review, Archive, and Integration

- [x] 4.1 Run fresh validation: focused tests, full `PYTHONPATH=src pytest -q`, `uv run ruff check .`, `uv run mypy src`, public data validation, DPO pair check, leak-scan, `git diff --check`, and `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`.
- [x] 4.2 Run Reviewer diff review, fix in-scope Must Fix items, and rerun required validation.
- [x] 4.3 Archive the OpenSpec change, rerun post-archive validation, refresh final leak scans, and apply guarded local auto integration when safe.
