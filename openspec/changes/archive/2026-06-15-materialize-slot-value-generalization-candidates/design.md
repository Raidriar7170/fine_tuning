## Context

The prior `design-slot-value-generalization-cases` phase produced a public-safe design artifact with four reviewed case groups:

- `form-email-slot-value-language-variant`
- `clarify-ambiguous-slot-value-canonical-phrase`
- `navigate-open-url-normalized-command-paraphrase`
- `blocked-payment-normalized-command-paraphrase`

That artifact deliberately stopped before data mutation. The formal public sample currently has 10 seed rows, 30 SFT rows, and 90 DPO pairs, with `dev` and `test` rows still serving as held-out public evidence. This phase must create usable candidate rows without weakening that boundary.

## Goals / Non-Goals

**Goals:**

- Materialize exactly one public-safe seed candidate per reviewed case group.
- Expand candidates into schema-compatible SFT rows by reusing the existing augmentation path.
- Keep all generated candidate data independent from the formal public sample artifacts.
- Write a manifest/report that records counts, case coverage, source design, and explicit non-claims.
- Provide a repeatable CLI command and tests for regeneration.

**Non-Goals:**

- No A100 execution, training, prediction, DPO generation, or public-sample rebuild.
- No edits to existing held-out `dev`/`test` public sample rows.
- No evaluator relaxation, prediction repair, semantic-equivalence scoring, or soft-slot-F1 promotion.
- No checkpoint, adapter, production, private-corpus, or live-browser benchmark claims.

## Decisions

1. Use a separate candidate seed file instead of appending to `seed_traces.jsonl`.
   - Rationale: this preserves held-out evidence and lets a later phase explicitly decide whether and how to merge candidates.
   - Alternative considered: append directly to public seed traces and rebuild SFT/DPO. Rejected because it would immediately change the public sample training surface and blur the current diagnostic boundary.

2. Use legal `train` split labels while marking candidate status in file names and provenance.
   - Rationale: `SFTDatasetRow` only accepts `train`, `dev`, and `test`; using `train` keeps rows schema-compatible for future controlled SFT experiments.
   - Alternative considered: introduce a `candidate_train` split. Rejected because it would broaden schema behavior and touch more validation surfaces than this phase needs.

3. Generate SFT candidate rows but not DPO candidate pairs.
   - Rationale: the approved design is about canonical accepted values first. Preference data would be a separate hypothesis and should remain a later decision.
   - Alternative considered: generate hard negatives from observed wrong values. Deferred to avoid silently changing the objective from SFT data materialization to DPO.

4. Treat source design case groups as an allowlist.
   - Rationale: materialization should fail if the design artifact drifts or has unreviewed case groups.
   - Alternative considered: infer arbitrary candidates from residual diagnosis. Rejected because it would bypass the reviewed design artifact.

## Risks / Trade-offs

- **Risk:** Candidate rows are mistaken for official public sample rows.  
  **Mitigation:** keep them in a separate candidate file/report, set `public_sample_modified=false`, and verify formal public-sample manifest counts stay unchanged.
- **Risk:** Materialized candidates leak held-out answers into training without review.  
  **Mitigation:** do not rebuild training artifacts or configs in this phase; stop before merge/training decisions.
- **Risk:** The phase is interpreted as model-quality improvement.  
  **Mitigation:** reports and Human Brief state `training_run=false`, `prediction_run=false`, and `held_out_generalization_recovered=false`.
- **Risk:** Hardcoded candidates drift from the design.  
  **Mitigation:** tests assert the exact case group IDs, canonical fields, and counts.

## Migration Plan

1. Add tests that describe the expected materialization output and current-public-sample non-mutation boundary.
2. Implement candidate generation, report writing, and CLI wiring.
3. Generate committed candidate data and evidence from the archived design artifact.
4. Validate focused tests, dataset validation, OpenSpec, leak scan, and diff hygiene.
5. Archive the OpenSpec change and commit if the worktree remains integration-safe.

Rollback is simple: remove the candidate seed file, evidence report, CLI/tests, and this archived OpenSpec change; existing public sample artifacts are not rewritten by the phase.

## Open Questions

- Whether to merge these candidates into the formal public sample, and whether to run a small train-only SFT probe or a full A100 rerun, remains a later user decision.
