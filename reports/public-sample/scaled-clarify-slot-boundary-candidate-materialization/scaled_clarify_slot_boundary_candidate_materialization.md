# Voice2Task scaled clarify slot-boundary candidate materialization

This is a standalone scaled clarify slot-boundary candidate materialization. It creates public-safe candidate seed/SFT sidecars and does not merge the formal public sample.

## Boundary

- Formal public sample seed, SFT, DPO, and manifest files are not rewritten.
- No formal public sample merge is performed.
- No DPO pairs, SFT training, prediction run, or A100 execution is performed.
- No prompt change, evaluator metric change, slot normalization, or prediction repair is introduced.
- strict `contract_exact_match` and strict `slot_f1` remain primary for later evaluation.
- No model-quality improvement can be inferred until a later strict prediction or training evaluation exists.

## Summary

- Source manifest: `public-sample-20260617T152259Z`
- Candidate themes: `3`
- Source families represented: `28`
- Source-family incidence represented: `78`
- Candidate seed rows: `9`
- Candidate SFT rows: `27`
- Seed split counts: `{'train': 3, 'dev': 3, 'test': 3}`
- SFT split counts: `{'train': 9, 'dev': 9, 'test': 9}`
- Formal public sample modified: `False`
- Recommended next change: `merge-scaled-clarify-slot-boundary-candidates`

## Theme Counts

| theme | candidate seeds |
| --- | ---: |
| `clarify_navigation_or_form_fill_ambiguity` | 3 |
| `clarify_pronoun_or_context_missing` | 3 |
| `clarify_search_or_extract_ambiguity` | 3 |

## Recommended Next Step

Review these standalone candidates before any later formal merge, DPO generation, training retry, or model-quality claim. A later bounded phase should create a new formal manifest boundary before comparing strict metrics.
