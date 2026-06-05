## ADDED Requirements

### Requirement: Clarify strict normalized-command string-mismatch interpretation
The system SHALL make public-facing evaluation and evidence surfaces explain that `normalized_command` string mismatches are strict exact-match evidence unless a separately scoped metric explicitly defines normalization or semantic equivalence.

#### Scenario: Publish README interpretation boundary
- **WHEN** public documentation references `normalized_command` string mismatches or `contract_exact_match`
- **THEN** it MUST state that `contract_exact_match` remains a strict exact-match metric and that string differences are not automatically treated as semantic equivalents

#### Scenario: Publish evidence-pack interpretation boundary
- **WHEN** a public evidence pack explains the confirmation-rerun normalized-command string mismatch diagnosis
- **THEN** it MUST include a reviewer-facing policy note that distinguishes explanatory row-level string evidence from metric changes, prediction repair, normalization, semantic-equivalence scoring, or re-scoring

#### Scenario: Bound claims for strict string mismatch policy
- **WHEN** README, evidence notes, Human Briefs, loop reports, or archived OpenSpec artifacts describe the strict string mismatch policy
- **THEN** they MUST NOT claim A100 execution, training or prediction rerun, prompt change, evaluator metric change, checkpoint release, adapter release, held-out generalization, production readiness, public full-corpus release, model-quality improvement, or live-browser benchmark improvement

#### Scenario: Validate public-surface wording
- **WHEN** the strict string mismatch policy is prepared for commit
- **THEN** focused tests MUST verify that public-facing surfaces preserve the strict exact-match boundary and the no-semantic-equivalence/no-metric-change boundary
