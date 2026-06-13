## ADDED Requirements

### Requirement: Publish held-out family strategy diagnosis
The system SHALL publish a public-safe local diagnosis that explains current
tiny-adapter held-out failures by task family, contract field, and training
subset coverage before another data, SFT, or DPO strategy is executed.

#### Scenario: Generate family-level strategy evidence
- **WHEN** current tiny-adapter held-out evidence and current public-sample rows are available
- **THEN** the diagnostic MUST report family-level train/dev/test coverage, tiny-adapter training subset coverage, held-out exact-match status, schema-invalid counts, field mismatch counts, and source-family residuals
- **AND** it MUST distinguish dataset-level train coverage from tiny-adapter subset coverage

#### Scenario: Recommend without executing strategy
- **WHEN** the diagnostic recommends a next strategy
- **THEN** the recommendation MUST identify whether the next bounded phase should investigate targeted SFT coverage, DPO hard negatives, prompt/policy adjustment, or local learning-signal evidence
- **AND** it MUST NOT generate new rows, train, run A100 prediction, change evaluator metrics, modify prompts, or execute DPO

#### Scenario: Bound strategy interpretation
- **WHEN** public documentation or Human Briefs describe the diagnosis
- **THEN** they MUST state that the diagnosis does not prove held-out generalization, model recovery, private-corpus generalization, checkpoint release, adapter release, production readiness, public full-corpus release, or live-browser benchmark improvement

#### Scenario: Validate strategy evidence boundaries
- **WHEN** held-out family strategy evidence is prepared for commit
- **THEN** leak-scan validation MUST reject raw private rows, local or remote private paths, secrets, private IP addresses, SSH details, raw logs, checkpoints, adapters, caches, oversized generated corpora, model snapshots, and private remote paths
