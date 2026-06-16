## ADDED Requirements

### Requirement: Publish formal held-out residual cluster inspection
The system SHALL publish public-safe residual-cluster inspection evidence derived only from committed formal public held-out evidence before recommending data, training, or evaluator changes.

#### Scenario: Inspect current residual clusters
- **WHEN** residual-cluster inspection is generated for the current formal public held-out evidence
- **THEN** the evidence MUST record the source manifest id, strict contract metrics, strict slot metrics, residual row counts, and source residual diagnosis links
- **AND** it MUST group residuals by split, task family, field path, mismatch category, source family, and representative examples

#### Scenario: Preserve analysis-only boundaries
- **WHEN** residual-cluster inspection evidence is generated
- **THEN** the evidence MUST state that no prediction run, SFT training, DPO training, GRPO training, dataset mutation, evaluator relaxation, semantic-equivalence scoring, prediction repair, prediction replacement, or prediction re-score occurred
- **AND** strict `contract_exact_match`, strict `slot_f1`, and the contract evaluation ladder MUST remain authoritative
- **AND** `slot_f1_soft` MUST remain an internal diagnostic only

#### Scenario: Bound recommended next actions
- **WHEN** the residual-cluster inspection recommends follow-up work
- **THEN** recommendations MUST be labeled as candidates derived from observed cluster evidence
- **AND** they MUST NOT mutate data, training, prompts, evaluator semantics, predictions, checkpoints, or adapter release status in the same phase
- **AND** they MUST NOT claim held-out recovery, model recovery, production readiness, private-corpus generalization, public full-corpus release, or live-browser benchmark improvement

#### Scenario: Validate cluster evidence boundaries
- **WHEN** residual-cluster inspection artifacts are prepared for commit
- **THEN** leak-scan validation MUST reject raw private rows, absolute local paths, private remote paths, host details, SSH details, secrets, tokens, raw logs, checkpoints, adapters, caches, and oversized generated corpora
