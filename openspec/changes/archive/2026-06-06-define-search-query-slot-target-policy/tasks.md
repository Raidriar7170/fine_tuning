## 1. Scope And Proposal

- [x] 1.1 Confirm this is a local policy/target-alignment phase with no A100 execution.
- [x] 1.2 Add OpenSpec proposal, design, spec deltas, and tasks for the search query slot target policy.
- [x] 1.3 Validate the OpenSpec change strictly before implementation.

## 2. Implementation

- [x] 2.1 Add failing tests for compact `slots.query` target data, no `city/date` accepted target shape, prompt metadata visibility, and strict no-normalization/no-repair claims.
- [x] 2.2 Update public-readonly search prompt guidance and prompt constraint metadata.
- [x] 2.3 Update public sample search seed/SFT/DPO target contracts to compact `slots.query` while preserving schema and public-safe validation.
- [x] 2.4 Generate `reports/public-sample/search-query-slot-target-policy/` with manifest, summary report, source links, validation evidence, and leak-scan sidecars.
- [x] 2.5 Generate `docs/human-briefs/2026-06-06-define-search-query-slot-target-policy.html`.

## 3. Validation And Closeout

- [x] 3.1 Run focused tests for formatting, dataset targets, and the new evidence pack.
- [x] 3.2 Run full local validation: pytest, ruff, mypy, public data validation, DPO check, leak scan, diff whitespace check, and OpenSpec strict validation.
- [x] 3.3 Complete Reviewer pass, fix Must Fix items only, archive the OpenSpec change, rerun post-archive/final validation, and commit the phase under guarded integration.
