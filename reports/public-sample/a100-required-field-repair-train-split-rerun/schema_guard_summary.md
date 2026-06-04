# Required-Field Repair Schema Guard Summary

This report preserves observed raw and retry attempt evidence. Invalid predictions remain invalid; no coercion or repair is applied to metrics.

## Counts

- Predictions: `3`
- Raw attempt schema-valid: `0`
- Retry attempted: `3`
- Retry attempt schema-valid: `0`
- Validated output schema-valid: `0`
- Validated output source counts: `{'none': 3}`

## Rows

- `seed-search-weather`: raw=`False` (non_json), retry=`False` (json_fragment_object), validated=`False` via `none`
- `seed-search-weather-aug-1`: raw=`False` (json_object), retry=`False` (json_fragment_object), validated=`False` via `none`
- `seed-search-weather-aug-2`: raw=`False` (json_object), retry=`False` (json_fragment_object), validated=`False` via `none`
