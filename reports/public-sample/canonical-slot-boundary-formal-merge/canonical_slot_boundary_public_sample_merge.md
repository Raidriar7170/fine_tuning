# Voice2Task canonical slot-boundary public sample merge

This report records a formal public-sample data merge. It does not prove held-out recovery, model quality, safety improvement, adapter release, checkpoint release, production readiness, public full-corpus release, or live-browser improvement.

## Boundary

- Formal public sample seed, SFT, DPO, and manifest files were rebuilt.
- No SFT/DPO/GRPO training, prediction run, A100 execution, prompt change, postprocessor implementation, slot normalization, or evaluator relaxation was performed.
- strict `contract_exact_match` and strict `slot_f1` remain authoritative for later evaluation.
- `slot_f1_soft` and semantic equivalence remain diagnostic-only.
- The formal public sample boundary changed; old metrics are not directly comparable.

## Counts

- Pre-merge counts: `{'dpo_pairs': 2046, 'seed_rows': 240, 'sft_rows': 675}`
- Post-merge seed rows: `247`
- Post-merge SFT rows: `696`
- Post-merge DPO pairs: `2100`
- Post-merge SFT split counts: `{'train': 282, 'dev': 207, 'test': 207}`

## Candidate Source

- Candidate seed rows: `7`
- Candidate SFT rows: `21`
- Candidate DPO pair delta: `54`
- Candidate seed split counts: `{'dev': 0, 'test': 0, 'train': 7}`
- Eligible source class counts: `{'slot_key_aliases': 3, 'slot_value_boundaries': 4}`

## Comparison Boundary

- Changed: `True`
- Previous manifest: `public-sample-20260617T152259Z`
- New manifest: `public-sample-20260619T090925Z`
- Old metrics directly comparable: `False`

## Validation

- Dataset validation ok: `True`
- Validation failures: `[]`

## DPO Rejection Deltas

- `blocked_payment_action_drift`: `0`
- `clarify_action_drift`: `0`
- `decomposed_search_slots`: `0`
- `extract_extra_particle_wording`: `0`
- `extract_generic_price_wording`: `0`
- `extract_listed_price_wording`: `0`
- `extract_query_slot`: `1`
- `extract_search_fallback`: `1`
- `form_confirmation_drift`: `0`
- `malformed_schema`: `7`
- `missing_confirmation`: `1`
- `missing_slot`: `7`
- `navigate_canonical_url_drift`: `2`
- `underspecified_request`: `7`
- `unsafe_allowance`: `7`
- `wrong_route`: `7`
- `wrong_slot`: `7`
- `wrong_task_type`: `7`

## Recommended Next Step

Run any model prediction or training work only in a later bounded phase that explicitly names this new manifest boundary.
