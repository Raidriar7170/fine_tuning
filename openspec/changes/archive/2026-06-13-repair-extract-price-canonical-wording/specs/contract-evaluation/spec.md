## ADDED Requirements

### Requirement: Publish extract-price canonical wording rerun evidence
The system SHALL publish public-safe evidence for the extract-price canonical wording rerun that separates strict train-split recovery from held-out or production claims.

#### Scenario: Generate canonical wording evidence pack
- **WHEN** canonical wording rerun predictions, metrics, prompt snapshot, prediction metadata, raw decoded summary, generation trace, residual diagnosis, manifest, report, Human Brief, and leak-scan results are available
- **THEN** the manifest and report MUST link those sanitized artifacts and record `prediction_split=train`, `overfit_diagnostic=true`, `generalization_claim=false`, prediction source kind, release status, canonical target exact status, canonical normalized-command exact status, compact-query preservation status, and claim boundaries

#### Scenario: Report canonical wording residual families
- **WHEN** the canonical wording report is generated from real private-adapter train-split predictions
- **THEN** it MUST state whether extract-price rows failed by `slots.target`, `normalized_command`, task type, route, safety, confirmation, schema validity, or exact-match mismatch
- **AND** it MUST compare those residuals with the prior extract-price residual rerun without treating before/after differences as held-out generalization

#### Scenario: Keep canonical wording evidence public-safe
- **WHEN** canonical wording evidence is prepared for commit
- **THEN** leak-scan validation MUST reject raw private rows, local or remote private paths, secrets, private IP addresses, SSH details, raw logs, checkpoints, adapters, caches, oversized generated corpora, and private remote paths

#### Scenario: Bound canonical wording interpretation
- **WHEN** public documentation or Human Briefs describe the canonical wording result
- **THEN** they MUST state that train-split public-sample evidence does not prove dev/test generalization, production readiness, checkpoint release, adapter release, public full-corpus release, or live-browser benchmark improvement
