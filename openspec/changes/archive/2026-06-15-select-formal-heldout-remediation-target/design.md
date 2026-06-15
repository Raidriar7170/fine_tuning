## Context

The current public evidence ladder ends with a formal held-out prediction report
and a residual-family diagnosis. That diagnosis shows weak strict exact-match
performance on formal dev/test, while also preserving the boundary that
`slot_f1_soft` is diagnostic-only. The next decision should be a small,
evidence-backed target selection step, not an immediate training or evaluator
change.

## Goals / Non-Goals

**Goals:**

- Rank formal held-out residual task families using existing committed
  diagnosis evidence.
- Select one first remediation target and explain why it should be handled
  before broader data/training changes.
- Publish public-safe JSON/Markdown/HTML evidence that can be reviewed and
  cited in a later OpenSpec remediation phase.
- Keep the decision boundary explicit: strict exact match and strict slot F1
  remain primary.

**Non-Goals:**

- No A100 job, model training, DPO, prediction rerun, adapter release, or
  checkpoint work.
- No new seed generation, gold rewrite, slot normalization, or public held-out
  split mutation.
- No evaluator metric relaxation or promotion of `slot_f1_soft`.
- No live browser benchmark claim or production-readiness claim.

## Decisions

1. **Use committed residual diagnosis as the only input.**
   - Rationale: this keeps the phase reproducible and avoids blending private
     corpus or A100 state into the public evidence.
   - Alternative considered: inspect raw private training data. Rejected because
     it would blur the public/private boundary.

2. **Rank by affected strict residual rows first, then residual field counts.**
   - Rationale: row impact is closer to the formal held-out exact-match
     denominator, while field counts explain what kind of remediation is needed.
   - Alternative considered: rank by field counts only. Rejected because one row
     can contribute many field mismatches after a route/task error.

3. **Recommend `form_fill` as the first target if it remains the largest row
   cluster.**
   - Rationale: the current diagnosis shows `form_fill` affects the most rows
     and is mostly strict wording/slot/confirmation-policy mismatch, making it a
     good scoped remediation target before safety or route ontology changes.
   - Alternative considered: start with `blocked_payment`. Rejected for this
     phase because safety remediation changes carry higher policy risk and
     should follow a separate proposal.

4. **Publish only sanitized summaries and selected examples.**
   - Rationale: the report should be useful for project planning without
     becoming a raw prediction dump or private-data leak.

## Risks / Trade-offs

- [Risk] A ranked report may look like a model-quality improvement.
  -> Mitigation: claims explicitly say no recovery, no training, and no metric
  change occurred.
- [Risk] `form_fill` may not be the highest business-risk family.
  -> Mitigation: report separates "first scoped target" from "highest safety
  priority" and leaves `blocked_payment` as a later safety-specific phase.
- [Risk] Ranking from a small public held-out sample may overfit planning to
  this sample.
  -> Mitigation: frame the output as a next OpenSpec target selection, not a
  global model diagnosis.
