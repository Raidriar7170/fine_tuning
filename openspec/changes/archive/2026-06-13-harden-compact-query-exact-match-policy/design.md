## Context

The compact-query exact-match residual diagnosis preserves strict source metrics: `json_valid_rate=1.0`, `slot_f1=0.6666666666666666`, and `contract_exact_match=0.0`. The remaining failures are field-level: two rows emit `normalized_command="搜索北京明天的天气"` while gold remains `搜索北京明天天气`, and one row still emits decomposed `city/date/topic` slots instead of compact `slots.query`.

The current prompt already exposes compact query slot and canonical `normalized_command` policies, but the residuals show the prompt can be made more explicit before another private-adapter rerun is justified.

## Goals / Non-Goals

**Goals:**

- Make the shared SFT/prediction prompt state that public-readonly search/weather `normalized_command` and `slots.query` should share the same compact query phrase.
- Make non-row-specific examples contrast accepted compact query output with rejected decomposed slots and particle-inserted `normalized_command` variants.
- Surface machine-readable prompt metadata for the strengthened policy.
- Keep expanded public seed fixtures, derived SFT/DPO artifacts, and DPO rejection validation internally consistent.
- Surface `slot_f1_soft` only as an internal diagnostic view that never changes strict `slot_f1` or `contract_exact_match`.
- Preserve local prediction smoke coverage while supporting real PEFT adapter merge/unload paths.
- Publish a local public-safe evidence pack and Human Brief derived from committed public artifacts and prompt rendering.

**Non-Goals:**

- No A100 execution, training, prediction rerun, model loading, or private adapter access.
- No parser relaxation, strict evaluator metric replacement, semantic-equivalence scoring, slot normalization, `normalized_command` normalization, prediction repair, prediction replacement, or re-score.
- No checkpoint release, adapter release, held-out generalization claim, production-readiness claim, public full-corpus release, model-quality improvement claim, model recovery claim, or live-browser benchmark improvement claim.
- No generic chat fine-tuning, skill routing, GUI action policy learning, first-phase GRPO, or public release of the full local corpus.

## Decisions

- **Prompt hardening is the only behavior change.** The phase changes model-visible target-format guidance and prompt metadata; it does not alter evaluation or historical predictions.
- **Strict metrics remain authoritative.** `slot_f1_soft` is allowed only as an internal diagnostic column; reports must keep `slot_f1` and `contract_exact_match` as the strict decision metrics.
- **Generated public sample artifacts move together.** If `seed_traces.jsonl` changes, `sft_public_sample.jsonl`, `dpo_public_sample.jsonl`, and `manifest_public_sample.json` must be regenerated in the same phase.
- **Adapter merge is capability-based.** Real PEFT adapters may expose `merge_and_unload`; local fake models in smoke tests must not be required to implement that PEFT-only method.
- **Examples remain non-row-specific.** Use generic examples such as `上海后天天气`, not the exact public train-row gold strings, to avoid leaking row-specific gold contracts into prediction prompts.
- **Strict metrics remain strict.** The evidence pack will state that future exact-match recovery still requires a real prediction to emit the exact target fields; this phase does not mark previous strings equivalent.
- **Evidence is local and public-safe.** Generate JSON/Markdown/manifest/leak-scan artifacts from prompt metadata, public sample checks, and links to the prior residual diagnosis.

## Risks / Trade-offs

- **Risk: Stronger prompt wording may still not change private-adapter behavior.** → Mitigation: label the phase as local prompt-policy hardening only and require a later real A100 rerun for behavioral evidence.
- **Risk: Examples could accidentally include row-specific gold targets.** → Mitigation: focused tests assert prediction prompts omit target-only row strings and use only non-row-specific examples.
- **Risk: Readers may confuse prompt policy with evaluator normalization.** → Mitigation: repeat explicit non-claims in the prompt metadata evidence, Markdown report, Human Brief, and OpenSpec artifacts.
- **Risk: Readers may confuse `slot_f1_soft` with strict recovery.** → Mitigation: label it internal diagnostic wherever surfaced and never use it to claim contract recovery.
