## ADDED Requirements

### Requirement: Expose public extract-price contract policy in SFT prompts
The system SHALL make SFT training and trained-adapter prediction prompts explicitly state the Browser Task Contract policy for current-page public price extraction while preserving gold-target boundaries.

#### Scenario: Serialize extract policy in training text
- **WHEN** the formatter converts an SFT dataset row into training text
- **THEN** the rendered system prompt MUST state that current-page price extraction uses `task_type="extract"`, `route="extract_page"`, `safety.allow=true`, `safety.reason="public_readonly"`, `confirmation_required=false`, object-shaped `slots.target`, and a concise extract normalized command
- **AND** it MUST state that the request MUST NOT be converted into public web search for price-like current-page extraction

#### Scenario: Serialize extract policy in prediction prompts without gold contract
- **WHEN** the formatter builds a trained-adapter prediction prompt
- **THEN** the prompt MUST include the same extract-price policy
- **AND** it MUST NOT include the full row-specific gold target contract or target-only slot values beyond policy text and strings already present in the user input

#### Scenario: Surface extract prompt constraint metadata
- **WHEN** prompt constraint metadata is recorded in prediction metadata, prompt snapshots, manifests, reports, or evidence packs
- **THEN** it MUST include explicit booleans for extract-page policy visibility, extract target-slot guidance visibility, extract search-fallback rejection visibility, and extract query/page-url slot rejection visibility

### Requirement: Run A100 extract-price contract residual train-split rerun
The system SHALL support a bounded, explicitly authorized 7B A100 public-sample train-split rerun after extract-price contract policy repair while keeping all private runtime artifacts outside git.

#### Scenario: Launch extract-price residual rerun
- **WHEN** a developer launches the rerun with explicit A100 approval, a repo-external private override, an idle A100 GPU, and an approved private output root represented in public artifacts as `<a100_project_root>`
- **THEN** the system MUST train on the current committed public-sample train rows with the extract-price prompt/data policy visible
- **AND** prediction MUST use `prediction_split=train`, `overfit_diagnostic=true`, `generalization_claim=false`, and sanitized sidecar exports

#### Scenario: Preserve compact-query behavior during extract repair
- **WHEN** train-split predictions are evaluated for the extract-price residual rerun
- **THEN** compact public-readonly search/weather train rows MUST be reported separately from extract-price train rows
- **AND** the report MUST state whether compact-query strict exact match was preserved, regressed, or could not be evaluated

#### Scenario: Keep private A100 artifacts private
- **WHEN** the rerun completes or fails
- **THEN** raw logs, checkpoints, adapters, model caches, private overrides, host details, SSH details, private paths, tokens, and private corpus rows MUST remain outside committed artifacts
