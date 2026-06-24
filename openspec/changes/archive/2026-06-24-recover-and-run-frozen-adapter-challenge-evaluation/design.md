## Context

The repository currently has a frozen 120-row public-safe challenge at `data/public-samples/copy-shadow-template-disjoint-challenge-v1.jsonl` and a blocked report bundle under `reports/public-sample/copy-shadow-template-disjoint-challenge-v1/`. The frozen policy is `copy-backed-scope-policy-v1` with hash `5dc14efb8ded13dc048ddb067c7c63a1a62b6c03896950e861303973d505cbc7`. The prior phase hardened the prediction shadow hook and archived the OpenSpec change after blocking adapter-backed inference due to zero identity-verifiable loadable frozen adapters.

This phase is not a naturalistic Chinese instruction or ASR benchmark. Challenge v1 is a copy-shadow verifier adversarial fixture with explicit verifier/scope cues. It can test whether the hook and verifier fail closed under adversarial source-span conditions, but it cannot establish real user-language or speech generalization.

## Goals / Non-Goals

**Goals:**

- Re-confirm the frozen challenge, manifest hash, template-disjoint audit, and frozen policy hash before any prediction.
- Discover existing step-matched Control/Treatment frozen adapters, optionally through a private override that never enters public artifacts.
- Verify adapter identity from public-safe metadata and readable adapter files before inference.
- Run prediction-only inference through the canonical prediction path and integrated hook when identity is verified.
- Write gold-free online sidecars and separate offline gold evaluation audits after predictions and sidecars are frozen.
- Report technical hook/verifier safety, per-scope/per-condition diagnostics, latency, privacy, and conservative final decision labels.
- Emit bounded blocked artifacts when boundary, availability, or identity gates fail.

**Non-Goals:**

- No SFT, DPO, GRPO, retraining, checkpoint continuation, model swap, prompt change, decoding change, evaluator change, schema change, policy change, enabled-triple change, challenge row/tag/gold change, prediction repair, slot-value replacement, runtime enforcement, action enablement, normalized trusted provenance, URL resolver, ambiguity representation, train/dev/test merge, model-quality improvement claim, executable-quality claim, natural-language generalization claim, production readiness, safety readiness, or automatic next phase.

## Decisions

1. **Boundary-first recovery.** The runner must validate the committed challenge hash, row count, template-disjoint audit, policy id/version/hash, `action_enabled=false`, `normalized_trusted=false`, and active OpenSpec state before adapter recovery. If any boundary fails, it writes `CHALLENGE_EVALUATION_BLOCKED_BOUNDARY_MISMATCH`.

2. **Identity before inference.** Adapter discovery may use private override inputs, but public artifacts record only sanitized fields: adapter role, run id, manifest id, base model id, config hash, adapter content hash, identity status, and failures. Any missing adapter becomes `CHALLENGE_EVALUATION_BLOCKED_ADAPTER_UNAVAILABLE`; any present but unverifiable adapter becomes `CHALLENGE_EVALUATION_BLOCKED_ADAPTER_IDENTITY`.

3. **Canonical path only.** Successful inference must go through `voice2task-train sft-predict` or the library-equivalent `run_sft_prediction_export`, not a standalone verifier or hand-built prediction file. Hook disabled, NullSink, and JsonlSink comparisons must prove output hash and parsed-contract invariance.

4. **Online/offline separation.** Online sidecars remain gold-free and hash/offset-only by default. Gold correctness is joined only in offline evaluation audit artifacts after predictions and sidecars are frozen.

5. **Blocked is a valid terminal result.** If no suitable adapter can be verified locally or through an allowed private override, this change should report the bounded blocked label, update docs briefly, archive, and stop rather than broadening into retraining or challenge v2.

## Risks / Trade-offs

- **Private path leakage** -> sanitize every report field, scan generated docs/reports, and never commit private override files.
- **Unverifiable adapter resemblance** -> require explicit identity metadata and content hashes; do not infer identity from similar directory names.
- **Challenge v1 overclaim** -> label it as a verifier adversarial fixture in summaries, README/CONTEXT, Human Brief, and final report.
- **Generation randomness** -> if stochastic configs are encountered, hold generation artifacts fixed and compare hook behavior at the post-parse boundary.
- **Remote/A100 availability** -> use existing SSH/private override mechanisms only when safe; otherwise block with public-safe evidence.
