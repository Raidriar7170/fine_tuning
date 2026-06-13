## 1. Local TDD And Diagnostic Design

- [x] 1.1 Add failing tests for public SFT learning-signal summaries, including split/task counts, target-span presence, target-pressure summaries, and unavailable runtime label evidence.
- [x] 1.2 Add failing evidence-boundary tests for the learning-signal manifest/report and prior negative repair metrics.
- [x] 1.3 Implement the minimal local diagnostic helper and/or CLI path required to pass those tests.

## 2. Evidence Generation

- [x] 2.1 Run the diagnostic against `data/public-samples/manifest_public_sample.json` and committed public SFT rows.
- [x] 2.2 Generate `reports/public-sample/sft-contract-learning-signal/` JSON, Markdown, manifest, and leak-scan artifacts.
- [x] 2.3 Generate `docs/human-briefs/2026-06-13-diagnose-sft-contract-learning-signal.html`.

## 3. Validation And Review

- [x] 3.1 Run focused tests for the diagnostic and evidence boundaries.
- [x] 3.2 Run full validation: `PYTHONPATH=src pytest -q`, `uv run ruff check .`, `uv run mypy src`, public data validate, DPO check, OpenSpec strict, public leak scan, and `git diff --check`.
- [x] 3.3 Perform a read-only diff/evidence review for Must Fix issues and rerun affected validation.

## 4. Archive And Integration

- [x] 4.1 Archive the OpenSpec change after successful validation and rerun post-archive validation.
- [x] 4.2 Auto-stage and commit only in-scope phase files when guarded auto-integration remains safe.
