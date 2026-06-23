# integrate-copy-backed-verification-prediction-shadow-hook

## Why
The copy-backed verifier and online shadow interface are ready for the next bounded step: an explicit opt-in hook in the canonical prediction pipeline. Before any runtime enforcement, the project needs proof that the hook can observe real prediction outputs without changing the prediction contract, output JSONL, evaluator inputs, exit behavior, runtime decisions, or gold isolation.

## What Changes
- Add a disabled-by-default `copy_backed_shadow` prediction config block for `voice2task-train sft-predict`.
- Attach a sidecar-only copy-backed shadow hook at the canonical `run_sft_prediction_export` post-prediction boundary.
- Add `NullShadowSink` and `JsonlShadowSink` so enabled shadow calculation can run without implicit persistence and JSONL sidecars require an explicit output path.
- Strengthen frozen scope-policy validation for full enabled/disabled/scope-row consistency, policy hash/version recording, action disabled, and normalized-trusted disabled.
- Fail-isolate invalid predictions, policy errors, verifier errors, serialization errors, and sink errors so primary prediction output and status remain unchanged.
- Default online sidecars to hash-and-offset-only retention with no gold, raw input text, raw model output, full prediction contract, raw request id, or span text.
- Publish compact public-safe evidence, docs, and a Chinese Human Brief for the observe-only hook.

## Out Of Scope
- Runtime enforcement, execution permission, action enablement, normalized trusted provenance, URL resolution, ambiguity representation, semantic similarity, LLM judge, evaluator changes, layered evaluator changes, V1 or ContractCoreV2 schema changes, parser semantic changes, prompt or decoding changes, model training, prediction repair, data/split changes, A100/GPU work, adapter/checkpoint release, or challenge-set construction.

## Success Criteria
- The canonical entrypoint is identified as `voice2task-train sft-predict` / `run_sft_prediction_export`.
- Old configs and `enabled=false` configs produce identical prediction behavior and no copy-shadow sidecar file.
- Enabled `NullShadowSink` and enabled explicit `JsonlShadowSink` keep prediction output JSONL and loaded predictions identical.
- Invalid contracts, malformed JSON/string predictions, policy drift, verifier failures, serialization failures, and sink failures are recorded as bounded hook outcomes and never escape into the primary prediction path.
- Trusted provenance is exact-unique only; normalized remains candidate-only; action remains untrusted.
- Online sidecars contain no gold fields and default to hash-and-offset-only source spans.
- Policy id, version, and hash are recorded for every sidecar.
- Final evidence reports zero contract mutation, runtime decision delta, V1 metric delta, provenance false accepts, silent fallback, normalized trusted count, and action trusted count.
- `ruff check .`, full pytest, OpenSpec validation, truth-surface check, leak scan, prediction-output invariance, deterministic rerun, and `git diff --check` are run before completion claims.
