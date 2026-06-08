## Context

The archived `run-a100-first-pass-fence-suppression-rerun` phase observed `0/3` Markdown-wrapped outputs and `3/3` strict schema-valid raw outputs after generation-time fence suppression. Strict exact match is still `2/3` and slot F1 is `2/3` because `seed-search-weather-aug-1` emits `slots={"city":"北京","date":"明天","topic":""}` while the gold row expects `slots={"query":"北京明天天气"}`.

This phase should explain that residual mismatch only. It should not reinterpret the successful wrapper/schema observation as a broad model-quality claim, and it should not normalize or repair the slot mismatch.

## Goals / Non-Goals

**Goals:**

- Generate a concise row-level diagnosis for the one residual slot mismatch.
- Preserve strict metric interpretation: exact slot key/value equality remains the scoring boundary.
- Link to the source A100 fence-suppression rerun artifacts and prior local suppression evidence.
- Generate public-safe evidence, tests, and a Human Brief.

**Non-Goals:**

- No A100 execution, training, prediction rerun, parser relaxation, evaluator metric change, slot normalization, semantic-equivalence scoring, prediction repair, re-score, checkpoint release, adapter release, production-readiness claim, held-out generalization claim, live-browser benchmark claim, model recovery claim, or broad model-quality improvement claim.

## Decisions

1. Use local artifact-derived diagnosis only.

   The source A100 rerun already produced the predictions, train gold, metrics, schema guard summary, and alignment diagnostics. Re-running prediction would mix a new observation into a diagnosis phase.

2. Keep strict slot exact-match semantics.

   The predicted `city/date/topic` object may be semantically related to weather search, but this phase must not treat it as equivalent to the gold compact `query` string.

3. Report wrapper/schema success and slot residual separately.

   The evidence should say wrapper/schema improved on train rows while one slot exact-match mismatch remains.

## Risks / Trade-offs

- [Risk] Report wording overstates `2/3` exact match as model-quality recovery. -> Keep non-claim fields and Human Brief wording explicit.
- [Risk] Diagnosis reads like a recommended slot normalization policy. -> State that normalization and semantic equivalence are not performed.
- [Risk] Public artifacts leak private A100 paths from source metadata. -> Use only sanitized source artifacts and run leak scans.
