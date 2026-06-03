## ADDED Requirements

### Requirement: Diagnose contract-like schema mismatches
The system SHALL provide public-safe diagnostics for generated predictions that are JSON or JSON-like but fail the Browser Task Contract schema.

#### Scenario: Contract-like prediction fails required fields and field constraints
- **WHEN** a prediction artifact contains objects with Browser Task Contract-like fields that fail required fields, enum values, field types, or non-empty string constraints
- **THEN** the diagnostic output MUST report the affected row id, field path, issue category, observed value summary, and expected contract constraint without converting the prediction into a valid contract

#### Scenario: Diagnostics preserve bounded evidence claims
- **WHEN** diagnostics are generated for private-adapter public-sample predictions
- **THEN** the report MUST state that invalid predictions remain invalid and MUST NOT claim checkpoint release, adapter release, production readiness, full-private-corpus release, or live-browser benchmark improvement
