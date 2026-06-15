## MODIFIED Requirements

### Requirement: Run A100 merged slot value public-sample SFT rerun
The system SHALL support a bounded 7B A100 SFT rerun after the reviewed slot
value candidates are merged into the formal public sample.

#### Scenario: Configure merged-candidate SFT rerun
- **WHEN** the merged-candidate SFT config is prepared
- **THEN** it MUST use `Qwen/Qwen2.5-7B-Instruct`, the regenerated
  `manifest_public_sample.json`, `dataset_split="train"`,
  `allow_heavy_training=true`, and `generalization_claim=false`
- **AND** it MUST keep private output paths as `<a100_project_root>`
  placeholders requiring a private override before remote execution
- **AND** it MUST train on the formal public train split rather than the
  standalone candidate manifest

#### Scenario: Configure split-specific merged-candidate predictions
- **WHEN** prediction configs are prepared for the merged-candidate adapter
- **THEN** the system MUST provide train, dev, and test templates that point to
  the merged-candidate adapter placeholder
- **AND** each prediction template MUST set its own `prediction_split`, require
  `allow_private_prediction=true`, and set `generalization_claim=false`

#### Scenario: Keep A100 runtime artifacts private
- **WHEN** merged-candidate training or prediction completes, fails, or is
  blocked
- **THEN** raw logs, adapters, checkpoints, caches, private overrides, host
  details, SSH details, private paths, tokens, model snapshots, and private
  corpus rows MUST remain outside committed artifacts

#### Scenario: Bound merged-candidate training interpretation
- **WHEN** public reports or Human Briefs describe the merged-candidate SFT run
- **THEN** train-split exact match MUST be described as learnability evidence
- **AND** held-out `dev`/`test` strict exact MUST be described as the primary
  generalization evidence
- **AND** the phase MUST NOT claim checkpoint release, adapter release,
  production readiness, private-corpus generalization, or live-browser
  benchmark improvement
