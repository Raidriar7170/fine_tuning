## ADDED Requirements

### Requirement: Design blocked-payment safety repair candidates before materialization
The system SHALL publish public-safe design evidence for `blocked_payment`
safety repair candidates before materializing new safety seed rows, generating
new DPO pairs, or launching another training phase intended to address
`blocked_payment` false negatives.

#### Scenario: Derive candidates from committed safety diagnosis
- **WHEN** the candidate design reads the SFT v3 safety regression diagnosis
- **THEN** it MUST identify source row ids, source task family, failure
  classification, accepted safety target shape, and rejected drift shapes for
  each proposed `blocked_payment` repair candidate
- **AND** it MUST preserve support counts for regressed and persistent-miss rows

#### Scenario: Preserve design-only boundaries
- **WHEN** blocked-payment repair candidates are published for review
- **THEN** the evidence MUST state that it performs no public-sample mutation,
  local/private corpus mutation, SFT, DPO, GRPO, prediction generation, A100
  execution, prompt change, evaluator change, prediction repair, semantic
  scoring, adapter release, checkpoint release, production-readiness claim, or
  live-browser benchmark
- **AND** the evidence MUST include a `formal_public_sample_modified=false`
  boundary or equivalent machine-readable flag

#### Scenario: Recommend a bounded follow-up
- **WHEN** the design identifies candidate families with enough coverage to
  repair the observed `blocked_payment` misses
- **THEN** it MAY recommend a later bounded materialization or training phase
- **AND** it MUST NOT generate seed rows, DPO pairs, or model-quality claims as
  part of the design phase
