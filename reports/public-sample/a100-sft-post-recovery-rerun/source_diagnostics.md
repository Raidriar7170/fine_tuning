# A100 SFT post-recovery training/prompt/decoding diagnostics

This source diagnostic is evidence-only: invalid predictions remain invalid. It does not repair, normalize, coerce, or replace predictions.

## Boundary

- This is not a checkpoint release.
- This is not an adapter release.
- This makes no production-readiness claim.
- This makes no full-private-corpus claim.
- This is not a live-browser benchmark or benchmark-improvement claim.

## Summary

- Gold rows: `12`
- Predictions: `12`
- Gold path-like route targets: `0`
- Gold list-shaped slots targets: `0`
- Prediction path-like routes: `12`
- Prediction list-shaped slots: `11`
- Schema-invalid predictions: `12`

## Split And Training Coverage

- Configured training split: `train`
- Configured prediction split: `all`
- Training rows in gold sample: `3`
- Prediction-split gold rows: `12`
- Gold split counts: `{'dev': 3, 'test': 6, 'train': 3}`
- Training task_type coverage: `{'search': 3}`
- Training route coverage: `{'search_web': 3}`

## Current Prompt Constraints

These describe the current formatter and future rerun preparation. They are not proof that older prediction artifacts used this strengthened prompt.

- task_type enum visible: `True`
- route enum visible: `True`
- route is not a URL/path visible: `True`
- slots object-not-array visible: `True`

## Prediction-Run Prompt Evidence

- prompt constraints present in metadata: `False`
- fields present: `[]`
- constraints: `{}`
- evidence gaps: `['prompt_constraints_at_prediction_time']`
- current prompt constraints are rerun preparation, not old-run evidence: `True`

## Decoding Evidence

Evidence gaps are missing evidence, not inferred cause.

- decoding_policy present: `False`
- fields present: `[]`
- policy: `{}`
- evidence gaps: `['decoding_policy', 'raw_decoded_sidecar', 'generated_token_count', 'eos_or_finish_state']`

## Symptom Examples

### Path-like Routes

- `seed-search-weather`: string(14): /weather/query
- `seed-search-weather-aug-1`: string(8): /weather
- `seed-search-weather-aug-2`: string(8): /weather
- `seed-open-example`: string(12): /example.com
- `seed-open-example-aug-1`: string(12): /example.com

### List-shaped Slots

- `seed-search-weather`: array with 0 item(s)
- `seed-search-weather-aug-1`: array with 1 item(s)
- `seed-search-weather-aug-2`: array with 0 item(s)
- `seed-open-example`: array with 0 item(s)
- `seed-open-example-aug-1`: array with 0 item(s)
