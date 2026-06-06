## Why

The archived retry decoding stop-boundary diagnosis found that `generation_trace.jsonl` records raw attempt token/finish evidence, but retry attempt token/finish evidence is missing. Without retry attempt traces, the project cannot distinguish retry stop-boundary behavior from retry wrapper-style instruction following in later A100 evidence.

## What Changes

- Add local instrumentation so real private-adapter prediction sidecars record attempt-level generation trace rows for both raw and retry attempts.
- Preserve existing prediction, schema guard, retry parsing, strict evaluator metrics, and invalid-output handling.
- Publish a local public-safe evidence pack and Human Brief proving that the instrumentation is present in tests and bounded by non-claims.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `supervised-contract-tuning`: require retry attempt generation trace sidecar rows when schema retry is attempted.
- `contract-evaluation`: require public-safe instrumentation evidence that separates raw and retry generation trace coverage without changing metrics or claims.

## Impact

- Affected code: `src/voice2task/training.py`.
- Affected tests: focused private-adapter sidecar tests plus existing public evidence tests.
- Affected evidence/docs: `reports/public-sample/retry-generation-trace-instrumentation/`, `docs/human-briefs/2026-06-06-instrument-retry-generation-trace.html`.
- Non-goals: no A100 execution, no training, no private prediction rerun, no decoding behavior change, no parser relaxation, no evaluator metric change, no prediction repair/re-score, no semantic-equivalence scoring, no slot normalization, no generic chat fine-tuning, no skill routing, no GUI action policy learning, no first-phase GRPO, no public release of the full local corpus, no checkpoint or adapter release, no model recovery claim, and no live-browser benchmark improvement claim.
