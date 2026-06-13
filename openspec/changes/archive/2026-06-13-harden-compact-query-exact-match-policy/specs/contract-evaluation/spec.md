## ADDED Requirements

### Requirement: Publish compact-query exact-match policy hardening evidence
The system SHALL publish public-safe local evidence for compact-query exact-match prompt policy hardening without reinterpreting prior A100 predictions or strict evaluator metrics.

#### Scenario: Generate compact-query exact-match policy hardening evidence pack
- **WHEN** the local prompt policy hardening phase completes
- **THEN** the evidence pack MUST include a manifest, machine-readable policy summary, human-readable report, leak-scan results, source residual-diagnosis links, prompt constraint metadata, public sample target checks, validation commands, and explicit non-claims
- **AND** it MUST record whether compact-query exact-match policy visibility, same-query-phrase alignment visibility, extra-particle avoidance visibility, and decomposed-slot rejection visibility are present
- **AND** it MUST link the prior compact-query exact-match residual diagnosis as historical source evidence without modifying that source evidence

#### Scenario: Preserve prior strict evidence
- **WHEN** the hardening evidence summarizes prior residuals
- **THEN** it MUST preserve prior source predictions, metrics, residual row ids, and field-family counts as historical evidence
- **AND** it MUST NOT repair, normalize, replace, re-score, or reinterpret prior outputs as exact-match recovery

#### Scenario: Bound compact-query hardening evidence claims
- **WHEN** reports, Human Briefs, loop reports, or archived OpenSpec artifacts describe the hardening phase
- **THEN** they MUST state that the phase performs no A100 execution, training, prediction rerun, parser relaxation, strict evaluator metric replacement or relaxation, semantic-equivalence scoring, slot normalization, `normalized_command` normalization, prediction repair, prediction replacement, or prediction re-score
- **AND** they MUST NOT claim held-out generalization, production readiness, model-quality improvement, model recovery, checkpoint release, adapter release, public full-corpus release, or live-browser benchmark improvement

### Requirement: Keep soft slot diagnostics separate from strict metrics
The system SHALL expose soft slot diagnostics only as internal analysis and SHALL keep strict contract metrics authoritative.

#### Scenario: Report slot_f1_soft as internal-only diagnostic
- **WHEN** the evaluator reports `slot_f1_soft`
- **THEN** it MUST continue to report strict `slot_f1` and `contract_exact_match`
- **AND** reports MUST label `slot_f1_soft` as an internal diagnostic rather than strict recovery, production readiness, semantic-equivalence scoring, prediction repair, or prediction re-score
