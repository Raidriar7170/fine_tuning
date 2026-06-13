## ADDED Requirements

### Requirement: Diagnose public SFT contract learning signal
The system SHALL provide a local, public-safe diagnostic that inspects whether public SFT rows expose assistant contract targets with enough structural learning signal before additional heavy SFT reruns are interpreted.

#### Scenario: Inspect rendered SFT targets
- **WHEN** the learning-signal diagnostic runs against the public sample manifest and SFT JSONL
- **THEN** it MUST report row count, split counts, task-family counts, rendered prompt character counts, assistant target character counts, assistant-target ratio, target field/key counts, and max-sequence risk summaries
- **AND** it MUST identify whether each inspected row has a detectable assistant contract target span

#### Scenario: Separate structural target evidence from runtime label evidence
- **WHEN** the diagnostic has not inspected real tokenizer/collator labels from the runtime training path
- **THEN** it MUST mark true runtime label-mask evidence as unavailable
- **AND** it MUST state that structural target-span evidence does not prove that real training labels were applied to those target tokens

#### Scenario: Link prior negative repair evidence
- **WHEN** prior public held-out residual repair evidence exists
- **THEN** the diagnostic MUST read the public-safe manifest or diagnosis summary and include the observed train/dev/test strict metrics as prior context without changing those artifacts

#### Scenario: Bound execution scope
- **WHEN** the diagnostic is run in its default local mode
- **THEN** it MUST NOT download models, load private adapters, start A100 execution, run training, or run prediction

### Requirement: Recommend the next SFT debugging phase from evidence
The system SHALL convert learning-signal findings into a bounded next-step recommendation without widening scope automatically.

#### Scenario: Recommend runtime label inspection
- **WHEN** assistant target spans are structurally present but true runtime label-mask evidence is unavailable
- **THEN** the diagnostic MUST recommend a bounded runtime label inspection or tiny overfit phase before additional full SFT reruns

#### Scenario: Recommend prompt or data repair
- **WHEN** assistant target spans are missing, target pressure is extreme, or prompt budget risk is high
- **THEN** the diagnostic MUST identify the affected rows or task families and recommend a local prompt/data repair phase before heavy training
