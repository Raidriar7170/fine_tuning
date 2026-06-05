## Why

The latest confirmation-required A100 train-split rerun improved strict schema-valid output to `2/3`, but `contract_exact_match` remained `0.0000`. Before changing prompts, training, decoding, or evaluation, the project needs a public-safe row-level diagnosis that separates schema failure, semantic field mismatch, and strict exact-match string mismatch.

## What Changes

- Add a bounded local diagnosis for the three train rows in `reports/public-sample/a100-confirmation-required-train-split-rerun/`.
- Generate machine-readable and human-readable evidence that compares each prediction with the train gold contract field by field.
- Classify remaining failure families without repairing, normalizing, coercing, or replacing model outputs.
- Generate a concise Chinese Human Brief and loop report that keep the conclusion bounded.
- No A100 execution, SFT/DPO/GRPO training, prompt repair, checkpoint release, adapter release, evaluation-metric change, dev/test rerun, production-readiness claim, public full-corpus release, or live-browser benchmark claim.

## Capabilities

### New Capabilities

### Modified Capabilities
- `contract-evaluation`: add public-safe row-mismatch diagnosis evidence for confirmation-required A100 rerun outputs.

## Impact

- Affected evidence: new public-safe report directory under `reports/public-sample/confirmation-rerun-row-mismatch-diagnosis/`.
- Affected documentation: Chinese Human Briefs under `docs/human-briefs/`.
- Affected tests: focused evidence tests for the new diagnosis pack and privacy/claim boundaries.
- Affected specs: `openspec/specs/contract-evaluation/spec.md` after archive.
- No new dependencies, no remote infrastructure access, no private corpus access, and no model runtime changes.
