## ADDED Requirements

### Requirement: Publish current-manifest tiny-overfit probe evidence
The system SHALL publish a public-safe evidence pack for the current-manifest tiny-overfit probe that separates train-internal memorization from held-out generalization and release claims.

#### Scenario: Import sanitized tiny-overfit evidence
- **WHEN** tiny-overfit training metadata, train-split predictions, metrics, prompt snapshot, sanitized raw decoded summary, generation trace, runtime-label reference, and leak-scan results are available
- **THEN** the manifest and report MUST link those sanitized artifacts, record `prediction_split=train`, `overfit_diagnostic=true`, `generalization_claim=false`, `base_model=Qwen/Qwen2.5-7B-Instruct`, `dataset_manifest_id=public-sample-20260613T072200Z`, selected train row IDs, prediction count, release status, and non-claim boundaries without private runtime details

#### Scenario: Report observed train-internal recovery
- **WHEN** the probe report is generated from real private-adapter train-split predictions
- **THEN** it MUST state whether schema validity, task type, route, slot, safety, confirmation, and strict contract exact match recovered, remained partial, or failed using observed metrics and failure slices

#### Scenario: Keep tiny-overfit evidence public-safe
- **WHEN** tiny-overfit evidence is prepared for commit
- **THEN** leak-scan validation MUST reject raw private rows, local or remote private paths, secrets, private IP addresses, SSH details, raw logs, checkpoints, adapters, caches, oversized generated corpora, model snapshots, and private remote paths

#### Scenario: Bound tiny-overfit interpretation
- **WHEN** public documentation or Human Briefs describe the probe result
- **THEN** they MUST state that train-internal tiny-overfit evidence does not prove dev/test generalization, private-corpus generalization, production readiness, checkpoint release, adapter release, public full-corpus release, or live-browser benchmark improvement
