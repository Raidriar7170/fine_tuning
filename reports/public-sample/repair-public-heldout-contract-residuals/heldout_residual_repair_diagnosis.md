# Held-out residual repair diagnosis

## Summary

- Overall interpretation: `public_heldout_residual_repair_failed`
- Train strict exact match: `0.3333`
- Dev strict exact match: `0.0000`
- Test strict exact match: `0.0000`
- Claims: no release, no private-corpus generalization, no production-readiness claim.

## Residuals

- train: confirmation_required=3, contract_version=1, normalized_command=11, route=7, safety.allow=2, safety.reason=5, slots=8, task_type=7
- dev: confirmation_required=3, normalized_command=6, route=4, safety.reason=3, slots=4, task_type=4
- test: confirmation_required=3, normalized_command=6, route=2, safety.allow=2, safety.reason=3, slots=5, task_type=2

## Next step

Open a bounded diagnostic phase for the training signal before more A100 reruns.
