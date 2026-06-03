## ADDED Requirements

### Requirement: Publish public-safe contract-output recovery evidence
The system SHALL publish a public-safe recovery evidence pack for A100 SFT contract-output recovery that records schema-failure diagnosis, rerun metrics when available, controlled smoke status, leak-scan status, and claim boundaries without exposing private infrastructure or unreleased model artifacts.

#### Scenario: Record pre-recovery failure evidence
- **WHEN** the recovery evidence pack is generated from the previous trained-path prediction/evaluation smoke
- **THEN** it records the prior schema failure count, JSON validity rate, prediction source kind, dataset manifest ID, and report links without copying raw private logs, checkpoints, adapters, caches, host details, or private paths

#### Scenario: Compare post-rerun metrics
- **WHEN** sanitized post-recovery public-sample predictions and metrics are available
- **THEN** the evidence pack reports post-rerun contract metrics and controlled smoke status alongside the pre-recovery baseline while labeling the result as a public-sample recovery smoke

#### Scenario: Keep recovery claims bounded
- **WHEN** the public recovery report describes the phase
- **THEN** it states that results are schema/contract-level public-sample evidence only and makes no checkpoint release, production-readiness, full-private-corpus, or live-browser benchmark improvement claim

#### Scenario: Validate recovery evidence boundaries
- **WHEN** the recovery evidence pack is prepared for commit
- **THEN** leak-scan validation rejects raw private rows, local absolute paths, secrets, tokens, private IP addresses, SSH details, raw logs, checkpoints, adapters, caches, and oversized generated corpora
