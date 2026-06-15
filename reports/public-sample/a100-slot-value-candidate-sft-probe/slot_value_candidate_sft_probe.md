# Voice2Task slot value candidate SFT probe

This is candidate-only evidence for the standalone slot value candidate SFT rows. It records dry-run, blocked, failed, or observed A100 execution status without publishing adapters or claiming held-out model recovery.

## Boundary

- Formal public sample seed, SFT, DPO, and manifest files are unchanged.
- No DPO training, checkpoint release, or adapter release is claimed.
- A100 SFT/prediction execution is recorded, but adapters, checkpoints, raw logs, caches, host details, private overrides, and private paths remain outside git.
- strict `contract_exact_match` remains primary; no evaluator relaxation is introduced.
- This is not held-out, private-corpus, production-readiness, or live-browser evidence.

## Summary

- Candidate SFT rows: `12`
- Selected candidate training rows: `12`
- Formal public sample modified: `False`
- A100 training status: `training_completed`
- A100 prediction status: `private_adapter_predictions_written`
- Recommended next step: `decide_candidate_merge_or_heldout_strategy`

## A100 Preflight

- SSH status: `ok`
- Output root status: `ok`
- Idle GPU status: `idle_gpu_available`
- Selected GPU index: `3`
- Available train dependencies: `['torch', 'transformers', 'peft', 'accelerate', 'trl', 'datasets']`
- Missing train dependencies: `[]`
- Safe to launch training now: `True`

## Remote Execution

- Workspace status: `created_under_approved_root`
- Dependency environment status: `ready`
- Sync status: `synced_minimal_project_snapshot`
- Training status: `training_completed`
- Prediction status: `private_adapter_predictions_written`

## Evidence

- Dry-run metadata: `not_provided`
- Training metadata: `<private_path>`
- Prediction metadata: `<private_path>`
- Metrics: `<private_path>`
- Candidate manifest: `data/public-samples/manifest_slot_value_candidate_probe.json`
- SFT config: `configs/sft-a100-slot-value-candidate-probe.json`
- Prediction config: `configs/sft-a100-slot-value-candidate-probe-prediction.json`
