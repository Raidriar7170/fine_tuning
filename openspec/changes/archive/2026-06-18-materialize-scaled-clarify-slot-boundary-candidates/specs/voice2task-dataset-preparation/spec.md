## ADDED Requirements

### Requirement: Materialize scaled clarify slot-boundary candidates as standalone data
The system SHALL materialize public-safe scaled clarify slot-boundary candidate
rows as standalone candidate artifacts before any formal public sample merge or
paired training retry.

#### Scenario: Derive standalone candidates from committed clarify design
- **WHEN** scaled clarify slot-boundary candidate design evidence exists
- **THEN** the materializer MUST derive deterministic candidate seed rows and
  SFT candidate sidecars from the committed design report
- **AND** it MUST record the source design artifact, source manifest id,
  candidate theme ids, source-family coverage, candidate seed count, candidate
  SFT row count, and split counts

#### Scenario: Preserve clarify contract shape
- **WHEN** candidate seed rows are materialized
- **THEN** every target contract MUST preserve `task_type="clarify"`,
  `route="clarify"`, `safety.allow=true`,
  `safety.reason="ambiguous_request"`, `confirmation_required=true`, and a
  non-empty `slots.ambiguity` description
- **AND** every candidate row MUST retain provenance linking it to the
  candidate design theme and source design artifact

#### Scenario: Keep standalone materialization separate from formal merge
- **WHEN** scaled clarify slot-boundary candidates are materialized
- **THEN** the phase MUST NOT modify formal `seed_traces.jsonl`,
  `sft_public_sample.jsonl`, `dpo_public_sample.jsonl`, or
  `manifest_public_sample.json`
- **AND** it MUST NOT generate formal DPO pairs, launch training, generate
  predictions, change prompts, change evaluator metrics, normalize slots,
  repair predictions, release checkpoints/adapters, or claim model recovery,
  held-out recovery, safety improvement, production readiness,
  private-corpus generalization, public full-corpus release, or live-browser
  benchmark improvement

#### Scenario: Recommend later formal merge only after reviewable artifacts
- **WHEN** standalone candidates validate and are public-safe
- **THEN** the report MAY recommend one later bounded formal public sample merge
  phase
- **AND** it MUST state that no model-quality improvement can be inferred until
  a later strict prediction or training evaluation exists
