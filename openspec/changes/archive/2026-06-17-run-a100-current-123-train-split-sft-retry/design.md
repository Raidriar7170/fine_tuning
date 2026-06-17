## Context

The public sample now points at `public-sample-20260617T045941Z` with 102 seeds, 261 SFT rows, 881 DPO pairs, and a 123-row train split. The latest model-quality evidence is still bound to `public-sample-20260616T165835Z`; the current-123 readiness pack only proves that the new train split and configs are ready for a bounded retry. This phase is the first model run that may produce current-manifest model evidence for the new boundary.

## Goals / Non-Goals

**Goals:**

- Train one private A100 LoRA SFT adapter on the 123-row train split for `public-sample-20260617T045941Z`.
- Run strict dev/test prediction evaluation with that paired adapter and the existing evaluator.
- Publish sanitized evidence under a manifest-specific report directory, including strict metrics, manifests, sidecars, blocked/failure evidence if needed, and a Human Brief.
- Keep strict `contract_exact_match`, strict `slot_f1`, safety recall, route accuracy, confirmation accuracy, and JSON validity visible; keep `slot_f1_soft` diagnostic-only.

**Non-Goals:**

- No DPO, GRPO, prompt changes, evaluator relaxation, slot normalization, prediction repair, prediction replacement, or public sample mutation.
- No checkpoint, adapter, raw log, private override, private path, GPU UUID, SSH detail, token, cache, private corpus row, or full local corpus publication.
- No production-readiness, live-browser benchmark, released-model, or private-corpus generalization claim.
- No generic chat fine-tuning, skill routing, or GUI action policy learning.

## Decisions

1. **Use a new current-123 evidence directory.** Evidence will be written under `reports/public-sample/a100-current-123-train-split-sft-retry/` rather than reusing the prior `a100-current-train-split-sft-retry/` directory. This keeps the manifest boundary visible and prevents stale metric comparisons.

2. **Use the existing config templates with private overrides.** The committed configs already target `public-sample-20260617T045941Z` and require `<a100_project_root>` resolution outside git. The remote run should create private override files under the approved A100 project root and keep repo commits limited to sanitized summaries.

3. **Run fresh A100 preflight before training.** The phase must inspect SSH/connectivity, `nvidia-smi`, disk/cache/temp roots, dependency availability, manifest counts, and readiness evidence before launching training. If GPU placement is unsafe or ambiguous, the phase records blocked evidence instead of launching.

4. **Treat dev/test strict metrics as current-manifest evidence only after paired training.** Prediction configs are valid only when their adapter path points to the new adapter trained for `public-sample-20260617T045941Z`. Prior adapter metrics remain context, not current evidence.

## Risks / Trade-offs

- **Small train split may overfit.** Mitigation: label results as a bounded SFT retry, report train split size, and avoid production or generalization claims.
- **Safety and confirmation may trade off again.** Mitigation: publish both strict metrics and row-level residual summaries; recommend diagnosis rather than another immediate training loop if trade-offs appear.
- **A100 resources may be unavailable.** Mitigation: stop with blocked evidence if no safe idle GPU exists or if dependency/preflight checks fail.
- **Private runtime leakage risk.** Mitigation: use public-safe placeholders, leak scan committed artifacts, and keep private overrides/raw logs/adapters/checkpoints outside git.
