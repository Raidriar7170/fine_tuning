## MODIFIED Requirements

### Requirement: Publish merged slot value held-out evaluation evidence
The system SHALL publish public-safe evidence for the merged-candidate A100
rerun that separates train learnability from held-out generalization.

#### Scenario: Generate merged-candidate evidence pack
- **WHEN** sanitized merged-candidate train/dev/test predictions, sidecars, and
  metrics are available
- **THEN** the evidence pack MUST record the regenerated manifest ID, formal
  public sample counts, training row counts, split prediction counts,
  `contract_exact_match`, `slot_f1`, schema-valid counts, residual rows, and
  source artifact links

#### Scenario: Compare with prior held-out baseline
- **WHEN** the merged-candidate report is generated
- **THEN** it MUST compare dev/test strict exact against the prior targeted
  family coverage evidence (`1/6` for each split)
- **AND** it MUST identify whether held-out strict exact improved, stayed
  partial, fully recovered on the public sample, or regressed

#### Scenario: Preserve strict metric boundaries
- **WHEN** merged-candidate evidence is described in reports or Human Briefs
- **THEN** strict `contract_exact_match` MUST remain the primary success metric
- **AND** soft slot F1 and semantic equivalence MUST remain diagnostic-only
- **AND** the report MUST NOT repair predictions, replace predictions, relax
  evaluator rules, or re-score prior evidence

#### Scenario: Validate public safety
- **WHEN** merged-candidate evidence is prepared for commit
- **THEN** leak-scan validation MUST reject raw private rows, local or remote
  private paths, secrets, private IP addresses, SSH details, host details, raw
  logs, adapters, checkpoints, caches, model snapshots, oversized generated
  corpora, and private remote paths
