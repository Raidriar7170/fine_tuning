## ADDED Requirements

### Requirement: Materialize reviewed blocked-payment safety repair candidates
The system SHALL materialize reviewed `blocked_payment` safety repair
candidates into public-safe seed rows and synchronized public derived artifacts
before any training or prediction phase uses them as data evidence.

#### Scenario: Materialize from reviewed candidate design
- **WHEN** the materialization phase reads the blocked-payment repair candidate design evidence
- **THEN** it MUST create public-safe seed rows for the reviewed repair families
- **AND** each materialized target contract MUST use `task_type=blocked`,
  `route=deny`, `safety.allow=false`, `safety.reason=unsafe_payment`, and
  `confirmation_required=false`
- **AND** the evidence MUST preserve candidate ids, repair families, source row
  ids, and source classification counts

#### Scenario: Rebuild synchronized public artifacts
- **WHEN** candidate seed rows are materialized
- **THEN** the system MUST rebuild the public manifest, SFT rows, and DPO pairs
  from the updated public seed traces
- **AND** the materialization evidence MUST record pre-materialization and
  post-materialization seed, SFT, and DPO counts
- **AND** public data validation and DPO family count checks MUST pass before
  the change is archived

#### Scenario: Preserve materialization-only boundaries
- **WHEN** materialization evidence, reports, or Human Briefs describe the phase
- **THEN** they MUST state that this phase performs no SFT, DPO, GRPO, A100
  execution, prediction generation, evaluator relaxation, semantic-equivalence
  scoring, prediction repair, prompt change, adapter release, checkpoint
  release, public full-corpus release, production-readiness claim, model-quality
  claim, or live-browser benchmark claim
- **AND** the evidence MUST include machine-readable boundary flags for those
  non-goals
