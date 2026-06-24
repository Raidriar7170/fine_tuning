## ADDED Requirements

### Requirement: Validate frozen challenge and policy boundary before adapter recovery
The system SHALL verify the frozen challenge and frozen copy-backed policy before any adapter recovery or prediction-only challenge run.

#### Scenario: Frozen boundary passes
- **WHEN** recovery evaluation starts
- **THEN** the system verifies the challenge row count is 120, the challenge hash matches the committed manifest, the template-disjoint audit is accepted, the challenge gold has not changed, policy id/version/hash match `copy-backed-scope-policy-v1`, `action_enabled=false`, `normalized_trusted=false`, and there is no conflicting active OpenSpec change
- **AND** prediction may proceed only after those checks pass

#### Scenario: Frozen boundary mismatch blocks evaluation
- **WHEN** the challenge hash, row count, gold hash, template-disjoint audit, policy hash, action flag, normalized-trusted flag, or active-change boundary mismatches
- **THEN** the system writes `blocked.json` with `decision=CHALLENGE_EVALUATION_BLOCKED_BOUNDARY_MISMATCH`
- **AND** it MUST NOT run inference, fabricate predictions, modify the challenge, modify the policy, or train an adapter

### Requirement: Verify existing frozen adapter content identity before inference
The system SHALL recover only existing step-matched frozen adapters whose content identity can be verified from public-safe expected hashes and readable adapter files.

#### Scenario: Adapter identity passes
- **WHEN** a step-matched Control or Treatment adapter is considered for challenge inference
- **THEN** the system verifies adapter directory presence, adapter config presence, readable adapter weights, adapter config SHA256, adapter model SHA256, expected run id, expected manifest id, and sanitized PEFT/LoRA config fields
- **AND** public artifacts record the content-hash identity method, sanitized identity fields, and verification failures
- **AND** the evidence MUST NOT claim adapter release, checkpoint release, private path disclosure, base/tokenizer revision attestation, source training config attestation, no-overwrite attestation, or broader experiment provenance unless those checks are explicitly implemented in a later change

#### Scenario: Adapter unavailable blocks evaluation
- **WHEN** no allowed step-matched adapter directory is available
- **THEN** the system writes `blocked.json` with `decision=CHALLENGE_EVALUATION_BLOCKED_ADAPTER_UNAVAILABLE`
- **AND** it MUST NOT train, substitute, or infer from a different adapter

#### Scenario: Adapter identity mismatch blocks evaluation
- **WHEN** an adapter path exists but identity cannot be verified or conflicts with the step-matched Control/Treatment evidence
- **THEN** the system writes `blocked.json` with `decision=CHALLENGE_EVALUATION_BLOCKED_ADAPTER_IDENTITY`
- **AND** it MUST NOT run inference with that adapter

#### Scenario: Private override remains private
- **WHEN** a private override is used to resolve adapter locations
- **THEN** committed configs, reports, docs, Human Briefs, and logs record only `private_override_used=true` and sanitized adapter identity fields
- **AND** they MUST NOT include private absolute paths, SSH aliases, hostnames, IPs, tokens, checkpoint contents, A100 usernames, or private project roots

### Requirement: Run verified adapters through the canonical prediction hook
The system SHALL evaluate verified adapters only through the canonical prediction pipeline and integrated copy-backed prediction shadow hook.

#### Scenario: Canonical prediction path runs
- **WHEN** a verified adapter is evaluated on the frozen challenge
- **THEN** prediction goes through `voice2task-train sft-predict` or library-equivalent `voice2task.training.run_sft_prediction_export`
- **AND** the existing parser and integrated copy-backed prediction shadow hook produce online sidecars
- **AND** standalone verifier scripts, hand-built predictions, gold-derived predictions, simulated hooks, parser bypasses, and gold-assisted span selection MUST NOT be used as the primary result

