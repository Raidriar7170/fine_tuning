# Voice2Task form-fill remediation public sample merge

This report records a formal data merge into the public sample. It does not prove held-out recovery, model recovery, adapter release, checkpoint release, production readiness, or live-browser improvement.

## Boundary

- Formal public sample seed, SFT, DPO, and manifest files were rebuilt.
- The new DPO pairs are data-construction artifacts, not DPO training evidence.
- No SFT/DPO/GRPO training, prediction run, or A100 execution was performed.
- strict `contract_exact_match` remains the future primary evaluation metric.
- Soft slot F1 and semantic equivalence remain diagnostic-only.

## Summary

- Seed rows: `86`
- SFT rows: `240`
- DPO pairs: `742`
- SFT split counts: `{'train': 102, 'dev': 69, 'test': 69}`
- Merged candidate seed rows: `9`
- Merged candidate SFT rows: `9`
- Candidate DPO pair contribution: `81`
- Source case groups: `['form-fill-clarify-boundary-protection', 'form-fill-confirmation-marker-preservation', 'form-fill-field-specificity-preservation']`
- Candidate seed split counts: `{'train': 9, 'dev': 0, 'test': 0}`

## DPO Rejection Deltas

- `form_confirmation_drift`: `9`
- `malformed_schema`: `9`
- `missing_confirmation`: `9`
- `missing_slot`: `9`
- `underspecified_request`: `9`
- `unsafe_allowance`: `9`
- `wrong_route`: `9`
- `wrong_slot`: `9`
- `wrong_task_type`: `9`

## Recommended Next Step

Use the new manifest ID for a later prediction-only eval phase. Do not compare new results to prior held-out metrics without noting that the formal public sample boundary changed.
