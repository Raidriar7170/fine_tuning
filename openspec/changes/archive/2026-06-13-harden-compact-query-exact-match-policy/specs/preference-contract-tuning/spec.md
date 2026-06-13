## ADDED Requirements

### Requirement: Validate wrong-task-type hard negatives
The system SHALL verify that `wrong_task_type` DPO hard negatives actually change the rejected contract task type.

#### Scenario: Reject mislabeled wrong-task-type pairs
- **WHEN** a DPO pair is labeled `wrong_task_type`
- **THEN** the rejected contract MUST have a different `task_type` from the chosen contract
- **AND** validation MUST fail if only other fields such as `safety.reason` changed

#### Scenario: Summarize wrong-task-type slice
- **WHEN** DPO slice summaries are generated
- **THEN** `wrong_task_type` pairs MUST be counted in the task-type rejection slice
