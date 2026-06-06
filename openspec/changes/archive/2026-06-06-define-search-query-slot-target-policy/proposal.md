# define-search-query-slot-target-policy

## Why

The retry-template A100 rerun recovered schema-valid output on the bounded train split, but exact match stayed at `0/3` because every row still failed the strict slot slice. The follow-up diagnosis showed two residual failures where the model emitted `slots.city/date` instead of the gold `slots.query`, and one residual failure where both sides used `slots.query` but the string differed only by internal spacing.

The project needs a small, explicit target policy before any more reruns: public-readonly search/weather contracts should train and prompt toward one canonical `slots.query` shape and one strict query-string style.

## What Changes

- Define the canonical public-readonly search slot target policy:
  - use object-shaped `slots.query`,
  - do not split weather/search entities into `city`, `date`, or other ad hoc slot keys,
  - use a compact query phrase such as `北京明天天气` rather than token-spaced `北京 明天 天气`,
  - keep `normalized_command` as `搜索` + the same compact query phrase.
- Update public sample seed/SFT/DPO search rows to the canonical compact query target.
- Strengthen model-visible prompt guidance and prompt metadata for the no-`city/date` query-slot rule.
- Publish a local evidence pack and Human Brief showing target/prompt alignment, with strict no-normalization/no-repair boundaries.

## Non-Goals

- No A100 execution.
- No training, fine-tuning, prediction rerun, parser change, evaluator metric change, semantic-equivalence scoring, slot normalization, prediction repair, prediction replacement, or re-score.
- No change to Browser Task Contract schema.
- No checkpoint/adapter release, held-out generalization, production-readiness, public full-corpus, model-quality improvement, or live-browser benchmark claim.

## Impact

- Affected specs: `supervised-contract-tuning`, `contract-evaluation`, `voice2task-dataset-preparation`
- Affected code/data: prompt formatting policy and public sample search target rows.
- Affected evidence: a new public-safe directory under `reports/public-sample/search-query-slot-target-policy/`.
