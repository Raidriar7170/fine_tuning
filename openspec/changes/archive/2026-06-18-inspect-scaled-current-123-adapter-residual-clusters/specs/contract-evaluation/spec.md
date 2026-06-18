## ADDED Requirements

### Requirement: Inspect scaled-manifest current-123 adapter residual clusters
The system SHALL publish public-safe cluster-inspection evidence for strict
residuals observed when the existing current-123 adapter is evaluated on the
scaled formal public sample manifest.

#### Scenario: Generate cluster inspection from scaled residual diagnosis
- **WHEN** the scaled residual-family diagnosis exists for
  `public-sample-20260617T152259Z`
- **THEN** the cluster inspection MUST group residual fields into actionable
  clusters by task family, source family, field path, residual category, and
  repeated mismatch pattern
- **AND** it MUST record top cluster rows, top cluster fields, source residual
  row/field count consistency, and source diagnosis artifact links

#### Scenario: Preserve strict metric and diagnosis-only boundaries
- **WHEN** scaled residual-cluster evidence is generated
- **THEN** it MUST state that no A100 job, training, prediction rerun, data
  mutation, prompt change, evaluator relaxation, semantic-equivalence scoring,
  slot normalization, prediction repair, DPO/GRPO run, adapter release,
  checkpoint release, production-readiness claim, or live-browser benchmark
  claim was performed
- **AND** `slot_f1_soft` MUST remain diagnostic only and not become the primary
  metric

#### Scenario: Recommend bounded next decision only
- **WHEN** the cluster inspection identifies dominant scaled-manifest residual
  clusters
- **THEN** it MAY recommend a later OpenSpec phase for data design,
  materialization, policy hardening, or training readiness
- **AND** it MUST NOT materialize data, launch training, or change evaluator
  behavior in this phase

#### Scenario: Validate public-safe cluster artifacts
- **WHEN** scaled residual-cluster artifacts, docs, Human Brief HTML, or archive
  files are prepared for commit
- **THEN** validation MUST reject raw private rows, absolute local paths,
  private remote paths, host details, SSH details, raw logs, tokens, secrets,
  private override configs, caches, checkpoints, adapters, and private corpus
  rows
