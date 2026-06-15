## MODIFIED Requirements

### Requirement: Merge reviewed slot value candidates into the formal public sample
The system SHALL support an explicitly approved merge of reviewed slot value
generalization candidates into the formal public sample while preserving
public-safety validation and held-out split boundaries.

#### Scenario: Merge candidate seeds as train rows
- **WHEN** the candidate merge command is run with the reviewed case design and
  current formal public seed file
- **THEN** it MUST append exactly the reviewed slot value candidate seed rows to
  `data/public-samples/seed_traces.jsonl`
- **AND** each merged candidate seed MUST use `split="train"`, public-safe
  provenance, and a schema-valid Browser Task Contract
- **AND** existing public `dev` and `test` rows MUST keep their split labels,
  row IDs, inputs, and target contracts

#### Scenario: Rebuild formal public sample artifacts
- **WHEN** candidate seeds have been merged
- **THEN** `sft_public_sample.jsonl`, `dpo_public_sample.jsonl`, and
  `manifest_public_sample.json` MUST be regenerated from
  `seed_traces.jsonl`
- **AND** the manifest counts MUST match generated JSONL row counts
- **AND** the manifest MUST record that slot value candidates are now formal
  public sample rows

#### Scenario: Generate hard negatives for merged candidates
- **WHEN** DPO pairs are generated for merged candidate original rows
- **THEN** each original candidate row MUST receive the standard
  `wrong_task_type` hard negative
- **AND** eligible candidate families MUST receive the relevant residual drift
  hard negatives through the normal public DPO builder
- **AND** augmented candidate rows MUST remain SFT rows and MUST NOT receive
  separate DPO hard negatives

#### Scenario: Preserve merge claim boundaries
- **WHEN** reports, manifests, tests, or Human Briefs describe the merge
- **THEN** they MUST state that data merge and SFT/DPO rebuild do not by
  themselves prove held-out recovery, model recovery, adapter release,
  checkpoint release, production readiness, private-corpus generalization, or
  live-browser benchmark improvement
