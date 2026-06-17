# Voice2Task current-retry confirmation-preservation public sample merge

This report records a formal data merge into the public sample. It does not prove held-out recovery, model recovery, safety improvement, adapter release, checkpoint release, production readiness, public full-corpus release, or live-browser improvement.

## Boundary

- Formal public sample seed, SFT, DPO, and manifest files were rebuilt.
- The new DPO pairs are data-construction artifacts, not DPO training evidence.
- No SFT/DPO/GRPO training, prediction run, A100 execution, prompt change, slot normalization, or evaluator relaxation.
- strict `contract_exact_match` and strict `slot_f1` remain authoritative future metrics.
- `slot_f1_soft` and semantic equivalence remain diagnostic-only.

## Summary

- Pre-merge counts: `{'dpo_pairs': 864, 'seed_rows': 100, 'sft_rows': 256}`
- Post-merge seed rows: `102`
- Post-merge SFT rows: `261`
- Post-merge DPO pairs: `881`
- SFT split counts: `{'train': 123, 'dev': 69, 'test': 69}`
- Merged candidate seed rows: `2`
- Merged candidate SFT rows: `5`
- Candidate DPO pair contribution: `17`
- Candidate families: `['public_navigation_non_confirmation_preservation', 'unsafe_payment_confirmation_preservation']`
- Candidate seed split counts: `{'train': 2, 'dev': 0, 'test': 0}`

## Validation

- Public artifact validation ok: `True`
- Validation counts: `{'sft_rows': 261, 'dpo_pairs': 881}`
- Validation failures: `[]`

## DPO Rejection Deltas

- `blocked_payment_action_drift`: `1`
- `malformed_schema`: `2`
- `missing_confirmation`: `1`
- `missing_slot`: `2`
- `navigate_canonical_url_drift`: `1`
- `underspecified_request`: `2`
- `unsafe_allowance`: `2`
- `wrong_route`: `2`
- `wrong_slot`: `2`
- `wrong_task_type`: `2`

## Recommended Next Step

Use the new manifest ID for a later bounded prediction-only or training-readiness phase. Do not compare new results to prior held-out metrics without noting that the formal public sample boundary changed.
