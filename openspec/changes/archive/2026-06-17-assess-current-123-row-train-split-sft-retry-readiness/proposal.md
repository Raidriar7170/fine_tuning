## Why

The formal public sample advanced to `public-sample-20260617T045941Z` after current-retry confirmation-preservation materialization, but the latest model evidence is still bound to the prior `public-sample-20260616T165835Z` train split. Before launching another private A100 SFT retry, the project needs a bounded readiness-only evidence pack that confirms the new 123-row train split, config boundary, and non-claim posture.

## What Changes

- Add a current-123-row train-split SFT retry readiness evidence phase.
- Generate dry-run metadata and a public-safe readiness report for `public-sample-20260617T045941Z`.
- Confirm the train split includes prior form-fill repair rows, blocked-payment repair rows, and current-retry confirmation-preservation rows.
- Refresh `CONTEXT.md`, final status, and a Human Brief with the new readiness boundary.
- Do not train, run prediction, mutate data, change prompts/evaluator metrics, release checkpoints/adapters, or claim model improvement.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `contract-evaluation`: extend readiness evidence requirements to cover the current 123-row train split after confirmation-preservation materialization, while preserving strict metric and non-claim boundaries.

## Impact

- Affects readiness/report artifacts, `CONTEXT.md`, final status documentation, and OpenSpec evidence.
- Reuses existing public sample manifest, SFT retry configs, dry-run SFT path, report CLI, leak scan, and strict baseline metrics.
- Does not require A100 execution, GPU allocation, model download, private corpus publication, or changes to dataset builders/training logic unless validation reveals a readiness metadata gap.
