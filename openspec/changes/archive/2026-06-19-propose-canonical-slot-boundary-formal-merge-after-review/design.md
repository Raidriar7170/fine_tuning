## Context

The canonical slot-boundary review is archived under
`openspec/changes/archive/2026-06-19-review-canonical-slot-boundary-candidates-before-merge/`.
Its machine-readable report says:

- `slot_key_aliases` is eligible for a later bounded formal-merge proposal;
- `slot_value_boundaries` is eligible for a later bounded formal-merge
  proposal;
- `normalized_command_display_diagnostic` is diagnostic/display-only;
- excluded non-equivalence cases stay blocked or deferred.

The source materialization is still report-local:
`reports/public-sample/canonical-slot-boundary-candidates/summary.json`.
Unlike earlier formal merge phases, there is no candidate seed JSONL file yet
for these canonical slot-boundary examples. The safe next phase is therefore a
formal-merge proposal/readiness packet, not a formal data merge.

## Goals / Non-Goals

**Goals:**

- Publish proposal/readiness evidence under
  `reports/public-sample/canonical-slot-boundary-formal-merge-proposal/`.
- Record eligible candidate classes, excluded classes, and the exact missing
  prerequisite for data mutation: a reviewed row-level candidate seed source.
- Define future merge acceptance criteria, required validation, comparison
  boundary warnings, and overclaim boundaries.
- Preserve formal public sample and generated artifacts unchanged.
- Produce focused tests, leak-scan evidence, status docs, and a Human Brief.

**Non-Goals:**

- No mutation of `data/public-samples/seed_traces.jsonl`,
  `sft_public_sample.jsonl`, `dpo_public_sample.jsonl`, or
  `manifest_public_sample.json`.
- No row-level candidate JSONL generation, SFT/DPO row generation, train/dev/test
  split change, formal public sample merge, training, prediction rerun, A100
  job, prompt change, evaluator definition change, strict-exact relaxation,
  LLM judge, semantic-equivalence scoring, prediction repair, deterministic
  postprocessor implementation, checkpoint/adapter release, model-improvement
  claim, held-out recovery claim, production-readiness claim,
  safety-readiness claim, or live-browser benchmark claim.

## Decisions

1. **Fail closed when row-level merge inputs are absent.**
   Class-level sketches are enough to write proposal/readiness evidence, but
   not enough to rewrite the formal public sample. The report must mark
   `formal_merge_readiness="not_ready_missing_row_level_candidate_source"`.

2. **Limit future merge eligibility to two reviewed classes.**
   Future formal merge planning may include `slot_key_aliases` and
   `slot_value_boundaries` only. Normalized-command diagnostics and excluded
   non-equivalence cases remain outside formal merge eligibility.

3. **Require a later materialization or merge phase to own exact rows.**
   Any later data mutation must name the exact candidate JSONL source, preserve
   or intentionally change split labels, regenerate derived SFT/DPO/manifest
   artifacts, and publish a comparison-boundary warning.

4. **Do not add a merge command before inputs exist.**
   This phase should not create generic merge code for a hypothetical source.
   A later implementation phase can reuse existing dataset merge patterns once
   exact candidate rows are present.

## Risks / Trade-offs

- [Risk] A proposal can be mistaken for approval to mutate data. ->
  Mitigation: set `formal_public_sample_modified=false`,
  `formal_merge_ready_now=false`, and `implemented_now=false`.
- [Risk] `normalized_command` examples might drift into strict scoring repair.
  -> Mitigation: keep them excluded from merge eligibility.
- [Risk] Future metrics might compare across changed manifest boundaries. ->
  Mitigation: proposal evidence must require a `comparison_boundary` before
  any future merge.
- [Risk] The stale active `merge-scaled-clarify-slot-boundary-candidates`
  change could be conflated with this canonical-slot proposal. -> Mitigation:
  tests must assert it remains untouched.
