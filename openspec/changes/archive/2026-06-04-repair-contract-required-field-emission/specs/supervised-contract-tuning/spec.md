## ADDED Requirements

### Requirement: Strengthen required-field prediction prompt
The system SHALL render SFT training and prediction prompts with an explicit Browser Task Contract skeleton and required-field checklist covering `task_type`, `route`, `safety`, `confirmation_required`, `slots`, `normalized_command`, `language`, and `contract_version`.

#### Scenario: Prompt includes complete contract skeleton
- **WHEN** SFT training text or prediction prompts are rendered
- **THEN** the rendered prompt MUST include a complete top-level Browser Task Contract skeleton, MUST show that `safety` contains `allow` and `reason`, and MUST state that every required field must be present even when values are simple

#### Scenario: Prediction prompt avoids gold leakage
- **WHEN** a prediction prompt is rendered for an input row
- **THEN** it MUST include the required-field checklist and generation boundary without including the row's gold assistant contract

### Requirement: Guard private-adapter predictions with schema validation
The system SHALL validate each raw private-adapter prediction attempt against the Browser Task Contract schema before recording validated output status.

#### Scenario: Raw attempt is schema-invalid
- **WHEN** a raw private-adapter prediction attempt is parseable JSON but missing required Browser Task Contract fields
- **THEN** the system MUST record that the raw attempt is schema-invalid, MUST preserve the raw attempt, and MUST NOT count it as validated schema recovery

#### Scenario: Bounded retry is attempted
- **WHEN** schema retry is enabled and the raw attempt is schema-invalid
- **THEN** the system MUST attempt at most one retry with an explicit required-field repair prompt and MUST record retry status, retry schema validity, and whether validated output came from raw attempt, retry attempt, or no valid attempt

#### Scenario: Retry remains invalid
- **WHEN** both raw and retry attempts are schema-invalid
- **THEN** the system MUST preserve invalid outputs, emit `validated_output_schema_valid=false`, and keep the prediction as a schema failure
