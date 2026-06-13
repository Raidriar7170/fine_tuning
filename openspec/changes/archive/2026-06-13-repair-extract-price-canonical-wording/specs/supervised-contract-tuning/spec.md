## ADDED Requirements

### Requirement: Expose extract-price canonical wording policy in SFT prompts
The system SHALL make SFT training and trained-adapter prediction prompts explicitly state the canonical wording rule for current-page public price extraction while preserving prediction gold-target boundaries.

#### Scenario: Serialize canonical wording policy
- **WHEN** the formatter renders an SFT training text or prediction prompt for a public-safe extract-price row
- **THEN** the system prompt MUST state that user wording such as `多少钱`, `标价`, and `页面上的商品价格` maps to `slots.target="商品价格"` and `normalized_command="提取页面商品价格"`
- **AND** it MUST state that `价格`, `标价`, `页面价格`, and `提取页面上的商品价格` are strict-wrong target variants for this public contract

#### Scenario: Preserve prediction gold boundary
- **WHEN** the formatter builds a prediction prompt for an extract-price row
- **THEN** the prompt MUST NOT include the full row-specific gold contract
- **AND** it MUST NOT include row-specific target-only values except canonical policy text and strings already present in the user input

#### Scenario: Surface canonical wording prompt metadata
- **WHEN** prompt constraint metadata is recorded for prediction metadata, prompt snapshots, manifests, reports, or evidence packs
- **THEN** it MUST include booleans for extract canonical商品价格 target visibility, alias-to-canonical mapping visibility, strict-wrong synonym rejection visibility, and extra-particle rejection visibility

### Requirement: Run A100 extract-price canonical wording train-split rerun
The system SHALL support a bounded, explicitly authorized 7B A100 public-sample train-split rerun after extract-price canonical wording repair while keeping all private runtime artifacts outside git.

#### Scenario: Launch canonical wording rerun
- **WHEN** a developer launches the rerun with explicit A100 approval, a repo-external private override, an idle A100 GPU, and an approved private output root represented in public artifacts as `<a100_project_root>`
- **THEN** the system MUST train on the current public-sample train rows with the canonical extract-price wording policy and hard negatives available
- **AND** prediction MUST use `prediction_split=train`, `overfit_diagnostic=true`, `generalization_claim=false`, and sanitized sidecar exports

#### Scenario: Preserve prior fixed behavior during canonical wording repair
- **WHEN** train-split predictions are evaluated for the canonical wording rerun
- **THEN** compact public-readonly search/weather rows and extract-price task/route shape MUST be reported separately
- **AND** the report MUST state whether compact-query exact match, extract task/route correctness, extract target exact match, and extract normalized-command exact match were recovered, preserved, regressed, or could not be evaluated

#### Scenario: Keep private A100 artifacts private
- **WHEN** the canonical wording rerun completes or fails
- **THEN** raw logs, checkpoints, adapters, model caches, private overrides, host details, SSH details, private paths, tokens, and private corpus rows MUST remain outside committed artifacts
