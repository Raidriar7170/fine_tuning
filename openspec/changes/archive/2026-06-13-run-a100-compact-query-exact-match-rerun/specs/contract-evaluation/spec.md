## ADDED Requirements

### Requirement: Publish A100 compact-query exact-match rerun evidence
The system SHALL publish public-safe evidence for the compact-query exact-match A100 rerun that reports strict metrics and residual-family outcomes without relaxing evaluator semantics.

#### Scenario: Generate compact-query exact-match rerun evidence pack
- **WHEN** sanitized rerun predictions, sidecars, metrics, and leak-scan results are available
- **THEN** the evidence pack MUST include a manifest, machine-readable diagnosis, human-readable report, prompt snapshot link, prediction metadata link, sanitized prediction link, metrics link, schema guard summary link, validation commands, leak-scan result, and explicit non-claims
- **AND** it MUST record the public sample manifest id, SFT row count, DPO pair count, prediction split, prediction source kind, overfit diagnostic flag, release status, and output-root placeholder policy

#### Scenario: Compare strict residual families
- **WHEN** rerun metrics and row-level comparisons are computed
- **THEN** the diagnosis MUST classify whether prior compact-query residual families improved, stayed the same, or regressed using strict `contract_exact_match`, strict `slot_f1`, `normalized_command` exact string comparison, and compact `slots.query` shape comparison
- **AND** it MUST specifically report whether public-readonly search predictions use compact `slots.query` or decomposed `city/date/topic` slots
- **AND** any `slot_f1_soft` value MUST be labeled as internal diagnostic context only

#### Scenario: Bound rerun interpretation
- **WHEN** reports, Human Briefs, loop reports, or OpenSpec artifacts describe the rerun
- **THEN** they MUST state that this is A100 public-sample train-split diagnostic evidence
- **AND** they MUST NOT claim dev/test generalization, production readiness, broad model-quality improvement, model recovery, checkpoint release, adapter release, public full-corpus release, live-browser benchmark improvement, parser relaxation, evaluator relaxation, slot normalization, `normalized_command` normalization, semantic-equivalence scoring as a primary metric, prediction repair, prediction replacement, or prediction re-score

#### Scenario: Validate evidence public-safety
- **WHEN** rerun evidence is prepared for commit
- **THEN** leak-scan validation MUST reject raw private rows, absolute local paths, private remote paths, secrets, tokens, private IP addresses, SSH details, raw logs, checkpoints, adapters, caches, model snapshots, oversized generated corpora, and private runtime details
