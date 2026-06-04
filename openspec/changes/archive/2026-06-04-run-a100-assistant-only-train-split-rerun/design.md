## Context

The repository has three relevant pieces of prior evidence: the original A100 train-split diagnostic, observed runtime label provenance showing the old path did not mask prompt tokens, and the local repair that makes SFT construct pretokenized assistant-only labels. This phase is the execution bridge between those pieces: rerun the smallest A100 train-split diagnostic after the objective repair, then publish only sanitized evidence.

The current milestone remains first-phase speech-to-contract normalization. A train-split rerun can show train-internal recovery or continued failure, but it cannot establish dev/test generalization, production readiness, checkpoint release, adapter release, or live-browser benchmark improvement.

## Goals / Non-Goals

**Goals:**

- Execute a new private A100 SFT training run using the current assistant-only SFT label path and explicit heavy-training opt-in.
- Run private-adapter prediction on the train split only, with `overfit_diagnostic=true` and `generalization_claim=false`.
- Record objective-mask evidence from the current tokenizer/collator path so the rerun can be interpreted against actual prompt/assistant label status.
- Commit only sanitized public-sample artifacts: predictions, sidecars, prediction metadata, adapter metadata summary, metrics, manifest, report, leak-scan result, OpenSpec archive, and Human Brief HTML.
- Preserve observed model failures without schema repair, fixture replacement, or gold-contract substitution.

**Non-Goals:**

- No DPO run, GRPO/rule reward stage, hyperparameter sweep, generic chat fine-tuning, skill routing, GUI action policy learning, private corpus publication, checkpoint release, adapter release, production-readiness claim, live-browser benchmark claim, or held-out dev/test generalization claim.

## Decisions

1. **Create a new evidence directory instead of overwriting the prior diagnostic.**
   - Rationale: the prior run is historically important because it predates assistant-only label repair. A new directory preserves before/after provenance and avoids silently changing old evidence.
   - Alternative considered: overwrite `reports/public-sample/a100-train-split-overfit-diagnostic/`. Rejected because it would blur historical evidence and make the old failure harder to audit.

2. **Use the current TRL/PEFT SFT entrypoint rather than a separate training script.**
   - Rationale: the point of the phase is to exercise the repository's primary transparent stack and assistant-only label path, not to prove a parallel A100 recipe.
   - Alternative considered: run a hand-written notebook or one-off remote script. Rejected because it would weaken reproducibility and evidence traceability.

3. **Treat runtime label provenance as an evidence dependency, not as a model-quality metric.**
   - Rationale: prompt mask status helps interpret the training objective. It does not prove prediction recovery on its own.
   - Alternative considered: skip objective evidence and rely on training metadata. Rejected because earlier phases showed intended formatting is not enough.

4. **Keep all raw remote artifacts private and import only sanitized rows and summaries.**
   - Rationale: public review needs bounded predictions, sidecars, metrics, manifests, and reports. Raw logs, adapters, caches, paths, host details, and private overrides are leak risks and out of scope.
   - Alternative considered: commit raw remote logs for debugging. Rejected by the public/private artifact boundary.

## Risks / Trade-offs

- [Risk] Remote model dependencies, private base model cache, or A100 access are unavailable -> Mitigation: stop with a blocked status and do not fabricate fixture evidence.
- [Risk] The current TRL version on A100 differs from local expectations -> Mitigation: record package versions and fail closed if assistant-only labels cannot be used by the trainer path.
- [Risk] The train split recovers but gets overclaimed -> Mitigation: enforce `generalization_claim=false`, state the result as train-internal only, and run leak/claim scans before archive.
- [Risk] The rerun still fails schema or slot shape -> Mitigation: preserve failures exactly as sanitized evidence and recommend the next bounded diagnostic rather than repairing outputs.
- [Risk] Sanitized sidecars omit details useful for debugging -> Mitigation: keep raw remote logs private while committing prompt hashes, decoded previews, generation traces, and aggregate failure slices.
