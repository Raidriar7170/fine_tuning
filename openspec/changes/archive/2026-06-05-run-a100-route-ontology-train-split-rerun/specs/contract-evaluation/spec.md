## ADDED Requirements

### Requirement: Publish route-ontology A100 train-split rerun evidence
The system SHALL publish a public-safe evidence pack for the route-ontology A100 train-split prediction rerun that separates raw attempt schema validity, retry attempt schema validity, validated output source, parse statuses, route validity, prompt constraints, and final contract metrics.

#### Scenario: Import sanitized route-ontology rerun evidence
- **WHEN** route-ontology prediction metadata, predictions, prompt snapshot, sanitized raw decoded summary, generation trace, metrics, schema guard summary, route-ontology diagnosis, and leak-scan results are available
- **THEN** the committed evidence MUST contain only public-safe artifacts and MUST omit private override files, raw private logs, private paths, host details, checkpoints, adapters, model caches, tokens, and private corpus rows

#### Scenario: Report route-ontology rerun status
- **WHEN** the route-ontology rerun report is generated from real private-adapter train-split predictions
- **THEN** it MUST report prediction count, raw attempt schema-valid count, retry attempt schema-valid count, validated output schema-valid count, route-valid count, invalid route values, validated output source distribution, parse status distribution, route ontology prompt constraints present at prediction time, and final contract metrics separately

#### Scenario: Compare only against the constrained-output baseline
- **WHEN** the report compares this rerun to prior evidence
- **THEN** it MUST identify `reports/public-sample/a100-constrained-output-train-split-rerun/` as pre-route-ontology-repair context and MUST NOT treat any before/after difference as held-out generalization, checkpoint release, adapter release, production readiness, public full-corpus release, or live-browser benchmark improvement

#### Scenario: Keep route-ontology rerun evidence public-safe
- **WHEN** evidence, Human Briefs, loop reports, or archived OpenSpec artifacts are prepared for commit
- **THEN** leak-scan validation MUST reject raw private rows, local or remote private paths, secrets, private IP addresses, SSH details, raw logs, checkpoints, adapters, model caches, oversized generated corpora, and private remote paths

#### Scenario: Bound route-ontology rerun interpretation
- **WHEN** public documentation, metrics reports, Human Briefs, or loop reports describe the route-ontology rerun
- **THEN** they MUST state that train-split prediction-only evidence does not prove dev/test generalization, production readiness, checkpoint release, adapter release, public full-corpus release, A100 model recovery, or live-browser benchmark improvement
