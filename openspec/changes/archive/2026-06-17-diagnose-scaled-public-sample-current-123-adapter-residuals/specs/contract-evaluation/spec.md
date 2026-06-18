## ADDED Requirements

### Requirement: Diagnose scaled-manifest current-123 adapter residuals
The system SHALL publish public-safe diagnosis evidence for strict residuals
observed when the existing current-123 adapter is evaluated on the scaled
formal public sample manifest.

#### Scenario: Generate residual-family diagnosis from scaled prediction evidence
- **WHEN** dev/test gold rows and predictions exist for
  `public-sample-20260617T152259Z` under the scaled A100 recovery prediction
  evidence
- **THEN** the diagnosis MUST group strict residual rows by split, task family,
  source family, residual category, and field path
- **AND** it MUST record the source evidence manifest id, strict exact metrics,
  strict slot metrics, residual row counts, and residual field counts

#### Scenario: Preserve diagnosis-only boundaries
- **WHEN** scaled residual diagnosis evidence is generated
- **THEN** it MUST state that no training, prediction rerun, data mutation,
  prompt change, evaluator relaxation, semantic-equivalence scoring, slot
  normalization, prediction repair, adapter release, checkpoint release,
  production-readiness claim, or live-browser benchmark claim was performed
- **AND** `slot_f1_soft` MUST remain diagnostic only and not become the primary
  metric

#### Scenario: Recommend bounded next decision only
- **WHEN** the diagnosis identifies the dominant scaled-manifest residual
  families or fields
- **THEN** the report MAY recommend a next bounded OpenSpec phase
- **AND** it MUST NOT automatically materialize new data, launch training, or
  change evaluator behavior as part of this diagnosis phase

#### Scenario: Validate public-safe artifacts
- **WHEN** scaled residual diagnosis artifacts, docs, Human Brief HTML, or
  archive files are prepared for commit
- **THEN** validation MUST reject raw private rows, absolute local paths,
  private remote paths, host details, SSH details, raw logs, tokens, secrets,
  private override configs, caches, checkpoints, adapters, and private corpus
  rows
