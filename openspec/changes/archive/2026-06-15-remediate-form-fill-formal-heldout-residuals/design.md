## Context

The previous formal target-selection phase selected `form_fill` as the first
bounded remediation target because it is the largest affected strict residual
row cluster in the current formal held-out evidence. Inspection shows three
dominant failure shapes: confirmation wording is often omitted or rearranged,
slot `field` values are often generalized to shorter aliases, and a small
number of rows are routed as `clarify` instead of `form_fill`.

## Goals / Non-Goals

**Goals:**

- Classify existing `form_fill` residual rows into remediation buckets.
- Identify whether the likely follow-up should be prompt/policy clarification,
  targeted public-safe data design, or training rerun.
- Provide public-safe representative examples and acceptance boundaries for the
  later implementation phase.
- Preserve strict metric boundaries and fail closed if the source target
  selection no longer selects `form_fill`.

**Non-Goals:**

- No new data generation or candidate materialization.
- No mutation of public held-out dev/test rows.
- No A100 job, SFT, DPO, prediction rerun, checkpoint, adapter, or release
  evidence.
- No evaluator metric relaxation, slot normalization, or soft metric promotion.

## Decisions

1. **Use source artifacts already committed to git.**
   - Rationale: the phase stays reproducible and public-safe.
   - Alternative considered: read private corpus or A100 logs. Rejected because
     the output is a public planning artifact.

2. **Bucket residuals by observed field/value shape.**
   - Rationale: `form_fill` has mixed strict residuals, and a single count is
     not enough to choose the repair method.
   - Buckets:
     - `confirmation_marker_missing_or_reordered`
     - `field_name_specificity_drift`
     - `clarify_boundary_confusion`
     - `other_form_fill_strict_drift`

3. **Recommend prompt/policy plus targeted public-safe case design first.**
   - Rationale: most residuals are canonical wording and field-specificity
     problems, not evidence that broad DPO or evaluator changes are needed.
   - A later phase may materialize reviewed cases or train, but this phase does
     not authorize that work.

## Risks / Trade-offs

- [Risk] The bucket names may look like the fix is already implemented.
  -> Mitigation: every artifact labels this as `plan_only`.
- [Risk] Focusing on `form_fill` may defer safety-sensitive `blocked_payment`.
  -> Mitigation: the report explicitly keeps `blocked_payment` for a separate
  safety-policy phase.
- [Risk] The small formal held-out sample may overfit remediation planning.
  -> Mitigation: recommend a bounded case-design phase before any training run.
