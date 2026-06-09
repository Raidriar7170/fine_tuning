## Why

The latest compact-query slot-preservation A100 train-split rerun improved strict JSON/schema validity but still reports `contract_exact_match=0.0`. A narrow local diagnosis is needed to explain whether the remaining exact-match residuals are compact-query slot-shape failures, strict `normalized_command` string differences, or both, without changing model outputs or evaluator semantics.

## What Changes

- Add a public-safe residual diagnosis pack derived only from committed sanitized A100 rerun evidence.
- Classify row-level exact-match residuals by field family, with special attention to `seed-search-weather-aug-1` and compact `slots.query` versus decomposed `city/date/topic`.
- Record inherited strict metrics, source artifact links, leak-scan status, validation commands, and explicit non-claim boundaries.
- Generate a concise Chinese Human Brief for this diagnostic phase.
- Do not run A100, train, rerun predictions, change parser or evaluator behavior, normalize slots, apply semantic-equivalence scoring, repair predictions, replace predictions, or re-score outputs.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `contract-evaluation`: Adds public-safe local diagnosis for compact-query exact-match residuals after the compact-query slot-preservation A100 rerun.

## Impact

- Affected tests: focused evidence-pack regression coverage under the existing A100 SFT prediction smoke tests.
- Affected reports: a new sanitized report directory under `reports/public-sample/` and a phase Human Brief under `docs/human-briefs/`.
- Affected OpenSpec artifacts: a `contract-evaluation` delta spec plus this phase proposal, design, tasks, and archive record.
- No new runtime dependency, public API, training job, private data exposure, or evaluator metric behavior change.
