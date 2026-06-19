## 1. Test-First Coverage

- [x] 1.1 Add focused tests for row-level candidate source presence, counts,
  schema validity, split labels, and provenance.
- [x] 1.2 Add tests that eligible rows come only from `slot_key_aliases` and
  `slot_value_boundaries`.
- [x] 1.3 Add tests that normalized-command diagnostics and excluded
  non-equivalence cases are not materialized.
- [x] 1.4 Add tests that formal public sample files, source review/materialize
  artifacts, and the stale active `merge-scaled-clarify-slot-boundary-candidates`
  change remain unmodified.

## 2. Row-Level Candidate Materialization

- [x] 2.1 Generate
  `data/public-samples/canonical_slot_boundary_seed_candidates.jsonl`.
- [x] 2.2 Generate report-local SFT candidate preview rows under
  `reports/public-sample/canonical-slot-boundary-row-level-candidates/`.
- [x] 2.3 Generate machine-readable materialization evidence, a human-readable
  summary, a manifest, and leak-scan result.
- [x] 2.4 Record candidate counts, split counts, eligible source classes,
  excluded classes, formal data boundary, comparison-boundary warning, and
  claims not to overstate.

## 3. Documentation and Human Brief

- [x] 3.1 Update `CONTEXT.md` and `reports/final_status.md` with the standalone
  row-level materialization result if the phase completes.
- [x] 3.2 Generate
  `docs/human-briefs/2026-06-19-materialize-canonical-slot-boundary-row-level-candidates.html`.

## 4. Review and Validation

- [x] 4.1 Run Worker implementation in the approved current workspace with
  minimal task-related changes.
- [x] 4.2 Run Reviewer diff review and address in-scope Must Fix items.
- [x] 4.3 Run focused tests, full `python -m pytest -q`,
  `openspec validate --all --strict`, `git diff --check`, public dataset
  validation, DPO check, and public leak-scan checks.
- [x] 4.4 Archive the completed OpenSpec change only after validation and
  review pass.
