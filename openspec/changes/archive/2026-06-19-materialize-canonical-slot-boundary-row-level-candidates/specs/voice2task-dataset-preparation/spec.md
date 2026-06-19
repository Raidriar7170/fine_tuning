## ADDED Requirements

### Requirement: Materialize canonical slot-boundary row-level candidates
The system SHALL materialize reviewed canonical slot-boundary candidate classes
into a standalone row-level public-safe candidate source before any future
formal public sample merge.

#### Scenario: Generate standalone row-level candidate source
- **WHEN** the canonical slot-boundary row-level materialization phase is
  applied
- **THEN** it MUST write
  `data/public-samples/canonical_slot_boundary_seed_candidates.jsonl`
- **AND** the file MUST contain exactly seven public-safe candidate seed rows:
  three from `slot_key_aliases` and four from `slot_value_boundaries`
- **AND** every row MUST use `split="train"` and
  `candidate_status="standalone_not_formal_public_sample"`.

#### Scenario: Preserve source traceability
- **WHEN** row-level candidates are generated
- **THEN** every candidate MUST include provenance linking to the archived
  canonical slot-boundary review, the source materialization evidence, the
  source policy evidence, the source candidate id, and the eligible source
  class
- **AND** every candidate MUST set `public_safe=true` and
  `source_mode="canonical_slot_boundary_candidate_seed"`.

#### Scenario: Exclude diagnostic and non-equivalence classes
- **WHEN** row-level candidates are generated
- **THEN** no row MAY be sourced from
  `normalized_command_display_diagnostic`
- **AND** no row MAY be sourced from excluded non-equivalence cases such as
  date, city/location, product, URL host, price/amount, query/product,
  location/destination, or action/reason changes.

#### Scenario: Publish standalone materialization evidence
- **WHEN** row-level candidate materialization completes
- **THEN** it MUST publish machine-readable evidence, a human-readable summary,
  a manifest, report-local SFT preview rows, and leak-scan evidence under
  `reports/public-sample/canonical-slot-boundary-row-level-candidates/`
- **AND** the evidence MUST record candidate counts, split counts, source
  classes, excluded classes, execution scope, formal data boundary, comparison
  boundary, and claims not to overstate.

#### Scenario: Preserve formal public sample boundary
- **WHEN** standalone row-level candidates are materialized
- **THEN** the system MUST NOT edit `data/public-samples/seed_traces.jsonl`,
  `sft_public_sample.jsonl`, `dpo_public_sample.jsonl`, or
  `manifest_public_sample.json`
- **AND** it MUST NOT generate formal SFT/DPO rows, rebuild a formal manifest,
  train, predict, run on A100, implement a deterministic postprocessor, relax
  strict exact, use an LLM judge, perform semantic-equivalence scoring, repair
  predictions, or claim model improvement.

#### Scenario: Validate public-safe row-level artifacts
- **WHEN** candidate source, report artifacts, docs, Human Brief HTML, or
  archive files are prepared for commit
- **THEN** validation MUST reject raw private rows, absolute local paths,
  private remote paths, host details, SSH details, raw logs, tokens, secrets,
  checkpoints, adapters, caches, and private corpus rows
- **AND** the source candidate review/materialization artifacts and the stale
  active `merge-scaled-clarify-slot-boundary-candidates` change MUST remain
  unmodified unless a separate bounded phase explicitly owns them.
