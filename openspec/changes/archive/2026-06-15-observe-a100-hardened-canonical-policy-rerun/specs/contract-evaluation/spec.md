## ADDED Requirements

### Requirement: Publish observed hardened canonical policy rerun evidence
The system SHALL publish public-safe observed rerun evidence without overwriting
the earlier blocked evidence directory.

#### Scenario: Preserve blocked evidence traceability
- **WHEN** the restored-adapter observed rerun report is generated
- **THEN** it MUST use a distinct public report directory from the earlier
  blocked rerun evidence
- **AND** diagnostic artifact paths MUST point at the requested observed output
  directory.

#### Scenario: Bound observed rerun claims
- **WHEN** the observed rerun evidence is published
- **THEN** it MAY report public-sample train/dev/test strict contract metrics,
  prompt-policy flags, residual rows, and comparison to prior merged evidence
- **AND** it MUST state that the phase is prediction-only and does not train,
  repair, normalize, or re-score predictions
- **AND** it MUST NOT claim model recovery, private-corpus generalization,
  production readiness, adapter release, checkpoint release, or live-browser
  benchmark improvement.
