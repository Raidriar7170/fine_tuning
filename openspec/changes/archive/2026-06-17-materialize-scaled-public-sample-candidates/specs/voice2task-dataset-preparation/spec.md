## ADDED Requirements

### Requirement: Materialize scaled public-sample candidates
The system SHALL materialize deterministic, public-safe scaled public-sample
candidate seed rows and derived SFT sidecars from the archived scaled-sample
design without mutating the formal public sample.

#### Scenario: Generate standalone scaled candidates
- **WHEN** a developer runs scaled public-sample candidate materialization
- **THEN** the system writes standalone candidate seed rows, SFT candidate rows,
  a machine-readable manifest, and a human-readable report under candidate and
  report paths that are not the formal public sample files
- **AND** the candidate manifest MUST record that formal public sample files were
  not modified

#### Scenario: Preserve scaled target accounting
- **WHEN** scaled candidates are materialized from the current `102` seed
  boundary
- **THEN** the evidence MUST record current formal counts, target core counts,
  target overlay counts, candidate seed counts by family, candidate SFT row
  counts, and split counts
- **AND** the evidence MUST distinguish core-family candidates from
  confirmation-boundary overlay candidates

#### Scenario: Protect formal public sample files
- **WHEN** the materializer is given an output path
- **THEN** it MUST reject attempts to write candidate seeds, sidecars, or reports
  over `seed_traces.jsonl`, `sft_public_sample.jsonl`,
  `dpo_public_sample.jsonl`, or `manifest_public_sample.json`

#### Scenario: Bound candidate evidence claims
- **WHEN** reports or Human Briefs describe scaled candidate materialization
- **THEN** they MUST state that the phase does not merge the formal public
  sample, rebuild formal SFT/DPO artifacts, train, predict, change prompts,
  change evaluator metrics, normalize slots, repair predictions, release
  checkpoints/adapters, or prove model recovery
