## 1. Test-First Coverage

- [x] 1.1 Add focused tests for guarded canonical slot-boundary formal merge,
  candidate source validation, duplicate rejection, already-formal rejection,
  and provenance promotion.
- [x] 1.2 Add tests that formal SFT/DPO/manifest artifacts are regenerated and
  validate after merge.
- [x] 1.3 Add tests for merge evidence, comparison-boundary warnings,
  fail-closed claims, and public leak-scan cleanliness.

## 2. Merge Implementation

- [x] 2.1 Add a dataset helper that merges exactly the reviewed canonical
  slot-boundary row-level candidates into the formal public sample.
- [x] 2.2 Add CLI support for the guarded merge.
- [x] 2.3 Add merge evidence/report generation under
  `reports/public-sample/canonical-slot-boundary-formal-merge/`.
- [x] 2.4 Rebuild formal public sample seed, SFT, DPO, and manifest artifacts.

## 3. Documentation and Human Brief

- [x] 3.1 Update `CONTEXT.md` and `reports/final_status.md` with the new formal
  data boundary if the phase completes.
- [x] 3.2 Generate
  `docs/human-briefs/2026-06-19-merge-canonical-slot-boundary-row-level-candidates.html`.

## 4. Review and Validation

- [x] 4.1 Run Worker implementation in the approved current workspace with
  minimal task-related changes.
- [x] 4.2 Run Reviewer diff review and address in-scope Must Fix items.
- [x] 4.3 Run focused tests, full `python -m pytest -q`, public dataset
  validation, DPO check, `openspec validate --all --strict`, public leak-scan,
  and `git diff --check`.
- [x] 4.4 Archive the completed OpenSpec change only after validation and
  review pass.
