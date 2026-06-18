## ADDED Requirements

### Requirement: Review safety repair candidates before materialization
The system SHALL publish public-safe review evidence for safety repair
candidate themes before any later phase materializes seed rows, mutates the
formal public sample, or launches training intended to address unsafe
false-negative behavior.

#### Scenario: Review current safety repair candidate design
- **WHEN** review evidence reads the committed safety repair candidate design
- **THEN** it MUST record the source design artifact path, manifest id, candidate count, source unsafe false-negative support, and per-candidate review decisions
- **AND** each decision MUST include review status, rationale, allowed later operation, and blocked operations

#### Scenario: Preserve review-only boundaries
- **WHEN** safety repair candidate review evidence is generated
- **THEN** it MUST state that it performs no seed materialization, public-sample mutation, train/dev/test split change, SFT, DPO, GRPO, A100 execution, prediction generation, prompt change, evaluator change, evaluator relaxation, LLM judge, semantic-equivalence scoring, prediction repair, adapter release, checkpoint release, production-readiness claim, safety-readiness claim, held-out recovery claim, or live-browser benchmark claim
- **AND** it MUST include machine-readable flags that keep those operations false

#### Scenario: Recommend only bounded follow-up phases
- **WHEN** candidate review decisions are selected
- **THEN** the evidence MAY recommend a later bounded materialization proposal for row-backed themes or a later safety-policy design proposal for broad themes
- **AND** it MUST NOT generate seed rows, mark candidates as merged, publish a checkpoint, or claim measurable safety improvement as part of this review phase

#### Scenario: Validate public-safe review artifacts
- **WHEN** safety repair review artifacts, docs, Human Brief HTML, or archive files are prepared for commit
- **THEN** validation MUST reject raw private rows, absolute local paths, private remote paths, host details, SSH details, raw logs, tokens, secrets, checkpoints, adapters, caches, and private corpus rows
- **AND** historical blocked-payment safety repair, layered-eval, residual-diagnosis, remediation-target-selection, and safety repair design artifacts MUST remain unmodified
