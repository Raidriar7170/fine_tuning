## Why

The latest assistant-only A100 rerun shows that generated outputs are raw-JSON parseable and not truncated, but all three train predictions still fail the Browser Task Contract schema because required fields are missing. The next bounded fix should target required-field emission before changing training data, private A100 execution, or broader model-quality claims.

## What Changes

- Strengthen the SFT prediction prompt with an explicit Browser Task Contract skeleton and required-field checklist.
- Add a schema-validating retry/guard path for private-adapter prediction attempts that records raw attempts separately from validated outputs.
- Preserve invalid raw model attempts without coercing, repairing, or counting guard/retry output as raw model recovery.
- Add local tests that prove missing required fields trigger the guard/retry metadata and that valid outputs remain unchanged.
- Generate public-safe evidence and Human Brief documentation for the local repair phase.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `supervised-contract-tuning`: require strengthened prediction prompts and bounded schema-validating retry/guard metadata for SFT prediction.
- `contract-evaluation`: require public-safe reporting that separates raw attempts, retry/guard attempts, schema-valid outputs, and non-claim boundaries.

## Impact

- Affects `src/voice2task/formatting.py`, `src/voice2task/training.py`, and focused tests.
- Does not run A100 training, release an adapter/checkpoint, modify the public dataset, or claim held-out generalization or live-browser benchmark improvement.
- Keeps full local/private corpus and private runtime artifacts out of git.
