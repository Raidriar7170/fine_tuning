## ADDED Requirements

### Requirement: Publish extract-price residual repair evidence
The system SHALL publish public-safe evidence for the extract-price contract residual repair phase that separates strict train-split recovery from held-out or production claims.

#### Scenario: Generate extract residual evidence pack
- **WHEN** extract-price residual rerun predictions, metrics, prompt snapshot, prediction metadata, raw decoded summary, generation trace, residual diagnosis, and leak-scan results are available
- **THEN** the manifest and report MUST link those sanitized artifacts and record `prediction_split=train`, `overfit_diagnostic=true`, `generalization_claim=false`, prediction source kind, release status, extract-price strict exact-match status, compact-query preservation status, and claim boundaries

#### Scenario: Report extract residual families
- **WHEN** the extract residual report is generated from real private-adapter train-split predictions
- **THEN** it MUST state whether extract-price rows failed by task type, route, slots, normalized command, safety, confirmation, schema validity, or exact-match mismatch
- **AND** it MUST compare those residuals with the prior compact-query rerun without treating before/after differences as held-out generalization

#### Scenario: Keep evidence public-safe
- **WHEN** extract residual evidence is prepared for commit
- **THEN** leak-scan validation MUST reject raw private rows, local or remote private paths, secrets, private IP addresses, SSH details, raw logs, checkpoints, adapters, caches, oversized generated corpora, and private remote paths

#### Scenario: Bound extract repair interpretation
- **WHEN** public documentation or Human Briefs describe the extract residual repair result
- **THEN** they MUST state that train-split public-sample evidence does not prove dev/test generalization, production readiness, checkpoint release, adapter release, public full-corpus release, or live-browser benchmark improvement
