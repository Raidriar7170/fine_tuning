## 1. Test-First Coverage

- [x] 1.1 Add tests for safety repair candidate review ingestion from committed design evidence.
- [x] 1.2 Add tests for review decisions, source-design consistency, and no-materialization boundaries.
- [x] 1.3 Add tests that committed review artifacts are public-safe; verify historical evidence remains unmodified with git status.

## 2. Core Implementation

- [x] 2.1 Implement review-only safety repair candidate review generation.
- [x] 2.2 Implement candidate decision rules for row-backed, confirmation-boundary, and broad policy-only themes.
- [x] 2.3 Implement review-only report writing under `reports/public-sample/safety-repair-candidate-design-review/`.

## 3. Evidence and Documentation

- [x] 3.1 Generate `safety_repair_candidate_design_review.json`, `safety_repair_candidate_design_review.md`, and `manifest.json`.
- [x] 3.2 Update `CONTEXT.md` and `reports/final_status.md` with the review-only result and next bounded recommendation.
- [x] 3.3 Generate `docs/human-briefs/2026-06-18-review-safety-repair-candidates-before-materialization.html`.

## 4. Review and Validation

- [x] 4.1 Verify historical blocked-payment safety repair, layered-eval, residual-diagnosis, remediation-target-selection, and safety design artifacts remain unmodified.
- [x] 4.2 Run focused tests, full `python -m pytest -q`, `openspec validate --all --strict`, `PYTHONPATH=src ruff check src tests`, `git diff --check`, and public leak scans.
