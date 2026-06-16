## Why

The post-confirmation-marker-merge formal held-out prediction phase was archived as blocked because the A100 runtime dependency was unavailable during SSH preflight. The A100 connection is now restored, so the next bounded step is to retry the same prediction-only evidence question against manifest `public-sample-20260616T074315Z` without reopening the archived blocked change.

## What Changes

- Run a bounded A100 prediction-only retry for the current formal public sample dev/test splits using the existing selected private adapter.
- Publish sanitized evidence in a distinct retry evidence directory so the blocked archive and the recovered retry are not conflated.
- Record manifest id, split counts, prediction metadata, sanitized predictions, metrics, failure slices, report metadata, leak-scan outputs, and a Human Brief.
- Preserve strict `contract_exact_match`, strict `slot_f1`, and the contract evaluation ladder as authoritative; keep `slot_f1_soft` diagnostic-only.
- Do not train SFT/DPO/GRPO, mutate datasets, change prompts, relax evaluator metrics, repair/replace predictions, publish adapters/checkpoints, or claim production/live-browser improvement.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `contract-evaluation`: allow a follow-up formal held-out prediction retry after a blocked A100 preflight, provided it publishes to a distinct evidence directory and preserves prediction-only, boundary-changed, and public-safety semantics.

## Impact

- Affected configs: private A100 overrides for the formal public held-out dev/test prediction configs.
- Affected reports: a new public-safe retry evidence pack under `reports/public-sample/` plus a Human Brief for the phase.
- Affected runtime: one prediction-only A100 run per dev/test split, using an idle GPU selected after preflight.
- Non-goals: generic chat fine-tuning, skill routing, GUI action policy learning, first-phase GRPO, public release of the full local corpus, new training, evaluator relaxation, prediction repair, checkpoint/adapter release, public full-corpus release, private-corpus generalization, production readiness, or live-browser benchmark claims.
