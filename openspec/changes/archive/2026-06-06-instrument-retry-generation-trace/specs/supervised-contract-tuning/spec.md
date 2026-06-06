## ADDED Requirements

### Requirement: Instrument retry generation trace attempts
The system SHALL record attempt-level generation trace rows for trained-adapter prediction exports whenever schema retry is attempted.

#### Scenario: Record raw and retry trace rows
- **WHEN** a real trained-adapter prediction export runs with generation trace sidecars enabled and a schema-invalid raw attempt triggers schema retry
- **THEN** `generation_trace.jsonl` MUST include one `attempt=raw_attempt` row and one `attempt=retry_attempt` row for that input id, using the same token count, EOS visibility, max-token limit, strategy, and finish-state fields for each attempt

#### Scenario: Preserve retry behavior
- **WHEN** retry generation trace instrumentation is added
- **THEN** the system MUST NOT change retry prompt text, decoding parameters, strict parser semantics, schema guard source selection, final predictions, evaluator metrics, output repair behavior, or prediction re-scoring

#### Scenario: Keep historical evidence bounded
- **WHEN** public documentation or evidence describes retry generation trace instrumentation
- **THEN** it MUST state that historical A100 traces are not retroactively instrumented and that a future A100/private-adapter rerun is required to observe real retry stop-boundary behavior
