## 1. Scope And Proposal

- [x] 1.1 Confirm this is a local evidence-only phase with no A100 execution.
- [x] 1.2 Add OpenSpec proposal, design, spec delta, and tasks for the narrow slot exact-match diagnosis.
- [x] 1.3 Validate the OpenSpec change strictly before implementation.

## 2. Implementation

- [x] 2.1 Add focused tests for retry-template slot exact-match diagnosis, family counts, source strict metrics, privacy boundaries, and no normalization/no-repair claims.
- [x] 2.2 Add a narrow helper/report writer for retry-template slot exact-match mismatch diagnosis.
- [x] 2.3 Generate `reports/public-sample/retry-template-slot-exact-match-mismatch-diagnosis/` from prior public-safe artifacts only.
- [x] 2.4 Generate leak-scan result artifacts and a concise Chinese Human Brief.

## 3. Validation And Closeout

- [x] 3.1 Run focused tests for the new evidence pack.
- [x] 3.2 Run full local validation: pytest, ruff, mypy, data validation, DPO check, leak scan, diff whitespace check, and OpenSpec strict validation.
- [x] 3.3 Complete Reviewer pass, fix Must Fix items only, archive the OpenSpec change, rerun post-archive/final validation, and commit the phase under guarded auto integration.
