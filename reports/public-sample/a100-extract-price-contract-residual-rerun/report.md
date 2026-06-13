# A100 extract-price contract residual rerun evidence

Status: A100 public-sample train-split diagnostic evidence. This is not a benchmark, not a release, and not a model-recovery claim.

## Scope

- Base model: `Qwen/Qwen2.5-7B-Instruct`
- Dataset manifest: `public-sample-20260613T060441Z`
- Public SFT rows in manifest: `18`
- Public DPO pairs in manifest: `48`
- Training rows used after split filter: `6`
- Prediction source kind: `private_a100_adapter`
- Prediction split: `train`
- Overfit diagnostic: `True`
- Generalization claim: `False`
- Release status: `not_released`

## Observed Result

The rerun produced `6` train predictions. Schema-valid Browser Task Contract rate was `1.0000`, strict `contract_exact_match` was `0.5000`, strict `slot_f1` was `0.6667`, and internal-only `slot_f1_soft` was `0.7778`.

Compact-query/search rows stayed `3/3` exact match. Extract-price rows improved on task/route shape (`3/3` task+route correct, no search fallback, no `slots.query`/`page_url` drift), but remained `0/3` strict exact due to `normalized_command` and target-slot wording mismatches.

## Public Artifacts

- `schema_guard_summary`: `reports/public-sample/a100-extract-price-contract-residual-rerun/schema_guard_summary.json`
- `diagnosis`: `reports/public-sample/a100-extract-price-contract-residual-rerun/extract_price_contract_residual_rerun_diagnosis.json`
- `metrics`: `reports/public-sample/a100-extract-price-contract-residual-rerun/metrics.json`
- `predictions`: `reports/public-sample/a100-extract-price-contract-residual-rerun/predictions.jsonl`
- `prompt_snapshot`: `reports/public-sample/a100-extract-price-contract-residual-rerun/prompt_snapshot.json`
- `raw_decoded_summary`: `reports/public-sample/a100-extract-price-contract-residual-rerun/raw_decoded_summary.jsonl`
- `generation_trace`: `reports/public-sample/a100-extract-price-contract-residual-rerun/generation_trace.jsonl`
- `leak_scan`: `reports/public-sample/a100-extract-price-contract-residual-rerun/leak_scan_result.json`
- `post_archive_leak_scan`: `reports/public-sample/a100-extract-price-contract-residual-rerun/post_archive_leak_scan_result.json`
- `final_leak_scan`: `reports/public-sample/a100-extract-price-contract-residual-rerun/final_leak_scan_result.json`
- `manifest`: `reports/public-sample/a100-extract-price-contract-residual-rerun/manifest.json`

## Boundary

The evidence pack contains sanitized public-sample contract predictions, aggregate metrics, schema guard summaries, prompt snapshots, raw decoded summaries, generation traces, and residual diagnosis. It does not copy raw logs, checkpoints, adapters, remote caches, private overrides, host details, SSH details, tokens, private paths, or private corpus rows into git.

## Interpretation

This phase answers a narrow question: the current 7B SFT path can preserve compact-query and recover extract task/route shape, but it still does not learn the strict canonical extract-price target. The next phase should be a small canonical target wording repair, not a claim that data volume alone solved the training problem.
