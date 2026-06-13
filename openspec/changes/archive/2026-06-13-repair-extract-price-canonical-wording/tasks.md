## 1. Local Canonical Wording Policy And Data

- [x] 1.1 Add failing tests for extract-price canonical wording prompt visibility, gold-boundary safety, and prompt constraint metadata.
- [x] 1.2 Add failing tests for extract-price canonical wording DPO hard negatives and validation failures.
- [x] 1.3 Implement canonical extract-price wording policy in formatting, schemas, dataset builder, and DPO validation.
- [x] 1.4 Regenerate `data/public-samples/sft_public_sample.jsonl`, `data/public-samples/dpo_public_sample.jsonl`, and `data/public-samples/manifest_public_sample.json`.

## 2. Local Validation And Configs

- [x] 2.1 Add public-safe 7B A100 SFT/prediction config templates for the canonical wording rerun.
- [x] 2.2 Run focused tests for formatting, dataset builder, DPO validation, public data validation, and DPO pair summaries.
- [x] 2.3 Run full local validation: `PYTHONPATH=src pytest -q`, `uv run ruff check .`, `uv run mypy src`, `openspec validate --all --strict`, public leak scan, and `git diff --check`.

## 3. A100 Execution And Evidence

- [x] 3.1 Inspect A100 GPU occupancy, choose a safe idle GPU, and set `CUDA_VISIBLE_DEVICES` explicitly.
- [x] 3.2 Sync only required public-safe repo files to the approved A100 project root and run bounded 7B SFT training.
- [x] 3.3 Export train-split predictions and sidecars, then copy back only sanitized public-safe evidence.
- [x] 3.4 Generate strict metrics, canonical wording residual diagnosis, manifest, report, leak scan, and concise Chinese Human Brief.

## 4. Review And Archive

- [x] 4.1 Perform a read-only diff/evidence review for Must Fix issues, fix in-scope issues, and rerun affected validation.
- [x] 4.2 Archive the OpenSpec change after successful validation and rerun post-archive validation.
