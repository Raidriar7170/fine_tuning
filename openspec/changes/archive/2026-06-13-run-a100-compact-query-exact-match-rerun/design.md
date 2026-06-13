## Context

The previous `harden-compact-query-exact-match-policy` phase was local-only. It synchronized the public sample, hardened the compact-query exact-match prompt/data policy, added `wrong_task_type` validation, and published public-safe evidence, but it intentionally did not train, rerun prediction, or claim model recovery.

The next question is narrow: after this hardening, can a small A100 public-sample SFT rerun reduce the strict exact-match residual family, especially `normalized_command` exact-string mismatches and decomposed `city/date/topic` slots for public-readonly search?

## Goals / Non-Goals

**Goals:**
- Run a bounded A100 SFT rerun against the current committed public sample and compact-query exact-match policy.
- Export sanitized trained-adapter predictions for the train split and evaluate strict contract metrics.
- Preserve raw model-output status and produce evidence that can answer whether the compact-query residual improved, stayed the same, or regressed.
- Keep all private runtime artifacts under the approved A100 project root and out of git.

**Non-Goals:**
- No full private corpus training, DPO, GRPO, generic chat fine-tuning, skill routing, GUI action policy learning, checkpoint release, adapter release, public full-corpus release, parser relaxation, strict evaluator relaxation, prediction repair, prediction replacement, semantic-equivalence scoring as a primary metric, dev/test generalization claim, production-readiness claim, or live-browser benchmark claim.

## Decisions

1. **Use current public sample only.**
   - Rationale: this phase tests whether the compact-query contract is learnable under a controlled, public-safe scope before spending more A100 time on private/full-corpus runs.
   - Alternative considered: use the 240-seed private normalized corpus. Rejected for this phase because it would mix public-policy validation with broad data-volume effects.

2. **Use Qwen2.5-7B for the diagnostic rerun.**
   - Rationale: the question is whether the earlier 7B training issue improves after compact-query hardening; 0.5B smoke templates are useful for fast plumbing checks but are not the deciding model for this phase.
   - Alternative considered: continue with `Qwen/Qwen2.5-0.5B-Instruct`. Rejected because it would answer a smaller smoke question and could not fairly validate the 7B training path.

3. **Train then predict, rather than prediction-only.**
   - Rationale: the archived hardening changed SFT-visible training policy and public targets; using an older adapter would not test whether the revised training signal helps.
   - Alternative considered: rerun prediction with the old adapter and new prediction prompt. Rejected because it would mostly test inference prompt sensitivity, not the training fix.

4. **Evaluate strict metrics first, soft diagnostics second.**
   - Rationale: `contract_exact_match`, strict `slot_f1`, and row-level residual families decide whether the phase worked. `slot_f1_soft` can help explain text similarity but must not become the success criterion.
   - Alternative considered: judge semantic equivalence with an LLM or soft string matching. Rejected as primary evidence for this strict-contract phase.

5. **Commit only sanitized evidence.**
   - Rationale: A100 outputs may contain private paths, runtime details, raw logs, adapters, caches, or checkpoints. The repo should only receive public-safe predictions, metrics, manifests, reports, leak scans, and Human Briefs.
   - Alternative considered: store raw remote logs locally for convenience. Rejected because committed artifacts must remain public-safe.

6. **Use explicit GPU selection and output-root policy.**
   - Rationale: remote GPU use has standing authorization only when occupancy is inspected, a safe GPU is chosen, `CUDA_VISIBLE_DEVICES` is explicit, and all writes stay under `<a100_project_root>`.

## Risks / Trade-offs

- **Risk: public-sample overfit succeeds but does not generalize.** -> Mitigation: label the phase as train-split/public-sample diagnostic evidence only and make no dev/test or production claim.
- **Risk: rerun still fails strict exact match.** -> Mitigation: preserve sanitized failure evidence and classify residuals without repairing, normalizing, or re-scoring outputs.
- **Risk: remote logs or paths leak into repo evidence.** -> Mitigation: use placeholders, leak scan every public-facing artifact, and keep raw runtime material out of git.
- **Risk: A100 environment or GPU occupancy blocks execution.** -> Mitigation: inspect `nvidia-smi`, use an idle GPU if safe, otherwise stop and record the blocker instead of interfering with other users.
- **Risk: training on 18 public SFT rows is too small.** -> Mitigation: interpret success/failure only as a controlled learnability signal, not as a final data-volume conclusion.

## Migration Plan

1. Prepare or reuse a repo-local public template and repo-external private override for the A100 run.
2. Inspect GPU occupancy on the A100 machine and select an idle GPU explicitly.
3. Run public-sample 7B SFT under the approved private project root.
4. Export sanitized train-split predictions and sidecars.
5. Pull back only public-safe evidence artifacts.
6. Run strict evaluation, residual diagnosis, leak scan, full local validation, and OpenSpec validation.
7. Generate a concise Chinese Human Brief and stop for review before archive.

## Open Questions

- None for proposal scope. Actual GPU availability and remote package state will be verified during apply.
