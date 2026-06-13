# A100 extract-price contract residual alignment diagnostics

This diagnostic is evidence-only: invalid predictions remain invalid. It reports field-level public-sample evidence only and does not repair, normalize, coerce, or replace prediction fields.

## Boundary

- This is not a checkpoint release.
- This is not an adapter release.
- This makes no production-readiness claim.
- This makes no full-private-corpus claim.
- This is not a live-browser benchmark or benchmark-improvement claim.

## Summary

- Gold rows: `6`
- Predictions: `6`
- Rows with mismatches: `3`
- Schema-invalid predictions: `0`

## Field Mismatch Counts

- `normalized_command`: `3`
- `slots`: `2`

## Mismatch Category Counts

- `value_mismatch`: `5`

## Row Mismatches

### `seed-extract-price`

- `normalized_command` (value_mismatch): gold string(8): 提取页面商品价格; prediction string(10): 提取页面上的商品价格

### `seed-extract-price-aug-1`

- `slots` (value_mismatch): gold object with keys: target; prediction object with keys: target
- `normalized_command` (value_mismatch): gold string(8): 提取页面商品价格; prediction string(4): 页面价格

### `seed-extract-price-aug-2`

- `slots` (value_mismatch): gold object with keys: target; prediction object with keys: target
- `normalized_command` (value_mismatch): gold string(8): 提取页面商品价格; prediction string(6): 提取页面标价
