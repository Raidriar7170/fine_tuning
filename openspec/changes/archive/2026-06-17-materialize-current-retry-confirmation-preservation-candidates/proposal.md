## Why

The current-train-split SFT retry recovered safety but regressed confirmation behavior on seven held-out rows. The previous design phase identified two public-safe confirmation-preservation candidate families; this change materializes those reviewed sketches into candidate rows and synchronized public artifacts so a later training-readiness or retry phase can use them without blurring evidence boundaries.

## What Changes

- Add a guarded materialization path for current-retry confirmation-preservation candidates derived from `reports/public-sample/current-retry-confirmation-preservation-candidate-design/`.
- Write public-safe candidate seed rows for the two reviewed families:
  - unsafe-payment confirmation preservation: accepted target remains `blocked/deny`, `safety.reason="unsafe_payment"`, `confirmation_required=true`.
  - public navigation non-confirmation preservation: accepted target remains `navigate/open_url`, `safety.reason="public_readonly"`, `confirmation_required=false`.
- Merge the reviewed candidate seed rows into the formal public sample as train rows and rebuild the public manifest, SFT rows, and DPO pairs.
- Publish public-safe materialization evidence, update project status surfaces, and generate a Human Brief.
- Do not train, generate predictions, repair predictions, change prompts, relax evaluator metrics, publish adapters/checkpoints, or claim model-quality recovery.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `voice2task-dataset-preparation`: add requirements for materializing reviewed current-retry confirmation-preservation candidates into public-safe seed rows and rebuilt public sample artifacts while preserving strict evidence boundaries.

## Impact

- Affected data: `data/public-samples/seed_traces.jsonl`, `manifest_public_sample.json`, `sft_public_sample.jsonl`, `dpo_public_sample.jsonl`, and a new candidate seed artifact if needed.
- Affected code: dataset/materialization helpers, CLI commands, report/evidence writer, and focused tests.
- Affected docs/evidence: `CONTEXT.md`, `reports/final_status.md`, `reports/public-sample/...`, and a Human Brief.
- Non-goals: generic chat fine-tuning, skill routing, GUI action policy learning, GRPO, public full-corpus release, A100 training, prediction generation, evaluator relaxation, model recovery claims, checkpoint/adapter release, and live-browser benchmark claims.
