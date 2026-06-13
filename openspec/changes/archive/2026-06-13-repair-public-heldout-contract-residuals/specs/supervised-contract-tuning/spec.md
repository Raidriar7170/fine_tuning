## ADDED Requirements

### Requirement: Expose held-out residual repair policy in SFT prompts
The system SHALL make SFT training and trained-adapter prediction prompts explicitly state the public held-out residual repair contract policies without including row-specific gold target contracts in prediction prompts.

#### Scenario: Serialize repair policy
- **WHEN** the formatter renders SFT training text or prediction prompts
- **THEN** the system prompt MUST include policy text for public navigation URL canonicalization, ambiguous clarify routing, confirmation-required form-fill safety, and unsafe payment blocking
- **AND** the policy text MUST state that these rules do not relax evaluator exact-match behavior and are not prediction repair or re-scoring

#### Scenario: Preserve prediction gold boundary
- **WHEN** the formatter builds a prediction prompt for public held-out rows
- **THEN** it MUST NOT include the full row-specific gold target contract
- **AND** it MUST NOT include held-out target-only slot values except generic policy examples and strings already present in the user input

### Requirement: Run A100 public held-out residual repair rerun
The system SHALL support a bounded A100 SFT rerun that trains on the expanded public train split and evaluates public `dev` and `test` splits separately.

#### Scenario: Configure repair SFT rerun
- **WHEN** a developer prepares the repair rerun config
- **THEN** the config MUST use the regenerated public-sample manifest, train on `dataset_split="train"`, keep private output paths as `<a100_project_root>` placeholders, require explicit heavy-training opt-in, and keep `generalization_claim=false`

#### Scenario: Configure split-specific repair predictions
- **WHEN** a developer prepares repair prediction templates
- **THEN** the templates MUST point to the repair rerun adapter placeholder and set `prediction_split` separately for `train`, `dev`, and `test`
- **AND** the templates MUST require explicit private prediction opt-in and keep `generalization_claim=false`

#### Scenario: Keep private A100 artifacts private
- **WHEN** the repair rerun and split-specific predictions complete or fail
- **THEN** raw logs, checkpoints, adapters, model caches, private overrides, host details, SSH details, private paths, tokens, and private corpus rows MUST remain outside committed artifacts
