# A100 SFT Contract-Output Recovery Evidence Template

Status: post-recovery public-sample rerun recorded.

## Pre-Recovery Baseline

- Source evidence: `reports/public-sample/a100-sft-prediction-eval-smoke/`
- Dataset manifest: `public-sample-20260601T162313Z`
- Prediction source kind: `private_a100_adapter`
- Prediction count: `12`
- Pre-recovery result: `json_valid_rate=0.0000`
- Pre-recovery failure slice: `12 schema failures`
- Controlled smoke: `0 passed / 12 failed`
- Leak scan: `ok=true`

## Post-Recovery Rerun

- post-rerun evidence: `reports/public-sample/a100-sft-post-recovery-rerun/`
- post-rerun prediction source kind: `private_a100_adapter`
- post-rerun prediction count: `12`
- post-rerun formatting policy: `shared_contract_chat_template`
- post-rerun result: `json_valid_rate=0.0000`
- post-rerun failure slice: `12 schema failures`
- post-rerun controlled smoke: `0 passed / 12 failed`
- post-rerun leak scan: `ok=true`
- rerun output placement: private checkpoints, adapters, raw logs, caches, private configs, and remote paths stayed under `<a100_project_root>`; only sanitized public-sample evidence was copied back

## Claim Boundaries

- This is schema/contract-level public-sample recovery evidence only.
- This is not a checkpoint release.
- This is not an adapter release.
- This is not a live-browser benchmark.
- This makes no production-readiness claim.
- This does not publish a full private corpus, raw logs, remote caches, checkpoints, adapters, host details, SSH details, tokens, or secrets.

## Recovery Checklist

- Rerun SFT training and private-adapter prediction with the shared contract chat-template formatting policy: completed.
- Preserve invalid private adapter outputs as schema failures when they remain invalid: completed.
- Compare post-rerun metrics against the pre-recovery baseline only after sanitized predictions and metrics exist: completed.
- Run leak-scan before treating copied recovery evidence as public-safe: completed.

## Interpretation

The post-recovery rerun completed the real A100 public-sample SFT and private-adapter prediction path, but it did not recover schema-valid Browser Task Contract output for the committed public sample. The correct claim is bounded failure evidence for the current trained path, not a model-quality improvement claim.
