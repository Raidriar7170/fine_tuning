## ADDED Requirements

### Requirement: Run A100 post-recovery public-sample SFT rerun
The system SHALL support a bounded A100 post-recovery public-sample SFT rerun that uses the recovered contract-only chat formatting policy and keeps all remote model artifacts private.

#### Scenario: Launch post-recovery SFT rerun with recovered formatting
- **WHEN** a developer launches the post-recovery A100 SFT rerun with an explicit training opt-in and a private config rooted under the approved A100 project directory
- **THEN** the system trains on the committed public-sample SFT rows using the shared contract-only SFT training text policy and records formatting policy, model source, dataset manifest ID, package versions, GPU selection policy, command summary, and release status using public-safe placeholders

#### Scenario: Rerun private adapter prediction after recovery
- **WHEN** the post-recovery SFT adapter is used for private-adapter public-sample prediction
- **THEN** the system generates sanitized public-sample prediction rows with the shared contract-only prediction prompt policy and records `prediction_source_kind=private_a100_adapter` without copying adapters, checkpoints, raw logs, remote caches, host details, SSH details, secrets, or private paths into git

#### Scenario: Preserve rerun failures honestly
- **WHEN** the post-recovery private adapter emits invalid JSON, non-contract JSON, or malformed text
- **THEN** the prediction artifact preserves the sanitized model output as a schema-failure candidate rather than substituting fixture-mode, rule-baseline, or gold-contract predictions
