## Context

The prior `repair-public-heldout-contract-residuals` phase added public train repair exemplars and prompt/DPO reinforcement, then ran a 7B SFT-only A100 rerun. The result was negative: train repair rows were only partially memorized and public `dev/test` strict contract exact match remained zero. That makes another broad data expansion or heavy rerun premature.

The repository already has local evidence concepts for SFT target-template alignment and label provenance. This change narrows those ideas to the current failure: whether committed public SFT rows render an assistant contract target with enough target-token signal, and whether true runtime labels are available or still an evidence gap.

## Goals / Non-Goals

**Goals:**

- Diagnose public SFT contract-learning signal without downloading models, loading private adapters, or starting heavy training by default.
- Inspect public SFT rows by split and task family, rendered prompt/assistant target spans, target token/character pressure, prompt budget pressure, and prior negative repair metrics.
- Distinguish structural assistant-target evidence from true runtime label-mask evidence.
- Produce public-safe JSON/Markdown evidence, leak scans, and a concise Chinese Human Brief.
- Recommend the next bounded phase based on evidence: runtime label inspection, tiny overfit, DPO, or data work.

**Non-Goals:**

- Do not train, run prediction, or run private full-corpus evaluation in this phase.
- Do not repair, normalize, coerce, replace, or re-score predictions.
- Do not relax evaluator strict exact-match behavior.
- Do not claim model recovery, private-corpus generalization, checkpoint release, adapter release, production readiness, public full-corpus release, or live-browser benchmark improvement.
- Do not introduce generic chat fine-tuning, skill routing, GUI action policy learning, or first-phase GRPO.

## Decisions

1. Use local deterministic inspection first.

   The failure is visible in committed public artifacts, so the first diagnostic should be local and reproducible. It can inspect formatting, target spans, manifest counts, and existing evidence without relying on A100 availability.

2. Treat true label-mask evidence as unavailable unless real runtime labels are inspected.

   A deterministic rendered prompt can prove that the assistant target exists in the training text. It cannot prove that the TRL/tokenizer/collator path actually labels the same target tokens. The evidence pack must keep these separate.

3. Summarize token pressure with local tokenizer-independent approximations.

   Local validation should avoid model downloads. Character counts and JSON key/value counts are enough to identify obvious target-signal dilution and max-sequence risk, while marking tokenizer-specific token counts as unavailable.

4. Link prior negative repair evidence instead of mutating it.

   The new report should reference `reports/public-sample/repair-public-heldout-contract-residuals/` and compare its metrics, but it must not rewrite prior predictions or metrics.

## Risks / Trade-offs

- [Risk] Local character-pressure summaries are not tokenizer-level proof. -> Mitigation: label them as approximate and recommend runtime label inspection if needed.
- [Risk] The diagnostic could be mistaken for model recovery. -> Mitigation: encode explicit non-claims in JSON, Markdown, tests, and Human Brief.
- [Risk] Evidence stays inconclusive. -> Mitigation: make the next-stage recommendation precise: a tiny runtime label/overfit phase, not a broad rerun.
- [Risk] Public rows are too small for statistical claims. -> Mitigation: report counts and use the evidence only to decide the next debugging step.
