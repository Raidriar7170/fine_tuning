## ADDED Requirements

### Requirement: Publish A100 generation stop-boundary rerun evidence
The system SHALL publish public-safe train-split evidence for the A100 generation stop-boundary rerun that separates strict final metrics from raw/retry stop-boundary trace observations while preserving non-claim boundaries.

#### Scenario: Generate stop-boundary rerun manifest
- **WHEN** train-split rerun predictions, metrics, prompt snapshot, raw decoded summary, generation trace, stop-boundary diagnosis, schema guard summary, and leak-scan results are available
- **THEN** the manifest MUST record `prediction_source_kind=private_a100_adapter`, `prediction_split=train`, `overfit_diagnostic=true`, `generalization_claim=false`, strict metric values, raw/retry trace attempt counts, stop-boundary field coverage, retry wrapper counts, prompt/retry policy visibility, and claim boundaries without private paths or host details

#### Scenario: Report stop-boundary diagnosis
- **WHEN** a stop-boundary diagnosis is generated
- **THEN** it MUST report per-row raw/retry trace availability, generated token count, max-token limit, max-token-hit status, EOS visibility, finish state, finish-state basis, stop-boundary evidence, actual-stop-reason-recorded status, actual stop reason, retry parse status, retry wrapper status, strict final schema validity, and whether any real stop-reason claim remains unproven

#### Scenario: Compare only against bounded prior evidence
- **WHEN** the public report describes the rerun result
- **THEN** it MUST compare only against `reports/public-sample/a100-retry-generation-trace-rerun/` and `reports/public-sample/generation-stop-reason-boundary-instrumentation/` and MUST NOT present the comparison as held-out generalization or model-quality improvement

#### Scenario: Bound stop-boundary rerun interpretation
- **WHEN** public documentation or Human Briefs describe the rerun
- **THEN** they MUST state that the phase performs no training, checkpoint release, adapter release, decoding behavior change, retry prompt change, parser relaxation, evaluator metric change, semantic-equivalence scoring, slot normalization, prediction repair, prediction re-score, production-readiness claim, held-out generalization claim, model-quality claim, public full-corpus release, or live-browser benchmark improvement claim
