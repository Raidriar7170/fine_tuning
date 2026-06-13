# A100 extract-price canonical wording rerun evidence

Status: A100 public-sample train-split diagnostic evidence. This is not a benchmark, not a release, and not a model-recovery claim.

## Scope

- Base model: `Qwen/Qwen2.5-7B-Instruct`
- Dataset manifest: `public-sample-20260613T063029Z`
- Public SFT rows in manifest: `18`
- Public DPO pairs in manifest: `51`
- Training rows used after split filter: `6`
- Prediction source kind: `private_a100_adapter`
- Prediction split: `train`
- Overfit diagnostic: `True`
- Generalization claim: `False`
- Release status: `not_released`

## Observed Result

The rerun produced `6` train predictions. Schema-valid Browser Task Contract rate was `1.0000`, strict `contract_exact_match` was `1.0000`, strict `slot_f1` was `1.0000`, and internal-only `slot_f1_soft` was `1.0000`.

Compact-query/search rows stayed `3/3` exact match. Extract-price rows are `3/3` strict exact, with `0` wrong price-synonym targets and `0` extra-particle normalized-command variants remaining.

## Public Artifacts

- `manifest`: `reports/public-sample/a100-extract-price-canonical-wording-rerun/manifest.json`
- `report`: `reports/public-sample/a100-extract-price-canonical-wording-rerun/report.md`
- `metrics`: `reports/public-sample/a100-extract-price-canonical-wording-rerun/metrics.json`
- `schema_diagnostics`: `reports/public-sample/a100-extract-price-canonical-wording-rerun/schema_diagnostics.json`
- `alignment_diagnostics`: `reports/public-sample/a100-extract-price-canonical-wording-rerun/alignment_diagnostics.json`
- `constrained_decoding_diagnosis`: `reports/public-sample/a100-extract-price-canonical-wording-rerun/constrained_decoding_diagnosis.json`
- `schema_guard_summary`: `reports/public-sample/a100-extract-price-canonical-wording-rerun/schema_guard_summary.json`
- `diagnosis`: `reports/public-sample/a100-extract-price-canonical-wording-rerun/extract_price_canonical_wording_rerun_diagnosis.json`
- `prediction_metadata`: `reports/public-sample/a100-extract-price-canonical-wording-rerun/prediction_metadata.json`
- `prompt_snapshot`: `reports/public-sample/a100-extract-price-canonical-wording-rerun/prompt_snapshot.json`
- `raw_decoded_summary`: `reports/public-sample/a100-extract-price-canonical-wording-rerun/raw_decoded_summary.jsonl`
- `generation_trace`: `reports/public-sample/a100-extract-price-canonical-wording-rerun/generation_trace.jsonl`
- `train_split_gold`: `reports/public-sample/a100-extract-price-canonical-wording-rerun/train_split_gold.jsonl`
- `leak_scan`: `reports/public-sample/a100-extract-price-canonical-wording-rerun/leak_scan_result.json`
- `phase_validation_leak_scan`: `reports/public-sample/a100-extract-price-canonical-wording-rerun/phase_validation_leak_scan_result.json`
- `post_archive_leak_scan`: `reports/public-sample/a100-extract-price-canonical-wording-rerun/post_archive_leak_scan_result.json`
- `final_leak_scan`: `reports/public-sample/a100-extract-price-canonical-wording-rerun/final_leak_scan_result.json`

## Boundary

The evidence pack contains sanitized public-sample contract predictions, aggregate metrics, schema guard summaries, prompt snapshots, raw decoded summaries, generation traces, and residual diagnosis. It does not copy raw logs, checkpoints, adapters, remote caches, private overrides, host details, SSH details, tokens, private paths, or private corpus rows into git.

## Interpretation

This phase answers a narrow question: after adding explicit canonical wording policy and DPO hard negatives, the current 7B SFT path can recover the strict extract-price canonical target on the bounded public train split. It does not prove dev/test generalization, private-corpus behavior, production readiness, or any checkpoint/adapter release quality.
