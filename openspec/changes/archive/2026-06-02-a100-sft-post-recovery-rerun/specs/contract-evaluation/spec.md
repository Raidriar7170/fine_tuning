## ADDED Requirements

### Requirement: Publish post-recovery A100 rerun evidence
The system SHALL publish a public-safe post-recovery A100 rerun evidence pack that compares the rerun result with the pre-recovery trained-path schema-failure baseline without exposing private infrastructure or unreleased model artifacts.

#### Scenario: Record post-recovery prediction metrics
- **WHEN** sanitized post-recovery public-sample predictions are available
- **THEN** the evidence pack records prediction count, prediction source kind, dataset manifest ID, formatting policy, metrics path, JSON validity rate, schema failure count, and failure slices alongside links to the pre-recovery baseline

#### Scenario: Record post-recovery controlled smoke
- **WHEN** controlled execution smoke is run against the sanitized post-recovery predictions
- **THEN** the evidence pack records passed and failed counts, target fixture path, and notes that the result is a controlled public-sample smoke rather than a live-browser benchmark

#### Scenario: Validate post-recovery evidence boundaries
- **WHEN** the post-recovery evidence pack is prepared for commit
- **THEN** leak-scan validation rejects raw private rows, absolute local paths, secrets, tokens, private IP addresses, SSH details, raw logs, checkpoints, adapters, caches, oversized generated corpora, and private remote paths

#### Scenario: Bound post-recovery interpretation
- **WHEN** the public report describes the post-recovery rerun
- **THEN** it states whether schema validity improved, remained partial, or still failed using the observed metrics, and makes no checkpoint release, adapter release, full-private-corpus, production-readiness, or live-browser benchmark improvement claim
