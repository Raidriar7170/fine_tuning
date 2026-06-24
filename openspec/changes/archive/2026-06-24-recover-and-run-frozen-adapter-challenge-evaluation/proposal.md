## Why

The frozen `copy-shadow-template-disjoint-challenge-v1` phase correctly blocked because no local loadable, identity-verifiable frozen adapter was available. The next bounded question is whether an existing step-matched frozen adapter can be recovered and evaluated through the canonical prediction shadow hook without changing the challenge, policy, prediction semantics, prompt, decoding, evaluator, or runtime behavior.

## What Changes

- Add a recovery-and-evaluation path for existing step-matched Control/Treatment adapters against the already frozen verifier-focused challenge v1.
- Verify adapter identity with public-safe metadata before inference and block if an adapter is unavailable or identity cannot be proven.
- Run prediction-only challenge inference through `voice2task-train sft-predict` / `voice2task.training.run_sft_prediction_export` and the integrated copy-backed prediction shadow hook only after all frozen boundary checks pass.
- Compare shadow disabled, enabled NullSink, and enabled JsonlSink boundaries without mutating primary prediction output or runtime decisions.
- Generate online gold-free sidecars, separate offline evaluation audits, per-scope/per-condition metrics, hook safety metrics, latency evidence, docs, and truth-surface updates.
- If recovery or boundary checks fail, write a bounded blocked artifact and stop without fabricating predictions or creating replacement adapters.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `copy-backed-verification-shadow-mode`: add frozen adapter recovery, identity verification, canonical challenge inference, online sidecar/offline audit separation, and conservative decision labels for the frozen verifier-focused challenge evaluation.

## Impact

- Affected code: adapter recovery/identity helpers, prediction-only challenge runner, hook-sidecar/evaluation audit report generation, tests, and local scripts.
- Affected artifacts: `reports/public-sample/copy-shadow-template-disjoint-challenge-v1/adapter-evaluation/`, `docs/copy-shadow-template-disjoint-challenge.md`, README/README_en/CONTEXT, evidence index, Human Brief, and OpenSpec archive.
- Explicitly not affected: model weights, SFT/DPO/GRPO, prompt, decoding, evaluator, BrowserTaskContract V1, ContractCoreV2, frozen challenge rows, frozen scope policy, enabled triples, downstream runtime decisions, action provenance, normalized trusted provenance, and production enforcement.
