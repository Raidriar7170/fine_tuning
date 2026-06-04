## Context

The current project stage remains first-phase speech-to-contract normalization: Chinese spoken command or ASR transcript to schema-valid Browser Task Contract. The constrained-output repair is now local and archived. It made the prompt show a valid canonical one-shot, made first-pass output boundaries explicit, and made raw prediction parsing whole-string JSON only.

The current remote baseline is `reports/public-sample/a100-strict-retry-train-split-rerun/`: it reused the private train-split adapter for prediction-only A100 evidence and observed `0/3` validated outputs schema-valid. It also proved strict retry rejected `3/3` wrapped retry fragments. This phase answers the next narrow remote question: does the newly constrained first-pass prompt and whole-string raw parser change train-split prediction evidence when run against the existing private adapter?

## Goals / Non-Goals

**Goals:**

- Run one explicitly authorized A100 prediction-only train-split rerun.
- Reuse the existing private adapter; do not retrain or create a new adapter.
- Keep the evidence scope train-internal with `generalization_claim=false`.
- Preserve private runtime boundaries: raw logs, private overrides, host details, checkpoints, adapters, caches, private paths, tokens, and SSH details stay out of git.
- Import sanitized evidence that separates raw attempt schema validity, retry attempt schema validity, validated output source, parse statuses, and final contract metrics.
- Publish a concise Chinese Human Brief and loop report with non-overclaim boundaries.

**Non-Goals:**

- No SFT/DPO/GRPO training.
- No dev/test, full-public-sample, public full-corpus, production, release, or live-browser benchmark evaluation.
- No checkpoint release, adapter release, public model upload, deployment, PR creation, or push.
- No post-hoc coercion, alias repair, rule-baseline replacement, fixture-mode replacement, or gold-contract repair.

## Decisions

1. **Prediction-only rerun.**
   - Rationale: the local change affects prompt serialization and parsing/guard behavior at prediction time. Reusing the same private adapter isolates that question without paying for another training run.
   - Alternative considered: retrain with the new shared prompt. Rejected for this phase because it changes the training variable and should happen only if prediction-only evidence shows a useful signal or a separate hypothesis is approved.

2. **Train split only.**
   - Rationale: the prior result is a train-split overfit diagnostic. If the adapter cannot produce schema-valid contracts on train rows under the new prompt/parser, dev/test evaluation is premature.
   - Alternative considered: run all 12 public-sample rows. Rejected because that would mix train-internal recovery with held-out generalization.

3. **Reuse the existing private adapter and private override.**
   - Rationale: current evidence compares constrained-output prompt/parser behavior against the closest prior strict-retry run.
   - Alternative considered: publish or commit private config/adapter paths. Rejected because repository artifacts must remain public-safe.

4. **Separate evidence fields instead of a single recovery claim.**
   - Rationale: `json_valid_rate` alone can obscure whether raw, retry, or validated outputs changed. Evidence must report the schema guard surface independently.
   - Alternative considered: summarize as pass/fail. Rejected because previous phases showed output can look JSON-like while remaining schema-invalid.

## Risks / Trade-offs

- [Risk] A100 access, idle GPU, private adapter, or dependency state is unavailable. -> Mitigation: stop blocked; do not create fixture evidence as a substitute.
- [Risk] The rerun stays at `0/3` schema-valid. -> Mitigation: report it as bounded failure evidence; do not widen to training repair inside this phase.
- [Risk] Private paths or logs leak into committed artifacts. -> Mitigation: import only sanitized JSON/Markdown evidence and run leak-scan over evidence, Human Briefs, loop report, and archived OpenSpec.
- [Risk] A positive train-split result is overclaimed. -> Mitigation: state explicitly that train-internal recovery does not prove dev/test generalization, release readiness, production readiness, or live-browser improvement.
