## Context

The current `main` includes the archived public-readonly search contract policy: `SYSTEM_PROMPT` now states that public-readonly lookup/search rows should use `task_type="search"`, `route="search_web"`, `safety.allow=true`, `safety.reason="public_readonly"`, `confirmation_required=false`, and `slots.query` as a compact query string. The latest A100 evidence is `reports/public-sample/a100-normalized-command-policy-train-split-rerun/`: it produced three train predictions from the private adapter path, reached final schema-valid output for `1/3` rows, reached normalized-command exact string match for `2/3`, but kept strict `contract_exact_match=0.0000`.

The following local diagnosis, `reports/public-sample/a100-normalized-rerun-row-mismatch-diagnosis/`, separated the remaining row-level failures into `schema_missing_confirmation_required`, `schema_invalid_task_type_enum`, and `schema_valid_task_route_safety_slot_mismatch`. This phase asks one narrow remote question: does the public-readonly search contract prompt policy change those same train-row private-adapter outputs when run through the existing prediction path?

## Goals / Non-Goals

**Goals:**

- Run one explicitly authorized A100 prediction-only train-split rerun.
- Reuse the existing private train-split adapter; do not retrain or create a new adapter.
- Keep the evidence train-internal with `prediction_split=train`, `overfit_diagnostic=true`, and `generalization_claim=false`.
- Preserve private runtime boundaries: raw logs, private overrides, host details, checkpoints, adapters, caches, private paths, tokens, and SSH details stay out of git.
- Import sanitized evidence that separates prompt-policy visibility, prediction-source provenance, strict schema metrics, task type/route/safety/confirmation/slot observations, row-level family counts, and non-claim boundaries.
- Publish concise Chinese Human Brief and loop closeout with honest limitations.

**Non-Goals:**

- No SFT/DPO/GRPO training.
- No dev/test, full-public-sample, public full-corpus, production, release, or live-browser benchmark evaluation.
- No checkpoint release, adapter release, public model upload, deployment, PR creation, or push.
- No post-hoc slot normalization, semantic-equivalence scoring, string canonicalization of predictions, rule-baseline replacement, fixture-mode replacement, gold-contract repair, or metric re-score.

## Decisions

1. **Prediction-only rerun.**
   - Rationale: the latest local change affects prompt serialization at prediction time. Reusing the same private adapter isolates the prompt-policy variable.
   - Alternative considered: retrain with the new target policy. Rejected for this phase because it would mix prompt-inference effects with training effects.

2. **Train split only.**
   - Rationale: prior evidence is a train-split diagnostic. If the adapter cannot improve the same train-row contract fields under the repaired prompt, dev/test evaluation remains premature.
   - Alternative considered: run all 12 public-sample rows. Rejected because it would blend train-internal observation with held-out/generalization claims.

3. **Keep strict exact-match evaluation.**
   - Rationale: this phase is meant to observe whether field outputs change, not to redefine metric semantics.
   - Alternative considered: add semantic-equivalence scoring or slot normalization. Rejected because either would be a separate evaluator-policy change and would invalidate comparison with prior strict metrics.

4. **Report row-level policy evidence separately.**
   - Rationale: final `contract_exact_match` can hide whether remaining failures are task type, route, safety reason, confirmation, slots, schema validity, or normalized-command. Evidence must separately report field counts while preserving strict final metrics.
   - Alternative considered: summarize only final exact match. Rejected because previous row mismatch diagnosis showed field-level failures deserve explicit but non-relaxing explanation.

## Risks / Trade-offs

- [Risk] A100 access, idle GPU, private adapter, or dependency state is unavailable. -> Mitigation: retry transient access failures in-bounds, then stop blocked without substituting fixture evidence.
- [Risk] The rerun remains `0/3` strict exact matches or worsens some field. -> Mitigation: report it as bounded negative evidence; do not widen to training repair inside this phase.
- [Risk] A positive train-split result is overclaimed. -> Mitigation: state explicitly that train-internal field improvement does not prove dev/test generalization, model quality, release readiness, production readiness, or live-browser improvement.
- [Risk] Private paths or logs leak into committed artifacts. -> Mitigation: import only sanitized JSON/Markdown evidence and run leak-scan over evidence, Human Briefs, loop report, and archived OpenSpec.
- [Risk] Prompt length regresses near the fake-tokenizer sequence cap. -> Mitigation: include prompt snapshot/constraint evidence and rerun A100 smoke tests in local validation.
