## ADDED Requirements

### Requirement: Keep public project visibility aligned with formal held-out evidence
The system SHALL keep public-facing project summaries aligned with the latest
committed formal public held-out evidence and conservative evaluation claim
boundaries.

#### Scenario: Refresh public summaries after formal held-out evidence
- **WHEN** README files, experiment reports, or Human Briefs describe the current
  Voice2Task model status
- **THEN** they MUST use the latest committed formal public held-out evidence as
  the headline status when such evidence exists
- **AND** they MUST identify strict `contract_exact_match` and strict `slot_f1`
  as primary evidence, with `slot_f1_soft` labeled as an internal diagnostic
  only
- **AND** they MUST NOT claim held-out recovery, model recovery, checkpoint
  release, adapter release, production readiness, private-corpus
  generalization, public full-corpus release, or live-browser benchmark
  improvement unless separate authoritative evidence exists

#### Scenario: Recommend the next bounded phase
- **WHEN** public summaries recommend future Voice2Task work after partial
  held-out evidence
- **THEN** they MUST recommend residual/family diagnosis before new data
  generation, broad retraining, DPO reruns, evaluator changes, or production
  positioning
- **AND** they MUST keep historical private-dev or train-split diagnostics
  separate from current formal public held-out results
