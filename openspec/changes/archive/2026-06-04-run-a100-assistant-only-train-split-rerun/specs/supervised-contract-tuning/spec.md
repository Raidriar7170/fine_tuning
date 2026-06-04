## ADDED Requirements

### Requirement: Run authorized A100 assistant-only train-split rerun
The system SHALL support a bounded, explicitly authorized A100 train-split rerun that trains through the current assistant-only SFT label path and keeps all private runtime artifacts outside committed files.

#### Scenario: Launch assistant-only rerun training
- **WHEN** a developer launches the rerun with explicit heavy-training opt-in, a repo-external private override, and an idle A100 GPU under the approved private project root
- **THEN** the system MUST train only the public-sample train split through the primary Transformers, PEFT, and TRL SFT path with pretokenized assistant-only labels, record loss-mask policy metadata, and keep checkpoints, adapters, caches, raw logs, private paths, host details, SSH details, tokens, and private corpus rows out of committed artifacts

#### Scenario: Inspect current runtime objective path
- **WHEN** the rerun evidence is interpreted
- **THEN** the system MUST include objective/runtime label evidence from the current tokenizer/collator SFT path that states whether prompt/system/user tokens were masked and assistant Browser Task Contract tokens carried loss

#### Scenario: Reject unresolved or accidental rerun execution
- **WHEN** rerun training or prediction is launched without explicit opt-in, with unresolved template paths, without a repo-external private override, without an approved output root, or without a configured private adapter path
- **THEN** the system MUST NOT load private model artifacts, download models through an unintended path, start heavy training, start private prediction, or write successful rerun evidence

#### Scenario: Preserve private artifact boundary after rerun
- **WHEN** the rerun completes or fails
- **THEN** raw logs, checkpoints, adapters, model caches, private overrides, host details, SSH details, private paths, tokens, and private corpus rows MUST remain outside committed artifacts

#### Scenario: Keep rerun scope train-internal
- **WHEN** the rerun prediction step emits public-safe evidence
- **THEN** the system MUST use `prediction_split=train`, `overfit_diagnostic=true`, `generalization_claim=false`, and preserve schema-invalid, truncated, non-JSON, or wrong-contract outputs without fixture, rule-baseline, or gold-contract replacement
