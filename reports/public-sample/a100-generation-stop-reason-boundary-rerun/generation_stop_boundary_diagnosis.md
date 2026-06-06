# A100 generation stop-boundary train-split diagnosis

Status: A100 prediction-only rerun completed on the train split with the existing private adapter. This is diagnostic evidence, not a benchmark or release.

## Result

- Strict final `json_valid_rate`: `0.0000`
- Strict final `contract_exact_match`: `0.0000`
- Final validated schema-valid rows: `0/3`
- Raw attempts are JSON objects but still miss `task_type`: `3/3`
- Retry attempts remain prose/markdown JSON fragments: `3/3`

## Stop-Boundary Evidence

The rerun recorded `6` generation trace rows, including `3` retry rows. All trace rows include `max_new_tokens_hit`, `finish_state_basis`, `stop_reason_evidence`, `actual_stop_reason_recorded`, and `actual_stop_reason`.

Raw attempts observed tokenizer EOS for `3/3` rows. Retry attempts had `not_recorded_below_max_without_tokenizer_eos` for `3/3` rows. The current code still records `actual_stop_reason_recorded=false` and `actual_stop_reason=null`; actual stop reason remains unknown.

## Boundary

No training, decoding behavior change, retry prompt change, parser relaxation, evaluator metric change, prediction repair, re-score, adapter release, checkpoint release, held-out generalization claim, model recovery claim, model-quality improvement claim, public full-corpus release, or live-browser benchmark claim is made.
