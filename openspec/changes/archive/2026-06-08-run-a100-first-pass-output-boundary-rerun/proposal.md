# run-a100-first-pass-output-boundary-rerun

## Why

The local output-boundary instrumentation repair made first-pass prediction prompts explicitly machine JSON-only, but local evidence cannot prove the trained adapter will stop emitting Markdown-wrapped fragments. The next bounded check is a prediction-only A100 train-split rerun using the current committed code to test whether strict schema-valid output improves relative to the latest search-query slot-policy rerun.

## What Changes

- Run one authorized A100 prediction-only train-split rerun with the existing private adapter, current committed repo state, current public sample manifest, and a repo-external private override.
- Use `prediction_split=train`, `overfit_diagnostic=true`, `generalization_claim=false`, greedy decoding, `schema_retry_enabled=true`, and the new `prediction_output_boundary` metadata.
- Publish only sanitized public evidence under `reports/public-sample/a100-first-pass-output-boundary-rerun/`.
- Compare against `reports/public-sample/a100-search-query-slot-policy-rerun/` and the local `repair-output-boundary-template-decoding-instrumentation` evidence.
- Generate a Chinese Human Brief at `docs/human-briefs/2026-06-08-run-a100-first-pass-output-boundary-rerun.html`.
- Keep training, DPO, GRPO, parser relaxation, evaluator metric changes, prediction repair, prediction re-score, semantic-equivalence scoring, slot normalization, checkpoint/adapter release, and live-browser benchmark claims out of scope.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `supervised-contract-tuning`: run a bounded A100 prediction-only train-split rerun that exercises the current first-pass output-boundary prompt/instrumentation against an existing private adapter without training or releasing model artifacts.
- `contract-evaluation`: publish public-safe evidence comparing strict schema/wrapper outcomes with prior A100 search-query slot-policy evidence without changing metrics or relaxing parser behavior.

## Impact

- Affected execution: A100 prediction-only train-split rerun, no training.
- Affected artifacts: sanitized predictions, prompt snapshot, raw decoded summary, generation trace, metadata, metrics, schema guard summary, comparison diagnosis, manifest, leak scans, and Human Brief.
- No committed private override, raw remote log, private path, SSH detail, host detail, token, secret, checkpoint, adapter, cache, or private corpus row.
