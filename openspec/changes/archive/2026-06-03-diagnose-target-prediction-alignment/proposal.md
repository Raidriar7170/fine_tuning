## Why

The previous schema diagnostics show that the post-recovery A100 predictions are JSON and contract-like, but they still fail Browser Task Contract validation. The next smallest useful step is to compare each raw prediction against the canonical gold target so we can see whether the model is missing the contract vocabulary itself, the field shapes, or the safety/confirmation decisions.

## What Changes

- Add target-vs-prediction alignment diagnostics for public-sample prediction artifacts, even when predictions are schema-invalid.
- Generate public-safe JSON and Markdown reports that summarize mismatched fields, gold value summaries, prediction value summaries, and aggregate mismatch counts.
- Keep the phase diagnostic-only: do not relax the Browser Task Contract schema, map invalid route paths into valid enums, convert list slots into objects, replace predictions with gold fixtures, rerun training, publish an adapter/checkpoint, or claim model-quality improvement.
- Preserve explicit non-goals for generic chat fine-tuning, skill routing, GUI action policy learning, first-phase GRPO, and public release of the full local/private corpus.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `contract-evaluation`: add a requirement for comparing schema-invalid but contract-like predictions with their gold Browser Task Contract targets to identify target alignment failures.

## Impact

- Affected code: contract evaluation helpers, CLI, reports, and focused evaluator/report tests.
- Affected artifacts: sanitized public-sample A100 post-recovery alignment diagnostic report.
- No new runtime dependencies, model checkpoints, adapters, private corpus files, private paths, or live-browser benchmark claims.
