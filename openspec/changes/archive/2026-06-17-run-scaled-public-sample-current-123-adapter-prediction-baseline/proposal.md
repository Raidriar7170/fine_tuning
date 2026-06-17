## Why

The current formal public sample advanced to `public-sample-20260617T152259Z` after scaled public-sample materialization, with dev/test splits expanded to 207 rows each. The latest paired adapter source remains the private current-123 train split SFT retry trained for `public-sample-20260617T045941Z`, so a bounded prediction-only baseline is needed to measure that source adapter on the scaled target boundary without implying new training or model recovery.

## What Changes

- Add public-safe dev/test prediction config templates for evaluating the existing private current-123 adapter on `public-sample-20260617T152259Z`.
- Bind target evidence to `public-sample-20260617T152259Z` while preserving the source adapter training boundary `public-sample-20260617T045941Z`.
- Require committed evidence to remain prediction-only, sanitized, and explicit about the comparison boundary.
- Publish metrics only after a future A100 prediction/evaluation run succeeds; this scaffold does not run A100 or generate predictions.
- Do not train SFT/DPO/GRPO, mutate datasets, change prompts, relax evaluator metrics, repair predictions, publish adapters/checkpoints, or claim production/live-browser improvement.

## Observed Update

- The read-only A100 preflight was attempted but stopped before private prediction because the configured SSH alias timed out.
- Committed evidence is therefore a public-safe blocked evidence pack, not an observed model-quality metrics pack.
- No private override was created, no GPU job was launched, no dev/test predictions were written, and no metrics were generated.
- The scaled target manifest still lacks observed model-quality metrics; the latest observed model evidence remains the prior `public-sample-20260617T045941Z` current-123 retry.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `contract-evaluation`: add requirements for a prediction-only baseline of the current-123 SFT retry adapter against the scaled public-sample target manifest.

## Impact

- Affected configs: `configs/sft-a100-scaled-public-sample-current-123-adapter-dev-prediction.json` and `configs/sft-a100-scaled-public-sample-current-123-adapter-test-prediction.json`.
- Affected tests: focused config and fixture-mode selection tests in `tests/test_formal_public_heldout_prediction.py`.
- Affected public evidence, when executed later: a future sanitized evidence pack under `reports/public-sample/a100-scaled-public-sample-current-123-adapter-prediction-baseline/` and a refreshed Human Brief.
- Affected runtime, when executed later: prediction-only A100 dev/test exports using private overrides under the approved private A100 project root.
