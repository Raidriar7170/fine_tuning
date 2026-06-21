## Context

`BrowserTaskContract` V1 is the authoritative external contract for Voice2Task. The latest recovered-input Contract V2 projection reached `PARTIAL_SCHEMA_BENEFIT`: derived/display fields, mainly `normalized_command`, account for a bounded strict-exact burden, but executable pass does not improve and core slot failures remain dominant. The useful implementation step is therefore a thin internal boundary, not a training-target migration or public schema upgrade.

The existing code already provides:

- V1 validation and canonical JSON through `BrowserTaskContract`, `as_contract()`, and `canonical_contract_json()`.
- Projection-only V2 helper logic and a deterministic `normalized_command` renderer in `contract_v2_projection.py`.
- Current recovered step-matched prediction/gold contracts under `reports/public-sample/step-matched-canonical-slot-ablation/raw-inputs/`.

## Goals / Non-Goals

**Goals:**

- Introduce an internal immutable `ContractCoreV2` DTO for the five core fields only.
- Introduce internal envelope metadata that separates V1 display/version fields from core fields.
- Provide pure, deterministic APIs for V1 -> Core -> V1-compatible envelope roundtrip.
- Prove preserve-mode roundtrip exactness across current committed public-safe contracts and recovered prediction contracts.
- Provide a small shadow compatibility CLI/report path without changing runtime decisions.
- Keep V1 evaluator metrics and controlled smoke behavior unchanged.

**Non-Goals:**

- No SFT, DPO, GRPO, A100 job, prediction rerun, data mutation, split change, prompt change, decoding change, LoRA change, evaluator change, strict-exact relaxation, prediction repair, LLM judge, or semantic-equivalence scoring.
- No public BrowserTaskContract V2 schema and no external `contract_version="v2"` default.
- No downstream Voice-to-Browser Agent runtime migration.
- No model improvement, executable-quality improvement, safety readiness, production readiness, checkpoint release, or adapter release claim.

## Decisions

1. **Use frozen dataclasses and existing V1 constants.**
   - Rationale: The project already uses frozen dataclasses for schema DTOs. Reusing `TASK_TYPES`, `ROUTES`, and `ValidationError` avoids a second taxonomy.
   - Alternative considered: Pydantic model. Rejected because it would add dependency/style surface without need.

2. **Place internal implementation in `src/voice2task/contract_core_v2.py`.**
   - Rationale: Keeps the internal boundary distinct from the projection experiment and from authoritative V1 schema.
   - Alternative considered: Add fields/classes to `schemas.py`. Rejected to avoid implying that V2 is an external schema peer.

3. **Reuse the existing deterministic renderer only for `derive_display`.**
   - Rationale: Projection evidence already tested the renderer support and deterministic roundtrip. `derive_display` must not create a competing rendering policy.
   - Alternative considered: Reuse `build_v2_envelope()`. Rejected because that function emits `contract_version="v2"`, which violates the V1-compatible external boundary.

4. **Define exactness as canonical V1 DTO exactness.**
   - Rationale: `BrowserTaskContract.from_dict()` and `to_dict()` define the committed V1 schema surface; field order and raw extra keys are not V1 semantics.
   - Alternative considered: Byte-for-byte raw JSON preservation. Rejected because existing evaluators canonicalize through DTOs and already ignore unknown extras.

5. **Add a shadow check/report rather than changing evaluator/runtime flow.**
   - Rationale: The phase must prove the code is usable without changing current model outputs, evaluator metrics, or runtime decisions.
   - Alternative considered: Insert core projection into the default parser/evaluator. Rejected as too broad and behavior-changing.

## Risks / Trade-offs

- [Risk] Unknown extra fields in raw input are not preserved by the canonical V1 roundtrip. → Mitigation: Document exactness as V1 DTO canonical exactness and keep formal schema unchanged.
- [Risk] `derive_display` renderer has unsupported cases. → Mitigation: Fail closed and report unsupported counts; keep `preserve_legacy` as default.
- [Risk] A compatibility report could be mistaken for model-quality evidence. → Mitigation: Report explicit claims flags and update docs with no-training/no-improvement boundaries.
- [Risk] Shadow check could accidentally mutate passed-in objects. → Mitigation: Use deep JSON copies in DTO projection/building and tests for object preservation.

## Migration Plan

1. Add tests for the new internal DTO, envelope metadata, preserve roundtrip, derive-display fail-closed behavior, and shadow report gates.
2. Implement the internal module and a minimal `voice2task-eval contract-core-v2-check` entry point.
3. Generate the public-safe internal compatibility evidence directory.
4. Verify the full test/lint/OpenSpec/current-truth/leak-scan ladder.
5. Archive the change once complete.

Rollback is deletion of the new module, CLI subcommand, docs, evidence, and OpenSpec change artifacts; no data, evaluator, model, schema, or runtime migration is performed.

## Open Questions

None for this phase. Future slot-representation analysis is explicitly a separate change.
