# A100 public held-out residual repair train schema diagnostics

This diagnostic is evidence-only: invalid predictions remain invalid. It does not repair, normalize, or convert private-adapter predictions into valid contracts.

## Boundary

- This is not a checkpoint release.
- This is not an adapter release.
- This makes no production-readiness claim.
- This makes no full-private-corpus claim.
- This is not a live-browser benchmark or benchmark-improvement claim.

## Summary

- Gold rows: `18`
- Predictions: `18`
- Invalid predictions: `2`

## Issue Counts

- `empty_required_string`: `1`
- `invalid_literal`: `1`

## Row Issues

### `seed-form-nickname-aug-1`

- `safety.reason` (empty_required_string): observed empty string; expected must be a non-empty string

### `seed-form-nickname-aug-2`

- `contract_version` (invalid_literal): observed int: 1; expected must be v1
