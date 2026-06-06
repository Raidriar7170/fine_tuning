## ADDED Requirements

### Requirement: Run A100 generation stop-boundary rerun
The system SHALL support a bounded A100 prediction-only train-split rerun after generation stop-boundary trace instrumentation while keeping all private runtime artifacts outside git.

#### Scenario: Launch stop-boundary rerun
- **WHEN** a developer launches the rerun with A100 authorization, a repo-external private override, an existing private adapter path, an idle A100 GPU, and an approved private output root represented in public artifacts as `<a100_project_root>`
- **THEN** the system MUST use `prediction_split=train`, `overfit_diagnostic=true`, `generalization_claim=false`, `schema_retry_enabled=true`, `schema_repair_applied=false`, and generate private-adapter predictions plus public-safe prompt snapshot, raw decoded summary, generation trace, prediction metadata, and leak-scan sidecars

#### Scenario: Record stop-boundary trace fields
- **WHEN** raw or retry generation trace rows are written during the rerun
- **THEN** each row MUST include generated token count, max-token limit, EOS visibility, finish state, max-token-hit status, finish-state basis, stop-boundary evidence, actual-stop-reason-recorded status, actual stop reason, strategy, sampling mode, prediction source kind, and attempt label when available

#### Scenario: Keep private A100 artifacts private
- **WHEN** the real rerun completes or fails
- **THEN** raw logs, checkpoints, adapters, caches, private overrides, host details, SSH details, private paths, tokens, and private corpus rows MUST remain outside committed artifacts

#### Scenario: Preserve diagnostic model output
- **WHEN** the private adapter emits schema-invalid, missing-field, JSON-fragment, prose-wrapped, Markdown-wrapped, or otherwise invalid output
- **THEN** the prediction artifact and sidecars MUST preserve sanitized model evidence without replacing it with fixture-mode, rule-baseline, gold-contract predictions, parser-relaxed outputs, normalized fields, semantic-equivalence labels, or repaired strings
