# Voice2Task form-fill remediation plan diagnosis

This report is a plan-only diagnosis for the selected `form_fill` formal held-out residuals. It does not generate data, change gold labels, launch training, rerun predictions, or relax evaluator metrics.

## Boundary

- strict `contract_exact_match` remains primary.
- Strict `slot_f1` remains authoritative for slot scoring.
- `slot_f1_soft` remains diagnostic-only.
- No current public held-out split is modified.
- Any future data design, training, DPO, or A100 work needs a separate confirmed phase.

## Summary

- Target: `form_fill`
- Task family: `form_fill|fill_form|requires_confirmation|confirm:true|slots:field`
- Residual rows: `29`
- Residual fields: `49`
- Bucket field counts: `{'confirmation_marker_missing_or_reordered': 23, 'field_name_specificity_drift': 18, 'clarify_boundary_confusion': 8}`
- Bucket row counts: `{'confirmation_marker_missing_or_reordered': 23, 'field_name_specificity_drift': 16, 'clarify_boundary_confusion': 2}`
- Field counts: `{'normalized_command': 27, 'route': 2, 'safety.reason': 2, 'slots': 16, 'task_type': 2}`
- Count consistency: `{'expected_residual_rows': 29, 'computed_residual_rows': 29, 'expected_residual_fields': 49, 'computed_residual_fields': 49, 'ok': True}`
- Recommended strategy: `prompt_policy_clarification_plus_targeted_public_safe_case_design`
- Recommended next change: `design-form-fill-remediation-cases`
- Training recommended now: `False`
- DPO recommended now: `False`
- Evaluator change recommended now: `False`

## Remediation Buckets

### `confirmation_marker_missing_or_reordered`

- Residual rows: `23`
- Residual fields: `23`
- By split: `{'dev': 10, 'test': 13}`
- By field path: `{'normalized_command': 23}`
- By source family: `{'family-confirmation-dev-1': 1, 'family-confirmation-dev-2': 2, 'family-confirmation-dev-3': 1, 'family-confirmation-test-1': 2, 'family-confirmation-test-2': 1, 'family-confirmation-test-3': 2, 'family-form_fill-dev-1': 2, 'family-form_fill-dev-2': 1, 'family-form_fill-dev-3': 3, 'family-form_fill-test-1': 2, 'family-form_fill-test-2': 3, 'family-form_fill-test-3': 3}`

Representative examples:
- `dev / family-form_fill-dev-1 / normalized_command`: gold string(8): 填写手机号并确认; prediction string(5): 填写手机号
- `dev / family-form_fill-dev-1-aug-2 / normalized_command`: gold string(8): 填写手机号并确认; prediction string(6): 填写手机号码
- `dev / family-form_fill-dev-2-aug-1 / normalized_command`: gold string(9): 填写收货地址并确认; prediction string(7): 填写地址到表单
- `dev / family-form_fill-dev-3 / normalized_command`: gold string(9): 填写发票抬头并确认; prediction string(6): 填写发票抬头
- `dev / family-form_fill-dev-3-aug-1 / normalized_command`: gold string(9): 填写发票抬头并确认; prediction string(6): 填写发票抬头

### `field_name_specificity_drift`

- Residual rows: `16`
- Residual fields: `18`
- By split: `{'dev': 10, 'test': 8}`
- By field path: `{'normalized_command': 4, 'slots': 14}`
- By source family: `{'family-confirmation-dev-1': 1, 'family-confirmation-dev-2': 1, 'family-confirmation-dev-3': 4, 'family-confirmation-test-2': 1, 'family-confirmation-test-3': 3, 'family-form_fill-dev-2': 1, 'family-form_fill-dev-3': 3, 'family-form_fill-test-1': 2, 'family-form_fill-test-2': 2}`

Representative examples:
- `dev / family-form_fill-dev-2-aug-1 / slots`: gold object with keys: field; prediction object with keys: field
- `dev / family-form_fill-dev-3 / slots`: gold object with keys: field; prediction object with keys: field
- `dev / family-form_fill-dev-3-aug-1 / slots`: gold object with keys: field; prediction object with keys: field
- `dev / family-form_fill-dev-3-aug-2 / slots`: gold object with keys: field; prediction object with keys: field
- `dev / family-confirmation-dev-1-aug-1 / slots`: gold object with keys: field; prediction object with keys: field

### `clarify_boundary_confusion`

- Residual rows: `2`
- Residual fields: `8`
- By split: `{'dev': 4, 'test': 4}`
- By field path: `{'route': 2, 'safety.reason': 2, 'slots': 2, 'task_type': 2}`
- By source family: `{'family-confirmation-dev-1': 4, 'family-form_fill-test-3': 4}`

Representative examples:
- `dev / family-confirmation-dev-1-aug-2 / task_type`: gold string(9): form_fill; prediction string(7): clarify
- `dev / family-confirmation-dev-1-aug-2 / route`: gold string(9): fill_form; prediction string(7): clarify
- `dev / family-confirmation-dev-1-aug-2 / safety.reason`: gold string(21): requires_confirmation; prediction string(17): ambiguous_request
- `dev / family-confirmation-dev-1-aug-2 / slots`: gold object with keys: field; prediction object with keys: ambiguity
- `test / family-form_fill-test-3-aug-2 / task_type`: gold string(9): form_fill; prediction string(7): clarify

## Recommended Next Step

Open a new bounded case-design phase for `form_fill`. That phase can propose reviewed public-safe examples or prompt/policy wording, but this diagnosis does not authorize materialization, training, DPO, or evaluator changes.
