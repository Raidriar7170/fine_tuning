## ADDED Requirements

### Requirement: Integrate observe-only prediction shadow hook
The system SHALL integrate a disabled-by-default copy-backed shadow hook into the canonical prediction pipeline.

#### Scenario: Canonical prediction entrypoint is hooked
- **WHEN** `voice2task-train sft-predict` or library callers use `run_sft_prediction_export`
- **THEN** the hook observes prediction values only after the existing prediction result has been determined
- **AND** it MUST NOT change model invocation, decoding, parser semantics, prediction output JSONL, evaluator input, runtime decision behavior, or exit status

#### Scenario: Default disabled behavior is unchanged
- **WHEN** prediction config omits `copy_backed_shadow` or sets `enabled=false`
- **THEN** prediction output and metadata behavior remain compatible with previous configs
- **AND** no copy-backed shadow sidecar file is created

#### Scenario: Enabled hook writes only explicit sidecars
- **WHEN** `copy_backed_shadow.enabled=true` and `sidecar_output_path` is null
- **THEN** the hook MAY compute in-memory outcomes but MUST NOT implicitly write a file
- **WHEN** `sidecar_output_path` is provided
- **THEN** sidecars are written as separate JSONL rows and MUST NOT be mixed into the prediction JSONL

### Requirement: Fail-isolate invalid prediction and hook errors
The system SHALL isolate all shadow-hook failures from the primary prediction path.

#### Scenario: Invalid predictions remain primary outputs
- **WHEN** a prediction is malformed JSON, empty, unsupported, parser-invalid, or not a valid BrowserTaskContract V1 object
- **THEN** the hook records a bounded invalid status
- **AND** the original prediction remains unchanged and unrepaired

#### Scenario: Hook internals cannot fail primary prediction
- **WHEN** policy loading, policy validation, verifier execution, sidecar serialization, or sidecar sink writing fails
- **THEN** the hook records a bounded isolated status and error code
- **AND** the primary prediction caller receives the same prediction result and status it would have received with the hook disabled

### Requirement: Fully validate frozen copy-backed scope policy
The system SHALL validate the frozen copy-backed scope policy before trusted provenance is emitted.

#### Scenario: Policy consistency passes
- **WHEN** `configs/copy-backed-scope-policy-v1.json` is loaded
- **THEN** policy id and version are non-empty, policy hash matches loaded content, enabled/disabled triple keys are unique and disjoint, scope rows are unique, scope-row keys equal enabled plus disabled keys, enabled rows equal `enabled_triples`, disabled rows equal `disabled_triples`, action is disabled, normalized trusted is false, and enabled triples are exactly `search:search_web:query`, `form_fill:fill_form:field`, and `extract:extract_page:target`
- **AND** every hook sidecar records policy id, policy version, and policy hash

#### Scenario: Policy invalid fails closed
- **WHEN** policy validation fails
- **THEN** the hook records `SHADOW_POLICY_INVALID`, emits no trusted provenance, does not use a fallback default policy, and does not affect primary prediction

### Requirement: Preserve exact-only trusted provenance and privacy defaults
The system SHALL emit trusted provenance only for exact unique source spans and default to hash-and-offset-only sidecars.

#### Scenario: Exact unique source span can be trusted
- **WHEN** an enabled slot is `VERIFIED_EXACT_UNIQUE`, exact, one candidate span, policy-valid, source-span-valid, current-input-hash-matched, and exact back-slice matched to the predicted value
- **THEN** the sidecar MAY set `trusted_provenance=true`

#### Scenario: Normalized and action paths are never trusted
- **WHEN** a slot is `VERIFIED_NORMALIZED_UNIQUE`
- **THEN** it MUST be candidate-only with `trusted_provenance=false`
- **WHEN** an action slot is observed
- **THEN** it MUST remain disabled and untrusted

#### Scenario: Sidecars avoid private text by default
- **WHEN** online sidecars are generated with default retention
- **THEN** they MUST NOT include full input text, raw model output, full prediction contract, raw request id, gold/evaluator fields, or `source_span.text`
- **AND** source span records default to start, end, source text hash, and span hash

### Requirement: Publish prediction-hook evidence and bounded decision
The system SHALL publish compact public-safe evidence and select one bounded decision label.

#### Scenario: Evidence proves output invariance
- **WHEN** the phase evidence is generated
- **THEN** it reports disabled, NullSink, and JsonlSink prediction output hashes, hash equality, contract mutation count, runtime decision delta count, V1 metric delta, deterministic rerun status, per-scope metrics, latency benchmark, leak scan result, and repo-wide lint status

#### Scenario: Ready observe-only label remains non-enforcement
- **WHEN** all acceptance gates pass
- **THEN** the decision MAY be `PREDICTION_SHADOW_HOOK_READY_OBSERVE_ONLY`
- **AND** the only recommended next change is `evaluate-frozen-copy-shadow-policy-on-template-disjoint-challenge-set`
- **AND** the system MUST NOT recommend runtime enforcement
