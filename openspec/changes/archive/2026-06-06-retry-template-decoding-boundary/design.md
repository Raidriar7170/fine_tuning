## Context

The A100 retry JSON-only rerun showed that stricter retry wording is visible in metadata and prompt evidence, but the adapter still emits prose/Markdown-wrapped retry fragments. The current retry path needs a local template/decoding-boundary inspection before any heavier A100, constrained decoding, or retry-only training phase.

This change stays local. It may adjust the retry prompt/template surface and metadata visibility, but it must not alter strict parsing, evaluator metrics, prediction repair, model training, or prior A100 artifacts.

## Goals / Non-Goals

**Goals:**

- Make the schema-retry prompt boundary explicit as a machine-only retry template rather than an ordinary explanatory prompt.
- Expose retry template boundary metadata in prediction metadata and prompt snapshots.
- Add tests proving strict wrapped retry fragments remain rejected.
- Publish a local evidence pack and Human Brief that explain the boundary and non-claims.

**Non-Goals:**

- No A100/private-adapter rerun, model training, checkpoint release, adapter release, public full-corpus release, parser relaxation, evaluator metric change, prediction repair, prediction re-score, semantic-equivalence scoring, slot normalization, generic chat fine-tuning, skill routing, GUI action policy learning, first-phase GRPO, production-readiness claim, held-out generalization claim, model-quality claim, or live-browser benchmark claim.

## Decisions

1. Treat this as a local template-boundary hardening phase.
   - Rationale: the previous phase already proved model behavior on A100 did not change; the next cheap question is whether retry prompt construction exposes the correct machine-only boundary before rerunning expensive private prediction.
   - Alternative considered: immediately run another A100 rerun. Rejected because the only expected change is local template/metadata behavior first.

2. Preserve strict whole-string JSON parsing.
   - Rationale: success must come from valid model output, not extracting embedded fragments from wrappers.
   - Alternative considered: parse JSON from Markdown fences. Rejected as parser relaxation/prediction repair.

3. Publish evidence as local policy/instrumentation, not model-quality evidence.
   - Rationale: local prompt/template visibility cannot prove private adapter behavior until a later explicitly scoped rerun.
   - Alternative considered: call it recovery evidence. Rejected because strict final A100 metrics remain zero.

## Risks / Trade-offs

- Template hardening may still not change A100 behavior later -> Mitigation: report this phase as local readiness only and require a separate A100 rerun before model-output claims.
- The retry template may duplicate existing JSON-only wording -> Mitigation: expose distinct metadata for template boundary and machine-only mode rather than only adding more prose.
- Overclaim risk -> Mitigation: reports, specs, and tests must state no A100 execution, no model recovery, and no model-quality improvement claim.
