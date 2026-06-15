## Context

The current formal public sample already contains reviewed train analogs for
the two remaining residual families:

- `candidate-clarify-ambiguous-canonical-scope`
- `candidate-blocked-payment-canonical-command`

The latest merged-candidate held-out diagnosis did not find schema, route,
safety, confirmation, or JSON validity failures. It found strict string/value
residuals:

- `slots.ambiguity` variants that are semantically close but not strict-equal
  to the canonical public target phrase.
- `normalized_command` drift from payment refusal to order refusal.

## Decision

Keep this phase local and policy-only. The implementation will harden the
existing residual repair prompt family instead of changing data or evaluator
behavior:

1. Add exact canonical policy text for ambiguous clarify:
   `slots.ambiguity="目标不明确，未指定具体网站或页面"`.
2. State that shorter variants such as `未指定具体页面` and `未指定具体操作`
   are strict-wrong for this canonical family.
3. Add exact canonical policy text for unsafe payment:
   `normalized_command="拒绝代替用户付款"`.
4. State that order/purchase wording such as `拒绝代替用户下单` is strict-wrong
   when the unsafe action includes payment or account-backed purchase.
5. Record these policy clauses through `prompt_constraint_summary()` so future
   prediction metadata and evidence can verify that the prompt used the hardened
   policy.

## Boundaries

- This phase does not claim the model has learned the policy.
- This phase does not rerun predictions or re-score old predictions.
- This phase does not move `slot_f1_soft` into a primary metric.
- This phase does not materialize new seeds, SFT rows, or DPO rows.
- The next A100 evaluation, if approved later, should be a separate phase that
  measures whether the policy hardening changes train/dev/test strict metrics.

## Risks

- Exact canonical phrases in prompts can look like held-out leakage if not
  documented. Mitigation: the strings are now formal policy text with train
  analogs already present in the public sample, and prediction prompts still
  exclude row-specific full gold target contracts.
- Prompt hardening may not be enough for 7B held-out generalization. Mitigation:
  evidence and Human Brief state that this is local prompt-policy readiness
  only, not model recovery.
