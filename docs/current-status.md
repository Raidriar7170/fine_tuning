# Current Status and Evidence

> This document preserves the detailed experimental state, evidence links, negative results, and claim boundaries. The repository README intentionally contains only a recruiter-facing summary.

## Current Snapshot

- Task: Chinese spoken / ASR browser commands -> schema-valid browser task contracts.
- Model path: Qwen2.5-7B-Instruct + LoRA; private A100 adapters are observed but not released.
- Current formal sample: `public-sample-20260619T090925Z`; 247 seeds / 696 SFT rows / 2100 DPO pairs; train/dev/test = 282/207/207.
- Latest training experiment: one-seed step-matched canonical-slot SFT ablation with 3132 optimizer steps per arm.
- Training conclusion: mixed / statistically inconclusive; no stable general canonical-data benefit.
- Latest architecture experiment: Contract V2 offline projection with recovered step-matched inputs.
- Projection conclusion: `PARTIAL_SCHEMA_BENEFIT`.
- Derived-field-only strict failures: 14.65%; normalized-command-only strict failures: 14.65%; metadata-only failures: 0%.
- V2 core exact: small improvement, +0.0193 / +0.0386 for Control dev/test and +0.0290 / +0.0242 for Treatment dev/test.
- V2 executable pass: no improvement.
- Dominant bottleneck: core slot failures remain about 68.79% of V1 strict failures.
- Renderer check: normalized-command renderer support is 99.88%; deterministic roundtrip is 1.0.
- Projection follow-up `decide-contract-v2-core-implementation-scope` is closed as an internal implementation boundary.
- Internal Contract V2 Core: `INTERNAL_V2_CORE_READY_RENDERER_PARTIAL`; preserve_legacy V1 roundtrip, safety, confirmation, and slots all remain 1.0; V1 evaluator metric deltas are all 0.
- Internal derive_display support is 99.77%, with 5 unsupported renderer cases; it is not the default path.
- Completed internal-core recommendation: `analyze-slot-error-mechanisms-and-design-slot-representation`.
- Slot mechanism analysis: `MIXED_SLOT_REPRESENTATION_REQUIRED`; exact/normalized source-copyable gold slots 50.53%; typed-derivable slots 0.00%; generation-required slots 49.47%; prediction unsupported-by-source 32.17%.
- Hybrid slot representation design: `HYBRID_DESIGN_READY_COPY_SLICE_FIRST`; overall representation coverage 100.00%; copy-backed coverage 57.32%; bounded structured coverage 31.21%; unresolved coverage 11.46%; current predictions deterministically verifiable at 51.80% and fail-closed at 48.20%.
- Copy-backed slot verification slice: `COPY_SLICE_READY_FOR_SHADOW_INTEGRATION`; enabled triples are `extract:extract_page:target`, `form_fill:fill_form:field`, and `search:search_web:query`; gold unique verified span rate is 86.38%; Control/Treatment source-verified prediction rate over eligible events is 87.44%; provenance false accepts and silent fallbacks are 0.
- Copy-backed verification shadow mode: `SHADOW_MODE_READY_FOR_REVIEW`; 828/828 current Control/Treatment prediction contracts have shadow sidecars; enforcement enabled count is 0; action source-verified count is 0; V1 evaluator metric deltas remain 0.
- Copy-backed shadow interface review: `SHADOW_INTERFACE_READY_FOR_PREDICTION_HOOK`; online sidecars are gold-free for 828/828 prediction contracts; evaluation audit rows are 942; trusted exact rate is 87.44%; eligible verification failure rate is 12.56%; out-of-scope rate is 54.35%; trusted-exact gold mismatch rate is 7.71%; false accepts, silent fallbacks, contract mutations, runtime deltas, normalized trusted cases, and action trusted cases are all 0.
- Copy-backed prediction shadow hook: `PREDICTION_SHADOW_HOOK_READY_OBSERVE_ONLY`; opt-in hook is integrated into `voice2task-train sft-predict` / `run_sft_prediction_export`; default is disabled; disabled/NullSink/JsonlSink prediction output hashes match; deterministic rerun is true; V1 metric deltas remain 0; public hook fixture emits 3 trusted exact spans and 1 normalized candidate span.
- Copy-shadow template-disjoint challenge v1: copy-shadow verifier adversarial fixture, not a naturalistic language benchmark; recovered step-matched A100 adapters select `CHALLENGE_V1_HOOK_UNSAFE_OR_INVALID`; 6 prediction runs completed across Control/Treatment disabled, NullSink, and JsonlSink modes, but adversarial source-absent, normalization-collision, and partial-span traps produced high-risk false-trust counts.
- Must Fix Phase 3 lockbox lineage guard: deterministic validator and `voice2task-data validate-lockbox` CLI are implemented for row hashes, exact/normalized text overlap, semantic family overlap, forbidden ancestry, provenance, duplicate hashes, manifest count/hash, and frozen manifest checks. Real new frozen lockbox rows are not present, so final lockbox evaluation and metrics remain blocked until content is authored separately.
- Current boundary: challenge v1 is observe-only verifier-fixture evidence with a failed safety gate; no runtime enforcement, action trusted provenance, normalized trusted provenance, model-quality claim, or safety/production readiness claim follows from it.

No model weights changed during the Contract V2 projection, slot mechanism analysis, hybrid slot representation design, copy-backed verification slice, shadow-mode integration, shadow interface review, prediction shadow hook, template-disjoint challenge freeze, or recovered-adapter challenge evaluation. strict exact remains canonical diagnostic. Prior metrics are historical unless marked `CURRENT` in the evidence index.

