## ADDED Requirements

### Requirement: Run authorized A100 constrained-output train-split prediction rerun
The system SHALL support a bounded, explicitly authorized A100 prediction-only train-split rerun after constrained-output repair while keeping all private runtime artifacts outside committed files.

#### Scenario: Launch constrained-output prediction rerun
- **WHEN** a developer launches the rerun with explicit private-prediction opt-in, a repo-external private override, an existing private adapter path, and an idle A100 GPU under the approved private project root
- **THEN** the system MUST use `prediction_split=train`, `overfit_diagnostic=true`, `generalization_claim=false`, `schema_retry_enabled=true`, the current constrained-output shared prompt, and the current whole-string raw and retry JSON parsers

#### Scenario: Reuse existing private adapter without retraining
- **WHEN** this constrained-output rerun is executed
- **THEN** the system MUST NOT run SFT, DPO, GRPO, or any adapter-training command and MUST NOT create or commit a new adapter/checkpoint

#### Scenario: Block unresolved or unsafe private configuration
- **WHEN** prediction is launched without explicit opt-in, with unresolved template paths, without a repo-external private override, without an approved output root, or without a configured private adapter path
- **THEN** prediction MUST fail closed or remain blocked without producing misleading fixture-mode evidence

#### Scenario: Keep private A100 artifacts private
- **WHEN** the constrained-output prediction rerun completes or fails
- **THEN** raw logs, checkpoints, adapters, model caches, private overrides, host details, SSH details, private paths, tokens, and private corpus rows MUST remain outside committed artifacts
