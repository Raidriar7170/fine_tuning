## ADDED Requirements

### Requirement: Assess form-fill remediation SFT v3 readiness safely
The system SHALL publish public-safe readiness evidence before a later
`form_fill` remediation SFT v3 run.

#### Scenario: Prepare public-safe SFT v3 templates
- **WHEN** readiness config templates are committed
- **THEN** they MUST target manifest `public-sample-20260616T074315Z`
- **AND** they MUST keep private A100 paths unresolved with `<a100_project_root>` placeholders
- **AND** they MUST NOT include private paths, host details, SSH details, tokens, raw logs, checkpoints, adapters, or model caches

#### Scenario: Record dry-run row selection
- **WHEN** readiness evidence is generated
- **THEN** it MUST include local SFT dry-run row-selection metadata for the current public train split
- **AND** it MUST state that no SFT/DPO/GRPO training was launched

#### Scenario: Bound readiness interpretation
- **WHEN** reports or Human Briefs describe SFT v3 readiness
- **THEN** they MUST state that readiness does not prove model recovery, held-out generalization, private-corpus generalization, checkpoint release, adapter release, production readiness, public full-corpus release, or live-browser benchmark improvement
