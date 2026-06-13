# A100 public held-out residual repair dev constrained decoding diagnosis

This diagnosis is A100 prediction-rerun evidence with a strict non-repair boundary: model outputs are not repaired, normalized, coerced, replaced, re-scored, or relaxed.

## Boundary

- This is not a checkpoint release.
- This is not an adapter release.
- This is not a model recovery claim.
- This is not held-out generalization evidence.
- This makes no production-readiness claim.
- This makes no full-private-corpus claim.
- This is not a live-browser benchmark or benchmark-improvement claim.

## Summary

- Predictions: `6`
- Decoded summary rows: `6`
- Prediction schema-valid count: `6`
- Invalid predictions: `0`
- Raw attempt schema-valid count: `0`
- Retry attempt schema-valid count: `6`
- Validated output schema-valid count: `6`
- Legacy task_type alias count: `0`
- Path-like route count: `0`
- Prose/Markdown wrapper count: `2`

## Parse Status Counts

### `raw_attempt`

- `json_object`: `4`
- `non_json`: `2`

### `retry_attempt`

- `json_object`: `6`

## Symptom Examples

### `legacy_task_type_alias`

- none

### `path_like_route`

- none

### `prose_markdown_wrapper`

- `seed-clarify-ambiguous-aug-1` `raw_attempt`: non_json
- `seed-clarify-ambiguous-aug-2` `raw_attempt`: non_json
