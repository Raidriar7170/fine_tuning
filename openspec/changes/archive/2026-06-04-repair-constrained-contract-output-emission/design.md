## Context

The project is still in first-phase speech-to-contract normalization. The latest A100 strict-retry train-split rerun showed that strict retry parsing now fails closed for Markdown/prose-wrapped JSON fragments, but it did not improve model output quality: raw attempts, retry attempts, and validated outputs all remained 0/3 schema-valid. The remaining local gap is that the first-pass prediction prompt exposes field constraints, but not a valid canonical one-shot JSON object plus explicit whole-object boundaries.

## Goals / Non-Goals

**Goals:**

- Strengthen the model-visible first-pass prediction prompt with a valid canonical Browser Task Contract one-shot.
- Add explicit first-pass boundaries: the first non-empty character must be `{`, the last non-empty character must be `}`, and Markdown/prose wrappers are forbidden.
- Keep strict retry and schema guard behavior fail-closed.
- Prove locally that prediction prompts do not include the gold target and that invalid wrapped fragments remain invalid.
- Publish a small public-safe local evidence pack and Human Brief for the repair.

**Non-Goals:**

- No A100 execution, no new SFT/DPO/GRPO training run, no data expansion, no generic chat fine-tuning, no skill routing, no GUI action policy learning, no checkpoint release, no adapter release, no public full-corpus release, no held-out generalization claim, no production-readiness claim, and no live-browser benchmark improvement claim.

## Decisions

1. **Repair the prompt, not the metric path.**
   - Rationale: the previous phase proved strict parser correctness; the remaining problem is model-visible output shape, not evaluator leniency.
   - Alternative considered: post-process invalid JSON-like outputs into valid contracts. Rejected because it would hide model failures and violate existing recovery honesty requirements.

2. **Use a valid canonical one-shot instead of only placeholder skeletons.**
   - Rationale: placeholders like `<boolean>` are useful as instructions but are not valid JSON examples. A valid minified Browser Task Contract example gives the model a concrete output shape without leaking row gold targets.
   - Alternative considered: add more prose instructions. Rejected because prior A100 evidence already showed the model can follow prose by wrapping JSON in prose; the repair should bias the raw output shape.

3. **Apply the output contract through the shared chat template.**
   - Rationale: the current training, prediction, and DPO formatting surfaces intentionally share `SYSTEM_PROMPT`. Updating that shared template keeps future fine-tuning text aligned with the prediction prompt, while tests still prove prediction prompts exclude row gold targets.
   - Alternative considered: add a prediction-only system prompt. Rejected for this phase because it would split the template surface and increase train/predict drift.

4. **Keep acceptance tied to whole-string JSON plus `BrowserTaskContract.from_dict()`.**
   - Rationale: the repair should only influence generation. A prediction is valid only if the full decoded output parses as one JSON object and passes the schema gate.
   - Alternative considered: accept JSON fragments or repair aliases such as `search_web` task types. Rejected because strict retry intentionally closed that false-positive path.

5. **Publish local prompt/evidence diagnostics before another A100 run.**
   - Rationale: this phase can be validated without private infrastructure. A later A100 rerun should only happen after the local prompt contract is locked down.

## Risks / Trade-offs

- [Risk] A valid one-shot example could bias outputs toward the example values. -> Mitigation: use it only as a generic shape exemplar, assert no gold target appears in prediction prompts, and keep metrics honest in later runs.
- [Risk] Prompt strengthening may not improve real model outputs. -> Mitigation: frame this as local constrained-output hardening, not model recovery; require a later authorized A100 rerun for remote evidence.
- [Risk] Stronger prompt text could be mistaken for coercive repair. -> Mitigation: tests and reports state that invalid model outputs remain invalid and only schema-valid whole JSON is accepted.
- [Risk] The prompt becomes overly long. -> Mitigation: keep the one-shot compact and use existing prompt constraint summary/test surfaces.
