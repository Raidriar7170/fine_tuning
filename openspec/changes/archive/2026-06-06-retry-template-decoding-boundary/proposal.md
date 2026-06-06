## Why

The latest A100 retry JSON-only rerun proved that stricter retry wording is visible, but the adapter still emits prose/Markdown-wrapped retry fragments. We need a smaller local phase to inspect and harden the retry prompt template/decoding boundary before deciding whether any A100 rerun, constrained decoding, or retry-only training is justified.

## What Changes

- Diagnose whether schema retry currently uses a weaker template boundary than first-pass prediction prompts.
- Add local, public-safe retry template boundary metadata that makes the retry prompt mode, chat-template use, machine-only output contract, and strict-parser boundary visible.
- Preserve strict parser/evaluator behavior: wrapped retry fragments remain invalid and no embedded contracts are extracted.
- Publish a local evidence pack and Human Brief comparing only against the prior retry JSON-only hardening and A100 retry JSON-only rerun evidence.
- Do not run A100, train, release adapters/checkpoints, change evaluator metrics, relax parsing, repair predictions, or claim model-quality improvement in this phase.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `supervised-contract-tuning`: expose and test a schema-retry template/decoding boundary policy for retry prompts without changing training or strict parsing.
- `contract-evaluation`: publish public-safe local evidence that separates retry template boundary instrumentation from model-output recovery or metric improvement claims.

## Impact

- Affected code: `src/voice2task/training.py` retry prompt construction, metadata summaries, prompt snapshot metadata, and tests.
- Affected artifacts: new local evidence pack under `reports/public-sample/retry-template-decoding-boundary/`, a Chinese Human Brief, and archived OpenSpec artifacts after implementation.
- No dependency changes, no A100 execution, no training, no parser relaxation, no evaluator metric change, no prediction repair/re-score, no public full-corpus release, and no released checkpoint/adapter.
