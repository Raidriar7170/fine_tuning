## ADDED Requirements

### Requirement: Observe restored-adapter hardened canonical policy rerun
The system SHALL run the hardened canonical policy rerun as prediction-only
after the required merged slot-value adapter is restored.

#### Scenario: Use restored adapter without training
- **WHEN** the observed hardened canonical policy rerun is executed
- **THEN** it MUST reuse the `a100-merged-slot-value-heldout-eval` adapter
- **AND** it MUST NOT run SFT, DPO, GRPO, adapter continuation training, or model
  merge
- **AND** it MUST run train/dev/test prediction-only configs.

#### Scenario: Require hardened prompt metadata
- **WHEN** observed rerun metrics are interpreted
- **THEN** prediction metadata for train/dev/test MUST show hardened canonical
  prompt-policy flags
- **AND** missing flags MUST prevent recovery claims even if exact-match metrics
  improve.
