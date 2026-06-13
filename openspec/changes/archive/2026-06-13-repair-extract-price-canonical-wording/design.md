## Context

The archived `repair-extract-price-contract-residual` phase showed that the current 7B SFT path can preserve compact-query rows and recover extract task/route shape on the public train split. The remaining extract-price failures are strict string/slot wording residuals:

- `seed-extract-price`: `slots.target` is correct, but `normalized_command` includes the extra particle `上的`.
- `seed-extract-price-aug-1`: the model emits generic `slots.target="价格"` and `normalized_command="页面价格"`.
- `seed-extract-price-aug-2`: the model emits `slots.target="标价"` and `normalized_command="提取页面标价"`.

This is not a schema problem, route problem, parser problem, or evaluator problem. It is a model-visible canonical target-writing problem.

## Goals / Non-Goals

**Goals:**

- Keep the phase narrow: canonical extract-price target wording only.
- Add explicit training-time and prediction-time policy text for the known public aliases.
- Add public-safe DPO hard negatives that contrast the canonical target with the strict-wrong aliases observed in A100 evidence.
- Run a bounded 7B A100 train-split rerun after local validation to test whether the policy improves strict exact match.
- Publish evidence that records either recovery or remaining residuals without overstating the result.

**Non-Goals:**

- Do not relax `contract_exact_match`, add semantic-equivalence scoring, normalize predictions, repair predictions, or replace predictions with gold/fixtures.
- Do not expand to private full corpus in this phase.
- Do not claim dev/test generalization, production readiness, checkpoint release, adapter release, live-browser benchmark improvement, or public full-corpus release.
- Do not change search compact-query behavior except to verify it remains preserved.

## Decisions

1. Add canonical wording as public extract policy, not evaluator logic.

   The correct place for this phase is the model-visible target policy and training data contrast. The evaluator remains strict so that a successful result means the model emitted the exact canonical contract.

2. Encode alias hard negatives as DPO categories, not extra SFT gold rows.

   The public SFT seed already has the canonical gold target across the original and two paraphrases. The missing signal is contrast against plausible wrong synonyms. Distinct DPO categories make the rejection reason auditable and keep slice summaries explicit.

3. Keep A100 evidence train-split and public-sample only.

   The purpose is to test whether the narrowed canonical wording residual is learnable by the 7B SFT path under controlled conditions. This still does not prove held-out generalization or production behavior.

## Risks / Trade-offs

- Canonical wording may overfit to the public aliases -> Mitigation: report train-split-only status and avoid private/generalization claims.
- Prompt wording may leak row-specific gold target into prediction prompts -> Mitigation: tests require prediction prompts not to include row-specific gold values unless already present in user input or generic policy text.
- Extra DPO categories may broaden pair counts and accidentally affect non-extract rows -> Mitigation: builder gates the new negatives to public-safe `extract`/`extract_page` rows with `slots.target="商品价格"`.
- A100 rerun may still fail strict exact match -> Mitigation: evidence pack records residual families honestly and recommends the next bounded step only if needed.
