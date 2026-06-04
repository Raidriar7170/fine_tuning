## ADDED Requirements

### Requirement: Publish required-field repair A100 rerun evidence
The system SHALL publish a public-safe evidence pack for the required-field repair A100 train-split rerun that separates raw attempt schema validity, retry attempt schema validity, validated output source, final contract metrics, and non-claim boundaries.

#### Scenario: Import sanitized rerun evidence
- **WHEN** rerun adapter metadata, objective/runtime label metadata, predictions, prediction metadata, prompt snapshot, sanitized raw decoded summary, generation trace, metrics, and leak-scan results are available
- **THEN** the manifest and report MUST link those sanitized artifacts, record `prediction_split=train`, `overfit_diagnostic=true`, `generalization_claim=false`, prediction source kind, release status, loss-mask policy, schema guard policy, and claim boundaries without private runtime details

#### Scenario: Report raw retry and validated outputs separately
- **WHEN** schema guard or retry metadata is available from rerun predictions
- **THEN** public reports and Human Briefs MUST separate raw attempt schema validity, retry attempt schema validity, validated output source, validated output schema validity, and final contract metrics

#### Scenario: Compare required-field repair narrowly
- **WHEN** the rerun evidence references prior assistant-only train-split evidence
- **THEN** it MUST identify the prior evidence as pre-required-field-repair context and MUST NOT treat any before/after difference as held-out generalization, checkpoint release, adapter release, production readiness, or live-browser benchmark improvement

#### Scenario: Keep rerun evidence public-safe
- **WHEN** required-field repair rerun evidence is prepared for commit
- **THEN** leak-scan validation MUST reject raw private rows, local or remote private paths, secrets, private IP addresses, SSH details, raw logs, checkpoints, adapters, model caches, oversized generated corpora, and private remote paths

#### Scenario: Bound rerun interpretation
- **WHEN** public documentation, metrics reports, Human Briefs, or loop reports describe the rerun
- **THEN** they MUST state that train-split overfit evidence does not prove dev/test generalization, production readiness, checkpoint release, adapter release, public full-corpus release, or live-browser benchmark improvement
