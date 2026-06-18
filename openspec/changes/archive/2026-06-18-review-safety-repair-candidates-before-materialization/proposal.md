## Why

The safety repair candidate design is now complete, but its recommended next
step is review before materialization. Because safety-related candidates can
change public data and later training behavior, the next bounded phase should
publish explicit review evidence before any seed rows, data merge, prediction
rerun, or training phase.

## What Changes

- Add review-only evidence under
  `reports/public-sample/safety-repair-candidate-design-review/`.
- Read the committed safety repair candidate design as source evidence.
- Classify each candidate theme as ready for a later bounded materialization
  proposal, deferred to policy design, or rejected before materialization.
- Record review rationale, follow-up constraints, unsupported claims, and
  machine-readable no-materialization/no-training boundaries.
- Add tests that enforce review-only scope, source-design consistency, public
  leak-scan cleanliness, and no historical evidence mutation.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `voice2task-dataset-preparation`: add review evidence for safety repair
  candidate themes before any materialization or public-sample mutation.

## Impact

- New or updated review-report code under `src/voice2task/`.
- New public-safe review artifacts under
  `reports/public-sample/safety-repair-candidate-design-review/`.
- New focused tests under `tests/`.
- New Human Brief HTML and OpenSpec archive material for this phase.
