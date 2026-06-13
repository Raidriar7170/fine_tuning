## ADDED Requirements

### Requirement: Run bounded current-manifest runtime label check
The system SHALL support a bounded runtime label provenance check for the current public SFT manifest without starting training, prediction, adapter loading, or broad model experimentation.

#### Scenario: Execute current-manifest runtime label check
- **WHEN** the current public manifest is selected for runtime label provenance inspection
- **THEN** the runtime check MUST inspect only public train-split SFT rows, use explicit runtime opt-in, require private override resolution under the approved private project root when remote execution is needed, and write only sanitized metadata intended for public evidence

#### Scenario: Avoid training and prediction side effects
- **WHEN** the current-manifest runtime label check runs
- **THEN** it MUST NOT train SFT, run DPO, run GRPO, export predictions, load a private adapter, copy checkpoints or adapters into git, or download public model snapshots into the repository

#### Scenario: Preserve next-step boundary
- **WHEN** the current-manifest runtime label check finishes
- **THEN** the result MUST recommend tiny-overfit only as a separate later phase when labels are fresh, inspectable, and assistant-only; otherwise it MUST recommend fixing the concrete label-path gap first
