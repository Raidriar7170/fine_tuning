## Why

The SFT v3 retry improved dev exact match and strict slot F1, but dev
`safety_recall` regressed from `0.6667` to `0.5556`. Before any further
training, data expansion, or public claim, the project needs a bounded
diagnosis that explains the safety false negatives on the current formal
public sample.

## What Changes

- Add a diagnosis-only evidence pass for the SFT v3 retry safety regression.
- Compare baseline and SFT v3 retry predictions for gold stop rows, with
  emphasis on `blocked_payment` rows and safety false negatives.
- Produce public-safe aggregate evidence and sanitized row-level summaries.
- Refresh `CONTEXT.md` and `reports/final_status.md` only if the diagnosis
  changes the recommended next step.
- Generate a concise Chinese Human Brief for the diagnosis phase.
- Non-goals: no SFT/DPO/GRPO, no evaluator relaxation, no semantic-equivalence
  scoring, no prediction repair/replacement, no new data materialization, no
  prompt change, no checkpoint or adapter release, no public full-corpus
  release, no generic chat fine-tuning, no skill routing, no GUI action policy
  learning, and no live-browser benchmark or production-readiness claim.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `contract-evaluation`: require public-safe safety-regression diagnosis
  evidence before interpreting the SFT v3 retry as a safety or recovery
  improvement.

## Impact

- Affected evidence: new report under `reports/public-sample/` that reads the
  existing baseline and SFT v3 retry prediction/evaluation artifacts.
- Affected docs: `CONTEXT.md`, `reports/final_status.md`, and one Human Brief
  if the recommendation changes.
- Affected tests: focused evidence tests for diagnosis structure and claim
  boundaries.
- No A100 execution, model loading, training, prediction generation, dataset
  mutation, evaluator change, or dependency change.
