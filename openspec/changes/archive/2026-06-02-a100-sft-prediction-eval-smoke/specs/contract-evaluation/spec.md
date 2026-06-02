## ADDED Requirements

### Requirement: Publish sanitized A100 trained-prediction evidence
The system SHALL produce a public-safe A100 trained-prediction evidence pack that reports sanitized predictions, contract metrics, controlled smoke status, and leak-scan results without exposing private infrastructure or unreleased model artifacts.

#### Scenario: Generate trained-prediction evidence report
- **WHEN** sanitized trained-path public-sample predictions are available
- **THEN** the system writes a machine-readable run manifest and a human-readable report that link the prediction artifact, base model, dataset manifest ID, metrics path, controlled smoke result, leak-scan result, and release status without claiming a public checkpoint

#### Scenario: Validate trained-prediction evidence boundaries
- **WHEN** the trained-prediction evidence pack is prepared for commit
- **THEN** leak-scan validation rejects raw private rows, local absolute paths, secrets, tokens, private IP addresses, SSH details, raw logs, checkpoints, adapters, caches, and oversized generated corpora

#### Scenario: Separate trained-prediction smoke from benchmark claims
- **WHEN** the public report describes trained-path prediction results
- **THEN** it labels the result as a public-sample prediction/evaluation smoke and separates contract metrics and controlled smoke from live-browser benchmark, production-readiness, or released-checkpoint claims
