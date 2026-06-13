## 1. Local Policy And Data Repair

- [x] 1.1 Add focused tests for public extract-price canonical targets, extract search-fallback hard negatives, and extract query/page-url slot hard negatives.
- [x] 1.2 Implement extract-price canonical policy and extract-specific DPO hard-negative generation in the public dataset builder.
- [x] 1.3 Add DPO validation and slice-summary support for extract search-fallback and extract query-slot hard-negative categories.
- [x] 1.4 Regenerate `data/public-samples/sft_public_sample.jsonl`, `data/public-samples/dpo_public_sample.jsonl`, and `data/public-samples/manifest_public_sample.json`.

## 2. Prompt And Config Preparation

- [x] 2.1 Add focused tests for extract-page prompt-policy visibility and prediction prompt gold-target boundaries.
- [x] 2.2 Expose public extract-price contract policy and prompt constraint metadata in shared SFT formatting.
- [x] 2.3 Add public-safe 7B A100 rerun and prediction config templates for the extract-price residual phase.

## 3. A100 Execution And Evidence

- [x] 3.1 Inspect A100 GPU occupancy, choose a safe idle GPU, and set `CUDA_VISIBLE_DEVICES` explicitly.
- [x] 3.2 Sync only required public-safe repo files to the approved A100 project root and run bounded 7B SFT training.
- [x] 3.3 Export train-split predictions and sidecars, then copy back only sanitized public-safe evidence.
- [x] 3.4 Generate strict metrics, extract-price residual diagnosis, manifest, report, leak scan, and concise Chinese Human Brief.

## 4. Validation, Review, And Archive

- [x] 4.1 Run focused tests, full `PYTHONPATH=src pytest -q`, `uv run ruff check .`, `uv run mypy src`, public data validation, DPO pair check, OpenSpec strict validation, leak scan, and `git diff --check`.
- [x] 4.2 Perform a read-only diff review for Must Fix issues, fix in-scope issues, and rerun affected validation.
- [x] 4.3 Archive the OpenSpec change after successful validation and rerun post-archive validation.
