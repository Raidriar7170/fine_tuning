## ADDED Requirements

### Requirement: Publish observed A100 candidate probe evidence safely
The system SHALL publish a public-safe evidence pack for observed or blocked A100 slot value candidate SFT probe execution.

#### Scenario: Report observed candidate SFT status
- **WHEN** A100 candidate SFT execution is attempted
- **THEN** the evidence MUST record sanitized remote preflight, dependency status, selected GPU label, training status, selected candidate row counts, and artifact policy
- **AND** it MUST omit raw logs, adapters, checkpoints, host details, SSH details, private paths, tokens, private overrides, and model caches

#### Scenario: Report candidate train-split prediction status
- **WHEN** train-split candidate prediction is attempted after candidate SFT
- **THEN** the evidence MUST record prediction status, split, row count, metric links when available, and non-claim boundaries using public-safe values
- **AND** if prediction is skipped or blocked, the evidence MUST state the reason without implying model recovery

#### Scenario: Preserve formal public sample boundary
- **WHEN** observed A100 candidate probe evidence is generated
- **THEN** it MUST state `formal_public_sample_modified=false`
- **AND** it MUST NOT rewrite formal public sample seed, SFT, DPO, or manifest files

#### Scenario: Bound observed candidate probe interpretation
- **WHEN** public documentation or Human Briefs describe observed candidate probe evidence
- **THEN** they MUST state that candidate train-split evidence does not prove held-out generalization, private-corpus generalization, checkpoint release, adapter release, production readiness, public full-corpus release, or live-browser benchmark improvement
