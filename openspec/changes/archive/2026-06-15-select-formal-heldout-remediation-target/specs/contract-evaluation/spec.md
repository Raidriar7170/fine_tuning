## ADDED Requirements

### Requirement: Publish formal held-out remediation target selection
The system SHALL publish a public-safe remediation target selection report from
the formal held-out residual-family diagnosis before any new data generation,
training, DPO, prediction rerun, evaluator change, or gold-policy change.

#### Scenario: Rank residual task families
- **WHEN** a committed formal held-out residual-family diagnosis is available
- **THEN** the target selection report MUST rank task families by affected
  strict residual row count and include residual field counts for each family
- **AND** it MUST identify the source diagnosis artifact and preserve source
  residual count consistency

#### Scenario: Select one first remediation target
- **WHEN** task-family rankings are computed
- **THEN** the report MUST select exactly one first remediation target
- **AND** it MUST explain why that target is first, why adjacent high-risk
  families are deferred, and what bounded follow-up OpenSpec phase is
  recommended

#### Scenario: Preserve evidence and metric boundaries
- **WHEN** the report references strict exact match, strict slot F1, or
  `slot_f1_soft`
- **THEN** strict `contract_exact_match` and strict `slot_f1` MUST remain the
  primary metrics
- **AND** `slot_f1_soft` MUST remain diagnostic-only
- **AND** the report MUST NOT claim model recovery, production readiness,
  semantic-equivalence scoring, adapter release, checkpoint release, private
  corpus generalization, public full-corpus release, or live-browser benchmark
  improvement

#### Scenario: Keep artifacts public-safe
- **WHEN** the report is written under `reports/public-sample`
- **THEN** it MUST omit private paths, host details, SSH details, secrets,
  checkpoints, adapters, raw logs, and private corpus rows
- **AND** it MUST use sanitized summaries rather than copying raw prediction
  streams as the planning artifact
