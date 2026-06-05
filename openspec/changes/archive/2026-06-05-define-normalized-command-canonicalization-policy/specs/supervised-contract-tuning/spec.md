## ADDED Requirements

### Requirement: Expose normalized-command canonicalization policy in SFT prompts
The system SHALL make SFT training text and trained-adapter prediction prompts expose a conservative `normalized_command` target-writing policy without including row-specific gold targets in prediction prompts.

#### Scenario: Serialize policy in SFT training text
- **WHEN** the formatter converts an SFT dataset row into training text
- **THEN** the rendered system prompt MUST state that `normalized_command` should be a concise canonical Chinese intent phrase rather than a verbatim transcript or ASR text

#### Scenario: Serialize policy in prediction prompts without gold leakage
- **WHEN** the formatter builds a trained-adapter prediction prompt
- **THEN** the prompt MUST include the same canonicalization guidance and MUST NOT include the row-specific gold target contract

#### Scenario: Show canonical examples without metric relaxation
- **WHEN** the shared prompt describes `normalized_command` examples
- **THEN** it MUST show current first-phase examples such as search/weather, navigation, confirmation-required form fill, and unsafe payment denial while stating that exact-match evaluation remains strict and predictions are not repaired or semantically re-scored

#### Scenario: Bound canonicalization-prompt claims
- **WHEN** public documentation or Human Briefs describe this prompt policy
- **THEN** they MUST NOT claim A100 execution, training or prediction rerun, evaluator metric change, semantic-equivalence scoring, checkpoint release, adapter release, held-out generalization, production readiness, public full-corpus release, model-quality improvement, or live-browser benchmark improvement
