# A100 generation stop-boundary train-split rerun

Status: train-internal A100 diagnostic rerun after local generation stop-boundary instrumentation. This is not a benchmark, not a release, and no held-out generalization claim is made.

## Result

The rerun produced `3` train predictions from the private A100 adapter path. Strict final-contract `json_valid_rate=0.0000` and `contract_exact_match=0.0000` remain unchanged from the comparable retry-trace rerun.

Raw attempts remain complete JSON objects but still omit `task_type` for `3/3` rows. Retry attempts remain prose/markdown JSON fragments for `3/3` rows. This must not be described as schema recovery or model recovery.

## Stop-Boundary Result

The new evidence pack records `6` generation trace rows with the new stop-boundary fields on every row. Raw attempts observed tokenizer EOS for `3/3` rows. Retry attempts show `not_recorded_below_max_without_tokenizer_eos` for `3/3` rows, with `max_new_tokens_hit=false` and `actual_stop_reason_recorded=false`.

This narrows the previous trace gap: retry attempts now carry explicit boundary evidence, but actual stop reason remains unrecorded and unknown.

## Boundary

The evidence pack contains sanitized public-sample predictions, aggregate metrics, schema diagnostics, constrained decoding diagnosis, schema guard summaries, generation stop-boundary diagnosis, and leak-scan status. It does not copy raw logs, checkpoints, adapters, remote caches, private configs, host details, tokens, SSH details, private paths, or private corpus rows into git.

No training, decoding behavior change, retry prompt change, parser relaxation, evaluator metric change, prediction repair, prediction re-score, semantic-equivalence scoring, slot normalization, production-readiness claim, held-out generalization claim, model-quality claim, public full-corpus release, or live-browser benchmark improvement claim is made.
