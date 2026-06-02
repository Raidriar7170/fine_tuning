# A100 SFT Prediction/Eval Smoke Evidence

Status: public-sample prediction/evaluation smoke evidence. This is not a checkpoint release and not a live-browser benchmark.

## Scope

- Base model: `Qwen/Qwen2.5-0.5B-Instruct`
- Model source: `modelscope`
- Dataset manifest: `public-sample-20260601T162313Z`
- Prediction source kind: `private_a100_adapter`
- Release status: `not_released`

## Interpretation

If `prediction_source_kind` is `public_sample_contract_fixture`, the predictions are deterministic public-sample contract fixtures used to validate the evidence pipeline. They are not private adapter model outputs and must not be presented as model-quality evidence.
If `prediction_source_kind` is `private_a100_adapter`, the predictions came from the private A100 adapter path, but the metrics and controlled smoke results still only describe this bounded public sample. Failed schema or smoke results must be reported as failures, not hidden behind the existence of a completed training run.

## Public Artifacts

- Predictions: `reports/public-sample/a100-sft-prediction-eval-smoke/predictions.jsonl`
- Metrics: `reports/public-sample/a100-sft-prediction-eval-smoke/metrics.json`
- Controlled smoke: `controlled_validation_command`
- Leak scan ok: `True`

## Boundary

The evidence pack may contain sanitized public-sample contract predictions, aggregate metrics, controlled smoke status, and leak-scan status. It does not copy raw logs, checkpoints, adapters, remote caches, private paths, host details, tokens, or private corpus rows into git.
