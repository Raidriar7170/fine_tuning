## ADDED Requirements

### Requirement: Design residual-driven safety repair candidates before materialization
The system SHALL publish public-safe safety repair candidate design evidence
from current layered evaluation and residual target-selection artifacts before
materializing new safety seed rows, mutating public samples, or launching a
training phase intended to address unsafe false-negative behavior.

#### Scenario: Derive safety repair design from current public artifacts
- **WHEN** the safety repair design reads current remediation target-selection, layered-eval, and residual-diagnosis artifacts
- **THEN** it MUST record source artifact paths, current manifest id, unsafe false-negative support, safety-related residual counts, and candidate design themes
- **AND** each candidate theme MUST include accepted target sketch, rejected drift sketches, evidence rationale, intended later operation, and public-safe utterance template descriptors

#### Scenario: Preserve design-only boundaries
- **WHEN** safety repair candidate design evidence is generated
- **THEN** it MUST state that it performs no seed materialization, public-sample mutation, train/dev/test split change, SFT, DPO, GRPO, A100 execution, prediction generation, prompt change, evaluator change, evaluator relaxation, LLM judge, semantic-equivalence scoring, prediction repair, adapter release, checkpoint release, production-readiness claim, safety-readiness claim, held-out recovery claim, or live-browser benchmark claim
- **AND** it MUST include machine-readable flags that keep those operations false

#### Scenario: Recommend bounded follow-up only
- **WHEN** candidate design themes are selected
- **THEN** the evidence MAY recommend a later bounded materialization or policy phase
- **AND** it MUST NOT generate seed rows, merge candidates, publish a checkpoint, or claim measurable safety improvement as part of this design phase

#### Scenario: Validate public-safe safety design artifacts
- **WHEN** safety repair design artifacts, docs, Human Brief HTML, or archive files are prepared for commit
- **THEN** validation MUST reject raw private rows, absolute local paths, private remote paths, host details, SSH details, raw logs, tokens, secrets, checkpoints, adapters, caches, and private corpus rows
- **AND** historical blocked-payment safety repair, layered-eval, residual-diagnosis, and remediation-target-selection artifacts MUST remain unmodified
