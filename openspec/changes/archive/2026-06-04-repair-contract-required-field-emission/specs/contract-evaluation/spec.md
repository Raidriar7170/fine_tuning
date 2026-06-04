## ADDED Requirements

### Requirement: Report required-field repair boundaries
The system SHALL publish public-safe repair evidence that separates prompt/guard changes from model-quality, release, and held-out generalization claims.

#### Scenario: Report raw and validated output separately
- **WHEN** required-field guard or retry metadata is available
- **THEN** public reports and Human Briefs MUST separate raw attempt schema validity, retry attempt schema validity, validated output schema validity, and final contract metrics

#### Scenario: Preserve non-claim boundaries
- **WHEN** required-field repair evidence is committed or documented
- **THEN** it MUST state that local prompt/guard repair does not prove A100 improvement, held-out generalization, production readiness, checkpoint release, adapter release, public full-corpus release, or live-browser benchmark improvement
