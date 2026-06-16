## ADDED Requirements

### Requirement: Run bounded A100 form-fill remediation SFT v3
The system SHALL run the `form_fill` remediation SFT v3 phase only after
readiness evidence exists and only within the approved private A100 project
root.

#### Scenario: Launch SFT v3 with private override
- **WHEN** the SFT v3 training job is launched
- **THEN** it MUST use manifest `public-sample-20260616T074315Z`
- **AND** it MUST use the train split selected by the committed readiness
  dry-run
- **AND** it MUST resolve private paths only through a repo-external private
  override under the approved A100 project root
- **AND** it MUST set an explicit `CUDA_VISIBLE_DEVICES` value selected after
  GPU occupancy preflight

#### Scenario: Keep SFT v3 artifacts private
- **WHEN** the SFT v3 training job completes or fails
- **THEN** raw checkpoints, LoRA adapters, model caches, raw logs, private
  overrides, host details, SSH details, tokens, and private paths MUST remain
  outside committed artifacts
- **AND** committed metadata MUST use public-safe placeholders or sanitized
  summaries

#### Scenario: Preserve SFT v3 scope
- **WHEN** SFT v3 training is launched
- **THEN** the phase MUST NOT start DPO, GRPO, generic chat fine-tuning, skill
  routing, GUI action policy learning, full private corpus training, prompt
  policy changes, evaluator relaxation, or prediction repair
