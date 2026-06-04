## ADDED Requirements

### Requirement: Publish assistant-only A100 train-split rerun evidence
The system SHALL publish a public-safe evidence pack for the assistant-only A100 train-split rerun that records objective-mask status, train-internal contract metrics, comparison context, and non-claim boundaries without exposing private infrastructure or unreleased model artifacts.

#### Scenario: Import sanitized rerun evidence
- **WHEN** assistant-only rerun adapter metadata, objective/runtime label metadata, predictions, prediction metadata, prompt snapshot, sanitized raw decoded summary, generation trace, metrics, and leak-scan results are available
- **THEN** the manifest and report MUST link those sanitized artifacts, record `prediction_split=train`, `overfit_diagnostic=true`, `generalization_claim=false`, prediction source kind, release status, loss-mask policy, and claim boundaries without private runtime details

#### Scenario: Report observed recovery status after objective repair
- **WHEN** the assistant-only rerun report is generated from real private-adapter train-split predictions
- **THEN** it MUST state whether train-internal schema validity, route correctness, slot shape, safety decision, and confirmation behavior recovered, remained partial, or failed using observed metrics and failure slices

#### Scenario: Compare against prior train-split diagnostic narrowly
- **WHEN** the rerun evidence references prior A100 train-split evidence
- **THEN** it MUST identify the prior evidence as pre-assistant-only-objective-repair context and MUST NOT treat a before/after difference as held-out generalization, checkpoint release, adapter release, production readiness, or live-browser benchmark improvement

#### Scenario: Keep rerun evidence public-safe
- **WHEN** assistant-only rerun evidence is prepared for commit
- **THEN** leak-scan validation MUST reject raw private rows, local or remote private paths, secrets, private IP addresses, SSH details, raw logs, checkpoints, adapters, model caches, oversized generated corpora, and private remote paths

#### Scenario: Bound rerun interpretation
- **WHEN** public documentation, metrics reports, Human Briefs, or loop reports describe the assistant-only rerun
- **THEN** they MUST state that train-split overfit evidence does not prove dev/test generalization, production readiness, checkpoint release, adapter release, public full-corpus release, or live-browser benchmark improvement
