## ADDED Requirements

### Requirement: Run authorized A100 required-field repair train-split rerun
The system SHALL support a bounded, explicitly authorized A100 train-split rerun after required-field prompt and schema guard repair while keeping all private runtime artifacts outside committed files.

#### Scenario: Launch required-field repair rerun
- **WHEN** a developer launches the rerun with explicit heavy-training opt-in, a repo-external private override, and an idle A100 GPU under the approved private project root
- **THEN** the system MUST train only the public-sample train split through the current assistant-only SFT label path and required-field prompt skeleton

#### Scenario: Predict with schema guard and bounded retry
- **WHEN** the rerun adapter is used for train-split prediction
- **THEN** the system MUST use `prediction_split=train`, `overfit_diagnostic=true`, `generalization_claim=false`, and the current schema guard/retry prediction path

#### Scenario: Preserve raw and retry evidence
- **WHEN** a prediction attempt is generated
- **THEN** the system MUST preserve raw attempt schema validity, retry attempt schema validity, validated output source, and final prediction status without replacing raw failures with fixture-mode, rule-baseline, or gold-contract predictions

#### Scenario: Reject unresolved or accidental execution
- **WHEN** rerun training or prediction is launched without explicit opt-in, with unresolved template paths, without a repo-external private override, without an approved output root, or without a configured private adapter path
- **THEN** the system MUST NOT load private model artifacts, download models through an unintended path, start heavy training, start private prediction, or write successful rerun evidence

#### Scenario: Keep private runtime artifacts private
- **WHEN** the rerun completes or fails
- **THEN** raw logs, checkpoints, adapters, model caches, private overrides, host details, SSH details, private paths, tokens, and private corpus rows MUST remain outside committed artifacts
