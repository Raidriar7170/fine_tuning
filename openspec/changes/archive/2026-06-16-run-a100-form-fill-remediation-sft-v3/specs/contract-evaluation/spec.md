## ADDED Requirements

### Requirement: Publish SFT v3 strict held-out evidence
The system SHALL publish public-safe dev/test prediction-only evidence for the
private SFT v3 adapter using the existing strict contract evaluation ladder.

#### Scenario: Evaluate SFT v3 dev and test splits
- **WHEN** sanitized SFT v3 predictions are available for the current public
  dev and test splits
- **THEN** the system MUST evaluate them with the existing strict metrics,
  including `contract_exact_match`, strict `slot_f1`, `task_type_accuracy`,
  `route_accuracy`, `safety_precision`, `safety_recall`,
  `confirmation_accuracy`, and `json_valid_rate`
- **AND** it MUST record the manifest id, split row counts, prediction source
  kind, and training config identity

#### Scenario: Keep diagnostic metrics bounded
- **WHEN** SFT v3 evidence reports include `slot_f1_soft`
- **THEN** they MUST label it as diagnostic-only
- **AND** they MUST NOT treat it as the public headline metric or as evidence
  of semantic-equivalence recovery

#### Scenario: Preserve evidence boundary
- **WHEN** SFT v3 held-out evidence is prepared for commit
- **THEN** committed artifacts MUST state whether strict metrics improved,
  regressed, or remained partial relative to the current prediction-only
  baseline
- **AND** committed artifacts MUST NOT claim checkpoint release, adapter
  release, production readiness, public full-corpus release,
  private-corpus generalization, or live-browser benchmark improvement
- **AND** leak-scan validation MUST reject raw private rows, absolute local
  paths, private remote paths, host details, SSH details, secrets, tokens, raw
  logs, checkpoints, adapters, caches, and oversized generated corpora

#### Scenario: Record blocked SFT v3 execution safely
- **WHEN** training, prediction, evaluation, GPU preflight, or private override
  setup cannot safely complete
- **THEN** the evidence MUST record a blocked status without fabricating
  predictions, metrics, adapters, or model-quality claims
