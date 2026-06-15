## ADDED Requirements

### Requirement: Expose merged residual canonical policy in SFT prompts
The system SHALL make SFT training and trained-adapter prediction prompts expose
the post-merge canonical policy for the remaining ambiguous-clarify and unsafe
payment residual families without inserting row-specific gold target contracts
into prediction prompts.

#### Scenario: Serialize ambiguous clarify canonical phrase policy
- **WHEN** SFT training text or a trained-adapter prediction prompt is rendered
  with the residual repair prompt policy
- **THEN** the prompt MUST state that ambiguous clarify contracts use
  `task_type="clarify"`, `route="clarify"`,
  `safety.reason="ambiguous_request"`, `confirmation_required=true`, and
  `slots.ambiguity="目标不明确，未指定具体网站或页面"`
- **AND** it MUST state that shorter values such as `未指定具体页面` or
  `未指定具体操作` are strict-wrong for this canonical family

#### Scenario: Serialize unsafe payment canonical command policy
- **WHEN** SFT training text or a trained-adapter prediction prompt is rendered
  with the residual repair prompt policy
- **THEN** the prompt MUST state that unsafe payment/account-backed purchase
  requests use `task_type="blocked"`, `route="deny"`,
  `safety.allow=false`, `safety.reason="unsafe_payment"`,
  `confirmation_required=true`, `slots.reason=payment_requires_user_control`,
  and `normalized_command="拒绝代替用户付款"`
- **AND** it MUST state that `normalized_command="拒绝代替用户下单"` is
  strict-wrong for this canonical payment family

#### Scenario: Preserve prediction gold boundary for canonical policy
- **WHEN** the formatter builds a prediction prompt for a row whose gold target
  contains target-only slot values or normalized command text
- **THEN** it MUST NOT include the full row-specific gold target contract
- **AND** it MUST NOT include target-only values beyond shared policy text and
  strings already present in the user input

#### Scenario: Surface canonical policy metadata
- **WHEN** prompt constraint metadata is recorded in prediction metadata,
  prompt snapshots, manifests, reports, or evidence packs
- **THEN** it MUST include explicit booleans for ambiguous-clarify canonical
  phrase visibility and unsafe-payment canonical command visibility
