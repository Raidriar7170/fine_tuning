## ADDED Requirements

### Requirement: Run 7B current-manifest tiny-overfit probe
The system SHALL provide a bounded A100 SFT probe that trains the 7B Qwen-family model on a tiny train-only slice from the current public sample manifest and records the run as train-internal evidence only.

#### Scenario: Configure current-manifest tiny-overfit training
- **WHEN** a developer prepares the current-manifest tiny-overfit training config
- **THEN** the committed template MUST use `Qwen/Qwen2.5-7B-Instruct`, `dataset_manifest_id=public-sample-20260613T072200Z`, `dataset_split=train`, `overfit_diagnostic=true`, `generalization_claim=false`, and unresolved `<a100_project_root>` placeholders that require a private override before remote execution

#### Scenario: Bound tiny training rows
- **WHEN** the A100 probe is launched from a private override
- **THEN** the training command MUST use only 1 to 3 train rows from the current public sample manifest and MUST record the selected row IDs in private metadata before any public evidence is prepared

#### Scenario: Keep heavy artifacts private
- **WHEN** the tiny-overfit training run completes or fails
- **THEN** raw logs, checkpoints, adapters, caches, private overrides, host details, SSH details, private paths, tokens, and private corpus rows MUST remain outside committed artifacts

#### Scenario: Preserve blocked execution honestly
- **WHEN** training dependencies, GPU placement, model files, or SSH access are unavailable
- **THEN** the phase MUST record a bounded public-safe blocked status and MUST NOT claim that tiny-overfit training occurred
