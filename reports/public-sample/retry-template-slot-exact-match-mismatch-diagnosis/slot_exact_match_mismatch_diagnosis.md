# Retry-template slot exact-match mismatch diagnosis

This is a local evidence-only analysis derived from prior public-sample artifacts. It explains strict slot exact-match failures only; it does not perform slot normalization, semantic-equivalence scoring, prediction repair, prediction replacement, or re-score.

## Boundary

- No A100 execution was performed in this phase.
- No training, prediction rerun, prompt change, decoding change, schema change, parser change, retry change, or evaluator metric change was performed.
- This is not slot normalization.
- This is not normalized-command normalization.
- This is not semantic-equivalence scoring.
- This is not a checkpoint release.
- This is not an adapter release.
- This is not held-out generalization evidence.
- This makes no production-readiness claim.
- This makes no public full-corpus release claim.
- This is not a live-browser benchmark improvement claim.
- This is not model-quality improvement evidence.

## Summary

- Gold rows: `3`
- Predictions: `3`
- Rows with mismatches: `3`
- Schema-invalid predictions: `0`
- Validated output schema-valid rows: `3`
- Normalized-command mismatches: `1`
- Strict final JSON-valid rate remains `1.0`
- Strict final slot_f1 remains `0.0`
- Strict final contract_exact_match remains `0.0`

## Slot Families

- `city_date_slots_instead_of_query`: `2`
- `query_slot_strict_string_mismatch`: `1`

## Field Mismatch Counts

- `normalized_command`: `1`
- `slots`: `3`

## Source Artifacts

- `manifest`: `reports/public-sample/a100-retry-template-boundary-rerun/manifest.json`
- `metrics`: `reports/public-sample/a100-retry-template-boundary-rerun/metrics.json`
- `predictions`: `reports/public-sample/a100-retry-template-boundary-rerun/predictions.jsonl`
- `retry_template_boundary_diagnosis`: `reports/public-sample/a100-retry-template-boundary-rerun/retry_template_boundary_diagnosis.json`
- `schema_guard_summary`: `reports/public-sample/a100-retry-template-boundary-rerun/schema_guard_summary.json`
- `train_split_gold`: `reports/public-sample/a100-retry-template-boundary-rerun/train_split_gold.jsonl`

## Row Diagnosis

### `seed-search-weather`

- Primary slot mismatch family: `city_date_slots_instead_of_query`
- Normalized-command mismatch present: `True`
- Source schema-valid prediction: `True`
- Validated output schema-valid: `True`
- Validated output source: `retry_attempt`
- `slots` (value_mismatch): gold object with keys: query; prediction object with keys: city, date
- `normalized_command` (value_mismatch): gold string(8): 搜索北京明天天气; prediction string(11): 帮我搜索北京明天的天气

### `seed-search-weather-aug-1`

- Primary slot mismatch family: `city_date_slots_instead_of_query`
- Normalized-command mismatch present: `False`
- Source schema-valid prediction: `True`
- Validated output schema-valid: `True`
- Validated output source: `raw_attempt`
- `slots` (value_mismatch): gold object with keys: query; prediction object with keys: city, date

### `seed-search-weather-aug-2`

- Primary slot mismatch family: `query_slot_strict_string_mismatch`
- Normalized-command mismatch present: `False`
- Source schema-valid prediction: `True`
- Validated output schema-valid: `True`
- Validated output source: `retry_attempt`
- `slots` (value_mismatch): gold object with keys: query; prediction object with keys: query
