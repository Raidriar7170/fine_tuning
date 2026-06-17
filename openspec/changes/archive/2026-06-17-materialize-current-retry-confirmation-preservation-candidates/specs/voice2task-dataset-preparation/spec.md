## ADDED Requirements

### Requirement: Materialize reviewed current-retry confirmation-preservation candidates
The system SHALL materialize reviewed current-retry confirmation-preservation candidates into public-safe train seed rows and synchronized public derived artifacts while preserving data-only evidence boundaries.

#### Scenario: Materialize exactly reviewed candidate families
- **WHEN** the materialization phase reads the current-retry confirmation-preservation candidate design evidence
- **THEN** it MUST validate the design manifest id and materialize exactly the reviewed candidate families
- **AND** it MUST reject missing, extra, duplicate, unreviewed, or already-merged candidate rows
- **AND** each materialized seed MUST include provenance linking back to the source design, source candidate id, candidate family, source row ids, and accepted target sketch

#### Scenario: Preserve accepted confirmation targets
- **WHEN** unsafe-payment confirmation-preservation candidates are materialized
- **THEN** each accepted target contract MUST use `task_type=blocked`, `route=deny`, `safety.reason="unsafe_payment"`, and `confirmation_required=true`
- **AND** the materialization evidence MUST preserve the source row ids and rejected drift sketches for auditability
- **WHEN** public-navigation non-confirmation preservation candidates are materialized
- **THEN** each accepted target contract MUST use `task_type=navigate`, `route=open_url`, `safety.reason="public_readonly"`, and `confirmation_required=false`
- **AND** the materialization evidence MUST preserve the source row ids and rejected drift sketches for auditability

#### Scenario: Rebuild public sample artifacts
- **WHEN** confirmation-preservation candidate seed rows are materialized
- **THEN** the system MUST rebuild the public manifest, SFT rows, and DPO pairs from the updated formal public seed file
- **AND** the new manifest MUST record the updated seed, SFT, DPO, and split counts
- **AND** the materialization evidence MUST record pre-materialization and post-materialization counts plus candidate seed, SFT, and DPO contributions

#### Scenario: Preserve materialization-only boundaries
- **WHEN** materialization evidence, reports, or Human Briefs describe the phase
- **THEN** they MUST state that no training, prediction generation, prediction repair, prompt change, evaluator metric change, slot normalization, adapter release, checkpoint release, live-browser benchmark, or private corpus publication occurred
- **AND** they MUST NOT claim model recovery, held-out recovery, safety improvement, production readiness, or semantic-equivalence recovery
