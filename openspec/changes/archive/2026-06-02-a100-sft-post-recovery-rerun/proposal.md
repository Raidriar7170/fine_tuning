## Why

The previous A100 trained-path prediction smoke produced 12 public-sample predictions, but all failed the Browser Task Contract schema. The contract-output recovery change fixed local SFT/prediction formatting and honest failure preservation; this follow-up reruns the bounded A100 path so the repository can record real post-recovery evidence instead of leaving the recovery slot pending.

## What Changes

- Rerun the public-sample A100 SFT smoke using the shared contract-only chat formatting policy from the recovery phase.
- Rerun private-adapter public-sample prediction with the recovered prompt format and preserve any invalid model outputs as schema failures.
- Copy back only sanitized public-sample prediction/evaluation evidence: predictions, prediction metadata, metrics, controlled smoke result, leak-scan result, manifest, and bounded report.
- Update the recovery evidence pack so it compares the pre-recovery baseline with the post-rerun result, whether the post-rerun result improves or still fails.
- Generate a concise Chinese Human Brief for the rerun phase.
- Non-goals: generic chat fine-tuning, Hermes-style skill routing, GUI action policy learning, first-phase GRPO/rule-reward training, publishing the full local/private corpus, publishing checkpoints or adapters, copying raw logs/caches/private paths into git, or claiming live-browser benchmark or production-readiness improvement.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `supervised-contract-tuning`: require the post-recovery A100 rerun to use the recovered contract-only SFT/prediction formatting policy and to record public-safe private-adapter prediction provenance.
- `contract-evaluation`: require the post-recovery rerun evidence pack to publish sanitized metrics, controlled smoke, leak-scan, and comparison against the pre-recovery schema-failure baseline.

## Impact

- Affects A100 runbook execution, private remote SFT/prediction commands, sanitized evidence under `reports/public-sample/`, recovery reporting, Human Brief HTML, and validation commands.
- Uses the existing Transformers + PEFT + TRL training path, Qwen-family public model ID, public sample manifest, and controlled evaluation ladder.
- Requires remote A100 execution under the approved private project root, but all public repository artifacts must remain sanitized and must not include host details, SSH details, raw logs, private filesystem paths, checkpoints, adapters, caches, tokens, secrets, or private corpus rows.
