## ADDED Requirements

### Requirement: Expose canonical search query slot target policy
The system SHALL make the shared SFT training and trained-adapter prediction prompt explicitly state the canonical slot target policy for public-readonly search/weather contracts without changing parser or evaluator semantics.

#### Scenario: Serialize prompt with compact query slot policy
- **WHEN** SFT training text or trained-adapter prediction prompt is rendered for public-readonly information lookup or weather search
- **THEN** the model-visible system prompt MUST state that search contracts use object-shaped `slots.query`
- **AND** it MUST state that the model MUST NOT split the same search query into ad hoc `city`, `date`, `topic`, or similar keys
- **AND** it MUST state that ordinary Chinese search query strings should be compact phrases such as `北京明天天气`, not artificial token-spaced strings such as `北京 明天 天气`
- **AND** it MUST state that this is target formatting guidance, not evaluator normalization, semantic-equivalence scoring, prediction repair, or re-score

#### Scenario: Surface search query slot policy metadata
- **WHEN** prompt constraint metadata is recorded in prediction metadata, prompt snapshots, manifests, reports, or evidence packs
- **THEN** it MUST include booleans for compact search query slot policy visibility and no-`city/date` search slot splitting visibility
