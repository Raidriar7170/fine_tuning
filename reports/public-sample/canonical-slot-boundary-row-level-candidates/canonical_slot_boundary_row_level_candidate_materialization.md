# Canonical Slot Boundary Row-Level Candidate Materialization

This report records a standalone row-level candidate source for the reviewed canonical slot-boundary classes. It does not merge the formal public sample and does not replace formal SFT or DPO artifacts.

## Result

- Status: `standalone_row_level_candidate_source_materialized`
- Candidate source: `data/public-samples/canonical_slot_boundary_seed_candidates.jsonl`
- Seed rows: 7
- Report-local SFT preview rows: 21
- Split: all rows stay `train`
- Candidate status: `standalone_not_formal_public_sample`

## Included Classes

| class | rows | source candidate ids |
| --- | ---: | --- |
| `slot_key_aliases` | 3 | `slot-key-alias-search-text-query`, `slot-key-alias-site-url`, `slot-key-alias-field-value` |
| `slot_value_boundaries` | 4 | `slot-value-boundary-whitespace-trim`, `slot-value-boundary-fullwidth-punctuation`, `slot-value-boundary-filler-removal`, `slot-value-boundary-url-email-casing` |

## Excluded Boundaries

`normalized_command_display_diagnostic` remains display-only. Excluded non-equivalence cases for date, city/location, product, URL host, price/amount, query/product, location/destination, and action/reason are not materialized.

## Formal Data Boundary

The formal public sample files remain outside this phase:

- `data/public-samples/seed_traces.jsonl`
- `data/public-samples/sft_public_sample.jsonl`
- `data/public-samples/dpo_public_sample.jsonl`
- `data/public-samples/manifest_public_sample.json`

This phase performs no formal SFT/DPO generation, manifest rebuild, split change, evaluator change, prediction run, training run, A100 job, postprocessor implementation, strict-exact relaxation, LLM judge, semantic-equivalence scoring, prediction repair, checkpoint release, or adapter release.

## Comparison Boundary

Because this is a standalone source only, the current formal sample boundary is unchanged and old formal metrics remain directly comparable. A later formal merge review/apply phase can inspect this source, but direct merge is not implemented now.

## Claims Not To Overstate

No model-quality improvement can be inferred. This is not held-out recovery, not production readiness, not safety readiness, not a `slot_f1_soft` recovery claim, and not live-browser benchmark evidence.
