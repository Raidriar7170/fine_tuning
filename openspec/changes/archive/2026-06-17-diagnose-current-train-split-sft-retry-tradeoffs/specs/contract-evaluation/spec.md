## ADDED Requirements

### Requirement: Publish current SFT retry trade-off diagnosis evidence
The system SHALL publish public-safe diagnosis evidence that compares the
current-train-split SFT retry against the current-manifest prediction-only
baseline before recommending any further model-quality phase.

#### Scenario: Compare baseline and retry row-level outcomes
- **WHEN** baseline and current retry dev/test predictions exist for the same
  current manifest row ids
- **THEN** the diagnosis MUST compare row-level contract equality, task type,
  route, safety, confirmation, and slot outcomes across the baseline and retry
- **AND** it MUST summarize recoveries, regressions, persistent failures, and
  unchanged successes by split

#### Scenario: Explain observed trade-offs without changing metrics
- **WHEN** diagnosis evidence is prepared for commit
- **THEN** it MUST explain the observed safety, confirmation, exact-match,
  route/task-type, and slot trade-offs using existing strict evaluation outputs
- **AND** it MUST keep strict `contract_exact_match` and strict `slot_f1` as
  public headline metrics while labeling `slot_f1_soft` diagnostic-only

#### Scenario: Preserve diagnosis-only boundaries
- **WHEN** current retry trade-off diagnosis evidence is published
- **THEN** it MUST state that no training, prediction generation, DPO, GRPO,
  dataset mutation, evaluator relaxation, semantic-equivalence scoring, slot
  normalization, prediction repair, prompt change, checkpoint release, adapter
  release, live-browser benchmark, held-out recovery claim, or
  production-readiness claim occurred
- **AND** leak-scan validation MUST reject raw private rows, absolute local
  paths, private remote paths, host details, SSH details, secrets, tokens, raw
  logs, checkpoints, adapters, caches, and oversized generated corpora

#### Scenario: Recommend a bounded next action
- **WHEN** the diagnosis identifies the dominant remaining trade-off or
  residual cluster
- **THEN** it MAY recommend one next bounded OpenSpec phase
- **AND** it MUST NOT automatically launch training, modify public sample data,
  change evaluator behavior, or publish model artifacts as part of the
  diagnosis phase
