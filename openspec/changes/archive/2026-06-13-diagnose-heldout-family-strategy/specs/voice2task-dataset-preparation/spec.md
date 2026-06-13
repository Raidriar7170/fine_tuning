## ADDED Requirements

### Requirement: Diagnose public-sample family coverage before scaling data
The system SHALL support a local public-sample coverage diagnosis that informs
whether the next data step should be targeted family coverage instead of broad
data scaling.

#### Scenario: Compare train coverage with held-out families
- **WHEN** the public sample contains train, dev, and test rows
- **THEN** the diagnosis MUST summarize coverage by source family, task type, route, safety reason, confirmation behavior, and slot keys for each split
- **AND** it MUST identify held-out families that appear in train at dataset level but were absent from the actual tiny-adapter training subset

#### Scenario: Preserve data-generation boundary
- **WHEN** coverage gaps are reported
- **THEN** the diagnosis MUST NOT create new public rows, mutate seed traces, mutate SFT/DPO rows, or change the public manifest
