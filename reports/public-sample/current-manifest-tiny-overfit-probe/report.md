# Current Manifest Tiny-Overfit Probe Evidence

Status: train-internal 7B tiny-overfit probe completed. This is not a benchmark, not a release, and not held-out generalization evidence.

## Scope

- Base model: `Qwen/Qwen2.5-7B-Instruct`
- Dataset manifest: `public-sample-20260613T072200Z`
- Training split: `train`
- Training rows used: `3`
- Training row ids: `seed-search-weather, seed-search-weather-aug-1, seed-search-weather-aug-2`
- Prediction split: `train`
- Prediction rows: `3`
- Prediction source kind: `private_a100_adapter`
- Overfit diagnostic: `True`
- Generalization claim: `False`
- Release status: `not_released`

## Objective Context

- Runtime label evidence: `reports/public-sample/current-runtime-label-provenance-check/runtime_label_provenance_check.json`
- Current-manifest runtime label proof: `True`
- Prompt tokens masked: `True`
- Assistant contract tokens carry loss: `True`
- True label-mask status: `inspectable`

## Observed Result

The 7B private A100 adapter produced schema-valid Browser Task Contract outputs for the same 3 current train rows used by the tiny-overfit SFT probe.

- `confirmation_accuracy`: `1.0`
- `contract_exact_match`: `1.0`
- `json_valid_rate`: `1.0`
- `route_accuracy`: `1.0`
- `safety_gold_stop_support`: `0.0`
- `safety_precision`: `1.0`
- `safety_predicted_stop_support`: `0.0`
- `safety_recall`: `1.0`
- `slot_f1`: `1.0`
- `slot_f1_soft`: `1.0`
- `task_type_accuracy`: `1.0`

Failure slices are all zero in `metrics.json` for this 3-row train-internal slice.

## Public Artifacts

- Adapter metadata: `reports/public-sample/current-manifest-tiny-overfit-probe/adapter_metadata_public.json`
- Predictions: `reports/public-sample/current-manifest-tiny-overfit-probe/predictions.jsonl`
- Train gold subset: `reports/public-sample/current-manifest-tiny-overfit-probe/train_split_gold.jsonl`
- Metrics: `reports/public-sample/current-manifest-tiny-overfit-probe/metrics.json`
- Prompt snapshot: `reports/public-sample/current-manifest-tiny-overfit-probe/prompt_snapshot.json`
- Raw decoded summary: `reports/public-sample/current-manifest-tiny-overfit-probe/raw_decoded_summary.jsonl`
- Generation trace: `reports/public-sample/current-manifest-tiny-overfit-probe/generation_trace.jsonl`
- Leak scan: `reports/public-sample/current-manifest-tiny-overfit-probe/leak_scan_result.json`

## Boundary

This evidence supports only a tiny train-internal memorization sanity check for the current manifest. It does not prove dev/test generalization, private-corpus generalization, model recovery, production readiness, checkpoint release, adapter release, public full-corpus release, or live-browser benchmark improvement. It does not relax the evaluator, normalize predictions, repair outputs, or replace model predictions with gold/fixture rows.
