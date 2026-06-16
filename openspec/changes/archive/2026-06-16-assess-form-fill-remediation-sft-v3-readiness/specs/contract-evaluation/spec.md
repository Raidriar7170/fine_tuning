## ADDED Requirements

### Requirement: Keep readiness separate from model-quality evidence
The system SHALL keep SFT v3 readiness evidence separate from prediction-only
held-out metrics and later model-quality claims.

#### Scenario: Reference the current strict baseline
- **WHEN** readiness evidence is generated
- **THEN** it MUST reference the current formal prediction-only baseline manifest and strict metrics
- **AND** it MUST keep `contract_exact_match` and strict `slot_f1` as the public headline metrics
- **AND** it MUST keep `slot_f1_soft` diagnostic-only

#### Scenario: Avoid prediction or evaluator claims
- **WHEN** readiness evidence is published
- **THEN** it MUST state that no prediction rerun, prediction repair, prediction replacement, prediction re-score, slot normalization, semantic-equivalence scoring, or evaluator relaxation occurred
- **AND** it MUST recommend a later bounded phase for any SFT v3 execution and held-out prediction follow-up
