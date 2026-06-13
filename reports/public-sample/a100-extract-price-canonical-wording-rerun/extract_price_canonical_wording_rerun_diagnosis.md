# A100 extract-price canonical wording rerun diagnosis

Overall interpretation: `extract_price_canonical_wording_recovered_on_train_split`.

## Summary

- Strict `contract_exact_match`: `1.0000`
- Strict `slot_f1`: `1.0000`
- Extract-price exact rows: `3/3`
- Wrong price synonym target count: `0`
- Extra-particle normalized command count: `0`
- Search fallback count: `0`

The residual targeted by this phase is recovered on the bounded public train split. This is still not a held-out generalization, model release, adapter release, or production-readiness claim.
