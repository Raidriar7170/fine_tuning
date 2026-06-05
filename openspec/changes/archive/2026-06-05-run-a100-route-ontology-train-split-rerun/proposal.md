## Why

The local `repair-route-task-ontology-output` phase made the shared SFT/prediction prompt explicitly frame `route` as a Browser Task Contract execution-channel enum and added a weather-to-`search_web` example. The next smallest evidence step is a prediction-only A100 train-split rerun that tests whether this prompt repair changes real private-adapter outputs on the same three train rows that previously stayed `0/3` schema-valid.

## What Changes

- Run one bounded A100 prediction-only train-split rerun using the current route ontology prompt, strict whole-string raw/retry parser, and existing private train-split adapter.
- Keep `prediction_split=train`, `overfit_diagnostic=true`, `generalization_claim=false`, `schema_retry_enabled=true`, greedy decoding, and no schema repair/coercion.
- Import only sanitized public-safe evidence: prediction metadata, predictions, prompt snapshot, raw decoded summary, generation trace, metrics, schema guard summary, route-ontology diagnosis, manifest, reports, leak scans, and Human Briefs.
- Compare narrowly against `reports/public-sample/a100-constrained-output-train-split-rerun/` as the pre-route-ontology-repair baseline.
- Preserve the result honestly whether schema/route recovery improves, remains partial, or stays `0/3`.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `supervised-contract-tuning`: add an explicitly authorized A100 route-ontology train-split prediction rerun path after local route ontology prompt repair.
- `contract-evaluation`: add public-safe evidence requirements and non-claim boundaries for the route-ontology A100 rerun.

## Impact

- Affected runtime path: `voice2task.cli.train sft-predict` on A100 with a repo-external private adapter config and approved private output root.
- Affected evidence: new public-safe report directory under `reports/public-sample/a100-route-ontology-train-split-rerun/` and a Chinese Human Brief under `docs/human-briefs/`.
- Non-goals: no generic chat fine-tuning, no skill routing, no GUI action policy learning, no first-phase GRPO, no public release of the full local corpus, no SFT/DPO training, no dev/test or full-public-sample rerun, no checkpoint or adapter release, no production-readiness claim, no held-out generalization claim, no public full-corpus release, and no live-browser benchmark improvement claim.
