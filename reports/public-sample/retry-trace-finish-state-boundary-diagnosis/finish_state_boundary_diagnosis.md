# Retry trace finish-state boundary diagnosis

This is a local evidence-only diagnosis from committed public artifacts. It does not rerun A100 prediction and does not change decoding behavior.

## Result

- Retry trace rows: `3`.
- Retry finish states: `{'no_eos_observed': 3}`.
- Retry generated token count range: `146` to `165`.
- Retry max-token-hit count: `0`.
- Retry no-eos-below-max count: `3`.
- Actual generation stop reason recorded: `False`.

## Interpretation Boundary

- `finish_state=no_eos_observed` means the tokenizer EOS id was not observed in the generated token slice.
- Because retry token counts are below `max_new_tokens`, max-token truncation is not proven by this evidence.
- Because the trace does not record model/generation-config stop reason, the actual stop reason remains unknown.
- This does not justify parser relaxation, prediction repair, or a model recovery claim.

## Non-Claims

- No A100 execution or prediction rerun was performed in this phase.
- No training, decoding behavior change, retry prompt change, parser relaxation, evaluator metric change, prediction repair, semantic-equivalence scoring, or slot normalization was performed.
- No model-quality, model-recovery, public full-corpus release, production-readiness, or live-browser benchmark improvement claim is made.
