## Why

The just-archived constrained-output repair made first-pass prediction prompts expose a valid Browser Task Contract one-shot and made raw prediction parsing whole-string JSON only. The latest A100 strict-retry train-split rerun remains the pre-repair baseline: validated outputs were still `0/3` schema-valid, while strict retry rejected `3/3` Markdown/prose-wrapped retry fragments. The next smallest evidence step is a prediction-only A100 train-split rerun that tests the new prompt/parser path against the existing private adapter without spending another training run.

## What Changes

- Run one bounded A100 prediction-only train-split rerun using the current constrained-output prompt and whole-string raw/retry parser.
- Reuse the existing private train-split adapter through a repo-external private override; do not retrain.
- Keep `prediction_split=train`, `overfit_diagnostic=true`, `generalization_claim=false`, `schema_retry_enabled=true`, and greedy decoding.
- Import only sanitized public-safe evidence: prediction metadata, predictions, prompt snapshot, raw decoded summary, generation trace, metrics, schema guard summary, constrained-output diagnosis, manifest, reports, leak scans, and Human Briefs.
- Compare narrowly against `reports/public-sample/a100-strict-retry-train-split-rerun/` as the pre-constrained-output baseline.

## Impact

- Modified capabilities:
  - `supervised-contract-tuning`: add an authorized A100 constrained-output train-split prediction rerun path after local constrained-output repair.
  - `contract-evaluation`: add public-safe evidence requirements and non-claim boundaries for the constrained-output A100 rerun.
- Affected runtime path: `voice2task.cli.train sft-predict` on A100 with a repo-external private adapter config.
- Non-goals: no training, no DPO/GRPO, no dev/test or full-public-sample rerun, no checkpoint or adapter release, no production-readiness claim, no held-out generalization claim, no public full-corpus release, and no live-browser benchmark improvement claim.
