## ADDED Requirements

### Requirement: Publish scaled-manifest current-123 adapter prediction-only baseline
The system SHALL publish public-safe prediction-only evidence for the private current-123 train split SFT retry adapter on the scaled public sample target manifest.

#### Scenario: Configure scaled-manifest dev/test prediction templates
- **WHEN** public-safe prediction configs are committed for this phase
- **THEN** they MUST set `dataset_manifest_id` and `target_dataset_manifest_id` to `public-sample-20260617T152259Z`
- **AND** they MUST set `source_adapter_runtime` to `a100-current-train-split-sft-retry`
- **AND** they MUST set `source_adapter_dataset_manifest_id` and `requires_paired_training_manifest_id` to `public-sample-20260617T045941Z`
- **AND** they MUST use adapter path `<a100_project_root>/runs/a100-current-train-split-sft-retry/adapter`
- **AND** they MUST require private overrides and public-safe placeholders rather than committed private paths

#### Scenario: Preserve prediction-only config boundaries
- **WHEN** the scaled target dev/test prediction configs are validated
- **THEN** they MUST be prediction-only configs with no `adapter_output_dir`, no `allow_heavy_training`, and no training launcher flags
- **AND** fixture-mode row selection MUST select 207 dev rows and 207 test rows from `public-sample-20260617T152259Z`
- **AND** committed config templates MUST omit raw private paths, A100 host details, SSH details, tokens, checkpoints, adapters, caches, and private corpus rows

#### Scenario: Evaluate scaled-manifest current-123 adapter predictions
- **WHEN** sanitized predictions are available for the scaled public sample dev and test splits
- **THEN** the system MUST evaluate them with the existing strict contract ladder, including `json_valid_rate`, `task_type_accuracy`, `route_accuracy`, `safety_precision`, `safety_recall`, `confirmation_accuracy`, strict `slot_f1`, diagnostic-only `slot_f1_soft`, and `contract_exact_match`
- **AND** evidence MUST record target manifest id `public-sample-20260617T152259Z`, source adapter manifest id `public-sample-20260617T045941Z`, source adapter runtime `a100-current-train-split-sft-retry`, 207 dev rows, 207 test rows, and scaled public sample counts of 240 seed rows, 675 SFT rows, and 2046 DPO pairs

#### Scenario: Preserve cross-boundary comparison semantics
- **WHEN** reports or Human Briefs describe scaled-manifest prediction-only metrics
- **THEN** they MUST state that the source adapter was trained for `public-sample-20260617T045941Z`
- **AND** they MUST NOT present old/new values as a clean improvement or regression unless the source/target manifest boundary is explicitly called out
- **AND** they MUST NOT imply that scaled target rows were included in the source adapter training

#### Scenario: Preserve public-safety and no-overclaim boundaries
- **WHEN** scaled-manifest prediction-only evidence is prepared for commit
- **THEN** committed artifacts MUST state that no SFT training, DPO training, GRPO training, dataset mutation, evaluator relaxation, semantic-equivalence scoring, slot normalization, prediction repair, prediction replacement, or prediction re-score was performed in this phase
- **AND** committed artifacts MUST NOT claim held-out recovery, model recovery, checkpoint release, adapter release, production readiness, public full-corpus release, private-corpus generalization, released-model quality, or live-browser benchmark improvement
- **AND** leak-scan validation MUST reject raw private rows, absolute local paths, private remote paths, host details, SSH details, secrets, tokens, raw logs, checkpoints, adapters, caches, and oversized generated corpora

#### Scenario: Record blocked prediction execution safely
- **WHEN** prediction-only A100 execution cannot safely run because the private adapter, private override, remote dependency, or idle GPU state is unavailable
- **THEN** the evidence MUST record a blocked status without writing fabricated predictions or model-quality metrics
- **AND** committed artifacts MUST omit raw logs, host details, SSH details, private paths, checkpoints, adapters, caches, tokens, and private corpus rows
