## Context

The current trained-adapter evidence shows a stable failure pattern on the bounded train split: raw outputs are strict JSON objects but miss `task_type`, while retry outputs often contain the missing Browser Task Contract shape inside prose/Markdown wrappers. The strict parser correctly rejects those retry fragments, so this phase targets the prompt/output-boundary contract rather than parser behavior.

Relevant current implementation:

- `_schema_retry_prompt(...)` builds the retry prompt.
- `schema_retry_prompt_constraint_summary(...)` publishes retry prompt visibility in metadata and prompt snapshots.
- `_extract_strict_json_object(...)` intentionally accepts only whole strict JSON objects and preserves wrapped text as invalid sanitized evidence.

## Goals / Non-Goals

**Goals:**

- Make the retry prompt boundary more explicit, redundant, and machine-oriented.
- Add policy visibility flags for the new JSON-only boundary clauses.
- Prove locally that metadata/prompt snapshots surface the stricter boundary.
- Publish public-safe evidence explaining the local prompt-policy change and prior A100 failure context.

**Non-Goals:**

- No A100 execution or private prediction rerun in this phase.
- No training, checkpoint release, adapter release, parser relaxation, evaluator metric change, prediction repair, prediction re-score, semantic-equivalence scoring, slot normalization, or live-browser benchmark claim.
- No claim that the model quality improved before a later real A100 rerun demonstrates changed output behavior.
- No change to strict final metrics or historical A100 artifacts.

## Decisions

1. Tighten retry prompt text instead of changing parser behavior.
   - Rationale: strict parser rejection is the desired guardrail; the observed failure is wrapped retry output, not evaluator strictness.
   - Alternative considered: extract JSON fragments from retry text. Rejected because it would hide the model-output failure and change metric semantics.

2. Add constraint-summary booleans for new boundary clauses.
   - Rationale: prompt text alone is easy to drift; metadata and prompt snapshots should prove the retry boundary was visible.
   - Alternative considered: only update focused tests to assert prompt strings. Rejected because public evidence packs also need machine-readable policy visibility.

3. Keep this as a local evidence phase before A100 rerun.
   - Rationale: prompt-policy hardening should be tested locally first; a real A100 rerun is a separate private-execution phase with GPU occupancy, remote output, and copy-back safety requirements.
   - Alternative considered: combine prompt change and A100 rerun. Rejected because it would widen the phase and mix behavior change with private runtime evidence.

## Risks / Trade-offs

- Prompt-only hardening may not change model behavior on A100 -> Mitigation: report this as a local policy hardening phase and require a later prediction-only rerun before claiming output recovery.
- More redundant prompt text may increase retry prompt length -> Mitigation: keep additions short and focused on output boundary clauses, not new schema semantics.
- Overclaim risk -> Mitigation: evidence pack and Human Brief must explicitly state no model-quality claim, no A100 rerun, and no strict metric improvement claim in this phase.
