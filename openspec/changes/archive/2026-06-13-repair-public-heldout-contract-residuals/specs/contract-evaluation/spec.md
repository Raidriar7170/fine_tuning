## ADDED Requirements

### Requirement: Publish public held-out residual repair evidence
The system SHALL publish public-safe evidence for the held-out residual repair rerun that reports train, dev, and test metrics separately and bounds interpretation.

#### Scenario: Generate repair evidence pack
- **WHEN** sanitized repair rerun predictions and sidecars are available for train, dev, and test
- **THEN** the evidence pack MUST include split-specific predictions, gold rows, strict metrics, schema diagnostics, alignment diagnostics, constrained decoding diagnostics, prompt snapshots, raw decoded summaries, generation traces, and prediction metadata

#### Scenario: Report repair interpretation
- **WHEN** the combined repair manifest and report are generated
- **THEN** they MUST record row counts, `contract_exact_match`, `slot_f1`, schema validity, residual rows, prompt-policy visibility, and artifact links per split
- **AND** they MUST identify whether public held-out strict contract behavior recovered, remained partial, or failed

#### Scenario: Bound repair claims
- **WHEN** public documentation or Human Briefs describe the repair result
- **THEN** they MUST state that public-sample train/dev/test evidence does not prove private-corpus generalization, checkpoint release, adapter release, production readiness, public full-corpus release, or live-browser benchmark improvement

#### Scenario: Validate repair evidence boundaries
- **WHEN** repair evidence is prepared for commit
- **THEN** leak-scan validation MUST reject raw private rows, local or remote private paths, secrets, private IP addresses, SSH details, raw logs, checkpoints, adapters, caches, oversized generated corpora, and private remote paths
