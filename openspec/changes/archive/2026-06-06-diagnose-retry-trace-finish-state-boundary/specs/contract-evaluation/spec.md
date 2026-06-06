## ADDED Requirements

### Requirement: Diagnose retry trace finish-state boundaries
The system SHALL publish a public-safe local diagnosis that explains retry generation trace finish-state semantics without changing decoding behavior or model outputs.

#### Scenario: Interpret finish state without overclaiming stop reason
- **WHEN** retry generation trace rows show `finish_state=no_eos_observed`
- **THEN** the diagnosis MUST state that tokenizer EOS was not observed in the generated token slice and MUST NOT claim the actual generation stop reason unless the evidence directly records model/generation-config stop reason

#### Scenario: Report max-token evidence
- **WHEN** retry generated token counts are below `max_new_tokens`
- **THEN** the diagnosis MUST report per-row generated token count, max token limit, max-token-hit status, EOS visibility, and finish state

#### Scenario: Preserve local diagnostic boundaries
- **WHEN** public documentation or Human Briefs describe the diagnosis
- **THEN** they MUST state that the phase performs no A100 execution, prediction rerun, training, decoding behavior change, retry prompt change, parser relaxation, evaluator metric change, prediction repair, semantic-equivalence scoring, model-quality claim, public full-corpus release, or live-browser benchmark improvement claim
