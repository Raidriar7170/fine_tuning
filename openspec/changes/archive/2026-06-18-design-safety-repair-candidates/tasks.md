## 1. Test-First Coverage

- [x] 1.1 Add tests for safety repair candidate design ingestion from current remediation target-selection, layered-eval, and residual-diagnosis artifacts.
- [x] 1.2 Add tests for design-only execution scope, candidate theme structure, and safety claim boundaries.
- [x] 1.3 Add tests that committed safety design artifacts are public-safe and do not modify historical evidence.

## 2. Core Implementation

- [x] 2.1 Implement current-artifact safety repair candidate design generation.
- [x] 2.2 Implement public-safe candidate themes, accepted target sketches, rejected drift sketches, and evidence rationale.
- [x] 2.3 Implement design-only report writing under `reports/public-sample/safety-repair-candidate-design/`.

## 3. Evidence and Documentation

- [x] 3.1 Generate `safety_repair_candidate_design.json`, `safety_repair_candidate_design.md`, and `manifest.json`.
- [x] 3.2 Update `CONTEXT.md` and `reports/final_status.md` with the design-only result and next bounded recommendation.
- [x] 3.3 Generate `docs/human-briefs/2026-06-18-design-safety-repair-candidates.html`.

## 4. Review and Validation

- [x] 4.1 Verify historical blocked-payment safety repair, layered-eval, residual-diagnosis, and remediation-target-selection artifacts remain unmodified.
- [x] 4.2 Run focused tests, full `python -m pytest -q`, `openspec validate --all --strict`, `PYTHONPATH=src ruff check src tests`, `git diff --check`, and public leak scans.
