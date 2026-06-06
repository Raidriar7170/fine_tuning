# Retry generation trace instrumentation

Conclusion: this phase adds attempt-level `generation_trace.jsonl` rows so future trained-adapter exports can distinguish `raw_attempt` from `retry_attempt` token/finish evidence.

## What changed

- `generation_trace.jsonl` keeps its existing fields and adds `attempt`.
- Raw generation rows are labelled `attempt=raw_attempt`.
- When schema retry is attempted, retry generation rows are written as `attempt=retry_attempt`.
- The retry prompt, decoding parameters, strict parser, schema guard selection, predictions, and metrics are unchanged.

## TDD evidence

- RED observed: focused test failed because trace rows did not include retry attempt coverage.
- GREEN observed: `PYTHONPATH=src pytest -q tests/test_a100_sft_prediction_smoke.py::test_real_sft_prediction_generation_trace_records_retry_attempt` passed after the minimal instrumentation change.

## Historical boundary

- Prior A100 artifacts are not rewritten.
- The previous A100 retry-wrapper rerun still lacks retry generation trace evidence.
- A future A100/private-adapter rerun is required before making real retry stop-boundary claims.

## Non-claims

No A100 execution, training, private prediction rerun, decoding change, parser relaxation, evaluator metric change, prediction repair, re-score, semantic-equivalence scoring, slot normalization, checkpoint release, adapter release, model recovery claim, model-quality claim, or live-browser benchmark improvement claim is made.
