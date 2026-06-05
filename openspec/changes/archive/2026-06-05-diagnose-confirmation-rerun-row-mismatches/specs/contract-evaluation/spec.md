## ADDED Requirements

### Requirement: Publish confirmation-rerun row-mismatch diagnosis evidence
The system SHALL publish public-safe row-level mismatch diagnosis evidence for the confirmation-required A100 train-split rerun without changing model outputs or evaluator metrics.

#### Scenario: Compare confirmation rerun rows with train gold
- **WHEN** the diagnosis is generated from committed confirmation-required rerun predictions, train-split gold rows, metrics, and schema guard evidence
- **THEN** it MUST report row-level field comparisons for each prediction id and aggregate mismatch counts by field path and failure family

#### Scenario: Preserve source prediction status
- **WHEN** a row is schema-invalid, schema-valid but semantically mismatched, or schema-valid but not exact-match
- **THEN** the diagnosis MUST preserve the source row status and MUST NOT repair, normalize, coerce, replace, or re-score the prediction

#### Scenario: Separate residual failure families
- **WHEN** the human-readable report explains why `contract_exact_match` remains `0.0000`
- **THEN** it MUST distinguish missing required-field schema failure, task/route/safety semantic mismatch, and strict string-field exact-match mismatch

#### Scenario: Bound row-mismatch diagnosis claims
- **WHEN** evidence, Human Briefs, loop reports, or archived OpenSpec artifacts describe the diagnosis
- **THEN** they MUST state that the phase is local evidence-only analysis and MUST NOT claim A100 rerun recovery, held-out generalization, checkpoint release, adapter release, production readiness, public full-corpus release, model-quality improvement, or live-browser benchmark improvement

#### Scenario: Keep row-mismatch diagnosis public-safe
- **WHEN** the diagnosis artifacts are prepared for commit
- **THEN** leak-scan validation MUST reject raw private rows, local or remote private paths, secrets, private IP addresses, SSH details, raw logs, checkpoints, adapters, model caches, oversized generated corpora, and private remote paths
