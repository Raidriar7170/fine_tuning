# Fence-suppression slot residual diagnosis

This is a local evidence-only diagnosis derived from the sanitized A100 first-pass fence-suppression rerun artifacts. It does not run A100, retrain, rerun prediction, change decoding, relax the parser, repair predictions, normalize slots, apply semantic-equivalence scoring, or re-score outputs.

## Conclusion

The wrapper/schema boundary improvement remains visible in the source rerun: `0/3` predictions are Markdown-wrapped and `3/3` predictions are strict schema-valid. The remaining strict failure is exactly one slot object mismatch.

## Residual Row

- Row id: `seed-search-weather-aug-1`
- Gold slots: `{"query": "北京明天天气"}`
- Predicted slots: `{"city": "北京", "date": "明天", "topic": ""}`
- Category: `strict_slot_object_mismatch`
- Strict metric impact: contributes to the slot failure slice and keeps contract exact match at `2/3`.

## Boundary

- No A100 execution was performed in this phase.
- No training, prediction rerun, parser relaxation, evaluator metric change, prediction repair, re-score, slot normalization, or semantic-equivalence scoring was performed.
- The semantic relation between `city/date/topic` and `query` is not counted as a pass under the strict evaluator.
- This is not held-out generalization, production readiness, live-browser benchmark, model recovery, or broad model-quality improvement evidence.

## Recommended Next Decision

The next behavior-changing step would need an explicit new scope decision: whether to train or prompt for compact `query` slot preservation, change task policy, or intentionally add a separate semantic-equivalence analysis. This diagnosis does not choose those changes.
