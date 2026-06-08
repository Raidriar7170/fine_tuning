## Context

The archived local phase `repair-output-boundary-template-decoding-instrumentation` added a prediction-only `PREDICTION_SYSTEM_PROMPT` and exposed `prediction_output_boundary` metadata. The latest A100 search-query slot rerun remains the comparison baseline: `3/3` predictions were Markdown-wrapped and strict schema-valid output stayed `0/3`.

This phase is remote execution, but not training. It uses the approved A100 development machine rules, keeps private overrides and model artifacts outside git, and commits only sanitized public-sample evidence.

## Goals / Non-Goals

**Goals:**

- Run one prediction-only train-split A100 rerun using the current committed code and existing private adapter.
- Verify whether first-pass prompt snapshots and metadata contain `prediction_output_boundary`.
- Compare strict schema-valid, wrapper, raw/retry parse status, and exact-match outcomes against `a100-search-query-slot-policy-rerun`.
- Publish public-safe evidence and a Human Brief.

**Non-Goals:**

- No training, DPO, GRPO, adapter/checkpoint release, deployment, parser relaxation, metric relaxation, prediction repair, prediction re-score, semantic-equivalence scoring, slot normalization, or live-browser benchmark claim.
- No committed private override, private path, raw log, host detail, SSH detail, token, model cache, checkpoint, adapter, or private corpus row.

## Decisions

1. Use train split only.

   This isolates whether the existing adapter follows the new first-pass output boundary on rows it has already been diagnosing. It is not held-out generalization evidence.

2. Compare against the latest search-query slot-policy rerun.

   That baseline is closest in target policy and failure shape: compact query fragments appeared, but wrappers kept strict schema-valid output at `0/3`.

3. Keep strict parser and metrics unchanged.

   If the model still emits wrapped fragments, they remain invalid. The evidence must report that outcome rather than extracting or repairing embedded JSON.

4. Keep A100 artifacts private by default.

   Only sanitized predictions, sidecars, metrics, summaries, manifests, leak scans, and Human Briefs are copied into git.

## Risks / Trade-offs

- [Risk] No idle GPU is safely available. -> Stop instead of launching.
- [Risk] Remote private adapter path or override is unavailable. -> Stop with a blocked evidence note rather than fabricating fixture results.
- [Risk] The adapter still emits Markdown wrappers. -> Preserve the failure and report no model-quality improvement.
- [Risk] The rerun improves train split only. -> Keep `generalization_claim=false` and recommend held-out validation only after separate user confirmation.
