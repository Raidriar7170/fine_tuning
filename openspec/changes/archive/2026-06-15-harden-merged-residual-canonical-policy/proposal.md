## Why

The archived `merged-slot-value-residual-diagnosis` phase shows that reviewed
slot-value candidates were already designed, materialized, merged into the
formal public sample, and rerun on the 7B A100 path. That rerun improved
held-out strict exact match, but the remaining four strict residuals are now
narrow: three `seed-clarify-ambiguous` slot-value canonical phrase mismatches
and one blocked-payment `normalized_command` mismatch.

This phase should therefore not repeat broad data expansion, DPO, evaluator
changes, or another A100 run. The bounded local step is to make the two
post-merge canonical residual policies model-visible in SFT training and
prediction prompts, then publish public-safe evidence that the policy text and
metadata are present without claiming model recovery.

## What Changes

- Strengthen the existing held-out residual repair prompt policy with exact
  canonical wording for:
  - ambiguous clarify slot value:
    `slots.ambiguity="目标不明确，未指定具体网站或页面"`;
  - unsafe payment block command:
    `normalized_command="拒绝代替用户付款"`.
- Add prompt constraint flags for those two canonical policies.
- Add focused tests that verify training and prediction prompts expose the
  policy text while prediction prompts still exclude row-specific gold target
  contracts.
- Publish a public-safe local evidence pack and concise Chinese Human Brief for
  this phase.
- Do not modify public sample rows, DPO pairs, evaluator semantics, strict
  metrics, historical predictions, A100 configs, adapters, checkpoints, or
  private runtime artifacts.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `supervised-contract-tuning`: require residual repair prompts to expose the
  exact canonical ambiguous-clarify phrase and unsafe-payment refusal command
  as policy text, without inserting row-specific gold contracts into prediction
  prompts.
- `contract-evaluation`: require public-safe evidence for this local prompt
  policy hardening phase with strict non-claim boundaries.

## Impact

- Affected code: SFT/prediction prompt formatting and prompt constraint
  metadata.
- Affected tests: focused prompt-formatting tests and committed evidence/public
  safety tests.
- Affected artifacts:
  `reports/public-sample/merged-residual-canonical-policy/` and
  `docs/human-briefs/2026-06-15-harden-merged-residual-canonical-policy.html`.
- Non-goals: no new training data, no DPO generation, no private A100
  execution, no prediction rerun, no evaluator relaxation, no semantic
  equivalence scoring, no slot normalization, no prediction repair or re-score,
  no checkpoint/adapter release, no production-readiness claim, and no
  live-browser benchmark claim.
