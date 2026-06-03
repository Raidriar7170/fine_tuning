## ADDED Requirements

### Requirement: Diagnose training-prompt-decoding source alignment
The system SHALL provide public-safe diagnostics that connect Browser Task Contract schema-invalid prediction symptoms to training targets, prompt constraints, split coverage, prediction shape, and decoding evidence availability.

#### Scenario: Audit targets and prediction symptoms
- **WHEN** diagnostics are generated for public-sample gold rows and contract-like private-adapter predictions
- **THEN** the output MUST report whether gold targets contain path-like routes or list-shaped slots, whether predictions contain path-like routes or list-shaped slots, and whether invalid predictions remain invalid

#### Scenario: Audit prompt and split coverage
- **WHEN** diagnostics are generated with SFT training configuration and prediction metadata
- **THEN** the output MUST report the configured training split, prediction split, training row count, training route/task-type coverage, and whether the visible prompt includes enum and slots-object constraints

#### Scenario: Audit decoding evidence boundaries
- **WHEN** diagnostics are generated for existing prediction metadata
- **THEN** the output MUST report decoding policy fields that are present and MUST record missing raw decoded sidecar, generated-token count, EOS, or finish-state evidence as evidence gaps rather than inferred causes

#### Scenario: Bound source-diagnostic claims
- **WHEN** source diagnostics are generated for private-adapter public-sample predictions
- **THEN** the report MUST state that it does not repair, normalize, coerce, or replace predictions and MUST NOT claim checkpoint release, adapter release, production readiness, full-private-corpus release, or live-browser benchmark improvement
