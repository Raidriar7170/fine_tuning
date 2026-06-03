## Why

The post-recovery A100 rerun produced JSON objects that look contract-like, but all 12 public-sample predictions still failed the Browser Task Contract schema. The current metrics collapse those cases into a single `schema` slice, which hides whether the failure is JSON parsing, missing fields, invalid enums, wrong object types, empty required strings, or unsafe contract semantics.

## What Changes

- Add field-level schema mismatch diagnostics for prediction artifacts so contract-like failures can be inspected without rerunning A100 training.
- Generate a public-safe diagnostic report for the post-recovery public-sample predictions that explains why the outputs are invalid.
- Keep the phase diagnostic-only: do not relax the Browser Task Contract schema, normalize invalid predictions into valid contracts, publish an adapter/checkpoint, or claim model-quality improvement.
- Preserve explicit non-goals for generic chat fine-tuning, skill routing, GUI action policy learning, first-phase GRPO, and public release of the full local/private corpus.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `contract-evaluation`: add a requirement for schema failure diagnostics that report concrete mismatch reasons for contract-like predictions.

## Impact

- Affected code: contract evaluation helpers and CLI/report surfaces.
- Affected artifacts: sanitized public-sample A100 post-recovery diagnostic report.
- No new runtime dependencies, model checkpoints, adapters, private corpus files, private paths, or live-browser benchmark claims.
