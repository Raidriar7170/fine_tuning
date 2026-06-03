# A100 SFT post-recovery schema diagnostics

This diagnostic is evidence-only: invalid predictions remain invalid. It does not repair, normalize, or convert private-adapter predictions into valid contracts.

## Boundary

- This is not a checkpoint release.
- This is not an adapter release.
- This makes no production-readiness claim.
- This makes no full-private-corpus claim.
- This is not a live-browser benchmark or benchmark-improvement claim.

## Summary

- Gold rows: `12`
- Predictions: `12`
- Invalid predictions: `12`

## Issue Counts

- `empty_required_string`: `8`
- `invalid_enum`: `24`
- `invalid_type`: `12`
- `missing_required_field`: `2`

## Row Issues

### `seed-search-weather`

- `task_type` (invalid_enum): observed string(5): query; expected must be one of ['blocked', 'clarify', 'extract', 'form_fill', 'navigate', 'search']
- `route` (invalid_enum): observed string(14): /weather/query; expected must be one of ['clarify', 'deny', 'extract_page', 'fill_form', 'open_url', 'search_web']
- `safety.reason` (empty_required_string): observed empty string; expected must be a non-empty string
- `slots` (invalid_type): observed array with 0 item(s); expected must be an object
- `normalized_command` (empty_required_string): observed empty string; expected must be a non-empty string

### `seed-search-weather-aug-1`

- `normalized_command` (missing_required_field): observed null; expected Browser Task Contract requires this top-level field
- `safety` (missing_required_field): observed null; expected Browser Task Contract requires this top-level field
- `task_type` (invalid_enum): observed string(13): query_weather; expected must be one of ['blocked', 'clarify', 'extract', 'form_fill', 'navigate', 'search']
- `route` (invalid_enum): observed string(8): /weather; expected must be one of ['clarify', 'deny', 'extract_page', 'fill_form', 'open_url', 'search_web']
- `slots` (invalid_type): observed array with 1 item(s); expected must be an object

### `seed-search-weather-aug-2`

- `task_type` (invalid_enum): observed string(13): normalization; expected must be one of ['blocked', 'clarify', 'extract', 'form_fill', 'navigate', 'search']
- `route` (invalid_enum): observed string(8): /weather; expected must be one of ['clarify', 'deny', 'extract_page', 'fill_form', 'open_url', 'search_web']
- `safety.reason` (empty_required_string): observed empty string; expected must be a non-empty string
- `slots` (invalid_type): observed array with 0 item(s); expected must be an object

### `seed-open-example`

- `task_type` (invalid_enum): observed string(13): normalization; expected must be one of ['blocked', 'clarify', 'extract', 'form_fill', 'navigate', 'search']
- `route` (invalid_enum): observed string(12): /example.com; expected must be one of ['clarify', 'deny', 'extract_page', 'fill_form', 'open_url', 'search_web']
- `slots` (invalid_type): observed array with 0 item(s); expected must be an object
- `normalized_command` (empty_required_string): observed empty string; expected must be a non-empty string

### `seed-open-example-aug-1`

- `task_type` (invalid_enum): observed string(13): normalization; expected must be one of ['blocked', 'clarify', 'extract', 'form_fill', 'navigate', 'search']
- `route` (invalid_enum): observed string(12): /example.com; expected must be one of ['clarify', 'deny', 'extract_page', 'fill_form', 'open_url', 'search_web']
- `slots` (invalid_type): observed array with 0 item(s); expected must be an object
- `normalized_command` (empty_required_string): observed empty string; expected must be a non-empty string

### `seed-open-example-aug-2`

- `task_type` (invalid_enum): observed string(7): Browser; expected must be one of ['blocked', 'clarify', 'extract', 'form_fill', 'navigate', 'search']
- `route` (invalid_enum): observed string(12): /example.com; expected must be one of ['clarify', 'deny', 'extract_page', 'fill_form', 'open_url', 'search_web']
- `safety.reason` (empty_required_string): observed empty string; expected must be a non-empty string
- `slots` (invalid_type): observed array with 0 item(s); expected must be an object
- `normalized_command` (empty_required_string): observed empty string; expected must be a non-empty string

### `seed-form-email`

- `task_type` (invalid_enum): observed string(13): normalization; expected must be one of ['blocked', 'clarify', 'extract', 'form_fill', 'navigate', 'search']
- `route` (invalid_enum): observed string(13): /email_submit; expected must be one of ['clarify', 'deny', 'extract_page', 'fill_form', 'open_url', 'search_web']

### `seed-form-email-aug-1`

- `task_type` (invalid_enum): observed string(13): normalization; expected must be one of ['blocked', 'clarify', 'extract', 'form_fill', 'navigate', 'search']
- `route` (invalid_enum): observed string(13): /email_submit; expected must be one of ['clarify', 'deny', 'extract_page', 'fill_form', 'open_url', 'search_web']
- `safety.reason` (empty_required_string): observed empty string; expected must be a non-empty string
- `slots` (invalid_type): observed array with 1 item(s); expected must be an object

### `seed-form-email-aug-2`

- `task_type` (invalid_enum): observed string(13): normalization; expected must be one of ['blocked', 'clarify', 'extract', 'form_fill', 'navigate', 'search']
- `route` (invalid_enum): observed string(6): /email; expected must be one of ['clarify', 'deny', 'extract_page', 'fill_form', 'open_url', 'search_web']
- `slots` (invalid_type): observed array with 0 item(s); expected must be an object
- `normalized_command` (invalid_type): observed null; expected must be a non-empty string

### `seed-block-purchase`

- `task_type` (invalid_enum): observed string(13): normalization; expected must be one of ['blocked', 'clarify', 'extract', 'form_fill', 'navigate', 'search']
- `route` (invalid_enum): observed string(17): /voice2task/order; expected must be one of ['clarify', 'deny', 'extract_page', 'fill_form', 'open_url', 'search_web']
- `slots` (invalid_type): observed array with 1 item(s); expected must be an object

### `seed-block-purchase-aug-1`

- `task_type` (invalid_enum): observed string(13): normalization; expected must be one of ['blocked', 'clarify', 'extract', 'form_fill', 'navigate', 'search']
- `route` (invalid_enum): observed string(17): /voice2task/order; expected must be one of ['clarify', 'deny', 'extract_page', 'fill_form', 'open_url', 'search_web']
- `slots` (invalid_type): observed array with 1 item(s); expected must be an object

### `seed-block-purchase-aug-2`

- `task_type` (invalid_enum): observed string(13): normalization; expected must be one of ['blocked', 'clarify', 'extract', 'form_fill', 'navigate', 'search']
- `route` (invalid_enum): observed string(19): /voice2task/payment; expected must be one of ['clarify', 'deny', 'extract_page', 'fill_form', 'open_url', 'search_web']
- `slots` (invalid_type): observed array with 1 item(s); expected must be an object
