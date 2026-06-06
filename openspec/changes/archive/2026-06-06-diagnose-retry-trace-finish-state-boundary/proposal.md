## Why

The archived `run-a100-retry-generation-trace-rerun` phase proved that retry attempts now emit generation trace rows on the real private-adapter A100 path. The same evidence also showed an important interpretation boundary: retry attempts recorded `finish_state=no_eos_observed` for `3/3` rows while generated token counts stayed below `max_new_tokens`. The current trace writer labels EOS visibility using the tokenizer EOS id, but it does not prove the full model-generation stop reason.

## What Changes

- Generate a local, evidence-only diagnosis from committed public artifacts and source code.
- Explain per-row retry finish-state evidence, max-token-hit status, and what remains unknown about actual generation stop reason.
- Record whether a future code change would be needed to distinguish tokenizer EOS visibility from model/generation-config stop reason.
- Add focused tests and a concise Chinese Human Brief.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `contract-evaluation`: add a public-safe diagnostic for retry generation trace finish-state interpretation boundaries.

## Impact

- Affected evidence: `reports/public-sample/retry-trace-finish-state-boundary-diagnosis/`.
- Affected tests: focused evidence-boundary tests.
- Affected docs: `docs/human-briefs/2026-06-06-diagnose-retry-trace-finish-state-boundary.html`.
- Non-goals: no A100 execution, no prediction rerun, no training, no decoding behavior change, no retry prompt change, no parser relaxation, no evaluator metric change, no model-quality claim, no stop-reason instrumentation change, no public full-corpus release, and no production/live-browser claim.
