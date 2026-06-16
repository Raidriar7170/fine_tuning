## 1. Readiness

- [x] 1.1 Verify repo state, active OpenSpec status, candidate source artifact, prior preview evidence, current formal counts, and formal merge scope.
- [x] 1.2 Run an Explorer pass or local pattern review for existing formal merge helpers, report writers, CLI commands, tests, and public-safety patterns.

## 2. Formal Merge

- [x] 2.1 Add failing tests for confirmation-marker extension candidate formal merge, including pre/post counts, split counts, formal artifact synchronization, duplicate-ID rejection, validation status, DPO contribution counts, and claim boundaries.
- [x] 2.2 Implement a guarded merge helper that validates exactly the 12 candidate rows, rejects duplicate formal IDs, appends candidates to the formal seed file, rebuilds formal public SFT/DPO/manifest artifacts, and validates them.
- [x] 2.3 Add a `voice2task-data` CLI entry point and report writer that publish formal merge JSON, Markdown, and manifest evidence.
- [x] 2.4 Run the merge command to update `data/public-samples/seed_traces.jsonl`, `sft_public_sample.jsonl`, `dpo_public_sample.jsonl`, and `manifest_public_sample.json`.
- [x] 2.5 Generate committed merge evidence under `reports/public-sample/form-fill-confirmation-marker-extension-merge/`.

## 3. Reporting And Validation

- [x] 3.1 Generate `docs/human-briefs/2026-06-16-merge-form-fill-confirmation-marker-extension-candidates.html`.
- [x] 3.2 Run focused tests, related dataset/form-fill tests, full tests, ruff, OpenSpec strict validation, public dataset validation on the updated formal sample, DPO check, leak scan, and `git diff --check`.
- [x] 3.3 Run a Reviewer pass and fix in-scope Must Fix items.
- [x] 3.4 Archive the OpenSpec change after tasks complete and validations pass.
