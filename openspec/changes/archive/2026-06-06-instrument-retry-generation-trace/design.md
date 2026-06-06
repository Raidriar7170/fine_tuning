## Context

The latest local diagnosis established a precise evidence gap:

- Raw attempt generation trace rows exist and can show token count, EOS visibility, and finish state.
- Retry decoded summaries exist, but retry attempt generation trace rows do not.
- The current implementation already receives retry `new_tokens` from `_decode_prediction_attempt(...)`, but discards them before writing `generation_trace.jsonl`.

This phase fills that observability gap only. It does not test a new decoding parameter, alter retry prompts, reinterpret parser output, or run A100.

## Design

Use one JSONL sidecar, `generation_trace.jsonl`, with one row per generation attempt:

- Raw attempt rows keep the existing fields and add `attempt="raw_attempt"`.
- Retry attempt rows use the same trace schema and add `attempt="retry_attempt"`.
- Retry trace rows are written only when schema retry is actually attempted.
- Existing consumers that group by `id` continue to have the same row id values, while new consumers can distinguish attempts via the `attempt` field.

This keeps evidence local and additive. It intentionally does not add retry stop conclusions to historical A100 artifacts; old traces remain old traces.

## Evidence Plan

- Add a TDD test that fails before implementation because retry trace rows are absent.
- Assert both raw and retry trace rows preserve token counts, EOS visibility, and `max_new_tokens` policy.
- Generate a public-safe evidence pack summarizing:
  - instrumentation is local only,
  - fake private-adapter test path observes raw and retry trace coverage,
  - historical A100 retry trace remains missing until a future rerun,
  - metrics and parser behavior are unchanged.

## Risks

- Historical evidence may be misread as retroactively instrumented. Mitigation: evidence and Human Brief explicitly say this only affects future prediction exports.
- Downstream tests that expected one trace row per id may need attempt-aware assertions. Mitigation: keep `id` unchanged and add `attempt` rather than renaming existing fields.
- A future A100 rerun is still required to observe real retry stop behavior. This phase prepares that evidence path but does not perform it.
