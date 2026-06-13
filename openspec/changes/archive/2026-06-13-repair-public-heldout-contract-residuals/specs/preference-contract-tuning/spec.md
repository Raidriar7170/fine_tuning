## ADDED Requirements

### Requirement: Validate held-out residual repair hard negatives
The system SHALL validate held-out residual repair DPO pairs so mislabeled or weak pairs cannot silently enter preference data.

#### Scenario: Accept clarify action-drift negative
- **WHEN** a DPO pair is labeled as clarify action drift
- **THEN** the chosen contract MUST be a clarify contract with `route="clarify"`, `confirmation_required=true`, `safety.reason="ambiguous_request"`, and an `ambiguity` slot
- **AND** the rejected contract MUST change away from the clarify task or route

#### Scenario: Accept blocked payment action-drift negative
- **WHEN** a DPO pair is labeled as blocked payment action drift
- **THEN** the chosen contract MUST be a blocked deny contract with `safety.allow=false` and `safety.reason="unsafe_payment"`
- **AND** the rejected contract MUST either allow the request, change away from `route="deny"`, or change away from `task_type="blocked"`

#### Scenario: Accept form confirmation drift negative
- **WHEN** a DPO pair is labeled as form confirmation drift
- **THEN** the chosen contract MUST require confirmation with `task_type="form_fill"`, `route="fill_form"`, `safety.reason="requires_confirmation"`, and `slots.field`
- **AND** the rejected contract MUST differ in confirmation, safety reason, or accepted field slot shape

#### Scenario: Accept navigate canonical URL drift negative
- **WHEN** a DPO pair is labeled as navigate canonical URL drift
- **THEN** the chosen contract MUST be a public-readonly navigation contract with `route="open_url"` and `slots.url`
- **AND** the rejected contract MUST differ in URL slot value or navigation normalized command

#### Scenario: Summarize held-out residual repair slices
- **WHEN** DPO slice summaries are generated
- **THEN** clarify action drift MUST count in the task-type or underspecified slice, blocked payment action drift MUST count in the safety slice, form confirmation drift MUST count in the confirmation slice, and navigate canonical URL drift MUST count in the slot or normalized-command slice
