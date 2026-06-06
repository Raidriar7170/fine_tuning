# Search Query Slot Target Policy

## Conclusion

Public-readonly search targets now use compact slots.query and no city/date slot splitting as the canonical local target policy.

## Source

- Prior slot mismatch diagnosis: `reports/public-sample/retry-template-slot-exact-match-mismatch-diagnosis/slot_exact_match_mismatch_diagnosis.json`
- Public sample SFT: `data/public-samples/sft_public_sample.jsonl`
- Public sample DPO: `data/public-samples/dpo_public_sample.jsonl`

## Checks

- Search SFT rows: `3`
- Compact query rows: `3`
- City/date slot rows: `0`
- Query values: `北京明天天气`
- DPO chosen compact query rows: `6`

## Boundaries

- No A100 execution was performed in this phase.
- No training or prediction rerun was performed.
- No slot normalization, semantic-equivalence scoring, prediction repair, prediction replacement, or re-score was performed.
- Prior A100 predictions remain historical evidence and are not reinterpreted as exact-match recovery.

## Validation

- Focused prompt/data/evidence tests: `3 passed`
- Full pytest: `174 passed`
- Ruff: `passed`
- Mypy src: `passed`
- Public data validate and DPO check: `passed`
- Phase leak scan, git diff check, and OpenSpec strict validation: `passed`
