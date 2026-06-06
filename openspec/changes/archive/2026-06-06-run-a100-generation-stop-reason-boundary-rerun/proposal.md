## Why

The local `instrument-generation-stop-reason-boundary` phase added public-safe stop-boundary fields to future `generation_trace.jsonl` rows. A bounded A100 prediction-only rerun is now needed to observe those fields on real private-adapter raw and retry attempts instead of relying on local instrumentation tests alone.

## What Changes

- Run one A100 private-adapter prediction-only train-split rerun after stop-boundary instrumentation.
- Preserve `prediction_split=train`, `overfit_diagnostic=true`, `generalization_claim=false`, `schema_retry_enabled=true`, `schema_repair_applied=false`, greedy decoding, strict parser semantics, and final metric semantics.
- Publish public-safe evidence under `reports/public-sample/a100-generation-stop-reason-boundary-rerun/`, including predictions, metrics, prompt snapshot, raw decoded summary, generation trace, schema guard summary, stop-boundary diagnosis, manifest, leak scans, and a concise Chinese Human Brief.
- Report whether real raw/retry trace rows include `max_new_tokens_hit`, `finish_state_basis`, `stop_reason_evidence`, `actual_stop_reason_recorded`, and `actual_stop_reason`.
- Do not train, change decoding, relax parser behavior, repair outputs, re-score predictions, release checkpoints/adapters, publish the full local corpus, or claim model-quality/live-browser benchmark improvement.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `supervised-contract-tuning`: add a bounded A100 prediction-only rerun that records the new stop-boundary generation trace fields on real private-adapter raw/retry attempts.
- `contract-evaluation`: add public-safe rerun evidence and claim boundaries for interpreting stop-boundary trace fields without overstating model recovery or stop reason.

## Impact

- Affected runtime: A100 private prediction path only, with all private files kept under the AGENTS-defined approved A100 root and public artifacts sanitized before commit.
- Affected public artifacts: `reports/public-sample/a100-generation-stop-reason-boundary-rerun/` and `docs/human-briefs/2026-06-06-run-a100-generation-stop-reason-boundary-rerun.html`.
- No dependency changes, no generic chat fine-tuning, no skill routing, no GUI action policy learning, no first-phase GRPO, no public full-corpus release, and no release-posture change.
