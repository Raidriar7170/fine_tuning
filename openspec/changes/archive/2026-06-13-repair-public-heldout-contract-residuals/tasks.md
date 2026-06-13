## 1. Local TDD And Public Data Repair

- [x] 1.1 Add failing dataset-builder tests for train-only repair exemplars and held-out split preservation.
- [x] 1.2 Add failing DPO validation tests for clarify action drift, blocked payment action drift, form confirmation drift, and navigate canonical URL drift.
- [x] 1.3 Add failing formatting tests for held-out residual repair prompt-policy visibility without held-out gold leakage.
- [x] 1.4 Implement the minimal dataset, DPO, and formatting changes required to pass those tests.
- [x] 1.5 Regenerate `data/public-samples/sft_public_sample.jsonl`, `dpo_public_sample.jsonl`, and `manifest_public_sample.json` from committed seeds.

## 2. Configs And Local Evidence

- [x] 2.1 Add public-safe A100 SFT rerun and split-specific train/dev/test prediction config templates for the repair phase.
- [x] 2.2 Add focused config/evidence boundary tests for the repair templates and future evidence manifest shape.
- [x] 2.3 Run focused tests, public data validate, DPO check, OpenSpec strict validation, leak scan, and `git diff --check`.

## 3. A100 Repair Rerun

- [x] 3.1 Inspect A100 GPU occupancy and verify remote writes stay under the approved private project root.
- [x] 3.2 Sync only required public-safe source/config/data files to the A100 project root.
- [x] 3.3 Run the repair SFT rerun on an explicitly selected idle GPU.
- [x] 3.4 Run split-specific prediction exports for train, dev, and test using the repair adapter.
- [x] 3.5 Copy back only sanitized predictions and sidecars.

## 4. Evidence And Human Brief

- [x] 4.1 Generate split-specific gold JSONL, strict metrics, schema diagnostics, alignment diagnostics, and constrained decoding diagnostics.
- [x] 4.2 Generate a combined repair diagnosis, manifest, report, leak scans, and concise Chinese Human Brief.
- [x] 4.3 Run full local validation: `PYTHONPATH=src pytest -q`, `uv run ruff check .`, `uv run mypy src`, public data validate, DPO check, OpenSpec strict, public leak scan, and `git diff --check`.

## 5. Review, Archive, And Integration

- [x] 5.1 Perform a read-only diff/evidence review for Must Fix issues and rerun affected validation.
- [x] 5.2 Archive the OpenSpec change after successful validation and rerun post-archive validation.
- [x] 5.3 Auto-stage and commit only in-scope phase files when guarded auto-integration remains safe.
