## ADDED Requirements

### Requirement: Design scaled clarify slot-boundary candidates before materialization
The system SHALL publish a public-safe candidate-design artifact for scaled
clarify slot-boundary residuals before modifying public sample seeds,
generating derived rows, or launching additional training.

#### Scenario: Derive candidates from scaled target-selection evidence
- **WHEN** scaled residual remediation target-selection evidence selects
  `clarify/slots`
- **THEN** the candidate design MUST identify source-family coverage, proposed
  clarify boundary themes, accepted target sketches, rejected drift sketches,
  and suggested public-safe utterance templates
- **AND** it MUST record the source manifest id, source target-selection
  artifact, source cluster-inspection artifact, selected residual row count,
  selected residual field count, and source count consistency

#### Scenario: Preserve clarify target shape
- **WHEN** candidate design covers ambiguous request rows
- **THEN** accepted target sketches MUST preserve `task_type="clarify"`,
  `route="clarify"`, `safety.allow=true`,
  `safety.reason="ambiguous_request"`, `confirmation_required=true`, and a
  non-empty `slots.ambiguity` description
- **AND** rejected drift sketches MUST include variants that incorrectly choose
  `search/search_web`, `navigate/open_url`, `form_fill/fill_form`, or
  `blocked/deny`

#### Scenario: Keep design separate from data mutation
- **WHEN** scaled clarify slot-boundary candidate-design evidence is published
- **THEN** it MUST state that no public seed rows, SFT rows, DPO pairs,
  manifest files, local/private corpora, prompts, evaluator metrics,
  predictions, checkpoints, or adapters were modified
- **AND** it MUST NOT claim model recovery, held-out recovery, safety
  improvement, production readiness, private-corpus generalization, or
  live-browser benchmark improvement

#### Scenario: Recommend bounded materialization only
- **WHEN** the candidate design identifies sufficient candidate coverage
- **THEN** it MAY recommend one later bounded materialization phase
- **AND** it MUST NOT automatically materialize candidates, rebuild public
  sample artifacts, train, run DPO/GRPO, generate predictions, or change
  evaluator behavior as part of the design phase
