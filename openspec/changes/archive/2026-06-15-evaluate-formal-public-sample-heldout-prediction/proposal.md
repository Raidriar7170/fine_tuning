## Why

The formal public sample now includes the reviewed family-stratified candidates, so the previous held-out prediction evidence is tied to an older manifest and no longer answers the current generalization question. We need a narrow prediction-only phase on the new manifest before deciding whether more data, DPO, prompt policy, or training work is warranted.

## What Changes

- Add a formal-public-sample held-out prediction evaluation phase for the current manifest `public-sample-20260615T111316Z`.
- Add dev/test prediction config templates that point at the current formal public sample and keep private A100 adapter paths as placeholders.
- Import or record sanitized prediction-only evidence for dev/test, including metrics, schema diagnostics, alignment diagnostics, manifest/report, and leak-scan results.
- Generate a concise Chinese Human Brief that separates observed held-out metrics from training, adapter release, and model recovery claims.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `contract-evaluation`: Add formal-public-sample held-out prediction evidence requirements for current-manifest dev/test evaluation.

## Impact

- Affected configs: new `configs/sft-a100-formal-public-heldout-*-prediction.json` templates.
- Affected evaluation/reporting: existing `voice2task-train sft-predict`, `voice2task-eval metrics`, `diagnose-schema`, `diagnose-alignment`, and leak-scan commands.
- Affected evidence: new `reports/public-sample/a100-formal-public-heldout-prediction/` artifacts and a Human Brief.
- Non-goals: generic chat fine-tuning, skill routing, GUI action policy learning, first-phase GRPO, public full-corpus release, checkpoint/adapter release, production readiness, and live-browser benchmark improvement claims.
