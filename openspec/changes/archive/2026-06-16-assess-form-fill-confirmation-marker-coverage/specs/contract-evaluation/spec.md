## ADDED Requirements

### Requirement: Publish form-fill confirmation-marker coverage assessment
The system SHALL publish a public-safe coverage assessment that compares the current form-fill confirmation-marker policy evidence with existing form-fill remediation artifacts before any further confirmation-marker data, prompt, training, or evaluator remediation.

#### Scenario: Assess coverage from committed artifacts
- **WHEN** the confirmation-marker coverage assessment is generated
- **THEN** the evidence MUST record the source policy artifact, source case-design artifact, source materialization artifact when available, source merge or integration artifacts when available, source held-out evaluation artifacts when available, source manifest id, confirmation-marker policy counts, existing confirmation candidate counts, represented field labels, and source count consistency
- **AND** it MUST state whether the assessment reads only committed public-safe artifacts

#### Scenario: Preserve assessment-only boundaries
- **WHEN** confirmation-marker coverage evidence is generated
- **THEN** it MUST state that no new candidate rows, seed traces, public sample splits, SFT rows, DPO pairs, held-out gold labels, prompts, evaluator metrics, predictions, checkpoints, adapters, or training jobs were created or changed
- **AND** strict `contract_exact_match`, strict `slot_f1`, and the contract evaluation ladder MUST remain authoritative
- **AND** `slot_f1_soft` MUST remain diagnostic-only

#### Scenario: Bound coverage decision and next action
- **WHEN** the assessment recommends follow-up work
- **THEN** the recommendation MUST be labeled as a bounded next OpenSpec candidate derived from observed coverage signals
- **AND** it MUST NOT materialize data, change prompts, change evaluator semantics, repair predictions, launch training, or claim held-out recovery in the same phase

#### Scenario: Validate coverage artifact public safety
- **WHEN** confirmation-marker coverage artifacts are prepared for commit
- **THEN** leak-scan validation MUST reject raw private rows, absolute local paths, private remote paths, host details, SSH details, secrets, tokens, raw logs, checkpoints, adapters, caches, and oversized generated corpora
