## Why

The archived `repair-public-readonly-search-contract-policy` phase made the search/weather public-readonly contract policy visible in the shared SFT and prediction prompt without changing evaluator semantics. The next smallest evidence step is one explicitly authorized A100 prediction-only train-split rerun to observe whether that prompt-policy hardening changes the same three private-adapter train-row outputs.

## What Changes

- Run one bounded A100 prediction-only train-split rerun using the current public-readonly search prompt policy, strict schema guard, greedy decoding, and existing private train-split adapter.
- Keep `prediction_split=train`, `overfit_diagnostic=true`, `generalization_claim=false`, `schema_retry_enabled=true`, and `schema_repair_applied=false`.
- Import only sanitized public-safe evidence: prediction metadata, predictions, prompt snapshot, raw decoded summary, generation trace, train-split gold rows, strict metrics, schema guard summary, public-readonly search policy diagnosis, manifest, reports, leak scans, and Human Briefs.
- Compare narrowly against `reports/public-sample/a100-normalized-command-policy-train-split-rerun/` as the pre-public-readonly-search-policy A100 baseline.
- Preserve the result honestly whether task type, route, safety reason, confirmation, slots, schema validity, or strict exact match improves, remains partial, or regresses.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `supervised-contract-tuning`: add an explicitly authorized A100 train-split prediction rerun path after public-readonly search contract prompt policy.
- `contract-evaluation`: add public-safe evidence requirements and non-claim boundaries for the public-readonly search policy train-split rerun.

## Impact

- Affected runtime path: `voice2task.cli.train sft-predict` on A100 with a repo-external private adapter config and approved private output root represented in public artifacts as `<a100_project_root>`.
- Affected evidence: new public-safe report directory under `reports/public-sample/a100-public-readonly-search-policy-train-split-rerun/` and Chinese Human Briefs under `docs/human-briefs/`.
- Non-goals: no generic chat fine-tuning, no skill routing, no GUI action policy learning, no first-phase GRPO, no public release of the full local corpus, no SFT/DPO training, no dev/test or full-public-sample rerun, no checkpoint or adapter release, no production-readiness claim, no held-out generalization claim, no public full-corpus release, no model-quality improvement claim, no live-browser benchmark improvement claim, no evaluator metric change, no semantic-equivalence scoring, no slot normalization, and no prediction repair/re-score.
