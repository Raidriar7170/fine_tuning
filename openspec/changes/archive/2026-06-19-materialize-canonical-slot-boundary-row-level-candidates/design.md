## Context

The archived formal-merge proposal/readiness evidence records:

- source review:
  `reports/public-sample/canonical-slot-boundary-candidate-review/summary.json`;
- required future source:
  `data/public-samples/canonical_slot_boundary_seed_candidates.jsonl`;
- eligible classes: `slot_key_aliases` and `slot_value_boundaries`;
- excluded classes: `normalized_command_display_diagnostic` and
  `excluded_non_equivalence_cases`;
- direct formal merge: false.

This phase supplies the missing row-level candidate source. It should follow
the existing standalone candidate pattern used by other public-sample candidate
materialization phases: candidate rows are public-safe, carry provenance, and
remain separate from formal public sample files until a later bounded merge
phase.

## Goals / Non-Goals

**Goals:**

- Write exactly seven standalone candidate seed rows:
  - 3 slot-key alias rows;
  - 4 conservative slot-value boundary rows.
- Use `split="train"` for every row so this source is train-only until a later
  formal merge phase explicitly chooses otherwise.
- Use `candidate_status="standalone_not_formal_public_sample"`,
  `public_safe=true`, `source_mode="canonical_slot_boundary_candidate_seed"`,
  and provenance back to the review/materialization/policy evidence.
- Write report-local SFT preview rows and a manifest under
  `reports/public-sample/canonical-slot-boundary-row-level-candidates/`.
- Preserve formal public sample files and source review/materialization
  artifacts unchanged.
- Produce focused tests, leak-scan evidence, status docs, and a Human Brief.

**Non-Goals:**

- No mutation of `data/public-samples/seed_traces.jsonl`,
  `sft_public_sample.jsonl`, `dpo_public_sample.jsonl`, or
  `manifest_public_sample.json`.
- No formal public sample merge, formal SFT/DPO row generation, train/dev/test
  split change for formal data, training, prediction rerun, A100 job, prompt
  change, evaluator definition change, strict-exact relaxation, LLM judge,
  semantic-equivalence scoring, prediction repair, deterministic postprocessor
  implementation, checkpoint/adapter release, model-improvement claim,
  held-out recovery claim, production-readiness claim, safety-readiness claim,
  or live-browser benchmark claim.

## Decisions

1. **Materialize only reviewed eligible classes.**
   The row-level source includes only slot-key alias and conservative
   slot-value boundary examples from the archived review. It excludes
   normalized-command display diagnostics and explicit non-equivalence cases.

2. **Use train-only candidate split labels.**
   These candidates are proposed as future training-source candidates, not new
   held-out examples. A later formal merge phase must own any split change and
   comparison-boundary warning.

3. **Keep SFT preview report-local.**
   Report-local SFT preview rows help reviewers inspect expansion shape, but
   do not replace or rebuild formal `sft_public_sample.jsonl`.

4. **Avoid new broad generators unless needed.**
   Static deterministic artifacts with focused tests are acceptable. Add shared
   code only if it materially reduces drift or validation risk.

## Risks / Trade-offs

- [Risk] Candidate source may be mistaken for formal public sample data. ->
  Mitigation: provenance and report fields state standalone status and tests
  assert formal files are unchanged.
- [Risk] Train-only split labels may be too narrow for a later merge. ->
  Mitigation: the later formal merge phase must own split-boundary accounting
  and can reject or revise candidate splits before data mutation.
- [Risk] Normalized-command examples may leak into strict scoring repair. ->
  Mitigation: this phase excludes them from row-level candidates.
- [Risk] Non-equivalence cases may be accidentally materialized. ->
  Mitigation: tests assert excluded case IDs are absent.
