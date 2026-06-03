# supervised-contract-tuning Specification

## Purpose
Define how supervised LoRA tuning teaches Qwen-family small instruction models to emit canonical browser task contracts from Chinese spoken commands or ASR transcripts.
## Requirements
### Requirement: Train supervised contract adapters
The system SHALL run LoRA SFT experiments that train a Qwen-family small instruction model to emit browser task contracts from Chinese spoken commands or ASR transcripts.

#### Scenario: Run SFT training
- **WHEN** a developer launches SFT training with a valid config and train/dev dataset paths
- **THEN** the system trains a LoRA adapter, writes checkpoints to a configured output directory, and records the model, dataset manifest, hyperparameters, and training command

### Requirement: Keep SFT outputs contract-focused
The system SHALL format supervised targets as browser task contracts rather than free-form assistant responses.

#### Scenario: Prepare SFT examples
- **WHEN** the training data formatter converts dataset rows into model messages
- **THEN** the target assistant content is the canonical browser task contract JSON and not explanatory prose

### Requirement: Provide prompt-only and rule baselines
The system SHALL support baseline evaluation for a rule normalizer and a prompt-only model before comparing SFT outputs.

#### Scenario: Compare SFT against baselines
- **WHEN** the SFT report is generated
- **THEN** it includes baseline metrics for at least rule normalization and prompt-only generation when the required providers or fixtures are available

### Requirement: Export adapter metadata
The system SHALL export SFT adapter metadata without implying a public checkpoint release unless an explicit release artifact exists.

#### Scenario: Export SFT adapter summary
- **WHEN** SFT training completes
- **THEN** the system writes an adapter summary containing base model, adapter path, dataset manifest ID, metrics path, and release status

### Requirement: Run A100 public-sample SFT smoke
The system SHALL provide a bounded, opt-in A100 SFT smoke workflow that trains the existing Qwen-family LoRA SFT path on the committed public sample and writes all remote outputs under the approved private A100 project root.

#### Scenario: Launch smoke with explicit opt-in
- **WHEN** a developer launches the A100 SFT smoke with `--run-training` and a config whose `allow_heavy_training` is `true`
- **THEN** the system uses the configured public-sample manifest, writes adapter/checkpoint outputs under the configured A100 project directory, and records the base model, dataset manifest ID, hyperparameters, package versions, output paths, and training command in adapter metadata

#### Scenario: Reject accidental heavy training
- **WHEN** a developer launches the A100 SFT smoke without `--run-training` or with `allow_heavy_training` unset or false
- **THEN** the system does not download models or start training and instead emits dry-run metadata that clearly states no heavy training occurred

#### Scenario: Keep remote evidence private by default
- **WHEN** the A100 smoke run completes
- **THEN** raw checkpoints, adapters, caches, and logs remain out of git unless a later explicit release change approves a sanitized artifact

### Requirement: Export A100 trained-path public-sample predictions
The system SHALL provide a bounded prediction export workflow for the A100 public-sample SFT adapter path that emits only sanitized public-sample prediction rows for contract evaluation.

#### Scenario: Launch trained-path prediction with explicit opt-in
- **WHEN** a developer launches trained-path public-sample prediction with an explicit prediction opt-in and a configured private adapter path
- **THEN** the system loads the configured adapter path, generates prediction rows for the committed public sample, and writes a sanitized prediction JSONL artifact without copying checkpoints, adapters, raw logs, caches, or private remote paths into git

#### Scenario: Reject accidental private prediction
- **WHEN** a developer launches prediction without the explicit prediction opt-in or without a configured adapter path
- **THEN** the system does not load private model artifacts and instead emits a dry-run or fixture-mode result that clearly states no private adapter prediction occurred

#### Scenario: Record prediction provenance safely
- **WHEN** trained-path prediction output is prepared for public evidence
- **THEN** the system records the base model ID, model source label, dataset manifest ID, adapter release status, prediction source kind, and command summary using public-safe placeholders rather than private filesystem paths or host details

### Requirement: Use consistent contract-only SFT chat formatting
The system SHALL serialize real SFT training examples and trained-adapter prediction prompts with a consistent contract-only chat format that uses tokenizer chat templates when available and a deterministic fallback when unavailable.

#### Scenario: Serialize real SFT training examples
- **WHEN** the real SFT training path builds text examples from public-sample or private SFT rows
- **THEN** each example contains the contract-only system instruction, the user command or ASR transcript, and the canonical Browser Task Contract JSON assistant target using the same chat serialization policy used by prediction

#### Scenario: Serialize trained-adapter prediction prompts
- **WHEN** trained-adapter prediction builds a prompt for a public-sample row
- **THEN** the prompt contains the contract-only system instruction, the user command or ASR transcript, and a generation prompt for a Browser Task Contract JSON object without explanatory prose, Markdown, or GUI actions

#### Scenario: Fall back without heavy dependencies
- **WHEN** a tokenizer does not expose a chat template or local validation does not load a tokenizer
- **THEN** the system uses a deterministic plain-text fallback that preserves the same roles, contract-only instruction, and assistant generation boundary

### Requirement: Keep recovery predictions honest
The system SHALL keep trained-adapter output recovery focused on model prompt/training format and shall not replace invalid private-adapter outputs with rule-baseline, fixture-mode, or gold-contract predictions.

#### Scenario: Preserve invalid model output
- **WHEN** a private adapter emits invalid JSON or a non-contract JSON object
- **THEN** the prediction artifact preserves the sanitized model output as a schema failure candidate rather than substituting a valid fixture or rule-normalized contract

#### Scenario: Record recovery run provenance
- **WHEN** a recovery SFT or prediction run is prepared for public evidence
- **THEN** the metadata records the formatting policy, base model public ID, dataset manifest ID, prediction source kind, adapter release status, and command summary using public-safe placeholders

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
