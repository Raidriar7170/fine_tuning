## ADDED Requirements

### Requirement: Publish retry generation trace instrumentation evidence
The system SHALL publish public-safe local evidence that retry generation trace instrumentation is available for future trained-adapter prediction exports without changing strict evaluation semantics.

#### Scenario: Generate instrumentation evidence pack
- **WHEN** the instrumentation phase is complete
- **THEN** the evidence pack MUST record source diagnosis links, generated artifacts, validation commands, leak-scan results, local test evidence for raw and retry attempt trace rows, and non-claim boundaries

#### Scenario: Bound instrumentation claims
- **WHEN** evidence, reports, tests, specs, or Human Briefs describe this phase
- **THEN** they MUST state that no A100 execution, training, private prediction rerun, decoding change, parser relaxation, evaluator metric change, prediction repair, prediction re-score, semantic-equivalence scoring, slot normalization, checkpoint release, adapter release, model recovery claim, model-quality claim, or live-browser benchmark improvement claim is made

#### Scenario: Preserve historical A100 interpretation
- **WHEN** the instrumentation evidence references prior A100 retry-wrapper artifacts
- **THEN** it MUST state that prior A100 `generation_trace.jsonl` files only prove their recorded fields and are not rewritten or upgraded by this local instrumentation phase
