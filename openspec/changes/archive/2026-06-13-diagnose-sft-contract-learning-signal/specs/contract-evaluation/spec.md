## ADDED Requirements

### Requirement: Publish SFT contract learning-signal evidence
The system SHALL publish a public-safe evidence pack for SFT contract learning-signal diagnostics that links local inspection results to prior repair evidence and claim boundaries.

#### Scenario: Generate learning-signal evidence pack
- **WHEN** the diagnostic completes in local mode
- **THEN** it MUST write machine-readable JSON and human-readable Markdown that include evidence kind, source manifest, inspected row counts, split/task summaries, target-span status, target-pressure summaries, prior repair metrics, evidence gaps, claims, and recommended next step

#### Scenario: Keep learning-signal evidence public-safe
- **WHEN** learning-signal evidence is prepared for commit
- **THEN** leak-scan validation MUST reject raw private rows, local or remote private paths, secrets, private IP addresses, SSH details, raw logs, checkpoints, adapters, caches, oversized generated corpora, and private remote paths

#### Scenario: Bound learning-signal interpretation
- **WHEN** public reports or Human Briefs describe the learning-signal diagnostic
- **THEN** they MUST state that the evidence does not prove model recovery, held-out generalization, private-corpus generalization, checkpoint release, adapter release, production readiness, public full-corpus release, or live-browser benchmark improvement
