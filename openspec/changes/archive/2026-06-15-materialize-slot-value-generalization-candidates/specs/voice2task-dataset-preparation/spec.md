## ADDED Requirements

### Requirement: Materialize reviewed slot value generalization candidates separately
The system SHALL materialize reviewed slot value generalization case groups into a public-safe candidate dataset that remains separate from the formal public sample until a later approved change merges it.

#### Scenario: Generate candidate seeds from reviewed design
- **WHEN** the slot value generalization case-design artifact contains the reviewed case groups
- **THEN** the materializer MUST write exactly one public-safe candidate seed row for each reviewed case group
- **AND** each candidate seed MUST use a schema-valid Browser Task Contract with canonical slot values or normalized command wording from the design
- **AND** each candidate seed MUST include provenance linking back to the source case group and design artifact

#### Scenario: Keep formal public sample unchanged
- **WHEN** candidate materialization runs
- **THEN** it MUST NOT edit `data/public-samples/seed_traces.jsonl`, `sft_public_sample.jsonl`, `dpo_public_sample.jsonl`, or `manifest_public_sample.json`
- **AND** the materialization manifest MUST state `public_sample_modified=false`, `training_run=false`, `prediction_run=false`, and `dpo_run=false`

#### Scenario: Expand candidate SFT rows without DPO
- **WHEN** candidate seeds contain schema-preserving augmentations
- **THEN** the materializer MUST expand them into candidate SFT rows using the existing SFT row schema and augmentation provenance
- **AND** it MUST NOT generate DPO pairs or hard negatives in this phase

#### Scenario: Preserve evaluation and claim boundaries
- **WHEN** materialized candidate artifacts, reports, or Human Briefs describe the phase
- **THEN** they MUST state that strict `contract_exact_match` remains the primary metric
- **AND** they MUST NOT claim held-out generalization recovery, model recovery, checkpoint release, adapter release, production readiness, private-corpus generalization, or live-browser benchmark improvement
