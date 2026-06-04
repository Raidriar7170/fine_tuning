# A100 Constrained-Output Train-Split Rerun

Status: train-internal constrained-output diagnostic evidence. This is not a benchmark, not a release, and not a live-browser improvement claim.

## Result

The rerun produced 3 train predictions with the repaired constrained-output prompt visible in the A100 prediction path: canonical JSON one-shot visible `True`, whole-object boundary visible `True`.

Observed schema-valid Browser Task Contract `json_valid_rate=0.0000`, `contract_exact_match=0.0000`, `route_accuracy=0.0000`, `slot_f1=0.0000`, and `task_type_accuracy=0.0000`.

Schema guard observed raw schema-valid `0/3`, retry schema-valid `0/3`, and final validated schema-valid `0/3`. The strict parser rejected `3/3` retry attempts that contained JSON fragments wrapped in Markdown/prose. Compared with the pre-repair strict-retry baseline, final validated schema-valid output remains `0/3`; the train split is not recovered and must not be described as model recovery.

## What Changed Versus Baseline

- The new A100 path includes the constrained-output prompt repair from `reports/public-sample/constrained-contract-output-emission-repair/`.
- The canonical Browser Task Contract one-shot and whole-object boundary rules are visible in `prompt_snapshot.json`.
- The model still emits invalid train outputs: one raw output is a full JSON object with an invalid route value, two raw outputs are malformed/non-JSON, and retries still wrap JSON fragments in Markdown/prose.

## Public Artifacts

- Predictions: `reports/public-sample/a100-constrained-output-train-split-rerun/predictions.jsonl`
- Train gold subset used for metrics: `reports/public-sample/a100-constrained-output-train-split-rerun/train_split_gold.jsonl`
- Metrics: `reports/public-sample/a100-constrained-output-train-split-rerun/metrics.json` / `reports/public-sample/a100-constrained-output-train-split-rerun/metrics.md`
- Schema guard summary: `reports/public-sample/a100-constrained-output-train-split-rerun/schema_guard_summary.json` / `reports/public-sample/a100-constrained-output-train-split-rerun/schema_guard_summary.md`
- Constrained decoding diagnosis: `reports/public-sample/a100-constrained-output-train-split-rerun/constrained_decoding_diagnosis.json` / `reports/public-sample/a100-constrained-output-train-split-rerun/constrained_decoding_diagnosis.md`
- Prompt snapshot: `reports/public-sample/a100-constrained-output-train-split-rerun/prompt_snapshot.json`
- Raw decoded summary: `reports/public-sample/a100-constrained-output-train-split-rerun/raw_decoded_summary.jsonl`
- Generation trace: `reports/public-sample/a100-constrained-output-train-split-rerun/generation_trace.jsonl`
- Prediction metadata: `reports/public-sample/a100-constrained-output-train-split-rerun/prediction_metadata.json`
- Manifest: `reports/public-sample/a100-constrained-output-train-split-rerun/manifest.json`

## Policy Fields

- Release status: `not_released`
- Prediction source kind: `private_a100_adapter`
- Prediction split: `train`
- Overfit diagnostic: `True`
- Generalization claim: `False`
- Schema retry enabled: `True`
- Strict parser: `whole_string_json_only_for_raw_and_retry`
- Decoding strategy: `greedy`

## Boundary

The evidence pack contains sanitized public-sample contract predictions, aggregate metrics, schema guard summaries, constrained decoding diagnosis, and leak-scan status. It does not copy raw logs, checkpoints, adapters, remote caches, private configs, host details, tokens, SSH details, or private corpus rows into git.

Claim boundaries: no checkpoint release, no adapter release, no held-out generalization claim, no production-readiness claim, no public full-corpus release, no A100 model recovery claim, and no live-browser benchmark improvement claim.

## Recommended Next Step

Open a small follow-up diagnostic/repair phase focused on ontology-constrained route and task-shape behavior. The current failure is no longer mainly missing required fields; it is invalid route/task semantics plus retry-format drift.
