## 1. Setup and Explorer

- [x] 1.1 Confirm branch, clean git status, no active OpenSpec conflicts, current validation baseline, and local-only/no-A100 scope.
- [x] 1.2 Run Explorer read-only analysis for source evidence files, gold rows, field comparison approach, report targets, test entry points, and stop conditions.
- [x] 1.3 Validate the OpenSpec proposal/design/spec/tasks strictly before implementation.

## 2. Row-Mismatch Diagnosis Evidence

- [x] 2.1 Add a focused failing evidence test for the new row-mismatch diagnosis pack and privacy/claim boundaries.
- [x] 2.2 Generate `reports/public-sample/confirmation-rerun-row-mismatch-diagnosis/` from committed public-safe rerun evidence and train gold only.
- [x] 2.3 Include machine-readable row comparisons, aggregate field mismatch counts, failure-family counts, source artifact links, manifest, Markdown report, and leak-scan results.
- [x] 2.4 Ensure the diagnosis preserves original prediction/evaluator status and does not repair, normalize, coerce, replace, or re-score predictions.

## 3. Documentation

- [x] 3.1 Generate a concise Chinese Human Brief HTML with project-stage progress, diagnosis result, evidence links, validation results, remaining risks, and recommended next step.

## 4. Validation, Review, Archive, and Integration

- [x] 4.1 Run fresh validation: focused diagnosis/evidence tests, full `PYTHONPATH=src pytest -q`, `uv run ruff check .`, `uv run mypy src`, public data validation, DPO pair check, leak-scan, `git diff --check`, and `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`.
- [x] 4.2 Run Reviewer diff review, fix in-scope Must Fix items, and rerun required validation.
- [x] 4.3 Archive the OpenSpec change, rerun post-archive validation, generate loop closeout report, and apply guarded auto integration when safe.
