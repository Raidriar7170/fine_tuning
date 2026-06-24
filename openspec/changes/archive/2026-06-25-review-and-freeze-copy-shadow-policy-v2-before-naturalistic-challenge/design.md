## Context

The previous phase generated `configs/copy-backed-scope-policy-v2.proposed.json`
and compact design evidence under
`reports/public-sample/copy-shadow-scope-policy-v2-design/`. That proposal is
inactive and reviewer-required for all scopes: form-fill is proposed disabled,
while search and extract are insufficient-evidence. The current recommended
next step is to freeze this reviewed proposal before any naturalistic challenge
v2 work.

This change must consume only committed public-safe artifacts. It must preserve
Policy V1, frozen challenge rows/gold, predictions, sidecars, audits,
evaluators, prompts, decoding, runtime hooks, model artifacts, and training
data.

## Goals / Non-Goals

**Goals:**

- Validate that the Policy V2 proposal is internally consistent,
  proposal-only, inactive, reviewer-required, and derived from the current
  Policy V2 design evidence.
- Emit an inactive frozen Policy V2 reference artifact with deterministic
  source hashes and per-scope frozen statuses.
- Publish compact freeze evidence and status documentation that make the
  frozen boundary reviewable before naturalistic challenge v2.
- Preserve a single next bounded recommendation without starting it.

**Non-Goals:**

- No runtime loading, enforcement, action enablement, normalized trusted
  provenance, prediction repair, evaluator relaxation, schema change,
  ContractCoreV2 change, browser automation, naturalistic challenge v2,
  training, A100 work, model artifact change, or data expansion.
- No generic chat fine-tuning, skill routing, GUI action policy learning,
  first-phase GRPO, public release of the full local/private corpus, checkpoint
  release, adapter release, model improvement claim, executable-quality claim,
  production-readiness claim, or safety-readiness claim.
- No overwrite or mutation of Policy V1 or historical raw artifacts.

## Decisions

1. Freeze a new inactive artifact instead of modifying the proposed policy in
   place.

   The implementation will write
   `configs/copy-backed-scope-policy-v2.frozen.json` with
   `status=frozen_reference`, `active=false`, `runtime_loaded=false`, and
   `enforcement_enabled=false`. The original proposed JSON remains available as
   source evidence.

   Alternative considered: rename the proposed file to the frozen artifact.
   Rejected because it would blur the review trail from proposal to freeze.

2. Freeze validation is fail-closed.

   The freeze script will validate source artifact hashes, design decision
   label, proposed policy status, inactive runtime flags, challenge hash,
   diagnosis artifact hash, scope set, gate/final status agreement,
   `reviewer_required=true` for every scope, execution-ineligible state, zero
   technical false accepts, and allowed final statuses. If any check fails, it
   writes a bounded blocked artifact and does not emit a frozen policy.

   Alternative considered: emit warnings for minor drift. Rejected because a
   frozen reference must not become a second inconsistent truth surface.

3. Frozen statuses are conservative and non-executable.

   The frozen reference records the current final statuses exactly:
   `form_fill:fill_form:field -> PROPOSE_DISABLE`,
   `search:search_web:query -> INSUFFICIENT_EVIDENCE`, and
   `extract:extract_page:target -> INSUFFICIENT_EVIDENCE`. No upward review
   is possible in this phase.

   Alternative considered: allow reviewer override during freeze. Rejected
   because the previous design phase already required review and this phase is
   only freezing that reviewed outcome.

4. Runtime paths must ignore the frozen artifact.

   The implementation will not add loaders or hook config for the frozen V2
   artifact. Tests will assert that freeze reports keep `runtime_loaded=false`
   and that no runtime integration file is modified for V2 loading.

   Alternative considered: add a disabled config knob for later wiring.
   Rejected because even disabled scaffolding would broaden the phase toward
   runtime integration.

5. The next phase is recommended but not executed.

   The freeze summary may recommend a later bounded
   `design-and-materialize-naturalistic-copy-shadow-challenge-v2` phase only if
   freeze validation succeeds. It must not create naturalistic data or launch
   prediction/training work.

   Alternative considered: start naturalistic v2 immediately after freeze.
   Rejected because challenge design changes evidence scope and should be its
   own OpenSpec phase.

## Risks / Trade-offs

- [Risk] Freezing an insufficient-evidence policy may be misread as approval to
  integrate. -> Mitigation: frozen artifact remains inactive and docs repeat
  non-enforcement boundaries.
- [Risk] Review evidence drifts from proposal artifacts. -> Mitigation:
  content hashes and strict source checks block freeze output.
- [Risk] A new frozen config filename could be mistaken for runtime input. ->
  Mitigation: keep runtime flags false and avoid any loader/config wiring.
- [Risk] Public reports become too verbose. -> Mitigation: publish compact
  summary artifacts and link back to existing design evidence.

## Migration Plan

1. Add focused tests for freeze success, fail-closed drift checks, inactive
   frozen policy invariants, and public-safe docs.
2. Add the freeze module and runner script.
3. Generate the frozen policy reference and compact evidence bundle.
4. Refresh status docs, evidence index, and Human Brief from generated outputs.
5. Run focused tests, full validation, truth-surface checks, leak scan, and
   `git diff --check`.

Rollback is deleting the new frozen artifact, freeze reports, docs refreshes,
and freeze code. Policy V1, proposed Policy V2, challenge v1, predictions,
sidecars, audits, evaluator behavior, runtime behavior, and training artifacts
are unaffected.

## Open Questions

- Whether naturalistic challenge v2 should collect independent observe-only
  evidence for insufficient-evidence scopes is intentionally deferred to the
  next OpenSpec phase.
