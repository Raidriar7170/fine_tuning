## ADDED Requirements

### Requirement: Publish retry template boundary evidence
The system SHALL publish public-safe local evidence for schema-retry template/decoding-boundary hardening while preserving strict metrics, prior A100 evidence interpretation, and non-claim boundaries.

#### Scenario: Generate local retry template evidence pack
- **WHEN** the local retry template boundary phase completes
- **THEN** the evidence pack MUST include a manifest, summary report, leak-scan results, source links to the prior retry JSON-only hardening and A100 retry JSON-only rerun, retry template boundary metadata, focused test evidence, validation commands, and explicit non-claims

#### Scenario: Bound interpretation of local template hardening
- **WHEN** public documentation or Human Briefs describe the retry template boundary phase
- **THEN** they MUST state that the phase performs no A100 execution, training, checkpoint release, adapter release, parser relaxation, evaluator metric change, semantic-equivalence scoring, slot normalization, prediction repair, prediction re-score, held-out generalization claim, model recovery claim, model-quality claim, public full-corpus release, or live-browser benchmark improvement claim

#### Scenario: Preserve prior A100 evidence interpretation
- **WHEN** the evidence pack references the prior A100 retry JSON-only boundary rerun
- **THEN** it MUST state that the prior strict final metrics remain `json_valid_rate=0.0` and `contract_exact_match=0.0`, retry attempts remained wrapped fragments, and this local phase does not prove any change in trained-adapter output behavior until a later real A100 rerun is performed
