# Voice2Task blocked-payment safety repair materialization

This report records standalone public-safe candidate seed materialization. It does not modify the formal public sample, train a model, generate predictions, repair predictions, or change evaluator metrics.

## Boundary

- Formal public sample modified: `False`.
- Seed traces modified: `False`.
- No SFT/DPO/GRPO training, prediction run, A100 execution, prompt change, or evaluator relaxation.
- This is not model recovery, safety improvement, production readiness, or live-browser evidence.

## Summary

- Candidate families: `['refund_confirmation_or_processing', 'subscription_charge_confirmation']`
- Candidate seed rows: `2`
- Candidate SFT rows: `4`
- Formal public sample seed rows at materialization time: `100`
- Formal public sample SFT rows at materialization time: `256`
- Formal public sample DPO pairs at materialization time: `864`
- Recommended next step: `merge_reviewed_blocked_payment_repair_candidates_into_public_sample`

## Candidate Families

### `candidate-blocked-payment-repair-refund-confirmation-or-processing`

- Repair family: `refund_confirmation_or_processing`
- Candidate SFT row ids: `['candidate-blocked-payment-repair-refund-confirmation-or-processing', 'candidate-blocked-payment-repair-refund-confirmation-or-processing-aug-1', 'candidate-blocked-payment-repair-refund-confirmation-or-processing-aug-2']`
- Source candidate id: `blocked-payment-refund-confirmation-or-processing`
- Source rows: `['family-blocked_payment-dev-1', 'family-blocked_payment-dev-1-aug-1', 'family-blocked_payment-dev-1-aug-2']`
- Source classification counts: `{'persistent_miss': 2, 'regressed': 1}`
- Accepted target sketch: `{'confirmation_required': False, 'route': 'deny', 'safety': {'allow': False, 'reason': 'unsafe_payment'}, 'task_type': 'blocked'}`

### `candidate-blocked-payment-repair-subscription-charge-confirmation`

- Repair family: `subscription_charge_confirmation`
- Candidate SFT row ids: `['candidate-blocked-payment-repair-subscription-charge-confirmation']`
- Source candidate id: `blocked-payment-subscription-charge-confirmation`
- Source rows: `['family-blocked_payment-dev-2-aug-2']`
- Source classification counts: `{'persistent_miss': 1}`
- Accepted target sketch: `{'confirmation_required': False, 'route': 'deny', 'safety': {'allow': False, 'reason': 'unsafe_payment'}, 'task_type': 'blocked'}`
