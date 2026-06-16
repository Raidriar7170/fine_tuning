## Why

The SFT v3 safety regression diagnosis found that all current safety misses
that matter for the regression are concentrated in `blocked_payment`: one dev
row regressed from `blocked/deny` to `form_fill/fill_form`, and three dev rows
remain persistent false negatives. Before adding rows or training again, the
project needs a bounded, reviewable repair-candidate design that defines which
payment/refund/charge-confirmation phrasings must remain `blocked/deny`.

## What Changes

- Add a design-only evidence pass for `blocked_payment` safety repair
  candidates.
- Read the committed SFT v3 safety regression diagnosis and current public
  sample manifest.
- Produce public-safe candidate definitions that identify repair families,
  accepted `blocked/deny` target contracts, and rejected drift shapes such as
  `form_fill/fill_form` or `clarify/clarify`.
- Recommend whether a later phase should materialize candidate seed traces or
  train, but do not perform either action in this phase.
- Generate a concise Chinese Human Brief and update status docs if the
  recommended next bounded phase changes.
- Non-goals: no SFT/DPO/GRPO, no evaluator relaxation, no semantic-equivalence
  scoring, no prediction repair/replacement, no new data materialization, no
  prompt change, no checkpoint or adapter release, no public full-corpus
  release, no generic chat fine-tuning, no skill routing, no GUI action policy
  learning, and no live-browser benchmark or production-readiness claim.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `voice2task-dataset-preparation`: require public-safe design evidence for
  `blocked_payment` safety repair candidates before materializing new safety
  rows or launching another training phase.

## Impact

- Affected evidence: new design report under `reports/public-sample/` derived
  from `reports/public-sample/sft-v3-safety-regression-diagnosis/`.
- Affected docs: `CONTEXT.md`, `reports/final_status.md`, and one Human Brief
  if the recommendation changes.
- Affected tests: focused evidence tests for candidate shape, public-safe
  boundaries, and non-claim flags.
- No A100 execution, model loading, training, prediction generation, committed
  dataset mutation, evaluator change, dependency change, adapter release, or
  checkpoint release.
