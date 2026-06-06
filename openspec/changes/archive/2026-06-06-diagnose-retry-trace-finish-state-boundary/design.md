## Context

The latest A100 retry generation trace rerun produced:

- `generation_trace.jsonl` with `6` rows: `3` raw attempts and `3` retry attempts.
- Raw attempts: `finish_state=eos_observed` for `3/3`.
- Retry attempts: `finish_state=no_eos_observed` for `3/3`.
- Retry generated token counts below `max_new_tokens=256` for `3/3`.
- Strict final `json_valid_rate=0.0000` and `contract_exact_match=0.0000`.

The trace implementation currently sets `finish_state` to `eos_observed` only when the configured tokenizer EOS id appears in the generated token slice; otherwise it sets `no_eos_observed`. The prediction call does not explicitly pass `eos_token_id` into `model.generate`, so this evidence is not enough to prove whether the model stopped on another generation-config EOS id, another stopping criterion, or an implementation-level boundary.

## Decision

Create a local diagnosis only. The diagnosis should read committed public evidence and source code, then publish a bounded interpretation:

- `finish_state=no_eos_observed` means tokenizer EOS was not observed in the generated token slice.
- It does not prove max-token truncation when `generated_token_count < max_new_tokens`.
- It does not prove that no stop token, model-generation EOS, or stopping criterion fired.
- It does not justify parser relaxation or model recovery claims.

## Evidence Plan

- Source artifacts:
  - `reports/public-sample/a100-retry-generation-trace-rerun/generation_trace.jsonl`
  - `reports/public-sample/a100-retry-generation-trace-rerun/retry_trace_diagnosis.json`
  - `src/voice2task/training.py`
- Output artifacts:
  - `finish_state_boundary_diagnosis.json`
  - `finish_state_boundary_diagnosis.md`
  - `manifest.json`
  - leak-scan outputs
  - Human Brief HTML

## Risks

- Overstating `no_eos_observed` as a full stop-reason claim would be misleading.
- Changing the trace writer in this phase would widen scope into instrumentation behavior; keep this phase diagnostic-only.
- Private A100 logs, configs, adapters, and raw remote details remain out of scope.
