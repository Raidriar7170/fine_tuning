## Why

The current formal public held-out evidence is prediction-only and still shows partial strict behavior: `contract_exact_match` is dev 30.43% / test 28.99%, with 97 residual rows. Before changing data, training, prompts, or evaluator semantics, the project needs a public-safe residual-cluster inspection that turns the residual-family diagnosis into actionable failure clusters.

## What Changes

- Add a residual-cluster inspection report derived only from committed formal public held-out gold/prediction/evidence artifacts.
- Group residuals by task family, field path, mismatch category, source family, and representative examples.
- Identify likely next actions as evidence-backed candidates, not as automatic data/training/evaluator changes.
- Generate a concise Human Brief for the phase.
- Preserve strict boundaries: no new predictions, no SFT/DPO/GRPO training, no dataset mutation, no evaluator relaxation, no prediction repair/re-score, no checkpoint/adapter release, and no held-out recovery claim.

## Capabilities

### New Capabilities

### Modified Capabilities

- `contract-evaluation`: require public-safe residual-cluster inspection before data, training, or evaluator changes are recommended from formal held-out residuals.

## Impact

- Affected reports: add a new public-safe residual-cluster report under `reports/public-sample/`.
- Affected tests: add focused tests for cluster summary, boundaries, and public-safety scanning.
- Affected specs: extend `contract-evaluation` with a residual-cluster inspection evidence requirement.
- Non-goals: generic chat fine-tuning, skill routing, GUI action policy learning, first-phase GRPO, public release of the full local corpus, any new prediction/training run, evaluator relaxation, prediction repair, checkpoint release, adapter release, production readiness, live-browser benchmark improvement, or private-corpus generalization claims.
