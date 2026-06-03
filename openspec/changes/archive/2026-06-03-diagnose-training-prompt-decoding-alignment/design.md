## Context

The post-recovery A100 rerun produced sanitized public-sample predictions that are JSON-like and share Browser Task Contract field names, but every row remains schema-invalid. Read-only investigation found that committed SFT/DPO targets use canonical enum `route` values and object `slots`; the path-like routes and list slots appear in private-adapter predictions, not in the public training targets or evaluator.

The visible SFT prompt currently lists required top-level fields but does not list the legal `task_type` and `route` values, does not explicitly say that `route` is an enum rather than a URL/path, and does not explicitly say that `slots` must be a JSON object instead of an array. The A100 public-sample smoke also trains only the `train` split, which currently contains three search rows, while prediction/evaluation is run over all 12 public-sample rows. The committed prediction metadata does not contain raw decoded summaries, generated-token counts, EOS/finish state, or a decoding sidecar, so truncation can only be recorded as an evidence gap.

## Goals / Non-Goals

**Goals:**

- Make the root-cause chain inspectable with a public-safe source diagnostic covering target shape, train/prediction split coverage, prompt constraints, prediction symptoms, and decoding metadata availability.
- Strengthen model-visible contract instructions for enum routes/task types and object-shaped slots.
- Record future decoding policy metadata so later reruns can distinguish greedy decoding settings, `max_new_tokens`, and repair policy from model-quality outcomes.
- Preserve the current evidence posture: invalid predictions remain invalid and are not repaired for metrics or smoke.

**Non-Goals:**

- No checkpoint or adapter release.
- No production-readiness, full-private-corpus, or live-browser benchmark claim.
- No generic chat fine-tuning, skill routing, GUI action policy learning, or first-phase GRPO.
- No automatic schema repair, constrained decoding, or replacement of model output with gold/rule-baseline contracts in this change.
- No A100 rerun in this local phase.

## Decisions

1. **Use a source-level diagnostic instead of adding another schema issue list.**
   - Rationale: schema and alignment diagnostics already show what is wrong in predictions. The missing artifact is why the current evidence points away from target corruption and toward prompt/data/decoding factors.
   - Alternative considered: extend the existing schema diagnostic rows only. This would duplicate field-level failures without explaining the upstream source chain.

2. **Strengthen the shared system prompt in place.**
   - Rationale: both SFT training examples and trained-adapter prediction prompts use the same formatting helper, so a focused prompt change improves both surfaces without introducing a second prompt source.
   - Alternative considered: only add a report warning. That would document the weakness but leave future reruns with the same model-visible ambiguity.

3. **Record decoding policy metadata without adding repair.**
   - Rationale: future public evidence needs to know whether predictions came from greedy decoding and whether any schema repair was applied. Recording policy does not change model output or metrics.
   - Alternative considered: add constrained decoding now. That changes the evaluation target and should be a later scoped change if needed.

4. **Keep split coverage diagnostic descriptive, not prescriptive.**
   - Rationale: a balanced train corpus or overfit micro-test is likely the next useful phase, but changing dataset splits affects training semantics and should remain explicit evidence-driven follow-up.

## Risks / Trade-offs

- Prompt hardening may improve schema adherence but cannot prove model quality without a fresh A100 rerun -> Mitigation: report it as rerun preparation only and make no improvement claim.
- Decoding metadata cannot reconstruct old raw decoded text -> Mitigation: current diagnostic records the missing sidecar as an evidence gap, not a conclusion.
- The public sample remains small and split-skewed -> Mitigation: source diagnostics report split coverage so future reruns can separate train-internal recovery from held-out generalization.
- Adding more diagnostic fields can look like a fix if worded loosely -> Mitigation: reports explicitly state they do not repair, normalize, coerce, or replace predictions.
