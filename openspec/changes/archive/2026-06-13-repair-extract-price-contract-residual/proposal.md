## Why

The archived A100 7B train-split rerun recovered the compact public-readonly search/weather rows, but all three remaining train-split strict exact-match failures are in the public `extract-price` family. The failure is no longer data volume in the broad sense: it is a narrow contract-policy ambiguity where price-reading requests can drift into `search` outputs or use `slots.query`/`page_url` instead of the gold `extract_page` target slot.

This change opens a small follow-up phase to make the extract-price contract target explicit in data, prompts, DPO hard negatives, and public-safe evidence, then rerun the same bounded 7B A100 public-sample train diagnostic.

## What Changes

- Define the public extract-price/read-page policy: price extraction from the current page uses `task_type="extract"`, `route="extract_page"`, `safety.allow=true`, `safety.reason="public_readonly"`, `confirmation_required=false`, `slots.target="商品价格"`, and `normalized_command="提取页面商品价格"` for the current public sample target.
- Add extract-specific hard negatives that reject search fallback and query/page-url slot shapes for public extract-price rows.
- Make the SFT training and prediction prompts expose the extract-price policy without leaking row-specific gold targets into prediction prompts beyond values already present in the user input.
- Regenerate synchronized public-sample SFT, DPO, and manifest artifacts after the DPO policy change.
- Run a bounded 7B A100 SFT rerun on the committed public-sample train rows, export sanitized train-split predictions and sidecars, and evaluate strict metrics.
- Publish public-safe residual diagnosis, report, manifest, leak scan, and Chinese Human Brief showing whether `extract-price` reached strict exact match while compact-query stayed fixed.
- Do not run full private corpus training, DPO training, GRPO, dev/test generalization evaluation, production/live-browser benchmark evaluation, parser relaxation, semantic-equivalence scoring as a primary metric, evaluator repair, prediction replacement, checkpoint release, or adapter release.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `voice2task-dataset-preparation`: Add public extract-price canonical target policy and extract-specific hard-negative generation.
- `preference-contract-tuning`: Validate and summarize extract-search-fallback and extract-query-slot hard negatives.
- `supervised-contract-tuning`: Expose extract-price contract policy in SFT prompts and run the bounded 7B public-sample train rerun.
- `contract-evaluation`: Publish public-safe extract-price residual repair evidence and claim boundaries.

## Impact

- Affected systems: public sample builder, DPO validator/slicer, shared SFT prompt formatting, A100 public-sample rerun templates, public evidence under `reports/public-sample/`, and Human Brief under `docs/human-briefs/`.
- Affected code: `src/voice2task/dataset.py`, `src/voice2task/dpo.py`, `src/voice2task/formatting.py`, tests, and generated public-sample data artifacts.
- Affected validation: focused unit tests, public data validation, DPO pair check, full pytest/lint/type checks, strict OpenSpec validation, leak scan, and `git diff --check`.
- Remote execution: authorized A100 use under `<a100_project_root>` with GPU occupancy inspection and explicit `CUDA_VISIBLE_DEVICES`.
