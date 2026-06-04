## ADDED Requirements

### Requirement: Publish constrained-output repair evidence
The system SHALL publish a public-safe local evidence pack for constrained-output repair that records prompt constraint coverage, strict schema acceptance boundaries, validation status, and non-claim boundaries before any later A100 rerun.

#### Scenario: Generate constrained-output repair evidence
- **WHEN** the constrained-output repair is implemented and local validation passes
- **THEN** the evidence pack MUST record prompt constraint coverage, canonical one-shot visibility, gold-target exclusion, strict retry preservation, schema-valid whole-object acceptance, and validation commands without private runtime details

#### Scenario: Keep constrained-output repair evidence public-safe
- **WHEN** constrained-output repair evidence, Human Briefs, or loop reports are prepared for commit
- **THEN** leak-scan validation MUST reject raw private rows, local or remote private paths, secrets, private IP addresses, SSH details, raw logs, checkpoints, adapters, model caches, oversized generated corpora, and private remote paths

#### Scenario: Bound constrained-output repair interpretation
- **WHEN** public reports, metrics reports, Human Briefs, or loop reports describe the constrained-output repair
- **THEN** they MUST state that local prompt/output-shape hardening does not prove dev/test generalization, production readiness, checkpoint release, adapter release, public full-corpus release, A100 model recovery, or live-browser benchmark improvement

#### Scenario: Recommend later A100 rerun only after local repair
- **WHEN** constrained-output repair evidence is reviewed
- **THEN** the recommended next A100 step, if any, MUST be framed as a later explicitly authorized prediction rerun rather than evidence already produced by this local repair phase
