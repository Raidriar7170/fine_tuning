## ADDED Requirements

### Requirement: Add train-only public held-out repair exemplars
The system SHALL add public-safe train split seed traces that cover the same contract families as the failed public held-out residuals without moving existing public `dev` or `test` rows into train.

#### Scenario: Build train repair rows
- **WHEN** the public sample dataset is generated after the repair seed expansion
- **THEN** it MUST include train split SFT rows for navigate/open-url, ambiguous clarify, confirmation-required form fill, and unsafe payment blocking
- **AND** those train rows MUST use distinct public-safe inputs and target values from the existing public held-out `dev` and `test` rows
- **AND** existing public `dev` and `test` rows MUST retain their split labels and target contracts

#### Scenario: Preserve repair target contracts
- **WHEN** schema-preserving augmentations are generated for the repair train seeds
- **THEN** each augmentation MUST preserve the original target contract, including task type, route, safety reason, confirmation expectation, slots, and canonical normalized command

### Requirement: Generate held-out residual repair hard negatives
The public sample DPO builder SHALL generate task-family-specific hard negatives for the public held-out residual families.

#### Scenario: Build clarify action-drift negative
- **WHEN** DPO pairs are generated for a public-safe clarify contract with `safety.reason="ambiguous_request"`
- **THEN** the builder MUST include a rejected contract that drifts to a concrete action such as search or navigate
- **AND** the chosen contract MUST retain `task_type="clarify"`, `route="clarify"`, `confirmation_required=true`, and an `ambiguity` slot

#### Scenario: Build blocked payment action-drift negative
- **WHEN** DPO pairs are generated for a public-safe unsafe payment block contract
- **THEN** the builder MUST include a rejected contract that allows or routes the request as a concrete search or navigation action
- **AND** the chosen contract MUST retain `task_type="blocked"`, `route="deny"`, `safety.allow=false`, `safety.reason="unsafe_payment"`, `confirmation_required=true`, and a payment-control reason slot

#### Scenario: Build form confirmation drift negative
- **WHEN** DPO pairs are generated for a public-safe confirmation-required form-fill contract
- **THEN** the builder MUST include a rejected contract that drops confirmation, changes the confirmation safety reason, or changes the accepted `slots.field` shape
- **AND** the chosen contract MUST retain `task_type="form_fill"`, `route="fill_form"`, `safety.reason="requires_confirmation"`, `confirmation_required=true`, and `slots.field`

#### Scenario: Build navigate canonical URL drift negative
- **WHEN** DPO pairs are generated for a public-safe navigation contract with a canonical URL slot and open-site normalized command
- **THEN** the builder MUST include a rejected contract with a strict-wrong URL or normalized-command variant
- **AND** the chosen contract MUST retain the canonical URL slot and canonical navigation normalized command

#### Scenario: Limit held-out residual negatives
- **WHEN** DPO pairs are generated for rows outside the matching public-safe task family
- **THEN** the builder MUST NOT invent held-out residual repair negatives for unrelated rows
