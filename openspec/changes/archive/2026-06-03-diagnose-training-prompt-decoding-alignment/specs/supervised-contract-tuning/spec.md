## ADDED Requirements

### Requirement: Expose contract value constraints in SFT prompts
The system SHALL make the model-visible SFT training and prediction prompt explicitly state the legal Browser Task Contract task type and route values, route non-path semantics, and object-shaped slots requirement.

#### Scenario: Serialize constrained SFT training examples
- **WHEN** the formatter converts an SFT dataset row into training text
- **THEN** the system prompt in the rendered text MUST include the allowed `task_type` values, allowed `route` values, a statement that `route` is not a URL or path, and a statement that `slots` must be a JSON object rather than an array

#### Scenario: Serialize constrained prediction prompts
- **WHEN** the formatter builds a trained-adapter prediction prompt
- **THEN** the prompt MUST include the same contract value constraints and MUST NOT include the gold target contract

### Requirement: Record decoding policy for trained-adapter prediction
The system SHALL record public-safe decoding policy metadata for trained-adapter prediction exports without implying that decoding constraints repair model output.

#### Scenario: Export prediction metadata with decoding policy
- **WHEN** trained-adapter prediction metadata is produced
- **THEN** it MUST record greedy decoding status, configured `max_new_tokens`, raw decoded sidecar availability, and schema repair status using public-safe values

#### Scenario: Preserve raw model-output status
- **WHEN** a private adapter prediction is generated or metadata is written
- **THEN** the metadata MUST state that schema repair is not applied and MUST NOT claim that invalid predictions were converted into valid Browser Task Contracts
