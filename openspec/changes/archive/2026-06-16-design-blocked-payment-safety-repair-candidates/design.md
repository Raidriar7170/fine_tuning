## Context

The current formal public held-out truth surface is bound to
`public-sample-20260616T074315Z`. The latest SFT v3 retry improved several
strict metrics, but the follow-up safety diagnosis shows a concentrated
`blocked_payment` risk:

- `21` gold-stop rows across dev/test;
- `18` of those rows are `blocked_payment`;
- `1` dev `blocked_payment` row regressed from safety-correct to false
  negative;
- `3` dev `blocked_payment` rows remain persistent false negatives.

Those rows share payment/refund/charge-confirmation language where the accepted
contract should remain `task_type="blocked"`, `route="deny"`,
`safety.allow=false`, and `safety.reason="unsafe_payment"`. The next step is
therefore a design-only repair-candidate pass, not immediate data mutation or
training.

## Goals / Non-Goals

**Goals:**

- Define public-safe `blocked_payment` repair-candidate families from the
  committed safety diagnosis.
- Specify accepted target contracts and rejected drift contracts for each
  candidate family.
- Preserve evidence about source rows, failure mode, and intended future
  materialization without writing new seed rows in this phase.
- Produce a JSON/Markdown design report and a concise Chinese Human Brief.
- Recommend the next bounded phase only after candidate coverage is explicit.

**Non-Goals:**

- No committed public-sample mutation.
- No private/local corpus mutation.
- No SFT, DPO, GRPO, prediction run, A100 execution, prompt change, evaluator
  change, prediction repair, semantic-equivalence scoring, adapter release,
  checkpoint release, production-readiness claim, or live-browser benchmark.

## Decisions

1. **Use the safety diagnosis as the only source artifact.**
   The design reads
   `reports/public-sample/sft-v3-safety-regression-diagnosis/` and the current
   public manifest. It does not inspect private training logs or remote adapter
   internals. This keeps the candidate set reviewable and reproducible.

2. **Represent candidates as design records, not seed rows.**
   Each candidate should include a stable id, family, source row ids,
   safety pattern, accepted target contract sketch, rejected drift sketches,
   suggested public-safe utterance templates, and whether it is intended for a
   later seed materialization phase. This prevents the design phase from
   silently changing the formal public sample.

3. **Focus on `unsafe_payment` false negatives.**
   The candidate families should cover refund confirmation, direct refund
   processing, subscription charge confirmation, and account/payment action
   phrasing. Non-payment blocked rows and unrelated route/slot residuals remain
   out of scope.

4. **Keep DPO/training as later decisions.**
   The design may recommend future rejected categories such as
   `blocked_payment_form_fill_drift` and `blocked_payment_clarify_drift`, but
   it must not generate DPO pairs or start SFT. A later OpenSpec phase should
   decide whether to materialize these candidates and rebuild public artifacts.

## Risks / Trade-offs

- Small support counts can overfit a narrow dev cluster -> keep source row ids
  and support counts visible, and avoid broad safety claims.
- Candidate text can accidentally become new gold data -> label artifacts as
  design-only and set explicit `formal_public_sample_modified=false`.
- Payment phrasing is safety-sensitive -> keep accepted targets conservative
  (`blocked/deny`) and defer any nuance policy to a separate safety policy
  proposal if needed.
- A design report does not prove model improvement -> require a later
  materialization/training/evaluation phase for any quality claim.
