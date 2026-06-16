# Voice2Task form-fill remediation SFT v3 readiness

This is readiness-only evidence for a later bounded `form_fill` remediation SFT v3 phase. It does not train, rerun predictions, mutate data, repair predictions, or relax evaluator metrics.

## Boundary

- No SFT/DPO/GRPO training was launched.
- No held-out prediction rerun was launched.
- No public sample data or evaluator metric was changed.
- No checkpoint, adapter, production-readiness, private-corpus, or live-browser claim is made.
- strict `contract_exact_match` and strict `slot_f1` remain authoritative.
- `slot_f1_soft` remains diagnostic-only.

## Summary

- Manifest: `public-sample-20260616T165835Z`
- Baseline interpretation: `formal_public_heldout_partial_signal`
- Train split rows selected by dry-run: `118`
- Merged form-fill train rows: `21`
- Selected residual rows / fields: `29` / `49`
- Readiness status: `ready_for_bounded_a100_sft_v3_phase`
- Recommended next change: `run-a100-form-fill-remediation-sft-v3`

## Current Strict Baseline

- `dev`: `{'prediction_count': 69, 'contract_exact_match': 0.30434782608695654, 'slot_f1': 0.391304347826087, 'slot_f1_soft': 0.7315387631291138, 'json_valid_rate': 1.0, 'route_accuracy': 0.855072463768116, 'safety_recall': 0.6666666666666666}`
- `test`: `{'prediction_count': 69, 'contract_exact_match': 0.2898550724637681, 'slot_f1': 0.5072463768115942, 'slot_f1_soft': 0.7609315000619348, 'json_valid_rate': 1.0, 'route_accuracy': 0.9130434782608695, 'safety_recall': 0.9166666666666666}`

## Evidence Inputs

- Dry-run metadata: `reports/public-sample/form-fill-remediation-sft-v3-readiness/sft-dry-run/adapter_metadata.json`
- Baseline evidence: `reports/public-sample/a100-formal-public-heldout-prediction-after-a100-recovery/formal_public_heldout_prediction.json`
- Target selection: `reports/public-sample/formal-heldout-remediation-target-selection/formal_heldout_remediation_target_selection.json`
- Remediation plan: `reports/public-sample/form-fill-remediation-plan/form_fill_remediation_plan.json`
- SFT config: `configs/sft-a100-form-fill-remediation-v3.json`
- Dev prediction config: `configs/sft-a100-form-fill-remediation-v3-dev-prediction.json`
- Test prediction config: `configs/sft-a100-form-fill-remediation-v3-test-prediction.json`

## Recommended Next Step

Open `run-a100-form-fill-remediation-sft-v3` as a separate bounded phase. That phase must perform fresh A100 GPU preflight, use private overrides outside git, keep all adapters/logs/checkpoints private, and publish only sanitized evidence.
