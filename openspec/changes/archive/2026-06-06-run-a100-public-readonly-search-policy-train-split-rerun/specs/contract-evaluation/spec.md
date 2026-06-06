## ADDED Requirements

### Requirement: Publish public-readonly search policy A100 rerun evidence
The system SHALL publish public-safe train-split evidence for the public-readonly search policy A100 rerun that separates strict final metrics from row-level task type, route, safety, confirmation, slot, normalized-command, and schema observations while preserving non-claim boundaries.

#### Scenario: Generate public-readonly search rerun manifest
- **WHEN** train-split rerun predictions, metrics, prompt snapshot, raw decoded summary, generation trace, row-level diagnosis, schema guard summary, and leak-scan results are available
- **THEN** the manifest MUST record `prediction_source_kind=private_a100_adapter`, `prediction_split=train`, `overfit_diagnostic=true`, `generalization_claim=false`, strict metric values, row-level field counts, and claim boundaries without private paths or host details

#### Scenario: Report public-readonly search field diagnosis
- **WHEN** a public-readonly search policy diagnosis is generated for the rerun
- **THEN** it MUST report per-row gold/predicted field summaries, exact field match status for `task_type`, `route`, `safety.reason`, `confirmation_required`, `slots`, and `normalized_command`, aggregate field counts, family counts, and whether the row was otherwise schema-valid without normalizing or re-scoring predictions

#### Scenario: Compare against prior A100 baseline narrowly
- **WHEN** the public report describes the rerun result
- **THEN** it MUST compare only against `reports/public-sample/a100-normalized-command-policy-train-split-rerun/` for train-split prediction-only evidence and MUST NOT present the comparison as dev/test generalization or model-quality improvement

#### Scenario: Validate public-readonly search rerun evidence boundaries
- **WHEN** the evidence pack is prepared for commit
- **THEN** leak-scan validation MUST reject raw private rows, local or remote private paths, secrets, private IP addresses, SSH details, raw logs, checkpoints, adapters, caches, oversized generated corpora, and private remote paths

#### Scenario: Bound public-readonly search rerun interpretation
- **WHEN** public documentation or Human Briefs describe the public-readonly search policy rerun
- **THEN** they MUST state that the phase performs no training, checkpoint release, adapter release, evaluator metric change, semantic-equivalence scoring, slot normalization, prediction repair, prediction re-score, production-readiness claim, held-out generalization claim, public full-corpus release, model-quality claim, or live-browser benchmark improvement claim
