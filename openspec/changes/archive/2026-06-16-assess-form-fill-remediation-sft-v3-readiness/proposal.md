## Why

The current formal held-out evidence for manifest `public-sample-20260616T074315Z`
shows that the model still has a concentrated `form_fill` residual cluster after
the reviewed remediation rows were merged into the public sample. The latest
prediction-only A100 retry did not train a new adapter, so it can only establish
the current baseline, not whether the merged train rows help the model.

A bounded readiness phase is needed before launching any SFT v3 run. It should
make the intended training input, private-runtime boundary, prediction follow-up,
and non-claim limits explicit without starting training.

## What Changes

- Add public-safe A100 config templates for a later `form_fill` remediation SFT
  v3 run and dev/test prediction follow-up.
- Generate a dry-run SFT row-selection artifact against the current public
  manifest to confirm the run would train on the current public train split.
- Publish a public-safe readiness report that ties together current metrics,
  `form_fill` residual counts, merged remediation row counts, dry-run selection,
  and the recommended next bounded phase.
- Preserve strict boundaries: no A100 training, no prediction rerun, no data
  mutation, no evaluator relaxation, no prediction repair, no checkpoint/adapter
  release, and no production or live-browser claim.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `supervised-contract-tuning`: record public-safe readiness evidence before a
  later formal-public-sample SFT v3 run using merged `form_fill` remediation
  rows.
- `contract-evaluation`: require readiness evidence to keep strict metrics and
  prediction-only baselines separate from future training claims.

## Impact

- Affected configs: new public-safe SFT v3 and prediction templates under
  `configs/`.
- Affected reports: new readiness evidence under
  `reports/public-sample/form-fill-remediation-sft-v3-readiness/`.
- Affected tests: focused tests for config safety, dry-run row selection, report
  boundaries, committed evidence, and leak scanning.
- Non-goals: SFT/DPO/GRPO training, dataset mutation, held-out prediction rerun,
  metric/evaluator changes, model recovery claims, checkpoint/adapter release,
  production readiness, private-corpus generalization, public full-corpus
  release, or live-browser benchmark improvement.
