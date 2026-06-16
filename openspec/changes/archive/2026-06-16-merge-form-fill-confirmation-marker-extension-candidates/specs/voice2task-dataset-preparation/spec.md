## ADDED Requirements

### Requirement: Merge form-fill confirmation-marker extension candidates into public sample
The system SHALL support a guarded formal merge of reviewed form-fill confirmation-marker extension candidate seeds into the committed public sample after candidate materialization and preview integration evidence exist.

#### Scenario: Merge reviewed extension candidates exactly once
- **WHEN** the merge command runs with the current formal public seed file and `form_fill_confirmation_marker_extension_seed_candidates.jsonl`
- **THEN** it MUST validate exactly the 12 reviewed confirmation-marker extension candidate seed rows
- **AND** it MUST fail if any candidate ID already exists in the formal public seed file
- **AND** it MUST append the candidate rows to the formal seed file without modifying unrelated formal rows

#### Scenario: Rebuild synchronized formal public artifacts
- **WHEN** the formal seed file is updated by the merge command
- **THEN** the system MUST rebuild `sft_public_sample.jsonl`, `dpo_public_sample.jsonl`, and `manifest_public_sample.json` from the updated formal seed file
- **AND** the resulting manifest MUST record 98 seed rows, 252 SFT rows, 850 DPO pairs, and split counts of train 114, dev 69, and test 69
- **AND** the derived artifacts MUST validate through the public dataset validator

#### Scenario: Publish merge evidence
- **WHEN** the merge completes
- **THEN** the system MUST publish JSON, Markdown, and manifest evidence under `reports/public-sample/`
- **AND** the evidence MUST record pre-merge counts, post-merge counts, candidate contribution counts, candidate source identity, validation status, and public-safety policy

#### Scenario: Preserve formal merge claim boundaries
- **WHEN** merge evidence, reports, or Human Briefs describe the phase
- **THEN** they MUST state that strict `contract_exact_match`, strict `slot_f1`, and the contract evaluation ladder remain authoritative
- **AND** they MUST state that `slot_f1_soft` is diagnostic-only
- **AND** they MUST NOT claim held-out generalization recovery, model recovery, checkpoint release, adapter release, production readiness, private-corpus generalization, public full-corpus release, or live-browser benchmark improvement
- **AND** they MUST state `training_run=false`, `prediction_run=false`, `a100_execution=false`, and `evaluator_metric_change=false`
