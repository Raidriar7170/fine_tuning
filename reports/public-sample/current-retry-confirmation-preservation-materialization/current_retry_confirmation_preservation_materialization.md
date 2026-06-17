# Voice2Task current-retry confirmation-preservation materialization

This report records standalone public-safe candidate seed materialization. It does not modify the formal public sample, train a model, generate predictions, repair predictions, normalize slots, or change evaluator metrics.

## Boundary

- Formal public sample modified: `False`.
- Seed traces modified: `False`.
- No SFT/DPO/GRPO training, prediction run, A100 execution, prompt change, slot normalization, or evaluator relaxation.
- This is not model recovery, safety improvement, production readiness, held-out recovery, or live-browser evidence.

## Summary

- Source manifest: `public-sample-20260616T165835Z`
- Candidate families: `['public_navigation_non_confirmation_preservation', 'unsafe_payment_confirmation_preservation']`
- Candidate seed rows: `2`
- Candidate SFT rows: `5`
- Formal public sample seed rows at materialization time: `100`
- Formal public sample SFT rows at materialization time: `256`
- Formal public sample DPO pairs at materialization time: `864`
- Recommended next step: `merge_current_retry_confirmation_preservation_candidates_into_public_sample`

## Candidate Families

### `candidate-current-retry-public-navigation-non-confirmation-preservation`

- Candidate family: `public_navigation_non_confirmation_preservation`
- Candidate SFT row ids: `['candidate-current-retry-public-navigation-non-confirmation-preservation', 'candidate-current-retry-public-navigation-non-confirmation-preservation-aug-1']`
- Source candidate id: `current-retry-public-navigation-non-confirmation-preservation`
- Source rows: `['family-navigation-test-1', 'family-navigation-test-3-aug-1']`
- Accepted target sketch: `{'confirmation_required': False, 'route': 'open_url', 'safety': {'allow': True, 'reason': 'public_readonly'}, 'slots': {'url': '<canonical public URL>'}, 'task_type': 'navigate'}`
- Rejected drift sketches: `[{'confirmation_required': True, 'drift': 'clarifies_public_navigation', 'route': 'clarify', 'safety': {'allow': True, 'reason': 'ambiguous_request'}, 'task_type': 'clarify'}, {'confirmation_required': False, 'drift': 'changes_canonical_navigation_url', 'route': 'open_url', 'safety': {'allow': True, 'reason': 'public_readonly'}, 'slots': {'url': '<strict-wrong public URL>'}, 'task_type': 'navigate'}]`

### `candidate-current-retry-unsafe-payment-confirmation-preservation`

- Candidate family: `unsafe_payment_confirmation_preservation`
- Candidate SFT row ids: `['candidate-current-retry-unsafe-payment-confirmation-preservation', 'candidate-current-retry-unsafe-payment-confirmation-preservation-aug-1', 'candidate-current-retry-unsafe-payment-confirmation-preservation-aug-2']`
- Source candidate id: `current-retry-unsafe-payment-confirmation-preservation`
- Source rows: `['family-blocked_payment-dev-1', 'family-blocked_payment-dev-1-aug-1', 'family-blocked_payment-dev-1-aug-2', 'family-blocked_payment-dev-2-aug-2', 'family-blocked_payment-dev-3']`
- Accepted target sketch: `{'confirmation_required': True, 'route': 'deny', 'safety': {'allow': False, 'reason': 'unsafe_payment'}, 'slots': {'action': '<unsafe payment action>', 'reason': '<payment control reason>'}, 'task_type': 'blocked'}`
- Rejected drift sketches: `[{'confirmation_required': False, 'drift': 'drops_confirmation_on_blocked_payment', 'route': 'deny', 'safety': {'allow': False, 'reason': 'unsafe_payment'}, 'task_type': 'blocked'}, {'confirmation_required': True, 'drift': 'allows_payment_as_form_fill', 'route': 'fill_form', 'safety': {'allow': True, 'reason': 'requires_confirmation'}, 'task_type': 'form_fill'}]`
