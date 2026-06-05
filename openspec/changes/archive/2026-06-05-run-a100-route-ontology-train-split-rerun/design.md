## Context

Voice2Task is still in the first-phase speech-to-contract normalization stage. The current main branch includes the local route ontology repair: `SYSTEM_PROMPT` now states that `route` is a Browser Task Contract execution-channel enum, not a domain/topic/intent/URL/path value, and shows a weather request using `task_type="search"` plus `route="search_web"`.

The current remote baseline is `reports/public-sample/a100-constrained-output-train-split-rerun/`: it reached the constrained-output prompt/parser path but still observed `0/3` validated outputs schema-valid. One raw JSON object used `route="weather"`, which is invalid against the Browser Task Contract route enum. This phase asks the narrow remote question: does the route ontology prompt repair alter those same train-row outputs when run against the existing private adapter?

## Goals / Non-Goals

**Goals:**

- Run one explicitly authorized A100 prediction-only train-split rerun.
- Reuse the existing private train-split adapter; do not retrain or create a new adapter.
- Keep the evidence train-internal with `prediction_split=train`, `overfit_diagnostic=true`, and `generalization_claim=false`.
- Preserve private runtime boundaries: raw logs, private overrides, host details, checkpoints, adapters, caches, private paths, tokens, and SSH details stay out of git.
- Import sanitized evidence that separates raw attempt schema validity, retry attempt schema validity, validated output source, route validity, parse statuses, prompt constraints, and final contract metrics.
- Publish a concise Chinese Human Brief and loop report with non-overclaim boundaries.

**Non-Goals:**

- No SFT/DPO/GRPO training.
- No dev/test, full-public-sample, public full-corpus, production, release, or live-browser benchmark evaluation.
- No checkpoint release, adapter release, public model upload, deployment, PR creation, or push.
- No post-hoc route aliasing, schema coercion, rule-baseline replacement, fixture-mode replacement, or gold-contract repair.

## Decisions

1. **Prediction-only rerun.**
   - Rationale: the latest local change affects prompt serialization and prompt constraint metadata at prediction time. Reusing the same private adapter isolates the route ontology variable.
   - Alternative considered: retrain with the new prompt. Rejected for this phase because it would mix prompt-inference effects with training effects.

2. **Train split only.**
   - Rationale: prior evidence is a train-split overfit diagnostic. If the adapter cannot improve train-row contract output under the repaired prompt, dev/test evaluation remains premature.
   - Alternative considered: run all 12 public-sample rows. Rejected because it would blend train-internal recovery with held-out generalization.

3. **Keep the route enum and schema guard strict.**
   - Rationale: accepting `weather` as an alias would hide the failure instead of measuring whether the model learned the Browser Task Contract route enum.
   - Alternative considered: post-process `route="weather"` into `route="search_web"`. Rejected because it is output coercion and would overstate model correctness.

4. **Report route ontology evidence separately.**
   - Rationale: final `json_valid_rate` alone can obscure whether the model stopped inventing route domain values. Evidence must separately report route enum validity, prompt constraint visibility, and raw/retry/validated source.
   - Alternative considered: summarize only pass/fail. Rejected because prior failures were contract-like but still schema-invalid.

## Risks / Trade-offs

- [Risk] A100 access, idle GPU, private adapter, or dependency state is unavailable. -> Mitigation: retry transient access failures in-bounds, then stop blocked without substituting fixture evidence.
- [Risk] The rerun remains `0/3` schema-valid. -> Mitigation: report it as bounded negative evidence; do not widen to training repair inside this phase.
- [Risk] Private paths or logs leak into committed artifacts. -> Mitigation: import only sanitized JSON/Markdown evidence and run leak-scan over evidence, Human Briefs, loop report, and archived OpenSpec.
- [Risk] A positive train-split result is overclaimed. -> Mitigation: state explicitly that train-internal recovery does not prove dev/test generalization, release readiness, production readiness, or live-browser improvement.