## Current Evidence

| Evidence | Current conclusion |
| --- | --- |
| [`reports/public-sample/contract-v2-projection/rerun-with-recovered-inputs/summary.json`](../reports/public-sample/contract-v2-projection/rerun-with-recovered-inputs/summary.json) | Current Contract V2 projection result: `PARTIAL_SCHEMA_BENEFIT`. |
| [`reports/public-sample/internal-contract-v2-core/summary.json`](../reports/public-sample/internal-contract-v2-core/summary.json) | Internal Contract V2 Core boundary is V1-compatible in preserve mode; derive_display remains partial. |
| [`reports/public-sample/slot-error-mechanism-analysis/summary.json`](../reports/public-sample/slot-error-mechanism-analysis/summary.json) | Slot mechanism analysis result: `MIXED_SLOT_REPRESENTATION_REQUIRED`; next change is `design-hybrid-slot-representation-v1`. |
| [`reports/public-sample/hybrid-slot-representation-v1/summary.json`](../reports/public-sample/hybrid-slot-representation-v1/summary.json) | Hybrid representation design result: `HYBRID_DESIGN_READY_COPY_SLICE_FIRST`; next change is `implement-copy-backed-slot-verification-slice`. |
| [`reports/public-sample/copy-backed-slot-verification-slice/summary.json`](../reports/public-sample/copy-backed-slot-verification-slice/summary.json) | Copy-backed verification slice result: `COPY_SLICE_READY_FOR_SHADOW_INTEGRATION`; sidecar-only provenance for task-scoped `query`/`field`/`target`. |
| [`reports/public-sample/copy-backed-verification-shadow-mode/summary.json`](../reports/public-sample/copy-backed-verification-shadow-mode/summary.json) | Shadow-mode integration result: `SHADOW_MODE_READY_FOR_REVIEW`; one sidecar per current prediction contract, no enforcement. |
| [`reports/public-sample/copy-backed-shadow-mode-review/summary.json`](../reports/public-sample/copy-backed-shadow-mode-review/summary.json) | Shadow interface review result: `SHADOW_INTERFACE_READY_FOR_PREDICTION_HOOK`; gold-free online sidecars, offline audit split, no enforcement. |
| [`reports/public-sample/copy-backed-prediction-shadow-hook/summary.json`](../reports/public-sample/copy-backed-prediction-shadow-hook/summary.json) | Prediction shadow hook result: `PREDICTION_SHADOW_HOOK_READY_OBSERVE_ONLY`; default-off sidecar hook, prediction output invariant, no enforcement. |
| [`reports/public-sample/copy-shadow-template-disjoint-challenge-v1/adapter-evaluation/challenge-evaluation-summary.json`](../reports/public-sample/copy-shadow-template-disjoint-challenge-v1/adapter-evaluation/challenge-evaluation-summary.json) | Recovered step-matched adapter challenge result: `CHALLENGE_V1_HOOK_UNSAFE_OR_INVALID`; adversarial false-trust evidence, no enforcement. |
| [`docs/lockbox.md`](lockbox.md) | Phase 3 lockbox workflow and one-look rule; workflow implemented, real frozen lockbox content blocked. |
| [`reports/public-sample/step-matched-canonical-slot-ablation/comparison.json`](../reports/public-sample/step-matched-canonical-slot-ablation/comparison.json) | Latest model experiment: mixed / inconclusive; no stable broad canonical-slot benefit. |
| [`data/public-samples/manifest_public_sample.json`](../data/public-samples/manifest_public_sample.json) | Current formal sample boundary: 247 seeds / 696 SFT rows / 2100 DPO pairs. |
| [`reports/public-sample/EVIDENCE_INDEX.md`](../reports/public-sample/EVIDENCE_INDEX.md) | Unified current / historical / superseded / blocked / design-only / raw-input / archived evidence map. |

## Claim Boundaries

Current evidence cannot claim model improvement. It cannot claim executable quality improvement. It cannot claim production readiness. It cannot claim safety readiness. It cannot claim held-out recovery. It cannot claim live-browser benchmark gain. It cannot claim checkpoint release. It cannot claim adapter release. It cannot claim DPO justification. It cannot claim another canonical-candidate loop.

The Contract V2 projection is offline schema-burden evidence only: it removes derived/display-field burden from strict exact comparison, but it does not claim model improvement. The internal Contract V2 Core boundary now exists behind a V1-compatible deterministic envelope; it does not change the public V1 schema, V1 evaluator, training target, predictions, or downstream runtime. The slot mechanism analysis and hybrid slot representation design are read-only/design-only evidence. The copy-backed verification slice, shadow-mode integration, shadow interface review, prediction shadow hook, and recovered-adapter challenge run are provenance/interface evidence only. Challenge v1 is observed through recovered frozen adapters, but it remains a verifier adversarial fixture, not naturalistic generalization or task correctness evidence. Source-backed provenance is not task correctness, slot accuracy, executable quality, runtime enforcement, production readiness, or challenge-set generalization.

## A100 / Private Artifact Boundary

GPU-heavy training and prediction are designed for a private A100 development machine. Public repo artifacts intentionally omit checkpoints, LoRA adapters, raw logs, remote caches, private corpus rows, hostnames, SSH details, credentials, private paths, private override configs, and production-readiness claims.
