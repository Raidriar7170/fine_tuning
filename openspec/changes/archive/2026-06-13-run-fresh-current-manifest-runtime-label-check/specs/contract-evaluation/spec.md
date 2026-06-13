## ADDED Requirements

### Requirement: Publish fresh current-manifest runtime label evidence
The system SHALL publish a public-safe runtime label provenance evidence pack for the current public manifest that clearly distinguishes fresh current-manifest evidence from stale prior artifacts.

#### Scenario: Generate current-manifest runtime label evidence
- **WHEN** runtime label provenance metadata is generated for the current public manifest
- **THEN** the evidence pack MUST report the current manifest ID, runtime check status, real label tensor availability, label source kind, tokenizer/template status, collator status, prompt mask status, assistant-target loss status, evidence gaps, leak-scan status, package/runtime policy, and prior artifact links

#### Scenario: Reject stale evidence as current proof
- **WHEN** prior runtime-label or tiny-overfit evidence references a different manifest ID than the current public manifest
- **THEN** the evidence pack MUST treat that prior evidence as historical context only and MUST NOT present it as current label-mask proof

#### Scenario: Bound current-manifest label interpretation
- **WHEN** public reports, Human Briefs, or loop reports describe current-manifest runtime label evidence
- **THEN** they MUST state whether real tokenizer/collator labels were inspected, whether prompt/system/user tokens were masked, and whether assistant contract tokens carried loss, and MUST NOT claim model recovery, held-out generalization, checkpoint release, adapter release, production readiness, public full-corpus release, or live-browser benchmark improvement

#### Scenario: Keep current-manifest runtime evidence public-safe
- **WHEN** current-manifest runtime label evidence is prepared for commit
- **THEN** leak-scan validation MUST reject raw rendered prompts, raw assistant targets, private rows, local or remote private paths, secrets, private IP addresses, SSH details, raw logs, checkpoints, adapters, caches, model snapshots, oversized generated corpora, and private remote paths
