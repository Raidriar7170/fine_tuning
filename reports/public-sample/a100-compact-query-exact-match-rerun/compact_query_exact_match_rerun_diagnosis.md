# A100 compact-query exact-match rerun diagnosis

This is A100 public-sample train-split diagnostic evidence. It does not claim held-out generalization, production readiness, checkpoint release, adapter release, parser relaxation, evaluator relaxation, prediction repair, or model recovery.

## Result

- Train predictions: `6`
- Schema-valid predictions: `6/6`
- Strict `contract_exact_match`: `0.5000`
- Strict `slot_f1`: `0.5000`
- Internal-only `slot_f1_soft`: `0.5000`
- Compact-query exact rows: `3/3`
- Compact-query decomposed `city/date/topic` rows: `0`
- Remaining non-compact extract residual rows: `3`

## Interpretation

The prior compact-query residual row now uses compact `slots.query` and exact `normalized_command` on the search/weather train rows. The compact-query residual family improved under this controlled 7B rerun.

The overall train split is not fully recovered: three extract-price rows still mismatch strict slots and/or normalized command, and one extract paraphrase is predicted as search. Keep the claim bounded to compact-query train-split evidence.

## Public Artifacts

- `predictions`: `reports/public-sample/a100-compact-query-exact-match-rerun/predictions.jsonl`
- `prediction_metadata`: `reports/public-sample/a100-compact-query-exact-match-rerun/prediction_metadata.json`
- `metrics`: `reports/public-sample/a100-compact-query-exact-match-rerun/metrics.json`
- `schema_guard_summary`: `reports/public-sample/a100-compact-query-exact-match-rerun/schema_guard_summary.json`
- `alignment_diagnostics`: `reports/public-sample/a100-compact-query-exact-match-rerun/alignment_diagnostics.json`
- `constrained_decoding_diagnosis`: `reports/public-sample/a100-compact-query-exact-match-rerun/constrained_decoding_diagnosis.json`
- `prompt_snapshot`: `reports/public-sample/a100-compact-query-exact-match-rerun/prompt_snapshot.json`
- `raw_decoded_summary`: `reports/public-sample/a100-compact-query-exact-match-rerun/raw_decoded_summary.jsonl`
- `generation_trace`: `reports/public-sample/a100-compact-query-exact-match-rerun/generation_trace.jsonl`
- `train_split_gold`: `reports/public-sample/a100-compact-query-exact-match-rerun/train_split_gold.jsonl`
