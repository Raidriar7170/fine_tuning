## Why

The completed blocked-payment repair-candidate design identified two
public-safe `blocked_payment` repair families covering four observed
persistent-miss or regressed safety rows. The next bounded step is to
materialize those reviewed candidates into public sample seed rows and derived
artifacts before any training or prediction rerun can make a model-quality
claim.

## What Changes

- Add public-safe seed rows for the reviewed `blocked_payment` repair
  candidates, preserving the accepted target shape as `task_type=blocked`,
  `route=deny`, and `safety.reason=unsafe_payment`.
- Rebuild the public sample derived artifacts so the manifest, SFT rows, DPO
  pairs, and validation evidence reflect the new materialized repair seeds.
- Publish machine-readable and Markdown materialization evidence that records
  candidate provenance, pre/post counts, public-safety boundaries, and the
  next recommended evaluation/training boundary.
- Keep this phase data-only: no SFT, DPO, GRPO, A100 execution, prediction
  generation, evaluator relaxation, semantic scoring, checkpoint/adapter
  release, public full-corpus release, generic chat fine-tuning, skill routing,
  GUI action policy learning, production-readiness claim, or live-browser
  benchmark claim.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `voice2task-dataset-preparation`: Materialize reviewed `blocked_payment`
  repair candidates into the public sample and derived artifacts while
  preserving public-safe data, provenance, and no-claim boundaries.

## Impact

- Affected data artifacts: `data/public-samples/seed_traces.jsonl`,
  `data/public-samples/manifest_public_sample.json`,
  `data/public-samples/sft_public_sample.jsonl`, and
  `data/public-samples/dpo_public_sample.jsonl`.
- Affected evidence/docs: `reports/public-sample/`, `CONTEXT.md`,
  `reports/final_status.md`, and a Human Brief under `docs/human-briefs/`.
- Affected code is limited to reproducible dataset/evidence helpers and tests
  needed to materialize and validate the public-safe candidates.
