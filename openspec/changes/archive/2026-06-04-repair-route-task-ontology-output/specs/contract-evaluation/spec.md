## ADDED Requirements

### Requirement: Publish local route ontology repair evidence
The system SHALL publish public-safe local evidence for route ontology prompt repairs that distinguishes prompt readiness from model-output recovery.

#### Scenario: Generate local repair evidence
- **WHEN** a local route ontology repair phase completes
- **THEN** the evidence pack MUST record the prompt constraint summary, affected prompt surface, validation commands, and links to prior failure evidence without launching or implying private A100 execution

#### Scenario: Bound local repair interpretation
- **WHEN** public reports or Human Briefs describe local route ontology repair evidence
- **THEN** they MUST state that the phase did not train, did not run private adapter prediction, did not repair or coerce model outputs, and does not prove model recovery, held-out generalization, checkpoint release, adapter release, production readiness, public full-corpus release, or live-browser benchmark improvement
