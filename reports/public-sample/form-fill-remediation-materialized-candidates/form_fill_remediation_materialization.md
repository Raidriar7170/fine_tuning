# Voice2Task form-fill remediation materialized candidates

This is candidate data only: it materializes reviewed form-fill remediation cases into a standalone public-safe candidate dataset, not merged into seed_traces.jsonl and not used as training evidence yet.

## Boundary

- Candidate rows are not formal public sample rows yet.
- Formal public sample seed, SFT, DPO, and manifest files are not rewritten.
- No DPO pairs, SFT training, prediction run, or A100 execution is performed.
- strict `contract_exact_match` remains primary.
- Soft slot F1 and semantic equivalence remain diagnostic-only.
- This is not a model recovery, held-out recovery, checkpoint, adapter, production, or live-browser claim.

## Summary

- Candidate groups: `3`
- Candidate seed rows: `9`
- Candidate SFT rows: `9`
- Formal public sample seed rows: `77`
- Formal public sample SFT rows: `231`
- Formal public sample DPO pairs: `661`
- Public sample modified: `False`
- Recommended next step: `run_local_form_fill_candidate_integration_check`

## Candidate Case Groups

### `form-fill-clarify-boundary-protection`

- Source bucket: `clarify_boundary_confusion`
- Candidate seeds: `['candidate-form-fill-remediation-ff-boundary-appointment-time', 'candidate-form-fill-remediation-ff-boundary-delivery-info', 'candidate-form-fill-remediation-ff-boundary-contact-phone']`
- Candidate SFT rows: `['candidate-form-fill-remediation-ff-boundary-appointment-time', 'candidate-form-fill-remediation-ff-boundary-delivery-info', 'candidate-form-fill-remediation-ff-boundary-contact-phone']`
- Source field paths: `{'route': 2, 'safety.reason': 2, 'slots': 2, 'task_type': 2}`
- Source expected normalized-command patterns: `['填写预约时间并确认', '填写配送信息并确认', '填写联系电话并确认']`
- Policy guidance: `form-fill-clarify-boundary-policy`

### `form-fill-confirmation-marker-preservation`

- Source bucket: `confirmation_marker_missing_or_reordered`
- Candidate seeds: `['candidate-form-fill-remediation-ff-confirm-phone', 'candidate-form-fill-remediation-ff-confirm-shipping-address', 'candidate-form-fill-remediation-ff-confirm-invoice-title']`
- Candidate SFT rows: `['candidate-form-fill-remediation-ff-confirm-phone', 'candidate-form-fill-remediation-ff-confirm-shipping-address', 'candidate-form-fill-remediation-ff-confirm-invoice-title']`
- Source field paths: `{'normalized_command': 23}`
- Source expected normalized-command patterns: `['填写手机号并确认', '填写收货地址并确认', '填写发票抬头并确认']`
- Policy guidance: `form-fill-confirmation-marker-policy`

### `form-fill-field-specificity-preservation`

- Source bucket: `field_name_specificity_drift`
- Candidate seeds: `['candidate-form-fill-remediation-ff-field-shipping-address', 'candidate-form-fill-remediation-ff-field-invoice-title', 'candidate-form-fill-remediation-ff-field-appointment-time']`
- Candidate SFT rows: `['candidate-form-fill-remediation-ff-field-shipping-address', 'candidate-form-fill-remediation-ff-field-invoice-title', 'candidate-form-fill-remediation-ff-field-appointment-time']`
- Source field paths: `{'normalized_command': 4, 'slots': 14}`
- Source expected normalized-command patterns: `['填写收货地址', '填写发票抬头', '填写预约时间']`
- Policy guidance: `form-fill-field-specificity-policy`

## Recommended Next Step

Run a later bounded OpenSpec phase for a local candidate integration check or a formal merge/probe decision. Keep DPO, evaluator relaxation, A100 training, and model-quality claims separate unless explicitly scoped.
