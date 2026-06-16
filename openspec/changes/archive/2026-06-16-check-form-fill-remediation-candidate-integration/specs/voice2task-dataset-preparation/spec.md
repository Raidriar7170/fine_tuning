## ADDED Requirements

### Requirement: Preview-check form-fill remediation candidate integration

The system SHALL support a local preview integration check for standalone `form_fill` remediation candidate seeds before any later formal public-sample merge, training probe, or A100 execution.

#### Scenario: Build preview artifacts without mutating the formal public sample

- **WHEN** the integration check runs with the current formal public seed file and the reviewed `form_fill` remediation candidate seed file
- **THEN** it MUST write preview seed, SFT, DPO, and manifest artifacts under a reports directory
- **AND** it MUST NOT edit `data/public-samples/seed_traces.jsonl`, `sft_public_sample.jsonl`, `dpo_public_sample.jsonl`, or `manifest_public_sample.json`
- **AND** the evidence manifest MUST state `formal_public_sample_modified=false`

#### Scenario: Validate reviewed candidate rows before preview build

- **WHEN** the integration check reads the candidate seed file
- **THEN** it MUST reject missing, extra, duplicate, already-formal, or non-standalone candidate rows
- **AND** it MUST reject candidate IDs that already exist in the formal public seed file
- **AND** every accepted candidate MUST remain public-safe, train split, and schema-valid

#### Scenario: Record preview counts and candidate contributions

- **WHEN** the preview public-sample build succeeds
- **THEN** the evidence MUST record the current formal public counts, preview public counts, candidate seed count, candidate SFT count, candidate preview DPO count, and preview validation status
- **AND** the preview DPO count MUST be marked as preview-only, not a formal DPO rebuild

#### Scenario: Preserve execution and claim boundaries

- **WHEN** integration check artifacts, reports, or Human Briefs describe the phase
- **THEN** they MUST state that strict `contract_exact_match` remains the primary metric
- **AND** they MUST NOT claim held-out generalization recovery, model recovery, checkpoint release, adapter release, production readiness, private-corpus generalization, public full-corpus release, or live-browser benchmark improvement
- **AND** they MUST state `training_run=false`, `prediction_run=false`, `a100_execution=false`, and `evaluator_metric_change=false`
