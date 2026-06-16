# Voice2Task blocked-payment safety repair public sample merge

This report records a formal data merge into the public sample. It does not prove held-out recovery, model recovery, safety improvement, adapter release, checkpoint release, production readiness, public full-corpus release, or live-browser improvement.

## Boundary

- Formal public sample seed, SFT, DPO, and manifest files were rebuilt.
- The new DPO pairs are data-construction artifacts, not DPO training evidence.
- No SFT/DPO/GRPO training, prediction run, A100 execution, prompt change, or evaluator relaxation.
- strict `contract_exact_match` and strict `slot_f1` remain authoritative future metrics.
- `slot_f1_soft` and semantic equivalence remain diagnostic-only.

## Summary

- Pre-merge counts: `{'dpo_pairs': 850, 'seed_rows': 98, 'sft_rows': 252}`
- Post-merge seed rows: `100`
- Post-merge SFT rows: `256`
- Post-merge DPO pairs: `864`
- SFT split counts: `{'train': 118, 'dev': 69, 'test': 69}`
- Merged candidate seed rows: `2`
- Merged candidate SFT rows: `4`
- Candidate DPO pair contribution: `14`
- Repair families: `['refund_confirmation_or_processing', 'subscription_charge_confirmation']`
- Candidate seed split counts: `{'train': 2, 'dev': 0, 'test': 0}`

## Validation

- Public artifact validation ok: `True`
- Validation counts: `{'sft_rows': 256, 'dpo_pairs': 864}`
- Validation failures: `[]`

## DPO Rejection Deltas

- `malformed_schema`: `2`
- `missing_slot`: `2`
- `underspecified_request`: `2`
- `unsafe_allowance`: `2`
- `wrong_route`: `2`
- `wrong_slot`: `2`
- `wrong_task_type`: `2`

## Recommended Next Step

Use the new manifest ID for a later bounded prediction-only or training-readiness phase. Do not compare new results to prior held-out metrics without noting that the formal public sample boundary changed.
