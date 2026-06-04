## Why

The latest strict-retry A100 train-split rerun proved that wrapped retry fragments are no longer accepted, but raw and retry model outputs still remain 0/3 schema-valid Browser Task Contracts. The next bounded step should strengthen local constrained output emission before spending another A100 rerun or changing training objectives.

## What Changes

- Strengthen the first-pass SFT prediction prompt with an explicit valid canonical JSON one-shot and whole-object output boundaries.
- Keep strict retry fail-closed: Markdown/prose-wrapped fragments remain invalid and invalid model outputs are not coerced into valid contracts.
- Record local public-safe evidence that the prompt now exposes a valid canonical Browser Task Contract example without including gold targets.
- Add focused tests for first-pass prompt constraints, no-gold prediction prompts, strict retry rejection, and schema-valid raw output acceptance.
- Generate a concise Chinese Human Brief and archive the OpenSpec change after validation.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `supervised-contract-tuning`: require prediction prompts to include a valid canonical JSON one-shot and whole-object output boundary before trained-adapter generation.
- `contract-evaluation`: require public-safe reporting for the local constrained-output repair and non-overclaim boundaries before any later A100 rerun.

## Impact

- Affected code: `src/voice2task/formatting.py`, focused prediction/export tests, and public-safe local evidence artifacts.
- No A100 execution, no new training run, no DPO/GRPO, no data expansion, no checkpoint release, no adapter release, no production-readiness claim, no dev/test generalization claim, and no live-browser benchmark improvement claim.
- Invalid raw or retry outputs remain invalid; this phase changes model-visible prompt constraints only, not metric coercion.
