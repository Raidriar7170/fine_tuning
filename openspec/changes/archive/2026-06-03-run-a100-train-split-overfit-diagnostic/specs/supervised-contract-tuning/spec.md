## ADDED Requirements

### Requirement: Run A100 train-split overfit diagnostic
The system SHALL support a bounded, explicitly authorized A100 train-split overfit diagnostic that uses the prepared diagnostic prediction contract and keeps all private runtime artifacts outside git.

#### Scenario: Launch real train-split diagnostic
- **WHEN** a developer launches the train-split diagnostic with an explicit prediction opt-in, a repo-external private override, and an idle A100 GPU under the approved private project root
- **THEN** the system MUST use `prediction_split=train`, `overfit_diagnostic=true`, `generalization_claim=false`, and generate train-split diagnostic predictions plus prompt snapshot, sanitized raw decoded summary, generation trace, and prediction metadata sidecars

#### Scenario: Reject unresolved or accidental diagnostic execution
- **WHEN** the diagnostic command is launched without explicit prediction opt-in, with unresolved template paths, or without a configured private adapter path
- **THEN** the system MUST NOT load private model artifacts or start remote prediction and MUST report that no private adapter diagnostic occurred

#### Scenario: Keep private A100 artifacts private
- **WHEN** the real diagnostic completes or fails
- **THEN** raw logs, checkpoints, adapters, caches, private overrides, host details, SSH details, private paths, tokens, and private corpus rows MUST remain outside committed artifacts

#### Scenario: Preserve diagnostic model output
- **WHEN** the private adapter emits schema-invalid, truncated, non-JSON, or contract-like but wrong output
- **THEN** the prediction artifact and sidecars MUST preserve sanitized failure evidence without replacing it with fixture-mode, rule-baseline, or gold contracts
