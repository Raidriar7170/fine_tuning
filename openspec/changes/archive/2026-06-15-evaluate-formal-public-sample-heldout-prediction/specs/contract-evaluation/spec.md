## ADDED Requirements

### Requirement: Publish formal public sample held-out prediction evidence
The system SHALL publish public-safe prediction-only evidence for formal public sample dev/test rows after the formal sample manifest changes.

#### Scenario: Evaluate current formal public sample predictions
- **WHEN** sanitized private-adapter predictions are available for the current formal public sample dev and test splits
- **THEN** the system MUST evaluate them with the existing strict contract ladder, including `json_valid_rate`, `task_type_accuracy`, `route_accuracy`, `safety_precision`, `safety_recall`, `confirmation_accuracy`, `slot_f1`, `slot_f1_soft`, and `contract_exact_match`
- **AND** the evidence MUST record the current manifest id and split row counts used for evaluation

#### Scenario: Preserve prediction-only boundary
- **WHEN** formal public sample held-out prediction evidence is generated
- **THEN** the evidence MUST state that no SFT training, DPO training, dataset mutation, evaluator relaxation, semantic-equivalence scoring, slot normalization, prediction repair, prediction replacement, or prediction re-score was performed
- **AND** it MUST NOT claim held-out recovery, model recovery, checkpoint release, adapter release, production readiness, public full-corpus release, private-corpus generalization, or live-browser benchmark improvement

#### Scenario: Record blocked prediction execution safely
- **WHEN** the current formal public sample prediction run cannot safely execute because the private adapter, remote dependency, or idle GPU state is unavailable
- **THEN** the evidence MUST record a blocked status without writing fabricated predictions or model-quality metrics
- **AND** committed artifacts MUST omit raw logs, host details, SSH details, private paths, checkpoints, adapters, caches, tokens, and private corpus rows

#### Scenario: Validate public evidence boundaries
- **WHEN** formal public sample held-out prediction artifacts are prepared for commit
- **THEN** leak-scan validation MUST reject raw private rows, absolute local paths, private remote paths, host details, SSH details, secrets, tokens, raw logs, checkpoints, adapters, caches, and oversized generated corpora
