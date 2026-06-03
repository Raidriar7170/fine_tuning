# A100 SFT Post-Recovery Rerun Evidence

Status: completed public-sample post-recovery rerun with private A100 adapter predictions. The rerun still failed the Browser Task Contract schema on all 12 public-sample rows.

## Scope

- Base model: `Qwen/Qwen2.5-0.5B-Instruct`
- Model source: `modelscope`
- Dataset manifest: `public-sample-20260601T162313Z`
- Prediction source kind: `private_a100_adapter`
- Prediction count: `12`
- Formatting policy: `shared_contract_chat_template`
- Release status: `not_released`

## Pre-Recovery Baseline

- Evidence: `reports/public-sample/a100-sft-prediction-eval-smoke/`
- JSON/schema validity rate: `0.0000`
- Schema failures: `12`
- Controlled smoke: `0 passed / 12 failed`

## Post-Recovery Result

- Predictions: `reports/public-sample/a100-sft-post-recovery-rerun/predictions.jsonl`
- Metrics: `reports/public-sample/a100-sft-post-recovery-rerun/metrics.json`
- JSON/schema validity rate: `0.0000`
- Schema failures: `12`
- Controlled smoke: `0 passed / 12 failed`

- Leak scan: `ok=true`, `0 findings`

## Interpretation

The post-recovery run used the recovered contract-only chat formatting policy and produced sanitized private-adapter public-sample predictions, but the observed metrics do not show schema-valid recovery. This is failure evidence for the current trained path, not a model-quality improvement claim.

## Boundary

This evidence pack contains sanitized public-sample predictions, aggregate metrics, controlled smoke status, and leak-scan status only. It does not publish checkpoints, adapters, raw logs, remote caches, private configs, private paths, host details, SSH details, tokens, secrets, full private corpus rows, production-readiness claims, or live-browser benchmark improvement claims.
