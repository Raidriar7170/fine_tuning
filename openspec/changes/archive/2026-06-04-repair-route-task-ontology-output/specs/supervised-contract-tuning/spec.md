## ADDED Requirements

### Requirement: Expose route ontology constraints in SFT prompts
The system SHALL make SFT training and trained-adapter prediction prompts explicitly distinguish Browser Task Contract `route` execution-channel enum values from domains, topics, intents, URLs, or paths.

#### Scenario: Serialize training prompt with route ontology
- **WHEN** the formatter converts an SFT dataset row into training text
- **THEN** the system prompt in the rendered text MUST state that `route` is an execution channel from the allowed enum and MUST state that weather, shopping, email, media, URL hosts, and other domain/topic values belong in `task_type`, `slots`, or `normalized_command` rather than `route`

#### Scenario: Serialize prediction prompt with route ontology
- **WHEN** the formatter builds a trained-adapter prediction prompt
- **THEN** the prompt MUST include the same route ontology constraints and MUST NOT include the row-specific gold target contract

#### Scenario: Represent weather requests without inventing routes
- **WHEN** route ontology examples are visible in SFT or prediction prompts
- **THEN** they MUST show that a weather-style information request uses `task_type="search"` and `route="search_web"` rather than `route="weather"`
