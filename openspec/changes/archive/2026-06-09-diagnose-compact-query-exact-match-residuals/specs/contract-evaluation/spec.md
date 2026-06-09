## ADDED Requirements

### Requirement: Publish compact-query exact-match residual diagnosis
The system SHALL publish public-safe local evidence that explains strict exact-match residuals after the compact-query slot-preservation A100 rerun without changing source predictions or evaluator semantics.

#### Scenario: Generate compact-query exact-match residual evidence pack
- **WHEN** the latest compact-query slot-preservation A100 rerun has sanitized predictions, gold targets, metrics, schema guard summary, and manifest artifacts available
- **THEN** the evidence pack MUST include a manifest, machine-readable residual diagnosis, human-readable summary, leak-scan results, source artifact links, inherited strict metrics, row-level residual classifications, validation commands, and explicit non-claims
- **AND** it MUST identify compact-query slot-shape residuals separately from strict `normalized_command` exact-string residuals
- **AND** it MUST record whether `seed-search-weather-aug-1` still predicts decomposed `city/date/topic` slots instead of compact `slots.query`

#### Scenario: Preserve strict source metrics and predictions
- **WHEN** the diagnosis summarizes exact-match residuals
- **THEN** it MUST preserve the source rerun strict metrics and predictions as historical evidence
- **AND** it MUST NOT repair, normalize, replace, re-score, or reinterpret source outputs as exact-match recovery

#### Scenario: Bound compact-query residual diagnosis claims
- **WHEN** reports, Human Briefs, loop reports, or archived OpenSpec artifacts describe the diagnosis
- **THEN** they MUST state that the phase performs no A100 execution, training, prediction rerun, prompt change, decoding change, parser relaxation, evaluator metric change, semantic-equivalence scoring, slot normalization, prediction repair, prediction replacement, or prediction re-score
- **AND** they MUST NOT claim held-out generalization, production readiness, model-quality improvement, model recovery, checkpoint release, adapter release, public full-corpus release, or live-browser benchmark improvement
