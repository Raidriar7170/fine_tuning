## Context

The current formal public sample contains `77` seed rows, `231` SFT rows, and
`661` DPO pairs, split as train/dev/test = `93/69/69`. The latest committed
prediction-only evidence is:

- `reports/public-sample/a100-formal-public-heldout-prediction/report.md`
- `reports/public-sample/a100-formal-public-heldout-prediction/dev/metrics.md`
- `reports/public-sample/a100-formal-public-heldout-prediction/test/metrics.md`

Those artifacts supersede older README headline numbers that came from a much
smaller public sample or from the private dev128 SFT v2 diagnostic run.

## Goals / Non-Goals

**Goals:**

- Make the README and experiment report point to the current formal held-out
  evidence.
- Preserve the strict evidence ladder: full-contract exact match and strict
  field metrics are primary; soft character-level slot F1 is diagnostic only.
- Make the recommended next step a bounded residual/family diagnosis before
  any data, training, DPO, evaluator, or production-positioning change.
- Keep documentation public-safe.

**Non-Goals:**

- No new predictions, training, data generation, split changes, or adapter work.
- No evaluator relaxation, semantic-equivalence scoring, prediction repair, or
  re-scoring.
- No claim that the model is recovered, production-ready, released, or validated
  on live-browser execution.

## Decisions

1. Treat `a100-formal-public-heldout-prediction` as the current headline.
   - Rationale: it is tied to the current formal public manifest and has
     balanced held-out rows.
   - Alternative: keep the old dev128 result as the headline. Rejected because
     it is not the current public evidence boundary.

2. Keep `slot_f1_soft` visible but explicitly diagnostic.
   - Rationale: it helps explain slot-value phrasing residuals, but it does not
     replace strict metrics.
   - Alternative: remove the metric from summary docs. Rejected because it is
     useful when clearly labeled.

3. Recommend residual diagnosis before new training.
   - Rationale: current failures span route/task-type, safety recall, and slot
     exactness, so jumping directly to more data or DPO risks treating the wrong
     bottleneck.
   - Alternative: immediately expand clarify or blocked-payment data. Rejected
     until residual family evidence is inspected.

## Risks / Trade-offs

- Documentation-only changes can drift again if future evidence lands without a
  report refresh.
- The stricter headline metrics are less flattering than the historical dev128
  diagnostic numbers, but they are the safer public claim boundary.
- Human Brief HTML is a review companion only; OpenSpec artifacts, metrics, and
  reports remain authoritative.
