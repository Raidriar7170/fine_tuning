# A100 compact-query exact-match rerun evidence

Status: A100 public-sample train-split diagnostic evidence. This is not a benchmark, not a release, and not a model-recovery claim.

## Scope

- Base model: `Qwen/Qwen2.5-7B-Instruct`
- Dataset manifest: `public-sample-20260613T043923Z`
- Public SFT rows in manifest: `18`
- Training rows used after split filter: `6`
- Prediction source kind: `private_a100_adapter`
- Prediction split: `train`
- Overfit diagnostic: `True`
- Generalization claim: `False`
- Release status: `not_released`

## Observed Result

The rerun produced 6 train predictions. Schema-valid Browser Task Contract rate was `1.0000`, strict `contract_exact_match` was `0.5000`, strict `slot_f1` was `0.5000`, and internal-only `slot_f1_soft` was `0.5000`.

Compact-query/search rows were `3/3` exact match and emitted compact `slots.query`; no decomposed `city/date/topic` compact-query rows were observed. The overall train split still has extract-price residuals, so this is not a full model recovery claim.

## Public Artifacts

- `schema_guard_summary`: `reports/public-sample/a100-compact-query-exact-match-rerun/schema_guard_summary.json`
- `compact_query_residual_diagnosis`: `reports/public-sample/a100-compact-query-exact-match-rerun/compact_query_exact_match_rerun_diagnosis.json`
- `leak_scan`: `reports/public-sample/a100-compact-query-exact-match-rerun/leak_scan_result.json`
- `final_leak_scan`: `reports/public-sample/a100-compact-query-exact-match-rerun/final_leak_scan_result.json`
- `post_archive_leak_scan`: `reports/public-sample/a100-compact-query-exact-match-rerun/post_archive_leak_scan_result.json`
- `manifest`: `reports/public-sample/a100-compact-query-exact-match-rerun/manifest.json`
- `report`: `reports/public-sample/a100-compact-query-exact-match-rerun/report.md`
- `diagnosis`: `reports/public-sample/a100-compact-query-exact-match-rerun/compact_query_exact_match_rerun_diagnosis.json`
- `schema_diagnostics`: `reports/public-sample/a100-compact-query-exact-match-rerun/schema_diagnostics.json`
- `alignment_diagnostics`: `reports/public-sample/a100-compact-query-exact-match-rerun/alignment_diagnostics.json`
- `constrained_decoding_diagnosis`: `reports/public-sample/a100-compact-query-exact-match-rerun/constrained_decoding_diagnosis.json`
- `predictions`: `reports/public-sample/a100-compact-query-exact-match-rerun/predictions.jsonl`
- `metrics`: `reports/public-sample/a100-compact-query-exact-match-rerun/metrics.json`
- `train_split_gold`: `reports/public-sample/a100-compact-query-exact-match-rerun/train_split_gold.jsonl`

## Boundary

The evidence pack contains sanitized public-sample contract predictions, aggregate metrics, schema guard summaries, prompt snapshots, raw decoded summaries, generation traces, and residual diagnosis. It does not copy raw logs, checkpoints, adapters, remote caches, private overrides, host details, SSH details, tokens, private paths, or private corpus rows into git.

## Validation

- `PYTHONPATH=src pytest -q tests/test_a100_sft_smoke.py::test_compact_query_exact_match_a100_rerun_configs_use_7b_and_stay_public_safe tests/test_a100_sft_smoke.py::test_compact_query_exact_match_a100_rerun_evidence_is_bounded_and_public_safe`: `2 passed`
- `PYTHONPATH=src pytest -q`: `197 passed`
- `uv run ruff check .`: passed
- `uv run mypy src`: passed
- `PYTHONPATH=src python -m voice2task.cli.data validate --sft data/public-samples/sft_public_sample.jsonl --dpo data/public-samples/dpo_public_sample.jsonl --manifest data/public-samples/manifest_public_sample.json --public`: `ok=true; sft_rows=18; dpo_pairs=46`
- `PYTHONPATH=src python -m voice2task.cli.data dpo-check --dpo data/public-samples/dpo_public_sample.jsonl`: `total_pairs=46`
- `PYTHONPATH=src python -m voice2task.cli.report leak-scan --paths reports/public-sample/a100-compact-query-exact-match-rerun docs/human-briefs/2026-06-13-run-a100-compact-query-exact-match-rerun.html configs/sft-a100-compact-query-exact-match-rerun.json configs/sft-a100-compact-query-exact-match-prediction.json --output reports/public-sample/a100-compact-query-exact-match-rerun/final_leak_scan_result.json`: `ok=true`
- `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`: `5 passed, 0 failed`
- `git diff --check`: passed
- Post-archive `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`: `4 passed, 0 failed`
- Post-archive focused evidence tests: `2 passed`
- Post-archive leak scan: `ok=true`
