## Why

The assistant-only A100 train-split rerun proved the objective path is now using assistant-contract labels, but the train predictions remained Browser Task Contract schema-invalid because required fields such as `safety` were omitted. The just-archived required-field prompt and schema guard/retry repair needs one narrow A100 train-split rerun to measure whether that specific failure pattern improves.

## What Changes

- Run a new bounded A100 SFT train-split rerun using the current required-field prompt skeleton and schema guard/retry prediction path.
- Keep training and prediction scoped to public-sample train rows with `prediction_split=train`, `overfit_diagnostic=true`, and `generalization_claim=false`.
- Publish only sanitized public-safe evidence: adapter metadata summary, objective/runtime label metadata, predictions, prompt snapshot, raw decoded summary, generation trace, metrics, manifest, report, leak-scan result, and Human Brief HTML.
- Preserve raw model attempts and schema guard metadata so raw attempt validity, retry attempt validity, validated output source, and final contract metrics remain separate.
- Do not publish checkpoints, adapters, raw logs, caches, private overrides, host details, SSH details, tokens, private paths, or private corpus rows.

## Capabilities

### New Capabilities

### Modified Capabilities

- `supervised-contract-tuning`: add a bounded A100 train-split rerun path after required-field repair.
- `contract-evaluation`: add public-safe evidence requirements for required-field repair rerun results and non-claim boundaries.

## Impact

- Affected runtime path: `voice2task.cli.train sft`, `voice2task.cli.train sft-predict`, runtime/objective label inspection, and contract metrics/report generation.
- Affected evidence surface: a new public-safe report directory under `reports/public-sample/`, one phase Human Brief under `docs/human-briefs/`, and an archived OpenSpec change.
- No generic chat fine-tuning, skill routing, GUI action policy learning, first-phase GRPO, public full-corpus release, checkpoint release, adapter release, production readiness claim, held-out generalization claim, or live-browser benchmark improvement claim.