#### Scenario: Hook mode invariance is proven
- **WHEN** shadow disabled, enabled NullSink, and enabled JsonlSink boundaries are compared for the same canonical prediction artifact
- **THEN** prediction output hash, parsed contracts, exit status, evaluator input, runtime decision, and V1 metrics remain unchanged
- **AND** hook output appears only as separate sidecar artifacts with no sidecar path conflicts

### Requirement: Keep online sidecars gold-free and audit gold offline
The system SHALL separate online hook sidecars from offline gold correctness audits.

#### Scenario: Online sidecars remain gold-free
- **WHEN** online challenge sidecars are written
- **THEN** they omit gold fields, correctness fields, full input text, span text, raw model output, private paths, raw request ids, and real PII
- **AND** exact unique spans are the only trusted provenance path, normalized matches are candidate-only, and action remains disabled and untrusted

#### Scenario: Offline audit joins gold after freeze
- **WHEN** evaluation audit rows are generated
- **THEN** they join frozen predictions, frozen online sidecars, and frozen challenge gold in a separate artifact after prediction and sidecar files are fixed
- **AND** they MUST NOT mutate sidecars, predictions, gold rows, evaluator inputs, runtime decisions, or V1 metrics

### Requirement: Report verifier fixture safety metrics and conservative decisions
The system SHALL report technical hook/verifier safety, adversarial condition metrics, per-scope metrics, latency evidence, and a bounded decision label.

#### Scenario: Technical safety metrics are reported
- **WHEN** evaluation completes or blocks
- **THEN** reports include prediction run success count/rate, hook invocation count, sidecar attachment count/rate, hook error count, sink error count, policy drift count, path conflict count, contract mutation count, runtime decision delta count, prediction output hash mismatch count, V1 metric delta, provenance false accept count, silent fallback count, action trusted count, normalized trusted count, privacy leak counts, and adapter identity status

#### Scenario: High-risk false trust hard-stops
- **WHEN** duplicate exact, source absent, normalization collision, partial span, out-of-scope action, action trusted, normalized trusted, prediction mutation, runtime decision delta, policy drift, privacy leak, or primary-impacting hook error appears
- **THEN** the decision MUST be `CHALLENGE_V1_HOOK_UNSAFE_OR_INVALID`
- **AND** the system MUST NOT recommend enforcement

#### Scenario: Observe-only validation remains narrow
- **WHEN** adapter content identity is verified, canonical prediction runs, challenge and policy hashes remain frozen, technical false accepts are zero, adversarial false-trust counts are zero, prediction mutation is zero, runtime decision delta is zero, V1 metric delta is zero, action trusted is zero, normalized trusted is zero, privacy leak is zero, policy drift is zero, and sidecar path conflict is zero
- **THEN** the decision MAY be `CHALLENGE_V1_VERIFIER_VALIDATED_OBSERVE_ONLY`
- **AND** the only recommended next change MUST be `design-and-materialize-naturalistic-copy-shadow-challenge-v2`
- **AND** runtime enforcement MUST NOT be recommended

#### Scenario: Scope limitations remain observe-only
- **WHEN** technical safety gates pass but one or more scopes have high trusted-gold mismatch, high not-found or ambiguity rates, or adapter-specific divergence
- **THEN** the decision MUST be `CHALLENGE_V1_VALIDATED_WITH_SCOPE_LIMITATIONS`
- **AND** the recommendation MUST remain observe-only and name the scope limitation without modifying the frozen policy

### Requirement: Document challenge v1 as a verifier adversarial fixture
The system SHALL update documentation and truth surfaces without presenting challenge v1 as a naturalistic language benchmark.

#### Scenario: Documentation states fixture boundary
- **WHEN** docs, reports, README, CONTEXT, evidence index, and Human Brief are updated
- **THEN** they state that challenge v1 is a copy-shadow verifier adversarial fixture with explicit scope/verifier instruction style
- **AND** they MUST NOT claim natural-language generalization, speech/ASR generalization, model quality improvement, slot accuracy improvement, runtime enforcement safety, production readiness, safety readiness, source provenance as task correctness, or realistic user benchmark coverage
