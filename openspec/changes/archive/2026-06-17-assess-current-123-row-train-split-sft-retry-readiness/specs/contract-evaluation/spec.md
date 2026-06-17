## ADDED Requirements

### Requirement: Publish current-123 train split SFT retry readiness evidence
The system SHALL publish public-safe readiness-only evidence for a potential current-train-split SFT retry after the formal public sample advances to `public-sample-20260617T045941Z`.

#### Scenario: Generate current-123 train split readiness evidence
- **WHEN** current-train-split SFT retry readiness evidence is generated for `public-sample-20260617T045941Z`
- **THEN** the evidence MUST record the manifest id, 102 seed rows, 261 SFT rows, 881 DPO pairs, and split counts of 123 train / 69 dev / 69 test
- **AND** it MUST record that the dry-run selected all 123 public train rows
- **AND** it MUST identify the represented train-row groups for prior form-fill repair, blocked-payment repair, and current-retry confirmation-preservation rows

#### Scenario: Preserve readiness-only interpretation
- **WHEN** reports, manifests, Human Briefs, or status docs describe current-123 train split readiness
- **THEN** they MUST state that no A100 training, prediction generation, prediction repair, prompt change, evaluator change, slot normalization, checkpoint release, adapter release, or private corpus publication occurred
- **AND** they MUST NOT claim model recovery, safety improvement, held-out recovery, production readiness, private-corpus generalization, or live-browser benchmark improvement
- **AND** they MUST state that current model evidence remains bound to the prior evaluated manifest until a later bounded training/evaluation phase produces new strict metrics

#### Scenario: Gate later prediction interpretation
- **WHEN** current-train-split retry prediction configs target `public-sample-20260617T045941Z`
- **THEN** readiness evidence MUST state that those prediction configs require a paired adapter trained for the same target manifest before their results can be interpreted as current-manifest model evidence
- **AND** it MUST recommend a later bounded A100 SFT retry phase before any prediction-only evaluation with that target adapter
