## Why

The current 7B tiny adapter memorized three current train rows but failed strict
exact match on the current public `dev` and `test` splits. Treating that result
as "just add more data" is too coarse: the repo already contains some train
coverage for held-out task families, while the tiny adapter only trained on
three search-weather rows.

Before creating more data, running SFT again, or entering DPO, we need a local
diagnostic that separates:

- public-sample family coverage
- the actual tiny-adapter training subset
- held-out failure families and contract fields
- the next strategy recommendation and its evidence boundary

## What Changes

- Add a local held-out family strategy diagnostic that reads committed public
  sample rows and the current tiny-adapter held-out evidence.
- Publish a public-safe report under
  `reports/public-sample/heldout-family-strategy-diagnosis/`.
- Add regression tests that keep the conclusion narrow: targeted strategy
  diagnosis first, not blind data scaling and not model recovery.
- Generate a concise Chinese Human Brief for this phase.

## Non-Goals

- No new public sample generation.
- No SFT, DPO, GRPO, adapter prediction, or A100 execution.
- No prompt, parser, evaluator, slot normalization, semantic-equivalence, or
  schema-repair changes.
- No checkpoint, adapter, production, private-corpus, or live-browser claim.

## Expected Outcome

The phase should produce a decision-quality diagnosis: whether the next bounded
step should be targeted SFT data coverage, DPO hard-negative validation, prompt
policy adjustment, or another local learning-signal check. It should not execute
that next strategy.
