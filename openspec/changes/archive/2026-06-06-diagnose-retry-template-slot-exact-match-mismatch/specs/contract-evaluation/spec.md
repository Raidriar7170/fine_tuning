## ADDED Requirements

### Requirement: Publish retry-template slot exact-match mismatch diagnosis
The system SHALL publish public-safe row-level diagnosis evidence for the residual exact-match failures after the A100 retry-template boundary rerun without changing source predictions, prompt behavior, decoding behavior, schema behavior, parser behavior, retry behavior, evaluator metrics, or source strict metric interpretation.

#### Scenario: Derive slot mismatch diagnosis from prior public artifacts
- **WHEN** the diagnosis is generated
- **THEN** it MUST derive only from `reports/public-sample/a100-retry-template-boundary-rerun/` public-safe artifacts
- **AND** it MUST record `diagnostic_kind=retry_template_slot_exact_match_mismatch_diagnosis`
- **AND** it MUST preserve source strict metrics including `json_valid_rate=1.0`, `contract_exact_match=0.0`, `task_type_accuracy=1.0`, `route_accuracy=1.0`, `confirmation_accuracy=1.0`, and `slot_f1=0.0`

#### Scenario: Classify residual slot exact-match failures
- **WHEN** row-level failures are reported
- **THEN** the diagnosis MUST report all three train rows and classify the residual slot mismatch families as two rows with `city/date` slot shape instead of gold `query` and one row with a `query` slot exact-string mismatch
- **AND** it MUST report normalized-command exact-string mismatch context when present
- **AND** field-level gold and prediction summaries MUST remain visible for reviewer inspection

#### Scenario: Bound slot diagnosis claims
- **WHEN** evidence, Human Briefs, loop reports, or archived OpenSpec artifacts describe the slot mismatch diagnosis
- **THEN** they MUST NOT claim A100 execution in this phase, training, prediction rerun, prompt change, decoding change, schema change, parser change, retry change, evaluator metric change, prediction repair, prediction replacement, prediction re-score, semantic-equivalence scoring, slot normalization, normalized-command normalization, checkpoint release, adapter release, held-out generalization, production readiness, public full-corpus release, model-quality improvement, or live-browser benchmark improvement

#### Scenario: Keep slot diagnosis public-safe
- **WHEN** diagnosis artifacts are prepared for commit
- **THEN** leak-scan validation MUST reject raw private rows, local or remote private paths, secrets, private IP addresses, SSH details, raw logs, checkpoints, adapters, caches, oversized generated corpora, and private remote paths
