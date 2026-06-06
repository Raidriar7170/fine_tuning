## ADDED Requirements

### Requirement: Publish search query slot target policy evidence
The system SHALL publish public-safe evidence that the canonical public-readonly search query slot target policy is visible in prompts and aligned in public sample targets without re-scoring historical predictions.

#### Scenario: Generate search query slot policy evidence pack
- **WHEN** the local policy phase completes
- **THEN** the evidence pack MUST include prompt constraint metadata, public sample row checks, DPO chosen/rejected contract checks, source links, validation commands, leak-scan results, and explicit non-claims
- **AND** it MUST record that no A100 execution, training, prediction rerun, evaluator change, parser change, semantic-equivalence scoring, slot normalization, prediction repair, prediction replacement, or re-score was performed

#### Scenario: Bound policy interpretation
- **WHEN** evidence, Human Briefs, loop reports, or archived OpenSpec artifacts describe the search query slot target policy
- **THEN** they MUST state that prior A100 predictions remain historical evidence and are not repaired, normalized, re-scored, or reinterpreted as exact-match recovery
- **AND** they MUST NOT claim held-out generalization, production readiness, model-quality improvement, checkpoint release, adapter release, public full-corpus release, or live-browser benchmark improvement
