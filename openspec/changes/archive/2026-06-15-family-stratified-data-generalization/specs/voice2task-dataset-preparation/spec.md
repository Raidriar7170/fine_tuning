## ADDED Requirements

### Requirement: Materialize family-stratified generalization candidates separately
The system SHALL materialize a public-safe family-stratified generalization
candidate dataset that remains separate from the formal public sample until a
later approved change explicitly merges it.

#### Scenario: Generate family-stratified candidate seeds
- **WHEN** the family-stratified materializer runs
- **THEN** it MUST write public-safe candidate seed rows for the text/ASR-to-contract families `search`, `navigation`, `clarify`, `form_fill`, `extract`, `blocked_payment`, and `confirmation`
- **AND** each family MUST contain `train`, `dev`, and `test` seed rows
- **AND** each candidate seed MUST include provenance with `source_mode="family_stratified_generalization_candidate_seed"`, `public_safe=true`, `candidate_status="standalone_not_formal_public_sample"`, `family_id`, `split_role`, and `family_stratification=true`

#### Scenario: Preserve split separation
- **WHEN** candidate seeds are generated
- **THEN** source IDs MUST be unique and MUST NOT appear in more than one split
- **AND** each family-specific slot signature MUST be disjoint across `train`, `dev`, and `test`
- **AND** the materialization manifest MUST record per-family per-split seed and SFT counts

#### Scenario: Expand candidate SFT rows without DPO
- **WHEN** candidate seeds contain schema-preserving augmentations
- **THEN** the materializer MUST expand them into candidate SFT rows using the existing SFT row schema and augmentation provenance
- **AND** it MUST NOT generate DPO pairs or hard negatives in this phase

#### Scenario: Keep formal public sample unchanged
- **WHEN** family-stratified candidate materialization runs
- **THEN** it MUST NOT edit `data/public-samples/seed_traces.jsonl`, `sft_public_sample.jsonl`, `dpo_public_sample.jsonl`, or `manifest_public_sample.json`
- **AND** the materialization manifest MUST state `formal_public_sample_modified=false`, `training_run=false`, `prediction_run=false`, `dpo_run=false`, `a100_execution=false`, and `evaluator_metric_change=false`

#### Scenario: Preserve evaluation and claim boundaries
- **WHEN** family-stratified candidate artifacts, reports, or Human Briefs describe the phase
- **THEN** they MUST state that strict `contract_exact_match` remains the primary metric
- **AND** they MUST NOT claim held-out generalization recovery, model recovery, checkpoint release, adapter release, production readiness, private-corpus generalization, public full-corpus release, or live-browser benchmark improvement
