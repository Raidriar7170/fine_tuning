## 1. Test-First Coverage

- [x] 1.1 Add focused tests for proposal/readiness artifact presence, source
  review traceability, readiness gating, and execution-scope flags.
- [x] 1.2 Add tests that only slot-key alias and conservative slot-value
  boundary classes are eligible for later formal merge planning.
- [x] 1.3 Add tests that normalized-command diagnostics and excluded
  non-equivalence cases remain outside future formal merge eligibility.
- [x] 1.4 Add tests that formal public sample files, the source candidate
  review/materialization artifacts, and the stale active
  `merge-scaled-clarify-slot-boundary-candidates` change remain unmodified.

## 2. Proposal / Readiness Evidence

- [x] 2.1 Generate
  `reports/public-sample/canonical-slot-boundary-formal-merge-proposal/summary.json`.
- [x] 2.2 Generate
  `reports/public-sample/canonical-slot-boundary-formal-merge-proposal/summary.md`.
- [x] 2.3 Generate a report-local leak scan record.
- [x] 2.4 Record missing row-level candidate source and
  `formal_merge_ready_now=false`.
- [x] 2.5 Record future merge acceptance criteria, comparison-boundary
  requirements, validation plan, and claims not to overstate.

## 3. Documentation and Human Brief

- [x] 3.1 Update `CONTEXT.md` and `reports/final_status.md` with the
  proposal/readiness result if the phase completes.
- [x] 3.2 Generate
  `docs/human-briefs/2026-06-19-propose-canonical-slot-boundary-formal-merge-after-review.html`.

## 4. Review and Validation

- [x] 4.1 Run Worker implementation in the approved current workspace with
  minimal task-related changes.
- [x] 4.2 Run Reviewer diff review and address in-scope Must Fix items.
- [x] 4.3 Run focused tests, full `python -m pytest -q`,
  `openspec validate --all --strict`, `git diff --check`, and public leak-scan
  checks.
- [x] 4.4 Archive the completed OpenSpec change only after validation and
  review pass.
