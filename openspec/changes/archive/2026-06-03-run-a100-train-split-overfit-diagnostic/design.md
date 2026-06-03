## Context

The repository already contains public-safe preparation for a train-split overfit diagnostic: a committed config template, objective inspection surface, prompt snapshot, sanitized raw decoded summary, generation trace, manifest/report fields, and fixture-mode evidence. The previous loop stopped before real A100 execution because that step requires private infrastructure, private override resolution, idle GPU selection, and careful sanitized artifact return.

This change is the execution phase. It uses the prepared diagnostic surfaces to run a real private A100 adapter prediction on train-internal rows and then imports only public-safe evidence back into the repository.

## Goals / Non-Goals

**Goals:**

- Run the real A100 train-split overfit diagnostic under the approved private project root.
- Use a repo-external private override that resolves the adapter and A100 project paths without committing private details.
- Capture objective inspection, prompt snapshot, sanitized raw decoded summary, generation trace, predictions, metrics, manifest, report, and leak-scan evidence.
- Preserve raw model failures honestly; do not repair, coerce, replace, or normalize invalid model outputs into valid contracts.
- Keep train-internal interpretation bounded with `overfit_diagnostic=true` and `generalization_claim=false`.

**Non-Goals:**

- No training-stack rewrite, TRL migration, DPO run, GRPO/rule reward stage, or hyperparameter search.
- No full private-corpus training or held-out dev/test generalization claim.
- No checkpoint release, adapter release, production-readiness claim, or live-browser benchmark improvement claim.
- No public commit of private overrides, raw logs, host details, SSH details, private paths, tokens, caches, checkpoints, adapters, or private corpus rows.

## Decisions

1. **Run diagnostic prediction rather than changing the training implementation first.**
   - Rationale: the last phase already prepared evidence sidecars. A real diagnostic can show whether train-internal recovery occurs before a larger training-stack change.
   - Alternative considered: immediately rewrite SFT loss masking. That may be a later phase, but it would change training architecture before collecting the prepared evidence.

2. **Use a private override outside git.**
   - Rationale: committed configs intentionally keep `<a100_project_root>` and adapter paths unresolved. The private override is the only safe place for real remote paths.
   - Alternative considered: edit committed config templates with resolved paths. That would violate the public/private artifact boundary.

3. **Return only sanitized evidence artifacts.**
   - Rationale: the repository needs reviewer-readable evidence, not remote runtime internals. Predictions, bounded sidecars, aggregate metrics, manifest, report, and leak-scan results are sufficient for the public evidence contract.
   - Alternative considered: copy raw decoded logs or training logs. That increases leak risk and is explicitly out of scope.

4. **Treat train-split results as diagnostic even if they pass.**
   - Rationale: the train split is small and train-internal. A pass can indicate recovery on memorized/in-scope examples only.
   - Alternative considered: combine diagnostic pass with quality claims. That would overstate the evidence.

## Risks / Trade-offs

- [Risk] Remote dependencies or private adapter paths may be unavailable -> Mitigation: stop with a clear blocked status and do not fabricate fixture evidence.
- [Risk] No idle A100 GPU is available -> Mitigation: stop rather than interrupting other users' processes.
- [Risk] Sanitization removes useful debugging detail -> Mitigation: keep bounded prompt/raw decoded/generation sidecars while leaving raw logs private.
- [Risk] A train-split pass is overclaimed -> Mitigation: enforce `generalization_claim=false`, explicit report boundaries, and leak/claim review before archive.
- [Risk] Model outputs still fail schema -> Mitigation: preserve failures as the result and use the evidence to scope a later fix, not to replace predictions.
