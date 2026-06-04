## Context

The assistant-only A100 rerun narrowed the remaining failure to contract shape: raw decoded outputs were JSON objects and finished with EOS, but all three train predictions missed required Browser Task Contract fields. The current prompt already names the required top-level fields, yet the model still omits `safety`, `normalized_command`, or `contract_version`, so this phase targets explicit required-field emission and validation metadata before any new training or A100 execution.

## Goals / Non-Goals

**Goals:**
- Make the prediction prompt visibly include a complete Browser Task Contract skeleton and required-field checklist.
- Add a bounded schema-validation guard/retry path around real private-adapter prediction attempts.
- Record whether raw attempts were schema-valid, whether retry was attempted, and whether validated output remains separate from raw output.
- Preserve invalid attempts as evidence and keep public claim boundaries intact.

**Non-Goals:**
- Do not run A100 training or private prediction in this phase.
- Do not modify SFT/DPO data, schemas, gold contracts, or evaluation success criteria.
- Do not coerce invalid predictions into raw model success.
- Do not claim held-out generalization, checkpoint release, adapter release, production readiness, public full-corpus release, or live-browser benchmark improvement.

## Decisions

- Strengthen `SYSTEM_PROMPT` rather than adding a second prompt template. The existing stack uses one shared training/prediction chat template, so the minimal fix is to make that template more explicit and test its constraints.
- Implement validation metadata in the prediction exporter rather than the evaluator. The exporter is where raw decoded attempts, retry attempts, and sidecars are produced, so it can preserve raw-vs-validated boundaries before metrics are computed.
- Keep retry optional and bounded. Retry/guard metadata is useful for future A100 runs, but local tests can validate the behavior with stubs without loading private adapters.
- Keep invalid raw attempts visible. If a retry succeeds later, the evidence must still record the first raw attempt and must not rewrite history.

## Risks / Trade-offs

- [Risk] Retry could be mistaken for raw model recovery. -> Mitigation: metadata and reports distinguish `raw_attempt_schema_valid` from `validated_output_schema_valid`.
- [Risk] Prompt strengthening could change training text. -> Mitigation: tests verify both SFT training text and prediction prompt include the skeleton, and docs describe this as a behavior change requiring a new phase.
- [Risk] Local tests do not prove A100 improvement. -> Mitigation: Human Brief and evidence explicitly mark the phase as local guard/prompt repair only.
