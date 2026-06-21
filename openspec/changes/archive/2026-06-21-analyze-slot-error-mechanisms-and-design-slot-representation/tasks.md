## 1. Boundary And Test Scaffolding

- [x] 1.1 Add focused tests for recovered-input boundary validation, slot flattening/alignment, missing/extra/alias classification, source support, prediction provenance, paired movement, report reproducibility, and non-mutation guarantees.
- [x] 1.2 Confirm the new tests fail before the implementation module/report command exists.

## 2. Deterministic Slot Analysis

- [x] 2.1 Implement `src/voice2task/slot_error_analysis.py` as a read-only deterministic analyzer with fail-closed input validation.
- [x] 2.2 Implement stable slot-path flattening, same-key alignment, alias-key candidate recording, mechanism taxonomy assignment, source support labels, value-type profiling, and prediction provenance labels.
- [x] 2.3 Implement Control/Treatment paired movement metrics and task-family/slot-path aggregation.
- [x] 2.4 Implement representation feasibility scoring, confidence labels, final decision label selection, and one recommended next change.

## 3. Report Generation And Evidence

- [x] 3.1 Add a bounded report script or CLI command that only accepts the approved recovered raw-input directory and output directory.
- [x] 3.2 Generate `reports/public-sample/slot-error-mechanism-analysis/` with only the approved compact artifact files.
- [x] 3.3 Write `docs/slot-representation.md` from the generated analysis and keep it design-only.
- [x] 3.4 Add a concise Chinese Human Brief under `docs/human-briefs/2026-06-21-analyze-slot-error-mechanisms-and-design-slot-representation.html`.
- [x] 3.5 Update README, CONTEXT, and the public evidence index briefly with the final decision label, next change, and no-training/no-model-improvement boundary.

## 4. Verification, Review, And Closeout

- [x] 4.1 Run targeted tests and confirm the new report is reproducible and public-safe.
- [x] 4.2 Run `PYTHONPATH=src pytest -q`.
- [x] 4.3 Run `PYTHONPATH=src ruff check src tests`.
- [x] 4.4 Run `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`.
- [x] 4.5 Run `python scripts/check_current_truth_surface.py`.
- [x] 4.6 Run `git diff --check` and a public leak scan over the new artifacts/docs.
- [x] 4.7 Complete a read-only Reviewer pass, fix Must Fix items if any, then archive the OpenSpec change if all tasks are complete.
