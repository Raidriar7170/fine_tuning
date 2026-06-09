# Compact-query exact-match residual diagnosis

This is a local evidence-only diagnosis. No A100 execution was performed in this phase. The pack does not train, rerun predictions, change decoding, relax the parser, change evaluator metrics, repair predictions, replace predictions, or re-score outputs; it does not perform slot normalization or semantic-equivalence scoring.

## Conclusion

The latest compact-query slot-preservation rerun has strict JSON/schema-valid output for all three train rows, but `contract_exact_match remains 0.0` because all rows still differ from the gold full contract under strict field equality.

## Source Evidence

- Source prior phase: `reports/public-sample/a100-compact-query-slot-preservation-rerun`
- Inherited `json_valid_rate`: `1.0`
- Inherited `contract_exact_match`: `0.0`
- Inherited `slot_f1`: `0.6666666666666666`
- Validated schema-valid outputs: `3/3`

## Residual Families

- `strict_normalized_command_string_mismatch`: `2` rows. The gold `normalized_command` is `搜索北京明天天气`, while the prediction is `搜索北京明天的天气`; slots already match as `{"query":"北京明天天气"}`.
- `compact_query_slot_shape_mismatch`: `1` row. `seed-search-weather-aug-1` gold slots are `{"query":"北京明天天气"}`, while predicted slots are `{"city":"北京","date":"明天","topic":""}`.

## Boundary

- The source predictions and strict metrics are preserved as historical evidence.
- The diagnosis explains residual families only; it does not reinterpret strict exact match as recovery.
- No held-out generalization, model-quality improvement, model recovery, production-readiness, full-corpus release, checkpoint/adapter release, or live-browser benchmark claim is made.
