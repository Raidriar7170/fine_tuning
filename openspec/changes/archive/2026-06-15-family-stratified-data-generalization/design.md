## Context

The current formal public sample is intentionally small and already carries
public evaluation evidence. It has 14 seed rows, 42 SFT rows, 125 DPO pairs, and
split counts of `train=30`, `dev=6`, `test=6`. Recent A100 evidence shows the
7B adapter can recover train rows but held-out `dev`/`test` exact match remains
partial.

The user approved the next phase as family-stratified data generalization, not
broad DPO, evaluator relaxation, multimodal expansion, or A100 training. This
phase should therefore create a larger public-safe data candidate surface while
leaving the formal evidence boundary untouched.

## Goals / Non-Goals

**Goals:**

- Generate an independent public-safe candidate dataset for family-stratified
  SFT generalization.
- Cover the first text/ASR-to-contract families: search, navigation, clarify,
  form-fill, extraction, unsafe payment blocking, and confirmation-sensitive
  requests.
- Give each family explicit train/dev/test coverage while keeping source IDs and
  slot values disjoint across splits.
- Reach a useful first expansion scale without jumping straight to a broad
  300-500 row corpus: 63 seed rows and 189 SFT rows, with 63 SFT rows per split.
- Write a manifest/report with family counts, split counts, non-claims, and
  next-step guidance.
- Preserve current formal public sample files and prior metrics.

**Non-Goals:**

- No changes to formal public sample seed/SFT/DPO/manifest files.
- No DPO pair generation, SFT/DPO/GRPO training, or A100 prediction.
- No visual-reference, GUI action policy, skill-routing, or generic chat data.
- No evaluator-side semantic scoring, prediction repair, exact-match relaxation,
  or re-scoring of prior evidence.
- No model recovery, held-out recovery, release, production, private-corpus, or
  live-browser claims.

## Decisions

1. Use an independent candidate dataset instead of editing the formal public
   sample.
   - Rationale: current public held-out evidence remains interpretable and can
     still be compared against later explicit merge/eval phases.
   - Alternative considered: append rows to `seed_traces.jsonl` immediately.
     Rejected because it changes the evidence boundary and would require a new
     held-out interpretation.

2. Generate a deterministic first expansion of 63 seeds / 189 SFT rows.
   - Rationale: this is large enough to give `dev` and `test` at least 50 SFT
     rows each, while still small enough for manual review and public safety.
   - Alternative considered: generate 300-500 SFT rows now. Deferred because the
     current residual signal is specific and should be expanded in controlled
     layers.

3. Use family-stratified splits, not split-exclusive task families.
   - Rationale: every split should contain each contract family, but source IDs,
     input phrasing clusters, and concrete slot values must not cross splits.
     This tests within-family generalization rather than whether a whole task
     type exists at all.
   - Alternative considered: hold entire families out of train. Deferred to a
     later family-holdout benchmark because the current goal is slot-value and
     phrasing generalization within known contract families.

4. Generate accepted SFT rows only.
   - Rationale: DPO hard negatives should come from observed model residuals
     after the new candidate surface is reviewed or evaluated.
   - Alternative considered: synthesize 500-1000 DPO pairs now. Rejected because
     that would change the objective before we know which residuals remain.

## Risks / Trade-offs

- **Risk:** Candidate data is mistaken for official evaluation data.
  **Mitigation:** store it under a separate candidate file/report, set
  `formal_public_sample_modified=false`, and assert existing formal counts do
  not change.
- **Risk:** Split leakage through duplicated source IDs or slot values.
  **Mitigation:** tests assert source IDs are unique and family slot signatures
  are disjoint across train/dev/test.
- **Risk:** The new dataset gets retold as model-quality progress.
  **Mitigation:** reports, manifests, and Human Brief state no training,
  prediction, DPO, or held-out recovery claim occurred.
- **Risk:** The confirmation family overlaps with form-fill.
  **Mitigation:** keep the family label separate while using the existing
  contract schema; it targets confirmation behavior, not a new task type.

## Migration Plan

1. Add failing tests for family-stratified candidate generation, CLI output,
   split separation, public safety, and formal public-sample non-mutation.
2. Implement deterministic candidate generation and report writing.
3. Generate committed candidate artifacts.
4. Generate a Chinese Human Brief from the new artifacts and validation output.
5. Run focused and full validation, then archive the OpenSpec change if complete.

Rollback is simple: remove the candidate artifacts and code paths introduced by
this change. Formal public sample files are not rewritten.

## Open Questions

- Whether to merge this candidate dataset into the formal public sample should
  be decided in a later OpenSpec phase after review.
- Whether to derive DPO hard negatives from the candidate dataset should wait
  until model residuals are observed on the new surface.
