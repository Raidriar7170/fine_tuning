## ADDED Requirements

### Requirement: Materialize form-fill remediation candidates separately

The system SHALL materialize reviewed `form_fill` remediation case groups into a public-safe candidate dataset that remains separate from the formal public sample until a later approved change merges or trains on it.

#### Scenario: Generate candidate seeds from reviewed form-fill design

- **WHEN** the form-fill remediation case-design artifact contains the reviewed case groups
- **THEN** the materializer MUST write public-safe candidate seed rows for the reviewed `form_fill` cases
- **AND** each candidate seed MUST use a schema-valid Browser Task Contract with the reviewed `slots.field` value
- **AND** each candidate seed MUST include provenance linking back to the source case group, case ID, residual bucket, and design artifact

#### Scenario: Preserve form-fill canonical confirmation policy

- **WHEN** a reviewed `form_fill` remediation case is materialized
- **THEN** its target contract MUST use `task_type="form_fill"`, `route="fill_form"`, `safety.reason="requires_confirmation"`, and `confirmation_required=true`
- **AND** its canonical `normalized_command` MUST use concise `填写...并确认` wording
- **AND** the materialization evidence MUST preserve the source expected normalized-command pattern for auditability

#### Scenario: Keep formal public sample unchanged

- **WHEN** form-fill remediation candidate materialization runs
- **THEN** it MUST NOT edit `data/public-samples/seed_traces.jsonl`, `sft_public_sample.jsonl`, `dpo_public_sample.jsonl`, or `manifest_public_sample.json`
- **AND** the materialization manifest MUST state `public_sample_modified=false`, `training_run=false`, `prediction_run=false`, `dpo_run=false`, `a100_execution=false`, and `evaluator_metric_change=false`

#### Scenario: Expand candidate SFT rows without DPO

- **WHEN** candidate seeds are materialized
- **THEN** the materializer MUST expand them into candidate SFT rows using the existing SFT row schema and original-row provenance
- **AND** it MUST NOT generate DPO pairs, hard negatives, schema-preserving augmentations, or training configs in this phase

#### Scenario: Preserve evaluation and claim boundaries

- **WHEN** materialized candidate artifacts, reports, or Human Briefs describe the phase
- **THEN** they MUST state that strict `contract_exact_match` remains the primary metric
- **AND** they MUST NOT claim held-out generalization recovery, model recovery, checkpoint release, adapter release, production readiness, private-corpus generalization, public full-corpus release, or live-browser benchmark improvement
