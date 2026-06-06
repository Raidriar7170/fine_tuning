## 1. Setup and Preflight

- [x] 1.1 Confirm clean `main`, no active OpenSpec changes beyond this phase, and latest A100 retry trace rerun commit.
- [x] 1.2 Validate proposal/design/spec/tasks strictly.

## 2. Diagnosis

- [x] 2.1 Generate `reports/public-sample/retry-trace-finish-state-boundary-diagnosis/` from committed public artifacts only.
- [x] 2.2 Include per-row token-count/max-token/EOS/finish-state evidence and explicit unknown-stop-reason boundaries.
- [x] 2.3 Add focused tests for public-safe artifacts, no A100 execution, no decoding behavior change, and no stop-reason/model-recovery overclaim.
- [x] 2.4 Generate a concise Chinese Human Brief HTML.

## 3. Validation, Archive, and Integration

- [x] 3.1 Run focused tests, full `PYTHONPATH=src pytest -q`, `uv run ruff check .`, `uv run mypy src`, public data validation, DPO pair check, leak scans, `git diff --check`, and `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`.
- [x] 3.2 Run Reviewer diff review, fix in-scope Must Fix items, and rerun required validation.
- [x] 3.3 Archive the OpenSpec change, rerun post-archive validation, generate/refresh final leak scans, and apply guarded auto integration when safe.
