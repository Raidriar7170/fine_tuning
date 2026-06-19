## Context

The standalone row-level source contains seven public-safe train split
candidate seeds:

- three `slot_key_aliases`;
- four `slot_value_boundaries`;
- zero normalized-command diagnostic examples;
- zero excluded non-equivalence examples.

The current formal public sample boundary is
`public-sample-20260617T152259Z` with 240 seeds, 675 SFT rows, and 2046 DPO
pairs. A formal merge will change this boundary, so reports and status docs
must avoid comparing old held-out metrics directly to future metrics unless a
future phase binds to the new manifest.

## Goals / Non-Goals

**Goals:**

- Validate the seven canonical slot-boundary candidate rows exactly before
  merge.
- Promote candidate provenance from
  `standalone_not_formal_public_sample` to `formal_public_sample`.
- Preserve `split="train"` for all seven candidates.
- Rebuild formal SFT, DPO, and manifest artifacts from the updated seed file.
- Publish machine-readable and human-readable merge evidence, including
  comparison-boundary warnings and claim boundaries.
- Produce focused tests, leak-scan evidence, status docs, and a Human Brief.

**Non-Goals:**

- No training, prediction rerun, A100 job, prompt change, evaluator definition
  change, strict-exact relaxation, LLM judge, semantic-equivalence scoring,
  prediction repair, deterministic postprocessor implementation,
  checkpoint/adapter release, model-improvement claim, held-out recovery claim,
  production-readiness claim, safety-readiness claim, or live-browser
  benchmark claim.

## Decisions

1. **Use guarded merge helper and CLI parity.**
   Follow existing candidate merge helpers: validate the candidate source,
   reject duplicates/unreviewed rows/already-formal rows, promote provenance,
   write the updated seed file, and run `build_public_sample_dataset`.

2. **Preserve train-only split labels.**
   These candidates were materialized as train-only candidate source. The merge
   must preserve those labels so no new held-out rows are introduced silently.

3. **Treat merge as a comparison-boundary change.**
   The manifest and evidence must record that the formal public sample boundary
   changed and old metrics are not directly comparable.

4. **Fail closed on unsupported claims.**
   Evidence/report writers must reject training, prediction, A100, evaluator
   change, postprocessor, slot normalization, checkpoint/adapter release, or
   model-quality claim fields.

## Risks / Trade-offs

- [Risk] Formal data mutation could be mistaken for model-quality evidence. ->
  Mitigation: strict execution-scope and claim fields plus Human Brief wording.
- [Risk] Candidate source could be merged twice. -> Mitigation: duplicate ID
  checks before writing formal sample files.
- [Risk] Split boundaries may be misunderstood. -> Mitigation: preserve
  train-only split labels and record split counts.
- [Risk] The stale active scaled-clarify change may be conflated with this
  canonical-slot merge. -> Mitigation: tests and status docs should keep these
  phases distinct.

## Validation Plan

- Focused merge tests and candidate-source tests.
- Full pytest.
- Public dataset validation.
- DPO check.
- OpenSpec strict validation.
- Public leak-scan over touched data/docs/evidence.
- `git diff --check`.
