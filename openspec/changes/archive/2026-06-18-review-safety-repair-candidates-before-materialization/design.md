## Context

The previous `design-safety-repair-candidates` phase produced three
public-safe candidate themes anchored by the current layered unsafe
false-negative signal and current public gold/prediction sidecars. Its
recommended next step is `review_safety_repair_candidates_before_materialization`.
This phase performs that review without generating data or changing any
evaluator behavior.

## Goals / Non-Goals

**Goals:**

- Publish review-only safety repair candidate evidence under
  `reports/public-sample/safety-repair-candidate-design-review/`.
- Validate the source design is current, public-safe, and internally
  consistent before review.
- Decide which candidate themes are acceptable inputs to a later bounded
  materialization proposal and which need additional policy design first.
- Preserve historical blocked-payment safety repair, layered-eval,
  residual-diagnosis, remediation-target-selection, and safety design artifacts
  as immutable source evidence.

**Non-Goals:**

- No seed materialization, public-sample mutation, train/dev/test split change,
  SFT/DPO/GRPO run, A100 job, prediction run, prompt change, evaluator change,
  evaluator relaxation, LLM judge, semantic-equivalence scoring, prediction
  repair, adapter/checkpoint release, production-readiness claim,
  safety-readiness claim, held-out recovery claim, or live-browser benchmark
  claim.

## Decisions

1. **Review source-design themes, not raw model behavior.**
   The authoritative source is
   `reports/public-sample/safety-repair-candidate-design/safety_repair_candidate_design.json`.
   The review may inspect the design's public-safe sketches and evidence
   rationale, but it must not rerun prediction or read private rows.

2. **Separate row-backed themes from broader policy themes.**
   A candidate directly anchored by the current unsafe false-negative row can be
   marked as ready for a later materialization proposal. Broader unsafe-action
   denial themes can be deferred to a safety-policy design proposal when their
   evidence is strategy-level rather than row-level.

3. **Keep review as evidence, not approval to mutate data.**
   A `ready_for_later_bounded_materialization_proposal` decision authorizes only
   a later OpenSpec proposal. It does not create reviewed seed IDs, merge rows,
   or claim model-quality impact.

## Risks / Trade-offs

- [Risk] Treating review as data approval. -> Mitigation: report artifact policy
  keeps all materialization and data-mutation flags false.
- [Risk] Over-broad unsafe-action theme becomes unsupported seed data. ->
  Mitigation: defer broad policy-only themes to a separate policy-design phase.
- [Risk] Review silently changes historical evidence. -> Mitigation: validation
  includes git status checks for historical evidence directories.
