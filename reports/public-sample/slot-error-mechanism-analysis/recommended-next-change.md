# Recommended Next Change

- Decision label: `MIXED_SLOT_REPRESENTATION_REQUIRED`
- Change id: `design-hybrid-slot-representation-v1`
- Scope: Design-only next OpenSpec change; no training, prediction rerun, evaluator relaxation, or runtime migration.
- Target slot paths: city, reason, query, ambiguity, field
- Target task families: blocked:deny, clarify:clarify, extract:extract_page, form_fill:fill_form, navigate:open_url, search:search_web

## Top Evidence

- Representation candidates by slot path: {'copy_or_normalize': 4, 'mixed_slot_value_representation': 3, 'task_slot_schema_constraints': 1}
- Confidence distribution: {'HIGH': 5, 'LOW': 1, 'MEDIUM': 2}
- Paired movement: persistent=70, recovered=10, regressed=12
- Top pressure slot paths: city, reason, query, ambiguity, field

## Acceptance Criteria

- keeps BrowserTaskContract V1 externally compatible
- preserves strict slot matching as the reported metric boundary
- uses deterministic copy, normalization, typed, and structure evidence only

## Non-Goals

- no DPO or GRPO
- no LLM judge
- no automatic alias repair
- no checkpoint or adapter release

## Metrics To Watch

- strict_slot_f1
- slot_value_exact_f1
- slot_value_normalized_f1
- executable_contract_pass_rate

## Migration Risks

- internal representation could drift from V1 contract serialization
- typed normalization could be mistaken for evaluator relaxation

## Claim Boundaries

- No training, prediction rerun, data mutation, evaluator relaxation, schema migration, or runtime migration occurred.
- Alias-key evidence is diagnostic only and does not repair strict matches.
- The report explains existing recovered Control/Treatment outputs only.
