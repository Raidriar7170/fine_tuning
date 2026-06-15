## ADDED Requirements

### Requirement: Execute slot value candidate SFT probe on A100 safely
The system SHALL support an explicitly bounded A100 execution path for the slot value candidate SFT probe while keeping private runtime artifacts outside git.

#### Scenario: Prepare isolated A100 execution workspace
- **WHEN** the A100 candidate probe phase prepares remote execution
- **THEN** all project snapshots, dependency environments, caches, temporary files, outputs, and evidence staging directories MUST be under the approved private A100 root
- **AND** the phase MUST stop before training if this placement cannot be enforced

#### Scenario: Launch candidate-only SFT when safe
- **WHEN** train dependencies are available, a private override resolves `<a100_project_root>`, and an idle GPU is selected
- **THEN** the SFT command MUST use the candidate-only manifest, `dataset_split=train`, the 7B base model, and explicit `CUDA_VISIBLE_DEVICES`
- **AND** it MUST write adapters, checkpoints, caches, logs, and raw runtime outputs only under the approved private remote workspace

#### Scenario: Preserve training failure or blocked status
- **WHEN** dependency setup, model loading, GPU placement, output-root policy, or training fails
- **THEN** the phase MUST write only sanitized status metadata to git
- **AND** it MUST NOT imply that candidate SFT training completed

#### Scenario: Bound candidate training interpretation
- **WHEN** real candidate training metadata is imported into public evidence
- **THEN** the evidence MUST label it as candidate train-split learnability evidence
- **AND** it MUST NOT claim held-out dev/test generalization, checkpoint release, adapter release, production readiness, private-corpus generalization, or live-browser improvement
