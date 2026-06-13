## ADDED Requirements

### Requirement: Run A100 compact-query exact-match public-sample SFT rerun
The system SHALL support a bounded 7B A100 public-sample SFT rerun after compact-query exact-match policy hardening while keeping private runtime artifacts outside git.

#### Scenario: Launch compact-query exact-match SFT rerun
- **WHEN** the rerun is launched with explicit apply-phase authorization, the current public sample manifest, a repo-external private override, an idle A100 GPU selected after occupancy inspection, and an approved private output root represented in public artifacts as `<a100_project_root>`
- **THEN** the rerun MUST train `Qwen/Qwen2.5-7B-Instruct` only on committed public-sample SFT rows using the compact-query exact-match training prompt policy
- **AND** it MUST set `CUDA_VISIBLE_DEVICES` explicitly for the selected GPU
- **AND** it MUST write raw checkpoints, adapters, logs, caches, and temporary outputs only under the approved private A100 project root

#### Scenario: Export compact-query exact-match train predictions
- **WHEN** the rerun adapter is used for trained-adapter prediction
- **THEN** prediction export MUST use `prediction_split=train`, `overfit_diagnostic=true`, `generalization_claim=false`, greedy decoding, current prompt/output-boundary policy, and the current public sample manifest
- **AND** it MUST write sanitized predictions plus prompt snapshot, prediction metadata, raw decoded summary, generation trace, and schema guard summary when those sidecars are available

#### Scenario: Preserve model output honestly
- **WHEN** the private adapter emits invalid JSON, Markdown-wrapped JSON, wrapper text, decomposed `city/date/topic` slots, extra-particle `normalized_command` strings, or any strict mismatch
- **THEN** the prediction artifact and sidecars MUST preserve sanitized model output and strict failure status without replacing it with fixture-mode, rule-baseline, normalized, repaired, semantically judged, or gold contracts

#### Scenario: Keep private A100 artifacts private
- **WHEN** the rerun completes or fails
- **THEN** raw logs, checkpoints, adapters, caches, private overrides, host details, SSH details, private paths, tokens, secrets, and private corpus rows MUST remain outside committed artifacts
