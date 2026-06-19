## ADDED Requirements

### Requirement: Publish canonical slot-boundary formal-merge proposal readiness
The system SHALL publish proposal/readiness evidence before any formal public
sample merge of reviewed canonical slot-boundary candidates.

#### Scenario: Generate proposal readiness artifacts
- **WHEN** the canonical slot-boundary formal-merge proposal phase is applied
- **THEN** it MUST write machine-readable readiness evidence and a
  human-readable summary under
  `reports/public-sample/canonical-slot-boundary-formal-merge-proposal/`
- **AND** the output MUST cite
  `reports/public-sample/canonical-slot-boundary-candidate-review/summary.json`
  as its source review evidence.

#### Scenario: Fail closed without row-level candidate source
- **WHEN** no reviewed row-level candidate seed source exists for formal merge
- **THEN** the readiness evidence MUST set `formal_merge_ready_now=false`
- **AND** it MUST set
  `formal_merge_readiness="not_ready_missing_row_level_candidate_source"`
- **AND** it MUST NOT mutate formal public sample data, generate JSONL seed
  candidates, generate SFT/DPO rows, rebuild manifests, or change splits.

#### Scenario: Preserve reviewed eligibility boundaries
- **WHEN** future merge eligibility is summarized
- **THEN** only `slot_key_aliases` and `slot_value_boundaries` MAY be listed as
  eligible future merge classes
- **AND** `normalized_command_display_diagnostic` MUST remain
  diagnostic/display-only
- **AND** excluded non-equivalence cases MUST remain blocked or deferred.

#### Scenario: Define future formal merge acceptance criteria
- **WHEN** proposal readiness evidence recommends a future data phase
- **THEN** it MUST require an exact reviewed row-level candidate source, public
  safety validation, duplicate/source-id validation, derived SFT/DPO/manifest
  synchronization, split-boundary accounting, and comparison-boundary warnings
- **AND** it MUST state that old metrics cannot be compared directly after a
  future formal sample boundary change.

#### Scenario: Preserve proposal-only execution boundary
- **WHEN** proposal readiness evidence is generated
- **THEN** it MUST state and machine-record that formal public sample seed
  traces, SFT rows, DPO pairs, manifests, train/dev/test splits, evaluator
  definitions, predictions, and model artifacts remain unchanged
- **AND** it MUST NOT train, predict, run on A100, implement a deterministic
  postprocessor, relax strict exact, use an LLM judge, perform
  semantic-equivalence scoring, repair predictions, or claim model
  improvement.

#### Scenario: Validate public-safe proposal artifacts
- **WHEN** proposal artifacts, docs, Human Brief HTML, or archive files are
  prepared for commit
- **THEN** validation MUST reject raw private rows, absolute local paths,
  private remote paths, host details, SSH details, raw logs, tokens, secrets,
  checkpoints, adapters, caches, and private corpus rows
- **AND** the source candidate review/materialization artifacts and the stale
  active `merge-scaled-clarify-slot-boundary-candidates` change MUST remain
  unmodified unless a separate bounded phase explicitly owns them.
