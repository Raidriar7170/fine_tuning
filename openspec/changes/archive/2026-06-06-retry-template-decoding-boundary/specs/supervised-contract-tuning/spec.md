## ADDED Requirements

### Requirement: Harden schema-retry template decoding boundary
The system SHALL expose a machine-only schema-retry template boundary for retry prompts without changing strict parser, evaluator, training, or prediction repair behavior.

#### Scenario: Build machine-only retry template
- **WHEN** the schema-retry prompt is generated for a schema-invalid raw attempt
- **THEN** the prompt MUST identify the retry as a machine-only contract regeneration step, require exactly one root Browser Task Contract JSON object, prohibit explanatory dialogue/wrapper text, and preserve the existing strict JSON-only field and enum requirements

#### Scenario: Report retry template boundary visibility
- **WHEN** prediction metadata or prompt snapshots summarize retry behavior
- **THEN** they MUST expose machine-readable booleans for retry template mode, machine-only output boundary, no conversational answer mode, strict whole-object parser boundary, and whether chat-template wrapping is explicitly documented for the retry prompt

#### Scenario: Preserve strict parser behavior
- **WHEN** a retry response contains a valid Browser Task Contract embedded inside Markdown, prose, wrapper text, or explanatory text
- **THEN** the strict retry parser MUST continue to reject it as a non-whole JSON-object retry attempt rather than extracting, repairing, coercing, normalizing, re-scoring, or replacing the embedded fragment

#### Scenario: Keep phase local
- **WHEN** retry template boundary hardening is implemented
- **THEN** the phase MUST NOT run A100 prediction, train a model, release an adapter/checkpoint, change evaluator metrics, relax parsing, repair predictions, rewrite prior A100 artifacts, or claim model-quality improvement
