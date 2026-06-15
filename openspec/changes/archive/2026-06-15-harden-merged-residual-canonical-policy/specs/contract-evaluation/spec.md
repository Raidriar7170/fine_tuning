## ADDED Requirements

### Requirement: Publish merged residual canonical policy evidence
The system SHALL publish public-safe local evidence for merged residual
canonical policy hardening that links back to the merged residual diagnosis
without claiming model recovery.

#### Scenario: Generate local canonical policy evidence
- **WHEN** the merged residual canonical policy evidence pack is generated
- **THEN** it MUST record the source prior phase
  `reports/public-sample/merged-slot-value-residual-diagnosis/`
- **AND** it MUST report residual counts for ambiguous clarify canonical phrase
  drift and unsafe payment canonical command drift
- **AND** it MUST record prompt constraint flags for ambiguous-clarify canonical
  phrase visibility and unsafe-payment canonical command visibility

#### Scenario: Bound local canonical policy evidence claims
- **WHEN** reports, Human Briefs, loop reports, or archived OpenSpec artifacts
  describe this phase
- **THEN** they MUST state that it is local prompt/policy hardening only
- **AND** they MUST NOT claim A100 execution, training, prediction rerun,
  evaluator metric change, semantic-equivalence scoring, slot normalization,
  prediction repair, prediction re-score, checkpoint release, adapter release,
  held-out generalization recovery, production readiness, model-quality
  improvement, or live-browser benchmark improvement

#### Scenario: Keep canonical policy evidence public-safe
- **WHEN** the evidence pack is prepared for commit
- **THEN** leak-scan validation MUST reject raw private rows, local or remote
  private paths, secrets, private IP addresses, SSH details, raw logs,
  checkpoints, adapters, caches, oversized generated corpora, and private
  runtime paths
