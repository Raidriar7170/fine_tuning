## 1. Diagnostics

- [x] 1.1 Add tests for field-level Browser Task Contract schema mismatch diagnostics on contract-like predictions.
- [x] 1.2 Implement diagnostic helpers that report row id, field path, issue category, observed value summary, and expected constraint without repairing invalid predictions.
- [x] 1.3 Add a CLI/report path that writes public-safe JSON and Markdown diagnostics for a gold/prediction pair.

## 2. Evidence

- [x] 2.1 Generate a diagnostic report for `reports/public-sample/a100-sft-post-recovery-rerun/predictions.jsonl`.
- [x] 2.2 Ensure the report states that invalid private-adapter predictions remain invalid and makes no checkpoint, adapter, production, full-corpus, or live-browser benchmark claim.

## 3. Validation and Closeout

- [x] 3.1 Run focused tests for schemas, evaluator/reports, formatting/training, and A100 prediction smoke.
- [x] 3.2 Run public dataset validation, DPO pair checks, post-recovery metrics, post-recovery controlled smoke, leak scan on generated diagnostics, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`, and `git diff --check`.
- [x] 3.3 Generate the Chinese Human Brief HTML and archive the completed OpenSpec change when validation evidence is fresh.
