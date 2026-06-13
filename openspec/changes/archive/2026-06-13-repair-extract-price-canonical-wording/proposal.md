## Why

The prior 7B A100 extract-price rerun recovered the `extract`/`extract_page` task and route shape, but all three extract-price train rows still failed strict exact match because the model emitted wording variants such as `页面价格`, `标价`, or `提取页面上的商品价格` instead of the canonical gold target.

This phase is needed now because the residual has narrowed from broad schema/route behavior to a small canonical wording failure, and fixing it should stay separate from private-corpus scale-up, evaluator relaxation, or production-readiness claims.

## What Changes

- Add public extract-price canonical wording policy for the known train aliases: `多少钱`, `标价`, and `页面上的商品价格` all map to `slots.target="商品价格"` and `normalized_command="提取页面商品价格"`.
- Add DPO hard negatives that reject plausible but strict-wrong extract target wording, including generic `价格`, `标价`, and extra-particle normalized-command variants.
- Expose the canonical wording policy in SFT training and prediction prompts without including row-specific gold contracts in prediction prompts.
- Prepare and run a bounded 7B A100 public-sample train-split rerun only after local validation passes.
- Publish public-safe evidence that reports strict extract-price exact-match recovery or remaining residuals without claiming held-out generalization, checkpoint release, adapter release, live-browser improvement, or production readiness.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `voice2task-dataset-preparation`: add extract-price canonical wording hard negatives and public-sample target checks.
- `preference-contract-tuning`: validate extract-price canonical wording hard-negative categories and slice summaries.
- `supervised-contract-tuning`: expose extract-price canonical wording policy in prompts and support a bounded 7B A100 rerun for this residual.
- `contract-evaluation`: publish bounded evidence for the canonical wording rerun and preserve strict evaluator semantics.

## Impact

- Affected code: `src/voice2task/dataset.py`, `src/voice2task/dpo.py`, `src/voice2task/formatting.py`, `src/voice2task/schemas.py`, and evidence/reporting helpers as needed.
- Affected public artifacts: `data/public-samples/*`, A100 config templates, `reports/public-sample/a100-extract-price-canonical-wording-rerun/`, and a concise Chinese Human Brief.
- Affected tests: dataset builder, DPO validation, prompt-formatting tests, evidence-boundary tests, and focused regression tests for extract-price strict canonical wording.
- Non-goals: generic chat fine-tuning, skill routing, GUI action policy learning, first-phase GRPO, evaluator normalization, semantic-equivalence scoring, prediction repair/replacement, public release of full private corpus, released checkpoint/adapter claims, and live-browser benchmark claims.
