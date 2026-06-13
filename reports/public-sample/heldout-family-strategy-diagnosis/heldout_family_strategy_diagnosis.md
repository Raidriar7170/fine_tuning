# Voice2Task held-out family strategy diagnosis

This local public-sample diagnosis explains why the current tiny adapter has zero held-out strict exact match. It is not blind data scaling, not a model recovery claim, and not held-out generalization evidence.

## Boundary

- This does not train, run prediction, generate data, or run DPO.
- This is not a checkpoint release.
- This is not an adapter release.
- This is not a model recovery claim.
- This makes no production-readiness or live-browser benchmark claim.
- Semantic equivalence is not promoted to the primary metric.

## Summary

- Source manifest: `public-sample-20260613T072200Z`
- Held-out strict exact match: `{'dev': 0.0, 'test': 0.0}`
- Tiny training subset family count: `1`
- Held-out residual family count: `4`
- Broad data scaling recommended now: `False`
- Recommended next step: `propose_targeted_family_coverage_probe`

## Strategy

- Primary: `targeted_family_coverage_probe_before_broad_scaling`
- Requires user confirmation: `True`
- Interpretation: targeted family coverage should be tested before broad data scaling.

## Rationale

- heldout strict exact match is zero on current dev/test
- all heldout contract families have train analog coverage in the dataset
- the current tiny adapter subset trained only one search-family source
- therefore the next falsifiable step should test targeted family coverage before broad data scaling

## Held-out Residual Families

### `seed-clarify-ambiguous`

- Split: `dev`
- Contract family: `clarify|clarify|ambiguous_request|confirm:true|slots:ambiguity`
- Rows: `3`
- Train analog family: `seed-clarify-target`
- Train analog rows: `3`
- Tiny subset rows: `0`
- Schema-invalid predictions: `0`
- Field mismatches: `{'confirmation_required': 3, 'normalized_command': 3, 'route': 2, 'safety.allow': 1, 'safety.reason': 2, 'slots': 3, 'task_type': 2}`
- DPO hard-negative category: `clarify_action_drift`
- Strategy bucket: `targeted_sft_family_coverage`

### `seed-open-example`

- Split: `dev`
- Contract family: `navigate|open_url|public_readonly|confirm:false|slots:url`
- Rows: `3`
- Train analog family: `seed-open-help`
- Train analog rows: `3`
- Tiny subset rows: `0`
- Schema-invalid predictions: `0`
- Field mismatches: `{'normalized_command': 3, 'route': 1, 'slots': 1, 'task_type': 1}`
- DPO hard-negative category: `navigate_canonical_url_drift`
- Strategy bucket: `targeted_sft_family_coverage`

### `seed-block-purchase`

- Split: `test`
- Contract family: `blocked|deny|unsafe_payment|confirm:true|slots:reason`
- Rows: `3`
- Train analog family: `seed-block-transfer`
- Train analog rows: `3`
- Tiny subset rows: `0`
- Schema-invalid predictions: `0`
- Field mismatches: `{'normalized_command': 3, 'slots': 3}`
- DPO hard-negative category: `blocked_payment_action_drift`
- Strategy bucket: `targeted_sft_family_coverage`

### `seed-form-email`

- Split: `test`
- Contract family: `form_fill|fill_form|requires_confirmation|confirm:true|slots:field`
- Rows: `3`
- Train analog family: `seed-form-nickname`
- Train analog rows: `3`
- Tiny subset rows: `0`
- Schema-invalid predictions: `2`
- Field mismatches: `{'normalized_command': 3, 'safety.allow': 1, 'safety.reason': 2, 'slots': 3}`
- DPO hard-negative category: `form_confirmation_drift`
- Strategy bucket: `targeted_sft_family_coverage`

## DPO Hard-negative Signal

- Categories available: `['blocked_payment_action_drift', 'clarify_action_drift', 'form_confirmation_drift', 'navigate_canonical_url_drift']`
- Category count: `4`
- Execute DPO in this phase: `False`

## Candidate Next Phases

- `propose_targeted_sft_family_coverage_probe`
- `validate_residual_family_dpo_hard_negatives`
- `inspect_prompt_policy_only_if_targeted_coverage_still_fails`
