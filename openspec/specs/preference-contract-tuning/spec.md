# preference-contract-tuning Specification

## Purpose
Define how DPO preference tuning uses chosen/rejected browser task contracts to prefer safer, more executable, and less ambiguous speech-to-contract outputs.
## Requirements
### Requirement: Train preference contract adapters
The system SHALL run DPO training over chosen/rejected browser task contract pairs to prefer safer, more executable, and less ambiguous contracts.

#### Scenario: Run DPO training
- **WHEN** a developer launches DPO training with a valid config and preference dataset path
- **THEN** the system trains a LoRA adapter or adapter continuation and records the base/SFT model reference, dataset manifest, hyperparameters, and training command

### Requirement: Validate chosen and rejected contracts
The system SHALL validate DPO pair structure before training.

#### Scenario: Reject weak preference pairs
- **WHEN** a DPO pair is missing a chosen contract, missing a rejected contract, uses different inputs across the pair, or lacks a rejection reason
- **THEN** the validator fails the pair and reports the pair identifier and failure category

### Requirement: Use meaningful rejection categories
The system SHALL categorize rejected contracts by contract-relevant failure type rather than relying only on random invalid JSON.

#### Scenario: Categorize hard negatives
- **WHEN** a rejected contract is generated or imported
- **THEN** it is labeled with a category such as wrong task type, wrong route, unsafe allowance, missing confirmation, missing slot, wrong slot, underspecified request, or malformed schema

### Requirement: Report DPO impact by slice
The system SHALL report DPO evaluation results by hard-negative and safety-relevant slices in addition to aggregate metrics.

#### Scenario: Generate DPO report
- **WHEN** DPO evaluation finishes
- **THEN** the report includes aggregate metrics and separate slices for route, safety, confirmation, slot, and schema failures

### Requirement: Validate wrong-task-type hard negatives
The system SHALL verify that `wrong_task_type` DPO hard negatives actually change the rejected contract task type.

#### Scenario: Reject mislabeled wrong-task-type pairs
- **WHEN** a DPO pair is labeled `wrong_task_type`
- **THEN** the rejected contract MUST have a different `task_type` from the chosen contract
- **AND** validation MUST fail if only other fields such as `safety.reason` changed

#### Scenario: Summarize wrong-task-type slice
- **WHEN** DPO slice summaries are generated
- **THEN** `wrong_task_type` pairs MUST be counted in the task-type rejection slice

### Requirement: Validate extract-price hard negatives
The system SHALL validate extract-specific DPO hard negatives so that mislabeled search fallback or query-slot pairs cannot silently enter preference training data.

#### Scenario: Accept extract search-fallback negative
- **WHEN** a DPO pair is labeled as extract search fallback
- **THEN** the chosen contract MUST be a public-safe `extract`/`extract_page` contract with a `target` slot
- **AND** the rejected contract MUST change to `task_type="search"` and `route="search_web"`
- **AND** validation MUST fail if the rejected contract keeps the extract task and route unchanged

#### Scenario: Accept extract query-slot negative
- **WHEN** a DPO pair is labeled as extract query-slot drift
- **THEN** the chosen contract MUST be a public-safe `extract`/`extract_page` contract with a `target` slot
- **AND** the rejected contract MUST remove `slots.target` and use a wrong query/page-url style slot shape
- **AND** validation MUST fail if the rejected contract keeps the same accepted slot shape

#### Scenario: Summarize extract hard negatives by slice
- **WHEN** DPO slice summaries are generated
- **THEN** extract search-fallback pairs MUST count in the task-type slice
- **AND** extract query-slot pairs MUST count in the slot slice

### Requirement: Validate extract-price canonical wording hard negatives
The system SHALL validate extract-price canonical wording hard negatives so that strict-wrong target synonyms cannot be mislabeled or silently accepted as canonical outputs.

#### Scenario: Accept generic price wording negative
- **WHEN** a DPO pair is labeled as generic extract-price wording drift
- **THEN** the chosen contract MUST be a public-safe `extract`/`extract_page` contract with `slots.target="商品价格"` and `normalized_command="提取页面商品价格"`
- **AND** the rejected contract MUST differ in `slots.target`, `normalized_command`, or both
- **AND** validation MUST fail if the rejected contract is identical to the canonical accepted contract

#### Scenario: Accept listed-price wording negative
- **WHEN** a DPO pair is labeled as listed-price wording drift
- **THEN** the chosen contract MUST be the canonical public-safe extract-price contract
- **AND** the rejected contract MUST contain a strict-wrong listed-price target or normalized command such as `标价` or `提取页面标价`

#### Scenario: Accept extra-particle normalized-command negative
- **WHEN** a DPO pair is labeled as extract-price extra-particle wording drift
- **THEN** the chosen contract MUST be the canonical public-safe extract-price contract
- **AND** the rejected contract MUST preserve `slots.target="商品价格"` while changing `normalized_command` away from `提取页面商品价格`

#### Scenario: Summarize canonical wording negatives by slice
- **WHEN** DPO slice summaries are generated
- **THEN** extract-price canonical wording negatives MUST count in the slot slice when `slots.target` changes
- **AND** they MUST count in a normalized-command slice when only `normalized_command` changes

### Requirement: Validate held-out residual repair hard negatives
The system SHALL validate held-out residual repair DPO pairs so mislabeled or weak pairs cannot silently enter preference data.

#### Scenario: Accept clarify action-drift negative
- **WHEN** a DPO pair is labeled as clarify action drift
- **THEN** the chosen contract MUST be a clarify contract with `route="clarify"`, `confirmation_required=true`, `safety.reason="ambiguous_request"`, and an `ambiguity` slot
- **AND** the rejected contract MUST change away from the clarify task or route

#### Scenario: Accept blocked payment action-drift negative
- **WHEN** a DPO pair is labeled as blocked payment action drift
- **THEN** the chosen contract MUST be a blocked deny contract with `safety.allow=false` and `safety.reason="unsafe_payment"`
- **AND** the rejected contract MUST either allow the request, change away from `route="deny"`, or change away from `task_type="blocked"`

#### Scenario: Accept form confirmation drift negative
- **WHEN** a DPO pair is labeled as form confirmation drift
- **THEN** the chosen contract MUST require confirmation with `task_type="form_fill"`, `route="fill_form"`, `safety.reason="requires_confirmation"`, and `slots.field`
- **AND** the rejected contract MUST differ in confirmation, safety reason, or accepted field slot shape

#### Scenario: Accept navigate canonical URL drift negative
- **WHEN** a DPO pair is labeled as navigate canonical URL drift
- **THEN** the chosen contract MUST be a public-readonly navigation contract with `route="open_url"` and `slots.url`
- **AND** the rejected contract MUST differ in URL slot value or navigation normalized command

#### Scenario: Summarize held-out residual repair slices
- **WHEN** DPO slice summaries are generated
- **THEN** clarify action drift MUST count in the task-type or underspecified slice, blocked payment action drift MUST count in the safety slice, form confirmation drift MUST count in the confirmation slice, and navigate canonical URL drift MUST count in the slot or normalized-command slice
