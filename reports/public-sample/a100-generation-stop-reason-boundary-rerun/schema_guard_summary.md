# A100 generation stop-boundary schema guard summary

Status: train-internal A100 prediction rerun using the existing private adapter. This summary is strict schema evidence only.

## Counts

- Predictions: `3`
- Raw attempts parsed as JSON objects: `3/3`
- Raw attempts missing `task_type`: `3/3`
- Retry attempts parsed as JSON fragments/wrappers: `3/3`
- Final validated schema-valid rows: `0/3`
- Generation trace rows: `6` total, including `3` retry rows
- New stop-boundary fields present on all trace rows: `True`
- Actual stop reasons recorded by generation API: `0`
- `max_new_tokens_hit` rows: `0`

## Boundary

The raw/retry schema failures are preserved by the strict parser. The trace now distinguishes tokenizer-EOS observations from below-max-token generations without a recorded actual stop reason. This is instrumentation evidence, not prediction repair, not parser relaxation, and not model recovery.
