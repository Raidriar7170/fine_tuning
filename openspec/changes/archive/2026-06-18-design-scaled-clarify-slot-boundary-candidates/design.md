# Design: Scaled Clarify Slot-Boundary Candidate Design

## Context

The scaled residual target-selection evidence is under
`reports/public-sample/scaled-residual-remediation-target-selection/` and
selects `clarify/slots` as the first remediation target. The selected source
cluster contains 78 strict slot residual rows, split 42 dev / 36 test, across
28 source families. The source examples are public-safe summaries only: both
gold and predicted values are summarized as `object with keys: ambiguity`.

This means the next safe step is not to invent rows directly. It is to design
the shape of future clarify boundary cases from committed aggregate evidence,
then review whether those designs should be materialized in a later phase.

## Goals / Non-Goals

**Goals:**

- Produce design-only public-safe candidate sketches for the selected
  `clarify/slots` cluster.
- Preserve the accepted target shape:
  `task_type=clarify`, `route=clarify`, `safety.allow=true`,
  `safety.reason=ambiguous_request`, `confirmation_required=true`, and
  `slots.ambiguity`.
- Record rejected drift sketches that future data should make unlikely.
- Recommend one later bounded materialization phase if coverage is adequate.

**Non-Goals:**

- No public sample mutation, seed/SFT/DPO row generation, A100 job, prediction
  run, training run, prompt change, evaluator relaxation, semantic-equivalence
  scoring, slot normalization, prediction repair, or adapter/checkpoint release.
- No claim that candidate design improves metrics or recovers the model.
- No direct use of raw private rows or raw prediction streams.

## Decisions

1. **Design from committed cluster evidence only.**

   The report reads target-selection and cluster-inspection JSON. It does not
   read raw predictions, private corpora, or remote files. This keeps the design
   public-safe and reviewable.

2. **Use three clarify boundary themes.**

   The candidate sketches should separate ambiguity from different neighboring
   routes:

   - `clarify_search_or_extract_ambiguity`: user asks for information but the
     target/source is underspecified.
   - `clarify_navigation_or_form_fill_ambiguity`: user names an action but not
     enough destination or field detail.
   - `clarify_pronoun_or_context_missing`: user uses deictic/context-dependent
     phrasing such as "这个", "那里", or "刚才那个".

   These themes cover future materialization without requiring raw source text.

3. **Keep safety-sensitive blocked residuals out of this design.**

   Blocked-payment residuals were deferred by target selection and should remain
   outside this change. Mixing them into clarify candidate design would blur
   safety precision/recall boundaries.

## Risks / Trade-offs

- **Risk:** Candidate themes are derived from aggregate summaries, not raw rows.
  **Mitigation:** Keep them as sketches and require later materialization review
  before any dataset changes.

- **Risk:** Clarify candidates could over-teach the model to clarify instead of
  executing valid tasks.
  **Mitigation:** Rejected drift sketches explicitly name neighboring task types
  and later materialization should include paired contrast examples.

- **Risk:** Readers may interpret design as model improvement.
  **Mitigation:** Carry claim-boundary flags and test for no training,
  prediction, data mutation, or recovery claims.
