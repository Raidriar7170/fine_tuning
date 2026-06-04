## MODIFIED Requirements

### Requirement: Publish observed runtime label provenance evidence
The system SHALL publish a public-safe observed runtime label provenance evidence pack that records sanitized A100 runtime label inspection results and bounded interpretation without exposing private infrastructure or unreleased model artifacts.

#### Scenario: Generate observed runtime evidence pack
- **WHEN** sanitized runtime label provenance metadata is available from an authorized A100 execution or local objective-mask preparation path
- **THEN** the system MUST write machine-readable JSON and human-readable Markdown that report runtime check status, real label tensor availability, label source kind, tokenizer/template status, collator status, prompt mask status, assistant-target loss status, evidence gaps, prior evidence links, leak-scan status, package/runtime policy, and non-claim boundaries

#### Scenario: Keep observed runtime evidence public-safe
- **WHEN** observed runtime label provenance evidence is prepared for commit
- **THEN** leak-scan validation MUST reject raw private rows, local or remote private paths, secrets, private IP addresses, SSH details, raw logs, checkpoints, adapters, caches, model snapshots, oversized generated corpora, and private remote paths

#### Scenario: Separate label evidence from model-quality claims
- **WHEN** public documentation or Human Briefs describe observed runtime label provenance evidence
- **THEN** they MUST state whether real tokenizer/collator labels were inspected, whether prompt/system/user tokens were masked, and whether assistant contract tokens carried loss, and MUST NOT claim model recovery, held-out generalization, checkpoint release, adapter release, production readiness, public full-corpus release, or live-browser benchmark improvement
