## 1. Alignment Diagnostics

- [x] 1.1 Add failing tests for target-vs-prediction alignment diagnostics on schema-invalid but contract-like predictions.
- [x] 1.2 Implement diagnostic helpers that report row id, field path, mismatch category, gold value summary, and prediction value summary without repairing invalid predictions.
- [x] 1.3 Add a CLI/report path that writes public-safe JSON and Markdown alignment diagnostics for a gold/prediction pair.

## 2. Evidence

- [x] 2.1 Generate an alignment diagnostic report for `reports/public-sample/a100-sft-post-recovery-rerun/predictions.jsonl`.
- [x] 2.2 Ensure the report states that the analysis is field-level public-sample evidence only and makes no checkpoint, adapter, production, full-corpus, or live-browser benchmark claim.

## 3. Validation and Closeout

- [x] 3.1 Run focused tests for evaluator/reports and A100 prediction smoke.
- [x] 3.2 Run public dataset validation, DPO pair checks, post-recovery metrics, schema diagnostics, alignment diagnostics, post-recovery controlled smoke, public leak scan on generated alignment diagnostics, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`, and `git diff --check`.
- [x] 3.3 Generate the Chinese Human Brief HTML and archive the completed OpenSpec change when validation evidence is fresh.
