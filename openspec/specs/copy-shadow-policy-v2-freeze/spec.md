# copy-shadow-policy-v2-freeze Specification

## Purpose

Define the inactive Policy V2 reference freeze boundary before any naturalistic
copy-shadow challenge design or runtime integration work.

## Requirements

### Requirement: Validate Policy V2 freeze inputs
The system SHALL validate the inactive Policy V2 proposal and its design
evidence before emitting a frozen Policy V2 reference.

#### Scenario: Accepted freeze input boundary
- **WHEN** the Policy V2 freeze process starts
- **THEN** it verifies the proposed policy hash, design summary hash, scope
  decisions hash, metrics hash, taxonomy migration hash, challenge v1 hash,
  diagnosis artifact hash, source Policy V1 hash, design decision label,
  recommended next change, inactive runtime flags, scope set, per-scope gate
  and final statuses, reviewer requirement, zero technical false accepts, zero
  execution eligibility, and proposal-only boundary claims
- **AND** frozen outputs may be emitted only when all checks pass

#### Scenario: Drifted freeze input blocks output
- **WHEN** any required proposal or design artifact is missing, drifted,
  contradictory, executable, runtime-loaded, enforcement-enabled, missing
  reviewer-required state, or inconsistent with the expected scope decisions
- **THEN** the system writes a bounded `blocked.json` report with a blocked
  decision label
- **AND** it MUST NOT emit or update a frozen Policy V2 reference, mutate Policy
  V1, mutate the proposed Policy V2 input, mutate challenge v1 rows or gold,
  mutate predictions, mutate sidecars, mutate audits, change evaluator
  behavior, or change runtime behavior

### Requirement: Emit inactive frozen Policy V2 reference
The system SHALL write a frozen Policy V2 reference only as an inactive,
non-runtime artifact.

#### Scenario: Frozen policy is inactive
- **WHEN** freeze validation succeeds
- **THEN** `configs/copy-backed-scope-policy-v2.frozen.json` records
  `status=frozen_reference`, `active=false`, `runtime_loaded=false`,
  `enforcement_enabled=false`, source proposal hash, source design evidence
  hashes, source Policy V1 id/hash, challenge v1 hash, diagnosis artifact hash,
  gate version, freeze timestamp or date, per-scope original gate status, final
  frozen status, reviewer requirement, execution eligibility, and evidence
  references
- **AND** no runtime loader, prediction hook, evaluator, prompt, decoding,
  training, or dataset path reads this frozen reference as an active policy

#### Scenario: Frozen statuses remain conservative
- **WHEN** the frozen reference is emitted
- **THEN** it preserves `form_fill:fill_form:field` as `PROPOSE_DISABLE`,
  `search:search_web:query` as `INSUFFICIENT_EVIDENCE`, and
  `extract:extract_page:target` as `INSUFFICIENT_EVIDENCE`
- **AND** every scope MUST record `reviewer_required=true` and
  `execution_eligible=false`

### Requirement: Publish bounded freeze evidence
The system SHALL publish compact public-safe freeze evidence and documentation
without expanding policy claims.

#### Scenario: Freeze evidence bundle is bounded
- **WHEN** the freeze process succeeds
- **THEN** `reports/public-sample/copy-shadow-policy-v2-freeze/` contains at
  most `summary.md`, `summary.json`, `freeze-input-audit.json`,
  `frozen-scope-decisions.json`, `recommended-next-change.md`, and
  `blocked.json` only when blocked
- **AND** the evidence records the freeze decision label, frozen policy path,
  source artifact hashes, final scope statuses, review outcome, non-goals, and
  recommended next bounded change

#### Scenario: Freeze documentation states boundaries
- **WHEN** docs, status surfaces, evidence index entries, or Human Brief HTML
  are emitted
- **THEN** they state that frozen Policy V2 is inactive, not runtime loaded,
  not enforcement, not action eligibility, not normalized trust, not training,
  not data expansion, not naturalistic challenge v2, not model improvement, and
  not a production or safety readiness claim

### Requirement: Select freeze decision and next bounded change
The system SHALL select exactly one freeze decision label and one recommended
next bounded change.

#### Scenario: Policy V2 freeze ready for naturalistic challenge design
- **WHEN** freeze validation succeeds, frozen Policy V2 is inactive, all scopes
  are reviewer-required and execution-ineligible, Policy V1 is unchanged,
  proposed Policy V2 is unchanged, runtime behavior is unchanged, and public
  evidence remains sanitized
- **THEN** the decision label is
  `POLICY_V2_FROZEN_INACTIVE_REFERENCE_READY_FOR_NATURALISTIC_CHALLENGE_DESIGN`
- **AND** the recommended next change is
  `design-and-materialize-naturalistic-copy-shadow-challenge-v2`

#### Scenario: Policy V2 freeze is blocked
- **WHEN** validation cannot prove the freeze boundary
- **THEN** the decision label is `POLICY_V2_FREEZE_BLOCKED`
- **AND** the recommended next change MUST NOT be a naturalistic challenge,
  runtime enforcement, action enablement, normalized trusted provenance,
  training, data expansion, model artifact change, or evaluator relaxation
