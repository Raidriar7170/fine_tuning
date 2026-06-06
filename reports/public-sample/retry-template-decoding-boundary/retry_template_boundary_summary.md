# Retry template decoding boundary

Status: local retry template/decoding-boundary hardening only. This does not prove trained-adapter output behavior changed.

## Result

- Retry decode now uses an explicit chat-template/fallback boundary for a machine-only schema retry turn.
- Prediction metadata and prompt snapshots expose retry template boundary booleans.
- Strict whole-object parser behavior is unchanged: wrapped fragments remain invalid.

## Prior A100 Context

- Prior strict final json_valid_rate: `0.0000`
- Prior strict final contract_exact_match: `0.0000`
- Prior retry prose/Markdown wrappers: `3/3`

## Boundary

No A100 execution, training, checkpoint release, adapter release, parser relaxation, evaluator metric change, schema repair/coercion, prediction repair, prediction re-score, semantic-equivalence scoring, slot normalization, held-out generalization claim, production-readiness claim, public full-corpus release claim, live-browser benchmark improvement claim, model recovery claim, or model-quality improvement claim is made.

## Archive And Validation

- OpenSpec archived at `openspec/changes/archive/2026-06-06-retry-template-decoding-boundary/`.
- Local tests, lint/type checks, data validation, DPO check, OpenSpec validation, and public-safe leak scans passed.
- Reviewer subagent was unavailable due to a tool timeout; main-thread Reviewer pass found no Must Fix items.
