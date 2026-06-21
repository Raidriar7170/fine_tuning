# internal-contract-core-v2 Specification

## Purpose
Define the internal ContractCoreV2 boundary, V1-compatible deterministic envelope behavior, and shadow compatibility diagnostics for Voice2Task while BrowserTaskContract V1 remains the external schema and training target.
## Requirements
### Requirement: Define an internal ContractCoreV2 DTO
The system SHALL define an internal ContractCoreV2 DTO containing exactly `task_type`, `route`, `safety`, `confirmation_required`, and `slots`, using the current BrowserTaskContract V1 field meanings and taxonomy.

#### Scenario: Core contains only V1 core fields
- **WHEN** a valid BrowserTaskContract V1 object is projected to ContractCoreV2
- **THEN** the core object MUST contain exactly `task_type`, `route`, `safety`, `confirmation_required`, and `slots`
- **AND** it MUST NOT contain `normalized_command`, `language`, `contract_version`, `allowed_actions`, `success_criteria`, `policy_tags`, or `runtime_hints`

#### Scenario: Core validation reuses V1 boundaries
- **WHEN** a ContractCoreV2 object is validated
- **THEN** `task_type` and `route` MUST be accepted only when they match the current V1 enum sets
- **AND** `safety.allow`, `safety.reason`, `confirmation_required`, and `slots` MUST satisfy the current V1 field constraints without silently repairing invalid values

### Requirement: Preserve V1-compatible envelope metadata internally
The system SHALL represent `language`, `contract_version`, `normalized_command`, and `normalized_command_provenance` as internal envelope metadata rather than ContractCoreV2 fields.

#### Scenario: Extract V1 envelope metadata
- **WHEN** a valid BrowserTaskContract V1 object is parsed for internal core processing
- **THEN** the system MUST extract `language`, `contract_version`, and `normalized_command` into envelope metadata
- **AND** it MUST mark `normalized_command_provenance` as `legacy_preserved`

#### Scenario: Keep provenance internal-only
- **WHEN** a V1-compatible envelope is serialized back to BrowserTaskContract V1 JSON
- **THEN** `normalized_command_provenance` MUST NOT appear in the serialized V1 JSON

### Requirement: Build deterministic V1-compatible envelopes
The system SHALL build V1-compatible BrowserTaskContract envelopes from ContractCoreV2 using either `preserve_legacy` or `derive_display` mode.

#### Scenario: Preserve legacy envelope fields by default
- **WHEN** a valid V1 contract is projected to ContractCoreV2 and rebuilt in `preserve_legacy` mode with extracted metadata
- **THEN** the canonical rebuilt V1 contract JSON MUST exactly match the canonical original V1 contract JSON
- **AND** safety, confirmation, slots, normalized_command, language, and contract_version MUST be preserved

#### Scenario: Derive display fields deterministically
- **WHEN** a valid ContractCoreV2 object is rebuilt in `derive_display` mode
- **THEN** the system MUST derive `normalized_command` only through the existing deterministic renderer
- **AND** it MUST emit V1-compatible `language="zh-CN"` and `contract_version="v1"`
- **AND** it MUST NOT read or reuse an old `normalized_command`

#### Scenario: Unsupported renderer fails closed
- **WHEN** the deterministic renderer cannot safely render a normalized command for a ContractCoreV2 object
- **THEN** `derive_display` mode MUST fail closed with a typed error or explicit failure result
- **AND** it MUST NOT fall back to free generation or silently copy legacy normalized_command text

### Requirement: Provide shadow V1 compatibility diagnostics
The system SHALL provide a shadow compatibility path that validates V1 input, projects it through ContractCoreV2, rebuilds a V1-compatible envelope in preserve mode, and reports compatibility without changing runtime decisions.

#### Scenario: Shadow check reports preservation fields
- **WHEN** shadow compatibility is checked for a V1 contract
- **THEN** the result MUST include `v1_valid`, `core_valid`, `roundtrip_exact`, `safety_preserved`, `confirmation_preserved`, `slots_preserved`, `normalized_command_preserved`, `language_preserved`, `contract_version_preserved`, and `failure_reason`

#### Scenario: Shadow check does not mutate input
- **WHEN** shadow compatibility is checked for a mutable dict or BrowserTaskContract instance
- **THEN** the input contract MUST remain unchanged after the check

### Requirement: Report current public-safe compatibility evidence
The system SHALL generate a compact public-safe evidence bundle under `reports/public-sample/internal-contract-v2-core/` for current committed public-safe V1 contracts and recovered step-matched prediction contracts.

#### Scenario: Compatibility report covers current committed public-safe contracts
- **WHEN** the compatibility report is generated
- **THEN** it MUST check current formal seed contracts, SFT target contracts, dev/test gold contracts, recovered Control/Treatment parse-valid prediction contracts, and execution smoke fixtures where present
- **AND** it MUST report total contracts checked, V1 valid count, core projection success count, preserve roundtrip exact count/rate, safety preservation rate, confirmation preservation rate, slots preservation rate, derive-display supported rate, derive-display unsupported count, and failures by reason

#### Scenario: Compatibility gates preserve V1 behavior
- **WHEN** the compatibility report is generated
- **THEN** preserve roundtrip exact rate MUST be `1.0`
- **AND** safety, confirmation, and slots preservation rates MUST each be `1.0`
- **AND** V1 evaluator metric deltas for the committed recovered prediction/gold artifacts MUST be exactly `0`
- **AND** current controlled smoke behavior MUST remain unchanged

#### Scenario: Report remains public-safe and bounded
- **WHEN** compatibility evidence, docs, or Human Brief HTML are prepared for commit
- **THEN** public leak-scan validation MUST reject raw private rows, local absolute paths, private remote paths, host details, credentials, raw logs, checkpoints, adapters, caches, and private corpus rows
- **AND** the evidence MUST state that no training, prediction rerun, data mutation, evaluator relaxation, schema migration, downstream runtime migration, checkpoint release, adapter release, model-improvement claim, executable-quality-improvement claim, safety-readiness claim, or production-readiness claim occurred
