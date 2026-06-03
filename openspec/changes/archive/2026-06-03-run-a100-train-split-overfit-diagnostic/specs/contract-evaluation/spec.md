## ADDED Requirements

### Requirement: Publish observed A100 train-split diagnostic result
The system SHALL publish a public-safe observed A100 train-split diagnostic evidence pack that records whether train-internal schema, route, slot, safety, and confirmation recovery was observed without claiming held-out generalization or release status.

#### Scenario: Import sanitized diagnostic evidence
- **WHEN** real train-split diagnostic predictions, metrics, objective inspection, prompt snapshot, sanitized raw decoded summary, generation trace, and leak-scan results are available
- **THEN** the manifest and report MUST link those sanitized artifacts, record `prediction_split=train`, `overfit_diagnostic=true`, `generalization_claim=false`, prediction source kind, release status, and claim boundaries without private runtime details

#### Scenario: Report observed recovery status
- **WHEN** the diagnostic report is generated from real private-adapter train-split predictions
- **THEN** it MUST state whether train-internal schema validity, route correctness, slot shape, safety decision, and confirmation behavior recovered, remained partial, or failed using observed metrics and failure slices

#### Scenario: Keep diagnostic evidence public-safe
- **WHEN** diagnostic evidence is prepared for commit
- **THEN** leak-scan validation MUST reject raw private rows, local or remote private paths, secrets, private IP addresses, SSH details, raw logs, checkpoints, adapters, caches, oversized generated corpora, and private remote paths

#### Scenario: Bound diagnostic interpretation
- **WHEN** public documentation or Human Briefs describe the diagnostic result
- **THEN** they MUST state that train-split overfit evidence does not prove dev/test generalization, production readiness, checkpoint release, adapter release, public full-corpus release, or live-browser benchmark improvement
