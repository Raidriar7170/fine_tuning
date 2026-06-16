## ADDED Requirements

### Requirement: Publish SFT v3 safety regression diagnosis evidence
The system SHALL publish public-safe diagnosis evidence for the SFT v3 retry
safety regression before interpreting the retry as a safety improvement or
launching another training phase.

#### Scenario: Diagnose gold stop rows
- **WHEN** the diagnosis reads current formal public held-out gold rows and
  baseline/retry predictions
- **THEN** it MUST identify gold stop rows and report safety true positives,
  false negatives, false positives, and true negatives for each compared run
- **AND** it MUST include support counts alongside safety rates

#### Scenario: Compare baseline and retry safety outcomes
- **WHEN** baseline and SFT v3 retry predictions exist for the same row id
- **THEN** the diagnosis MUST classify the row as `regressed`, `recovered`,
  `persistent_miss`, `stable_correct`, or `unchanged_non_stop` for safety
  outcome comparison
- **AND** it MUST aggregate those classifications by split and task family

#### Scenario: Preserve diagnosis-only boundaries
- **WHEN** safety regression diagnosis evidence is prepared for commit
- **THEN** it MUST state that the phase performs no training, prediction
  generation, evaluator relaxation, semantic-equivalence scoring, data
  mutation, prediction repair, prompt change, checkpoint release, adapter
  release, live-browser benchmark, or production-readiness claim
- **AND** leak-scan validation MUST reject raw private rows, absolute local
  paths, private remote paths, host details, SSH details, secrets, tokens, raw
  logs, checkpoints, adapters, caches, and oversized generated corpora

#### Scenario: Recommend bounded next action
- **WHEN** the diagnosis identifies a likely safety failure cluster
- **THEN** it MAY recommend a next bounded OpenSpec phase
- **AND** it MUST NOT automatically materialize new data, change safety policy,
  launch training, or change evaluator behavior as part of the diagnosis phase
