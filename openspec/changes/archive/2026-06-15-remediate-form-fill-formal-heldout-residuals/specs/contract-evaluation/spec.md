## ADDED Requirements

### Requirement: Publish form-fill remediation plan diagnosis
The system SHALL publish a public-safe, plan-only diagnosis for the selected
formal held-out `form_fill` residual target before any data generation,
training, DPO, prediction rerun, gold-policy change, or evaluator change.

#### Scenario: Validate source target selection
- **WHEN** the diagnosis is generated from formal held-out remediation target
  selection evidence
- **THEN** it MUST fail rather than publish if the selected target is not
  `form_fill`
- **AND** it MUST preserve the source selection residual row and field counts

#### Scenario: Classify remediation buckets
- **WHEN** `form_fill` residual rows are available
- **THEN** the diagnosis MUST classify residuals into remediation buckets for
  confirmation marker drift, field-name specificity drift, clarify-boundary
  confusion, and any remaining strict drift
- **AND** it MUST include counts by bucket, field path, split, and source family

#### Scenario: Recommend only bounded follow-up
- **WHEN** remediation buckets are summarized
- **THEN** the diagnosis MUST recommend a bounded follow-up phase and acceptance
  boundary
- **AND** it MUST NOT automatically generate data, change prompts, change gold
  labels, launch training, launch DPO, launch A100 prediction, or change
  evaluator behavior

#### Scenario: Preserve public-safe strict metric boundaries
- **WHEN** the diagnosis is written to public-sample reports
- **THEN** it MUST omit private paths, host details, SSH details, secrets,
  checkpoints, adapters, raw logs, and private corpus rows
- **AND** it MUST keep strict `contract_exact_match` and strict `slot_f1` as the
  primary metrics
- **AND** `slot_f1_soft` MUST remain diagnostic-only and MUST NOT be used as a
  semantic-equivalence primary metric
