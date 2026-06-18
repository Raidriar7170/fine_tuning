## Context

The preceding residual-driven target selection chose
`safety-repair-unsafe-false-negative` as the first target because the current
layered evaluator reports one unsafe false-negative signal on the test split.
The committed layered and residual summaries provide the aggregate signal, and
the current public gold/prediction sidecars expose the public-safe boundary row
and contract sketch. This phase must use those committed public artifacts to
propose candidate themes rather than materialize data.

## Goals / Non-Goals

**Goals:**

- Publish design-only safety repair candidate evidence under
  `reports/public-sample/safety-repair-candidate-design/`.
- Read current remediation target-selection, layered-eval, and
  residual-diagnosis artifacts as source evidence.
- Design public-safe candidate themes for unsafe downgrade,
  confirmation-required drop, and clarify-vs-blocked drift.
- Record accepted target sketches, rejected drift sketches, evidence counts,
  later allowed operations, unsupported changes, and claim boundaries.
- Keep older blocked-payment safety repair artifacts intact as historical
  evidence.

**Non-Goals:**

- No seed materialization, public-sample mutation, train/dev/test split change,
  SFT/DPO/GRPO run, A100 job, prediction run, evaluator relaxation, LLM judge,
  semantic-equivalence scoring, prediction repair, adapter/checkpoint release,
  production-readiness claim, safety-readiness claim, held-out recovery claim,
  or live-browser benchmark claim.

## Decisions

1. **Design from current public artifacts only.**
   The new report should not read private rows or rerun prediction. It should
   cite `remediation-target-selection`, `layered-eval`, and
   `residual-diagnosis` as its aggregate evidence base, and may cite the
   committed public gold/prediction sidecar row only as a public-safe contract
   boundary sketch.

2. **Use theme-level candidates instead of seed rows.**
   Because this phase is not a data phase, it should design safety-boundary
   themes with public-safe target sketches and rejected drift sketches instead
   of emitting new seed rows.

3. **Separate safety repair from model readiness.**
   Even if the design targets unsafe downgrade behavior, it is not safety
   readiness or model improvement evidence. A later phase must materialize,
   train, or evaluate separately before any measurable effect can be claimed.

## Risks / Trade-offs

- [Risk] Treating aggregate unsafe-FN evidence as row-level proof. -> Mitigation:
  record the primary source as `layered_eval_summary` and avoid raw-row claims.
- [Risk] Repeating older blocked-payment repair work as if it were current. ->
  Mitigation: cite older blocked-payment artifacts only as pattern history, not
  as the current evidence source.
- [Risk] Candidate design could be mistaken for data. -> Mitigation: machine
  flags must keep materialization, public-sample mutation, training, prediction,
  and evaluator changes false.
