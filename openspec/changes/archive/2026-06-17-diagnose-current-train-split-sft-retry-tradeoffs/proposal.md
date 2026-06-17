## Why

The current 118-row train-split SFT retry produced a mixed partial signal: safety
recall recovered and strict slot F1 improved, but dev exact match and
confirmation accuracy regressed. Before any additional training, DPO, evaluator
change, or release claim, the project needs a bounded residual/trade-off
diagnosis tied to the current manifest.

## What Changes

- Add a current retry trade-off diagnosis evidence pack comparing
  `a100-current-train-split-sft-retry` against the current-manifest
  prediction-only baseline.
- Identify and summarize confirmation regressions, exact-match regressions,
  route/task-type regressions, safety changes, and remaining slot residuals on
  dev/test without mutating predictions, data, prompts, or evaluator metrics.
- Refresh `CONTEXT.md`, `reports/final_status.md`, and a concise Chinese Human
  Brief with the diagnosis result and the next bounded recommendation.
- Keep strict `contract_exact_match` and strict `slot_f1` as public headline
  metrics; keep `slot_f1_soft` diagnostic-only.
- Non-goals: generic chat fine-tuning, skill routing, GUI action policy
  learning, first-phase GRPO, public release of the full local/private corpus,
  checkpoint/adapter release, live-browser benchmark claims, evaluator
  relaxation, DPO reruns, or new training.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `contract-evaluation`: require a public-safe trade-off diagnosis for the
  current-train-split SFT retry before any further model-quality phase.

## Impact

- Affects reporting code and tests only if a reusable diagnosis writer/CLI is
  needed.
- Adds public-safe evidence under `reports/public-sample/`.
- Updates project status docs and OpenSpec evidence boundaries.
- Does not change model training, prediction generation, data builders,
  evaluator scoring definitions, prompts, dependencies, or public/private data
  posture.
