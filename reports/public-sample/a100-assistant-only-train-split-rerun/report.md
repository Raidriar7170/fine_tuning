# A100 Assistant-Only Train-Split Rerun Evidence

Status: train-internal assistant-only rerun evidence. This is not a benchmark, not a release, and not a live-browser improvement claim.

## Scope

- Base model: `Qwen/Qwen2.5-0.5B-Instruct`
- Dataset manifest: `public-sample-20260601T162313Z`
- Public SFT source rows in manifest: `12`
- Training rows used after split filter: `3`
- Training row ids: `seed-search-weather`, `seed-search-weather-aug-1`, `seed-search-weather-aug-2`
- Prediction source kind: `private_a100_adapter`
- Prediction split: `train`
- Overfit diagnostic: `True`
- Generalization claim: `False`
- Release status: `not_released`

## Objective Evidence

- Prompt tokens masked: `True`
- Assistant contract tokens carry loss: `True`
- True label mask status: `inspectable`
- Label source kind: `private_training_runtime`

## Observed Result

The rerun produced 3 train predictions. Observed schema-valid Browser Task Contract `json_valid_rate=0.0000`, `contract_exact_match=0.0000`, `route_accuracy=0.0000`, `slot_f1=0.0000`, and `task_type_accuracy=0.0000`.

## Recovery Status

- Schema validity: failed. Observed 3/3 schema failures.
- Route correctness: failed.
- Slot shape: failed.
- Safety decision: partial.
- Confirmation behavior: failed.

## Comparison Boundary

The prior train-split diagnostic is pre-assistant-only-objective-repair context. Any difference here is train-internal before/after diagnostic evidence only, not held-out generalization, checkpoint release, adapter release, production readiness, or live-browser benchmark improvement.

## Public Artifacts

- Adapter metadata: `reports/public-sample/a100-assistant-only-train-split-rerun/adapter_metadata.json`
- Objective inspection: `reports/public-sample/a100-assistant-only-train-split-rerun/objective_inspection.json`
- Predictions: `reports/public-sample/a100-assistant-only-train-split-rerun/predictions.jsonl`
- Metrics: `reports/public-sample/a100-assistant-only-train-split-rerun/metrics.json`
- Prompt snapshot: `reports/public-sample/a100-assistant-only-train-split-rerun/prompt_snapshot.json`
- Raw decoded summary: `reports/public-sample/a100-assistant-only-train-split-rerun/raw_decoded_summary.jsonl`
- Generation trace: `reports/public-sample/a100-assistant-only-train-split-rerun/generation_trace.jsonl`
- Leak scan artifact: `reports/public-sample/a100-assistant-only-train-split-rerun/leak_scan_result.json`

## Boundary

The evidence pack may contain sanitized public-sample contract predictions, objective-mask status, aggregate metrics, and sidecar summaries. It does not copy raw logs, checkpoints, adapters, model caches, private overrides, host details, SSH details, tokens, private paths, or private corpus rows into git.
