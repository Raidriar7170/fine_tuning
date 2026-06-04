## ADDED Requirements

### Requirement: Constrain first-pass contract output emission
The system SHALL make trained-adapter first-pass prediction prompts expose a valid canonical Browser Task Contract one-shot and strict whole-object output boundaries without including row gold targets.

#### Scenario: Build first-pass constrained prediction prompt
- **WHEN** the formatter builds a trained-adapter prediction prompt for an SFT row
- **THEN** the prompt MUST include a valid canonical Browser Task Contract JSON one-shot, legal `task_type` and `route` enum values, required `safety.allow` boolean shape, and instructions that the first non-empty character must be `{`, the last non-empty character must be `}`, and Markdown/prose/code fences are forbidden

#### Scenario: Exclude gold contract from prediction prompt
- **WHEN** a prediction prompt is rendered for a row with a target Browser Task Contract
- **THEN** the prompt MUST NOT include target-only slot values, target-only normalized command text, or the full gold target contract

#### Scenario: Preserve fail-closed schema guard behavior
- **WHEN** raw or retry model output is non-JSON, JSON-fragment wrapped in Markdown/prose, schema-invalid, or uses illegal enum values
- **THEN** the prediction artifact MUST preserve the observed failure and MUST NOT replace it with fixture-mode, rule-baseline, gold-contract, alias-normalized, or locally coerced output

#### Scenario: Accept only schema-valid whole-object output
- **WHEN** first-pass raw model output parses as a whole JSON object and passes `BrowserTaskContract.from_dict()`
- **THEN** the prediction artifact MAY mark `validated_output_source=raw_attempt` and count the prediction as schema-valid
