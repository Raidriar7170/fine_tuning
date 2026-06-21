# Voice2Task Current Context

## 1. Project Scope

Voice2Task Post-Training is an evidence-first companion project for Chinese spoken command / ASR transcript -> schema-valid browser task contracts. The project studies public-safe SFT/DPO data construction, Qwen2.5-7B-Instruct + LoRA training paths, prediction artifacts, strict contract evaluation, and offline schema projections. It is not a browser controller, GUI action policy learner, generic chat fine-tune, checkpoint release, or production system.

## 2. Current Formal Data Boundary

The current formal public sample is `public-sample-20260619T090925Z` in `data/public-samples/manifest_public_sample.json`: 247 seeds / 696 SFT rows / 2100 DPO pairs, with train/dev/test = 282/207/207. This boundary was produced by the canonical slot-boundary formal merge and is the current data boundary only; it is not a model-quality claim.

Prior manifests, prior prediction runs, and prior A100 training retries are historical unless explicitly marked `CURRENT` in `reports/public-sample/EVIDENCE_INDEX.md`.

## 3. Latest Model Experiment

The latest model experiment is the one-seed step-matched canonical-slot SFT ablation under `reports/public-sample/step-matched-canonical-slot-ablation/`. Control and Treatment used the same explicit 3132 optimizer-step budget, frozen dev/test inputs, same evaluator, same decoding boundary, and private unreleased Qwen2.5-7B-Instruct LoRA adapters.

The canonical slot treatment under the step-matched condition has no stable general benefit. The result is mixed / statistically inconclusive: some strict exact numbers improve, but guardrails do not establish broad canonical-data gain. It does not trigger a 3-seed confirmation, DPO/GRPO, another small canonical-candidate loop, adapter/checkpoint release, production readiness, safety readiness, held-out recovery, or live-browser claim.

## 4. Latest Architecture Experiment

The latest architecture experiment is the recovered-input Contract V2 offline projection under `reports/public-sample/contract-v2-projection/rerun-with-recovered-inputs/summary.json`. It used recovered metric-reproduced step-matched prediction contracts and aligned gold contracts from `reports/public-sample/step-matched-canonical-slot-ablation/raw-inputs/`.

Decision: `PARTIAL_SCHEMA_BENEFIT`. Derived-field-only strict failures are 14.65%; normalized-command-only strict failures are 14.65%; metadata-only failures are 0%. V2 core exact improves slightly by +0.0193 / +0.0386 for Control dev/test and +0.0290 / +0.0242 for Treatment dev/test. V2 executable pass has no improvement. Renderer support is 99.88%; deterministic roundtrip is 1.0. Core slot failures remain the dominant bottleneck at about 68.79%.

No model weights changed during the Contract V2 projection. No training, prediction rerun, prediction repair, evaluator relaxation, schema implementation, LLM judge, semantic-equivalence scoring, checkpoint release, or adapter release occurred.

## 5. Current Technical Interpretation

strict exact remains canonical diagnostic. The Contract V2 projection only reduces derived/display-field burden, mainly `normalized_command`; it does not repair core slot errors and does not improve executable contract pass. The main engineering bottleneck is still slot representation / slot error mechanisms, not whether another small canonical candidate loop should be run.

Projection follow-up `decide-contract-v2-core-implementation-scope` is now closed by an internal boundary implementation. The internal Contract V2 Core status is `INTERNAL_V2_CORE_READY_RENDERER_PARTIAL`: 2185 current public-safe V1 contracts passed preserve_legacy roundtrip with exact V1 compatibility, safety preservation, confirmation preservation, and slot preservation all at 1.0; V1 evaluator metric deltas are all 0. The derive_display renderer remains partial at 99.77% support with 5 unsupported cases, so it is not the default path.

Contract V2 should not be packaged as model improvement. The external schema remains BrowserTaskContract V1, the training target remains V1, downstream runtime remains V1, and the internal Core boundary exists only as a shadow-compatible engineering boundary.

## 6. Current Claim Boundaries

Current evidence cannot claim model improvement. It cannot claim executable quality improvement. It cannot claim production readiness. It cannot claim safety readiness. It cannot claim held-out recovery. It cannot claim live-browser benchmark gain. It cannot claim checkpoint release. It cannot claim adapter release. It cannot claim DPO justification. It cannot claim another canonical-candidate loop.

Do not merge metrics across manifests. Do not treat JSON validity, executable smoke, train-internal success, or derived-field projection as model capability recovery. Do not delete or rewrite negative, blocked, superseded, or historical results.

## 7. Current Recommended Next Change

The single recommended next technical change is `analyze-slot-error-mechanisms-and-design-slot-representation`. That future phase should analyze missing key, extra key, wrong key, wrong entity, copy error, normalization error, clarify ambiguity error, and family-specific slot error mechanisms. Do not start it automatically from the internal Contract V2 Core closeout.

## 8. Evidence Index Link

Use `reports/public-sample/EVIDENCE_INDEX.md` for the unified evidence map and `reports/public-sample/evidence-index.json` for the machine-readable classification. Raw report directories under `reports/public-sample/<phase>/` remain authoritative and unchanged.
