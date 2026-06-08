## ADDED Requirements

### Requirement: Publish first-pass output-boundary A100 rerun evidence
The system SHALL publish public-safe evidence for the first-pass output-boundary A100 prediction-only rerun while preserving strict parser, metric, privacy, and non-claim boundaries.

#### Scenario: Generate rerun evidence pack
- **WHEN** the A100 prediction-only rerun completes
- **THEN** the evidence pack MUST include predictions, gold train rows, prediction metadata, prompt snapshot, raw decoded summary, generation trace, metrics, schema guard summary, output-boundary comparison diagnosis, manifest, report, leak scans, and Human Brief links
- **AND** it MUST compare against the prior A100 search-query slot-policy rerun and the local output-boundary instrumentation evidence
- **AND** it MUST record strict schema-valid counts, strict exact-match counts, Markdown wrapper counts, compact query fragment counts, raw/retry parse status, and `prediction_output_boundary` visibility

#### Scenario: Bound rerun claims
- **WHEN** reports, manifests, Human Briefs, or archived OpenSpec artifacts describe the rerun
- **THEN** they MUST state that this is train-split-only prediction evidence
- **AND** they MUST NOT claim held-out generalization, model-quality improvement, production readiness, checkpoint release, adapter release, public full-corpus release, live-browser benchmark improvement, slot normalization, semantic-equivalence scoring, prediction repair, prediction replacement, metric relaxation, or re-score
