# Confirmation-rerun row mismatch diagnosis

This is a local evidence-only analysis derived from prior public-sample artifacts. It does not repair, normalize, coerce, replace, or re-score predictions.

## Boundary

- No A100 execution was performed in this phase.
- No training, prediction rerun, prompt change, decoding change, or evaluator metric change was performed.
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
- Schema-invalid predictions: `1`
- Strict final JSON-valid rate remains `0.6666666666666666`
- Strict final contract_exact_match remains `0.0`

## Failure Families

- `missing_required_field_schema_failure`: `1`
- `semantic_task_route_safety_mismatch`: `1`
- `strict_string_field_exact_match_mismatch`: `1`

## Field Mismatch Counts

- `confirmation_required`: `1`
- `normalized_command`: `3`
- `route`: `1`
- `safety.reason`: `1`
- `task_type`: `1`

## Mismatch Category Counts

- `missing_prediction_field`: `1`
- `value_mismatch`: `6`

## Source Artifacts

- `manifest`: `reports/public-sample/a100-confirmation-required-train-split-rerun/manifest.json`
- `metrics`: `reports/public-sample/a100-confirmation-required-train-split-rerun/metrics.json`
- `predictions`: `reports/public-sample/a100-confirmation-required-train-split-rerun/predictions.jsonl`
- `schema_guard_summary`: `reports/public-sample/a100-confirmation-required-train-split-rerun/schema_guard_summary.json`
- `train_split_gold`: `reports/public-sample/a100-confirmation-required-train-split-rerun/train_split_gold.jsonl`

## Row Diagnosis

### `seed-search-weather`

- Primary failure family: `missing_required_field_schema_failure`
- Source schema-valid prediction: `False`
- Validated output schema-valid: `False`
- Validated output source: `none`
- `confirmation_required` (missing_prediction_field): gold bool: False; prediction missing
- `normalized_command` (value_mismatch): gold string(8): 搜索北京明天天气; prediction string(9): 搜索北京明天的天气

### `seed-search-weather-aug-1`

- Primary failure family: `semantic_task_route_safety_mismatch`
- Source schema-valid prediction: `True`
- Validated output schema-valid: `True`
- Validated output source: `raw_attempt`
- `task_type` (value_mismatch): gold string(6): search; prediction string(9): form_fill
- `route` (value_mismatch): gold string(10): search_web; prediction string(8): open_url
- `safety.reason` (value_mismatch): gold string(15): public_readonly; prediction string(9): form_fill
- `normalized_command` (value_mismatch): gold string(8): 搜索北京明天天气; prediction string(8): 查询北京明天天气

### `seed-search-weather-aug-2`

- Primary failure family: `strict_string_field_exact_match_mismatch`
- Source schema-valid prediction: `True`
- Validated output schema-valid: `True`
- Validated output source: `raw_attempt`
- `normalized_command` (value_mismatch): gold string(8): 搜索北京明天天气; prediction string(9): 搜索北京明天的天气
