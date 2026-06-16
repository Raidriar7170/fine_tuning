# Voice2Task form-fill confirmation-marker extension public sample merge

This report records a formal data merge into the public sample. It does not prove held-out recovery, model recovery, adapter release, checkpoint release, production readiness, private-corpus generalization, public full-corpus release, or live-browser improvement.

## Boundary

- Formal public sample seed, SFT, DPO, and manifest files were rebuilt.
- The 108 DPO pairs are data-construction artifacts, not DPO training evidence.
- No SFT/DPO/GRPO training, prediction run, or A100 execution was performed.
- strict `contract_exact_match` remains the authoritative primary metric.
- strict `slot_f1` remains the authoritative primary metric.
- `slot_f1_soft` and semantic equivalence remain diagnostic-only.

## Summary

- Pre-merge counts: `{'seed_rows': 86, 'sft_rows': 240, 'dpo_pairs': 742}`
- Post-merge seed rows: `98`
- Post-merge SFT rows: `252`
- Post-merge DPO pairs: `850`
- SFT split counts: `{'train': 114, 'dev': 69, 'test': 69}`
- Merged candidate seed rows: `12`
- Merged candidate SFT rows: `12`
- Candidate DPO pair contribution: `108`
- Source family IDs: `['family-confirmation-dev-1', 'family-confirmation-dev-2', 'family-confirmation-dev-3', 'family-confirmation-test-1', 'family-confirmation-test-2', 'family-confirmation-test-3', 'family-form_fill-dev-1', 'family-form_fill-dev-2', 'family-form_fill-dev-3', 'family-form_fill-test-1', 'family-form_fill-test-2', 'family-form_fill-test-3']`
- Candidate seed split counts: `{'train': 12, 'dev': 0, 'test': 0}`

## Validation

- Public artifact validation ok: `True`
- Validation counts: `{'sft_rows': 252, 'dpo_pairs': 850}`
- Validation failures: `[]`

## DPO Rejection Deltas

- `form_confirmation_drift`: `12`
- `malformed_schema`: `12`
- `missing_confirmation`: `12`
- `missing_slot`: `12`
- `underspecified_request`: `12`
- `unsafe_allowance`: `12`
- `wrong_route`: `12`
- `wrong_slot`: `12`
- `wrong_task_type`: `12`

## Recommended Next Step

Use the new manifest ID for a later prediction-only eval phase. Do not compare new results to prior held-out metrics without noting that the formal public sample boundary changed.
