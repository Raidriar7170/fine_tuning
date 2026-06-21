## Why

The latest recovered-input Contract V2 projection and internal ContractCoreV2 work show that display-field/schema burden is limited while core slot failures remain the dominant residual. We need a deterministic slot-level analysis to decide whether the next bounded implementation should prioritize span/copy extraction, typed normalization, task-specific slot schemas, or a mixed internal representation.

## What Changes

- Add a read-only slot error mechanism analysis over the recovered step-matched Control/Treatment predictions and aligned gold contracts.
- Quantify gold slot source support, predicted value provenance, Control/Treatment paired error movement, task-family and slot-path hotspots, and representation feasibility.
- Publish a compact public-safe evidence bundle under `reports/public-sample/slot-error-mechanism-analysis/`.
- Add `docs/slot-representation.md` as a design-only proposal for future internal slot representation work.
- Add a concise Human Brief and short README/CONTEXT updates reflecting the final decision label and claim boundaries.
- Do not train, rerun predictions, mutate data, change gold or recovered predictions, relax evaluators, modify BrowserTaskContract V1, modify ContractCoreV2, or implement a new slot representation.

## Capabilities

### New Capabilities

- `slot-error-mechanism-analysis`: deterministic, public-safe slot-level residual analysis and design-only slot representation recommendation from recovered per-sample contracts.

### Modified Capabilities

- None.

## Impact

- Adds `src/voice2task/slot_error_analysis.py`, a report script or CLI entry point, and focused tests.
- Adds compact analysis artifacts, `docs/slot-representation.md`, and a Human Brief.
- Leaves existing evaluator semantics, layered evaluator behavior, BrowserTaskContract V1 schema, ContractCoreV2, dataset builders, training configs, recovered predictions, and gold contracts unchanged.
- Makes no checkpoint, adapter, model-improvement, executable-quality, production-readiness, safety-readiness, held-out-recovery, or live-browser claims.
