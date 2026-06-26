# Frozen Lockbox and Lineage Guard

Updated: 2026-06-27

The Phase 3 lockbox workflow is implemented as a deterministic validator and
CLI guard. `lockbox-v1` has now been authored from the manually reviewed draft
and frozen under `data/lockbox/`. Final model evaluation has not been run, and
no lockbox metrics exist yet.

## Lockbox Row Contract

Each lockbox JSONL row must contain:

- `row_id`: stable row identifier, unique within the lockbox.
- `semantic_family_id`: family identifier used for family-disjointness checks.
- `input_text`: final lockbox input text.
- `gold_contract`: Browser Task Contract V1 gold label.
- `source.category`: provenance category, for example
  `new_lockbox_authoring`; it must not be `train`, `training`, `analysis`, or
  `remediation`.
- `source.provenance`: non-empty provenance object.
- `derived_from`: ancestry list; it must not reach train, analysis, or
  remediation rows.
- `analysis_seen`: boolean flag. Final lockbox rows must be `false`.
- `content_hash`: deterministic SHA-256 over the row excluding `content_hash`.

The manifest must contain:

- `frozen`: exactly `true`.
- `row_count`: number of JSONL rows.
- `family_count`: number of unique `semantic_family_id` values.
- `schema_version` or `schema_id`: non-empty schema identifier.
- `created_at` or `frozen_at`: non-empty timestamp string.
- `provenance_summary`: non-empty object summarizing lockbox source categories.
- `content_hashes`: optional row-ordered list; when present it must match the
  deterministic row hashes in lockbox order.
- `lockbox_hash`, `lockbox_sha256`, or `dataset_sha256`: deterministic SHA-256
  over the row content hash list. Supplying multiple hash fields is allowed;
  every supplied hash field is checked.

See [`lockbox-manifest-template.json`](lockbox-manifest-template.json) for a
minimal template. The template is not a real frozen lockbox manifest.

## Validator

`derived_from` may contain strings or objects with `row_id`, `id`,
`source_id`, `source_case_id`, `source_candidate_id`, `source_row_id`, or a
nested `provenance` object containing those source identifiers. Nested
`derived_from` lists are traversed recursively.

Run:

```bash
voice2task-data validate-lockbox \
  --lockbox path/to/lockbox.jsonl \
  --manifest path/to/manifest.json \
  --train data/public-samples/sft_public_sample.jsonl \
  --analysis path/to/analysis.jsonl \
  --require-family-disjointness
```

The validator prints machine-readable JSON:

```json
{
  "ok": false,
  "failures": [],
  "counts": {},
  "manifest": {}
}
```

It exits `0` only when all checks pass and `1` when any failure is present.

The validator fails closed for:

- duplicate `row_id`
- lockbox `row_id` overlap with train or analysis reference `id` / `row_id`
- exact input text overlap with train or analysis data
- normalized input text overlap with train or analysis data
- semantic family overlap when `--require-family-disjointness` is set
- ancestry that reaches train, analysis, or remediation rows
- missing provenance fields
- duplicate content hashes
- row content hash mismatch
- manifest row count, family count, schema, timestamp, provenance summary, or
  hash mismatch
- final manifest not marked frozen

## One-Look Rule

Development must use train/dev data only. Do not inspect lockbox failures while
tuning data, prompts, decoding, code, or model weights.

Before final lockbox evaluation, freeze:

- code commit
- model or adapter identity
- prompt template
- decoding settings
- evaluator version
- lockbox manifest hash

Then run final evaluation once. Report aggregate results only. Do not tune,
patch, select, or reweight anything against individual lockbox failures. Any
post-lockbox diagnosis is a new phase with the lockbox result already spent.

## Frozen Lockbox V1

Committed lockbox v1 artifacts:

- `data/lockbox/lockbox-v1.draft.jsonl`: manually reviewed candidate input.
- `data/lockbox/lockbox-v1.jsonl`: frozen materialized lockbox with
  deterministic `content_hash` values.
- `data/lockbox/lockbox-v1.manifest.json`: frozen manifest.

Freeze summary:

- `row_count`: 120.
- `family_count`: 120.
- `lockbox_hash`: `06114cf3ad6029930284af5f2245fb2c4a8174fd35c6a1107f4c73482b555b33`.
- `dataset_sha256`: `06114cf3ad6029930284af5f2245fb2c4a8174fd35c6a1107f4c73482b555b33`.

Final model evaluation has not been run. No lockbox metrics exist yet. The
one-look rule still applies: freeze code, prompt, evaluator, model/adapter,
decoding config, and lockbox hash before running the final evaluation once.
