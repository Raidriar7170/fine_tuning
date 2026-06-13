## ADDED Requirements

### Requirement: Harden compact-query exact-match prompt policy
The system SHALL make the shared SFT training and trained-adapter prediction prompt explicitly align public-readonly search/weather `normalized_command` and `slots.query` target formatting without changing parser or evaluator semantics.

#### Scenario: Serialize compact-query exact-match policy
- **WHEN** SFT training text or a trained-adapter prediction prompt is rendered for a Browser Task Contract
- **THEN** the model-visible system prompt MUST state that public-readonly search/weather contracts use `normalized_command="搜索" + <compact query phrase>` and `slots.query=<same compact query phrase>`
- **AND** it MUST state that compact query phrases do not insert extra particles such as `的` when the canonical target phrase omits them
- **AND** it MUST state that the model MUST NOT split the same search query into ad hoc `city`, `date`, `topic`, or similar keys
- **AND** it MUST state that this is target-formatting guidance, not evaluator normalization, semantic-equivalence scoring, prediction repair, prediction replacement, or re-score

#### Scenario: Show non-row-specific accepted and rejected examples
- **WHEN** the prompt demonstrates compact-query exact-match formatting
- **THEN** it MUST include non-row-specific examples showing an accepted compact `slots.query` contract shape and a rejected decomposed `city/date/topic` shape
- **AND** the examples MUST NOT include row-specific gold target strings for the current prediction row unless those strings are already present in the user input

#### Scenario: Surface compact-query exact-match policy metadata
- **WHEN** prompt constraint metadata is recorded in prediction metadata, prompt snapshots, manifests, reports, or evidence packs
- **THEN** it MUST include booleans for compact-query exact-match policy visibility, same-query-phrase alignment visibility, extra-particle avoidance visibility, and decomposed-slot rejection visibility

#### Scenario: Bound local prompt-hardening interpretation
- **WHEN** public documentation, reports, Human Briefs, or OpenSpec artifacts describe this prompt hardening
- **THEN** they MUST state that the phase performs no A100 execution, training, prediction rerun, parser relaxation, strict evaluator metric replacement or relaxation, semantic-equivalence scoring, slot normalization, `normalized_command` normalization, prediction repair, prediction replacement, or prediction re-score
- **AND** they MUST NOT claim held-out generalization, production readiness, model-quality improvement, model recovery, checkpoint release, adapter release, public full-corpus release, or live-browser benchmark improvement

#### Scenario: Preserve SFT training sequence budget
- **WHEN** SFT training text is rendered for public sample rows
- **THEN** it MUST retain the compact-query exact-match target-formatting policy
- **AND** it MAY omit prediction-only one-shot examples when needed to keep training text within the configured local sequence budget
- **AND** trained-adapter prediction prompts MUST still retain prediction-only one-shot and output-boundary guidance
