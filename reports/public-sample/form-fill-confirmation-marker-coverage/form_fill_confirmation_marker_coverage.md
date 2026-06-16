# Voice2Task form-fill confirmation-marker coverage assessment

This is a coverage assessment only. It compares committed public-safe form-fill confirmation policy evidence with existing remediation artifacts; it does not generate data, change prompts, run predictions, train, repair predictions, or relax evaluation.

## Boundary

- strict `contract_exact_match` and strict `slot_f1` remain authoritative.
- `slot_f1_soft` remains diagnostic-only.
- Existing remediation coverage is not held-out recovery evidence.
- Current residual evidence still observes the confirmation-marker normalized-command cluster.
- Any data, prompt, evaluator, prediction, checkpoint, adapter, or training change requires a separate OpenSpec phase.

## Summary

- Source manifest id: `public-sample-20260616T022151Z`
- Source count consistency: `True`
- Policy bucket: `missing_confirmation_marker`
- Policy cluster-row incidence total: `27`
- Policy residual fields: `27`
- Policy source families: `12`
- Existing confirmation candidate cases: `3`
- Materialized confirmation seed rows: `3`
- Represented field labels: `['发票抬头', '手机号', '收货地址']`
- Confirmation marker preserved by all candidate patterns: `True`
- Merge status: `formal_public_sample_rebuilt`
- Current top residual cluster rows: `27`
- Current top residual cluster fields: `27`
- Coverage decision: `partial_legacy_coverage_current_residual_still_observed`
- Recommended next step: `propose_bounded_confirmation_marker_coverage_extension_before_training`

## Interpretation

The existing remediation chain provides partial legacy coverage: 3 confirmation-marker candidate cases cover 3 field labels, while the current policy evidence spans 12 source families and still has 27 cluster-row incidences in the top residual cluster.

This report makes no held-out recovery claim and does not authorize immediate data or prompt changes.

## Unsupported Changes

- `data_mutation`: coverage assessment does not add or rewrite rows
- `prompt_change`: prompt changes require a separate OpenSpec phase
- `training_run`: training requires a separate A100 phase and fresh evaluation
- `evaluator_relaxation`: strict contract metrics remain authoritative
- `prediction_repair`: predictions are not repaired, replaced, normalized, or re-scored
- `held_out_recovery_claim`: current held-out residual evidence still observes the cluster
