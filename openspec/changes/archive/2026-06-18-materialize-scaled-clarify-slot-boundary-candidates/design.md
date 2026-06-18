## Context

The archived target-selection phase selected `clarify/slots` as the first
scaled residual remediation target. The archived candidate-design phase then
reduced that target into three public-safe themes with accepted
`clarify/clarify` sketches and rejected drift sketches for `search`,
`navigate`, `form_fill`, and `blocked` outputs.

This phase turns those sketches into deterministic standalone candidate data.
It deliberately does not merge the formal public sample yet. A later bounded
merge phase should create a new manifest boundary after the standalone
candidates are inspectable in git.

## Goals / Non-Goals

**Goals:**

- Read the committed scaled clarify candidate design report as the source of
  truth.
- Materialize public-safe candidate seed rows that preserve:
  `task_type=clarify`, `route=clarify`, `safety.allow=true`,
  `safety.reason=ambiguous_request`, `confirmation_required=true`, and
  non-empty `slots.ambiguity`.
- Generate deterministic SFT candidate sidecars from the seed rows.
- Publish materialization evidence with candidate counts, theme coverage,
  split counts, execution-scope flags, and claim boundaries.
- Add CLI and tests so the materialization is reproducible.

**Non-Goals:**

- No formal public sample merge in this phase.
- No rebuild of `seed_traces.jsonl`, `sft_public_sample.jsonl`,
  `dpo_public_sample.jsonl`, or `manifest_public_sample.json`.
- No formal DPO-pair generation for these candidates.
- No A100 training, prediction, prompt change, evaluator change, slot
  normalization, prediction repair, checkpoint/adapter release, production
  readiness claim, held-out recovery claim, or live-browser benchmark claim.
- No generic chat fine-tuning, skill routing, GUI action policy learning,
  first-phase GRPO, or public full local/private corpus release.

## Decisions

1. **Keep materialization deterministic.**

   Rationale: the source design already contains public-safe templates and
   accepted target sketches. The materializer should derive candidate rows from
   those templates without calling an LLM or reading private/raw prediction
   rows.

2. **Use one seed per suggested template.**

   Rationale: each of the three themes contains three suggested utterance
   templates. Materializing `9` seed rows gives a bounded, reviewable first
   candidate set while still covering all three ambiguity patterns.

3. **Use stable split assignment.**

   Rationale: standalone candidates should be easy to review and later merge.
   Assign one seed per theme to each split (`train`, `dev`, `test`) so later
   merge evidence can preserve split labels explicitly.

4. **Do not generate formal DPO pairs yet.**

   Rationale: candidate seed rows and SFT sidecars are enough for review. A
   later formal merge phase can rebuild synchronized public SFT/DPO artifacts
   from the updated formal seed file.

## Risks / Trade-offs

- **[Risk] Nine seed rows may under-cover the full 28-family residual cluster.**
  → Mitigation: record source-family coverage from the design and keep this as
  a first bounded materialization, not a final data scale-up.
- **[Risk] Clarify examples could over-teach unnecessary clarification.** →
  Mitigation: preserve rejected drift sketches and require later merge/training
  phases to keep contrast examples explicit.
- **[Risk] Readers may confuse standalone candidates with formal public sample
  mutation.** → Mitigation: evidence, manifest, tests, and Human Brief must
  state standalone-only and no formal manifest rebuild.
