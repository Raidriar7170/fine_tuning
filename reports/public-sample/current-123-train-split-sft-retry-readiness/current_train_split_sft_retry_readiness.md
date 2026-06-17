# Voice2Task current train split SFT retry readiness

This is readiness-only evidence for a later bounded current-train-split SFT retry. It does not train, rerun predictions, mutate data, repair predictions, change prompts, or relax evaluator metrics.

## Boundary

- No A100 SFT/DPO/GRPO training was launched.
- No held-out prediction rerun was launched.
- No public sample data, prompt, or evaluator metric was changed.
- No checkpoint, adapter, safety-improvement, production-readiness, private-corpus, or live-browser claim is made.
- strict `contract_exact_match` and strict `slot_f1` remain authoritative.
- `slot_f1_soft` remains diagnostic-only.

## Summary

- Manifest: `public-sample-20260617T045941Z`
- Prior evaluated model manifest: `public-sample-20260616T165835Z`
- Prior model interpretation: `current_train_split_sft_retry_partial_signal`
- Train split rows selected by dry-run: `123`
- Form-fill repair train rows: `21`
- Blocked-payment repair train rows: `4`
- Current-retry confirmation-preservation train rows: `5`
- Future retry runtime: `a100-current-train-split-sft-retry`
- Readiness status: `ready_for_bounded_a100_sft_retry_phase`
- Recommended next change: `run-a100-current-train-split-sft-retry`

## Prior Strict Metrics Input

These strict metrics are prior model evidence bound to `public-sample-20260616T165835Z`. They are included as context only and are not current-manifest model evidence for `public-sample-20260617T045941Z`.

- `dev`: `{'prediction_count': 69, 'contract_exact_match': 0.43478260869565216, 'slot_f1': 0.5797101449275363, 'slot_f1_soft': 0.8671497584541064, 'json_valid_rate': 1.0, 'route_accuracy': 0.9130434782608695, 'safety_recall': 1.0}`
- `test`: `{'prediction_count': 69, 'contract_exact_match': 0.4057971014492754, 'slot_f1': 0.5386473429951691, 'slot_f1_soft': 0.7681912960898468, 'json_valid_rate': 1.0, 'route_accuracy': 0.8985507246376812, 'safety_recall': 1.0}`

## Evidence Inputs

- Dry-run metadata: `reports/public-sample/current-123-train-split-sft-retry-readiness/sft-dry-run/adapter_metadata.json`
- Prior model evidence: `reports/public-sample/a100-current-train-split-sft-retry/current_train_split_sft_retry.json`
- Public merge evidence: `reports/public-sample/current-retry-confirmation-preservation-public-sample-merge/current_retry_confirmation_preservation_public_sample_merge.json`
- SFT config: `configs/sft-a100-current-train-split-retry.json`
- Dev prediction config: `configs/sft-a100-current-train-split-retry-dev-prediction.json`
- Test prediction config: `configs/sft-a100-current-train-split-retry-test-prediction.json`

## Recommended Next Step

Open `run-a100-current-train-split-sft-retry` as a separate bounded phase. That phase must perform fresh A100 GPU preflight, use private overrides outside git, train a paired adapter trained for `public-sample-20260617T045941Z`, keep all adapters/logs/checkpoints private, and publish only sanitized strict held-out evidence.
