## Context

The current project stage remains first-phase speech-to-contract normalization: Chinese spoken command or ASR transcript to schema-valid Browser Task Contract. Prior evidence now separates three facts:

- The assistant-only loss path is inspectable and prompt/system/user tokens are masked.
- The previous assistant-only A100 train-split rerun emitted raw JSON objects but all three train predictions failed the Browser Task Contract schema, mainly by omitting required fields.
- The required-field repair phase added a complete contract skeleton, checklist, schema guard, and bounded one-attempt retry path, but did not run A100.

This phase is the smallest remote execution step that can test whether the new prompt/guard path changes the observed train-split failure pattern.

## Goals / Non-Goals

**Goals:**

- Run one authorized A100 train-split SFT rerun through the current assistant-only SFT path and required-field prompt.
- Run train-split private-adapter prediction through the current schema guard/retry path.
- Record raw attempt schema validity, retry attempt schema validity, validated output source, final contract metrics, and objective-mask status separately.
- Import only sanitized public evidence into git-backed artifacts.
- Compare narrowly against the previous assistant-only train-split rerun and required-field repair evidence.

**Non-Goals:**

- No DPO run, GRPO/rule reward stage, hyperparameter sweep, private-corpus training, generic chat fine-tuning, skill routing, GUI action policy learning, checkpoint release, adapter release, public full-corpus release, held-out generalization claim, production-readiness claim, or live-browser benchmark improvement claim.

## Decisions

1. **Use a new evidence directory rather than overwriting prior assistant-only rerun evidence.**
   - Rationale: the previous directory documents the pre-required-field-repair failure and remains the baseline.
   - Alternative considered: overwrite `reports/public-sample/a100-assistant-only-train-split-rerun/`. Rejected because it would blur before/after evidence.

2. **Keep the run train-internal and public-sample only.**
   - Rationale: the next question is whether required-field failures recover on the exact train split, not whether the model generalizes.
   - Alternative considered: immediately run dev/test. Rejected because train-split recovery is still unproven after the repair.

3. **Keep retry metadata separate from model raw output metrics.**
   - Rationale: retry can be useful as a guard, but raw attempt validity and final validated output source must not be conflated.
   - Alternative considered: report only final predictions. Rejected because it would overstate recovery if retry succeeds while raw attempts remain invalid.

4. **Use private A100 overrides and import only sanitized evidence.**
   - Rationale: remote outputs, logs, adapters, caches, private paths, and host details are out of scope for committed artifacts.
   - Alternative considered: commit remote command logs for debugging. Rejected by the public/private evidence boundary.

## Risks / Trade-offs

- [Risk] A100 access, model cache, or dependency state is unavailable -> Mitigation: stop with blocked status and do not create fixture evidence.
- [Risk] Schema retry improves validated output but raw attempts remain invalid -> Mitigation: report raw attempt validity, retry validity, validated output source, and final metrics separately.
- [Risk] Train split recovers and gets overclaimed -> Mitigation: keep `generalization_claim=false` and state that train-internal evidence does not prove dev/test generalization.
- [Risk] Sanitized artifacts omit useful debugging detail -> Mitigation: keep raw logs private and commit public-safe prompt hashes, decoded summaries, generation traces, metrics, and failure slices.
