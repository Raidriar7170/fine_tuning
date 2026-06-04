# A100 Required-Field Repair Train-Split Rerun

Status: train-internal overfit diagnostic evidence. This is not a benchmark, not a release, and not a live-browser improvement claim.

## Result

The rerun produced 3 train predictions. Observed schema-valid Browser Task Contract `json_valid_rate=0.0000`, `contract_exact_match=0.0000`, `route_accuracy=0.0000`, `slot_f1=0.0000`, and `task_type_accuracy=0.0000`.

Schema guard observed raw schema-valid `0/3`, retry schema-valid `0/3`, and validated schema-valid `0/3`. The train split is not recovered and must not be described as schema recovery.

## What Changed Versus Prior Rerun

- The prediction prompt exposed the required-field skeleton/checklist at prediction time.
- The prediction path preserved raw and retry attempt summaries in `raw_decoded_summary.jsonl`.
- The adapter was rerun on the same public-sample train split with assistant-only labels and runtime label provenance inspected.

## Public Artifacts

- Predictions: `reports/public-sample/a100-required-field-repair-train-split-rerun/predictions.jsonl`
- Metrics: `reports/public-sample/a100-required-field-repair-train-split-rerun/metrics.json` / `reports/public-sample/a100-required-field-repair-train-split-rerun/metrics.md`
- Schema guard summary: `reports/public-sample/a100-required-field-repair-train-split-rerun/schema_guard_summary.json` / `reports/public-sample/a100-required-field-repair-train-split-rerun/schema_guard_summary.md`
- Prompt snapshot: `reports/public-sample/a100-required-field-repair-train-split-rerun/prompt_snapshot.json`
- Raw decoded summary: `reports/public-sample/a100-required-field-repair-train-split-rerun/raw_decoded_summary.jsonl`
- Generation trace: `reports/public-sample/a100-required-field-repair-train-split-rerun/generation_trace.jsonl`
- Prediction metadata: `reports/public-sample/a100-required-field-repair-train-split-rerun/prediction_metadata.json`
- Adapter metadata: `reports/public-sample/a100-required-field-repair-train-split-rerun/adapter_metadata.json`
- Objective inspection: `reports/public-sample/a100-required-field-repair-train-split-rerun/objective_inspection.json`
- Leak scan: `reports/public-sample/a100-required-field-repair-train-split-rerun/leak_scan_result.json`

## Policy Fields

- Release status: `not_released`
- Loss-mask policy: `assistant_only_completion_only`
- Loss-mask assistant target: `browser_task_contract_json`
- Schema guard enabled: `True`
- Schema retry enabled: `True`
- Schema retry max attempts: `1`
- Decoding strategy: `greedy`
- Raw decoded sidecar written: `True`
- Generation trace sidecar written: `True`

## Boundary

The evidence pack contains sanitized public-sample contract predictions, aggregate metrics, schema guard summaries, objective-path evidence, and leak-scan status. It does not copy raw logs, checkpoints, adapters, remote caches, private paths, host details, tokens, SSH details, or private corpus rows into git.

Claim boundaries: no checkpoint release, no adapter release, no held-out generalization claim, no production-readiness claim, no public full-corpus release, and no live-browser benchmark improvement claim.
