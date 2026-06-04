## ADDED Requirements

### Requirement: Run authorized A100 runtime SFT label provenance check
The system SHALL support a bounded, explicitly authorized A100 runtime label provenance check that inspects labels produced by the tokenizer/collator SFT data path while keeping private runtime artifacts outside committed files.

#### Scenario: Launch real runtime label provenance check
- **WHEN** a developer launches the runtime label provenance check with explicit runtime opt-in, a repo-external private override, and an idle A100 GPU under the approved private project root
- **THEN** the system MUST inspect labels from the configured tokenizer/collator SFT path, record real label tensor availability, label source kind, tokenizer/template status, collator status, prompt mask status, assistant-target loss status, package/runtime policy, and output-root policy without committing private paths or host details

#### Scenario: Reject unresolved or accidental runtime inspection
- **WHEN** the runtime check is launched without explicit runtime opt-in, with unresolved template paths, without a repo-external private override, or outside the approved A100 project-root policy
- **THEN** the system MUST NOT download models, load private adapters, connect to private infrastructure, inspect private labels, or write runtime evidence as successful, and MUST emit a structured blocked/skipped status

#### Scenario: Keep private runtime artifacts private
- **WHEN** the runtime label provenance check completes or fails
- **THEN** raw logs, checkpoints, adapters, caches, model snapshots, private overrides, host details, SSH details, private paths, tokens, and private corpus rows MUST remain outside committed artifacts

#### Scenario: Bound objective interpretation
- **WHEN** real runtime label provenance evidence is available
- **THEN** the system MUST state that label-mask evidence only supports SFT objective-path interpretation and MUST NOT claim checkpoint release, adapter release, held-out generalization, production readiness, public full-corpus release, or live-browser benchmark improvement
