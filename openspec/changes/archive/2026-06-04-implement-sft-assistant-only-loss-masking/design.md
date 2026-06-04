## Context

The repository already has contract-only SFT formatting, prediction prompts without gold targets, train-split overfit diagnostics, and runtime label provenance evidence. The blocking evidence is now objective-path specific: the inspected runtime labels show that assistant contract tokens are in loss, but prompt/system/user tokens are also in loss. This prevents an assistant-only/completion-only loss-mask claim and weakens any later attempt to interpret train-split overfit outcomes.

This phase repairs the local training objective path and the corresponding inspector/reporting surface. It does not run a private A100 retrain by default. If a real A100 rerun is needed after local validation, the autonomous loop must stop at the private-infrastructure gate and report exactly what is ready to run.

## Goals / Non-Goals

**Goals:**

- Add failing tests for assistant-only SFT labels: prompt/system/user tokens must be masked with `-100`, while assistant Browser Task Contract target tokens must carry loss.
- Implement a version-tolerant local label-construction path that can be used by objective inspection and, where supported, real SFT training.
- Keep the implementation fail-closed when token offsets or assistant target spans cannot be identified.
- Update runtime label provenance metadata/evidence so objective-mask repair is visible and bounded.
- Generate a concise Chinese Human Brief with validation results, remaining A100 rerun boundary, and non-overclaim language.

**Non-Goals:**

- No new private A100 training run, DPO run, model prediction repair, schema coercion, checkpoint release, adapter release, private corpus publication, production-readiness claim, live-browser benchmark claim, or dev/test generalization claim.

## Decisions

1. Build labels from the rendered SFT training text and the assistant-target character boundary.
   - Rationale: the formatter already defines the shared contract chat template. Masking labels after tokenization keeps objective inspection and training aligned with the text actually shown to the model.
   - Alternative considered: rely only on TRL version-specific completion-only or assistant-only trainer switches. Rejected as the sole path because those routes depend on template compatibility and optional training dependencies, while this project needs a deterministic label contract that local tests can validate without downloading models or requiring A100 access. The real SFT path still uses TRL `SFTTrainer`; the deterministic layer prepares pretokenized labels before trainer handoff.

2. Fail closed when labels cannot be proven.
   - Rationale: `prompt_tokens_masked=true` must be evidence-backed, not inferred from formatting structure alone.
   - Alternative considered: mark unknown tokenizers as assistant-only based on intended policy. Rejected because previous phases already showed intended formatting is not enough.

3. Keep model-output evidence unchanged.
   - Rationale: objective masking repair can justify a later rerun, but it does not itself make prior invalid predictions valid.
   - Alternative considered: regenerate prediction metrics from fixtures. Rejected because that would confuse pipeline validation with model quality.

4. Stop before private A100 execution unless the execution gate is already explicitly satisfied.
   - Rationale: local code and evidence repair can be completed without private infrastructure; real A100 rerun still requires private overrides, idle GPU selection, and sanitized evidence handling.

## Risks / Trade-offs

- [Risk] Assistant boundary differs between tokenizer chat templates and fallback text -> Mitigation: compute boundary from the actual rendered training text and verify via offset mappings in tests.
- [Risk] TRL SFTTrainer API varies by installed version -> Mitigation: keep a deterministic label builder and add metadata explaining whether real trainer integration used that path directly or is blocked by dependency/API availability.
- [Risk] Objective repair gets overclaimed as model recovery -> Mitigation: reports and Human Briefs must state that no new train-split recovery, dev/test generalization, checkpoint release, production readiness, or live-browser improvement is proven.
- [Risk] A100 rerun is needed to finish model-quality validation -> Mitigation: prepare exact commands/artifact boundaries and stop at the private-infrastructure gate instead of faking evidence.
