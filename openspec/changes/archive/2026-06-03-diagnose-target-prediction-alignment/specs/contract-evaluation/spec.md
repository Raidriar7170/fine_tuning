## ADDED Requirements

### Requirement: Diagnose target-prediction alignment mismatches
The system SHALL provide public-safe diagnostics that compare generated prediction fields with their gold Browser Task Contract targets, including when predictions are schema-invalid but contract-like.

#### Scenario: Compare raw prediction fields with gold targets
- **WHEN** the evaluator receives gold public-sample rows and prediction artifacts with matching row ids
- **THEN** the alignment diagnostic output MUST report aggregate mismatch counts by contract field path and row-level mismatches with row id, field path, gold value summary, prediction value summary, and mismatch category without converting invalid predictions into valid contracts

#### Scenario: Preserve invalid prediction status
- **WHEN** a prediction fails Browser Task Contract schema validation but contains comparable contract-like fields
- **THEN** alignment diagnostics MUST NOT repair, normalize, coerce, or count the prediction as schema-valid

#### Scenario: Bound alignment evidence claims
- **WHEN** alignment diagnostics are generated for private-adapter public-sample predictions
- **THEN** the report MUST state that the evidence is field-level public-sample analysis only and MUST NOT claim checkpoint release, adapter release, production readiness, full-private-corpus release, or live-browser benchmark improvement
