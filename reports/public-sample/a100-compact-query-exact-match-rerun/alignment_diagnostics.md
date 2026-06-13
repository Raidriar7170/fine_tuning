# A100 compact-query exact-match rerun alignment diagnostics

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
- `route`: `1`
- `slots`: `3`
- `task_type`: `1`

## Mismatch Category Counts

- `value_mismatch`: `8`

## Row Mismatches

### `seed-extract-price`

- `slots` (value_mismatch): gold object with keys: target; prediction object with keys: page_url, query
- `normalized_command` (value_mismatch): gold string(8): 提取页面商品价格; prediction string(9): 提取页面上商品价格

### `seed-extract-price-aug-1`

- `task_type` (value_mismatch): gold string(7): extract; prediction string(6): search
- `route` (value_mismatch): gold string(12): extract_page; prediction string(10): search_web
- `slots` (value_mismatch): gold object with keys: target; prediction object with keys: query
- `normalized_command` (value_mismatch): gold string(8): 提取页面商品价格; prediction string(8): 搜索现在卖多少钱

### `seed-extract-price-aug-2`

- `slots` (value_mismatch): gold object with keys: target; prediction object with keys: query
- `normalized_command` (value_mismatch): gold string(8): 提取页面商品价格; prediction string(8): 提取页面上的价格
