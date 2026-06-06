## ADDED Requirements

### Requirement: Tighten schema-retry JSON-only output boundary
The system SHALL strengthen the local schema-retry prompt/output-boundary policy without changing strict parser, evaluator, training, or prediction repair behavior.

#### Scenario: Publish stricter retry prompt clauses
- **WHEN** the schema-retry prompt is generated for a schema-invalid raw attempt
- **THEN** the prompt MUST explicitly require the retry response to be exactly one JSON object, start with `{`, end with `}`, contain no Markdown/code fences/prose/prefix/suffix/trailing analysis, avoid second JSON objects, and avoid natural-language introductions such as Chinese "this/following" prefixes or "Here is"

#### Scenario: Report retry prompt boundary visibility
- **WHEN** retry prompt constraints are summarized in prediction metadata or prompt snapshots
- **THEN** the summary MUST expose machine-readable booleans for the stricter JSON-only boundary clauses, including exact-only output, no Markdown/code fences, no natural-language preface, no suffix/trailing analysis, no second object, and strict-parser rejection visibility

#### Scenario: Preserve strict retry parsing
- **WHEN** a retry response contains a valid Browser Task Contract embedded inside Markdown, prose, or other wrapper text
- **THEN** the strict parser MUST continue to reject it as a non-whole JSON-object retry attempt rather than extracting, repairing, coercing, normalizing, or re-scoring the embedded fragment

#### Scenario: Keep local phase private-runtime free
- **WHEN** this local retry boundary hardening phase is implemented
- **THEN** it MUST NOT run A100 prediction, train a model, release an adapter/checkpoint, change decoding parameters, change evaluator metrics, or rewrite prior A100 artifacts
