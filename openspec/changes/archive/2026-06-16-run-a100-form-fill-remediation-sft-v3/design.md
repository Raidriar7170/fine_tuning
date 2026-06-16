## Context

The current public-facing baseline is
`reports/public-sample/a100-formal-public-heldout-prediction-after-a100-recovery/`
on manifest `public-sample-20260616T074315Z`. It is a prediction-only partial
signal: dev/test `contract_exact_match` is 0.3043 / 0.2899, strict `slot_f1` is
0.3913 / 0.5072, and `json_valid_rate` is 1.0000. The selected residual target
is `form_fill`, and the readiness phase proved that the current train split has
114 rows including 21 merged `form_fill` remediation / confirmation-marker
rows.

This phase is the first phase that may actually train a private A100 SFT v3
adapter after that readiness evidence. It must keep public and private
boundaries crisp: committed files can describe configs, metadata, aggregate
metrics, and sanitized evidence; private overrides, checkpoints, adapters,
logs, caches, and remote paths stay outside git.

## Goals / Non-Goals

**Goals:**

- Perform a fresh A100 GPU safety preflight and pick a safe idle GPU.
- Create a repo-external private override from the committed public-safe config
  templates.
- Run one SFT v3 training job on the current public train split.
- Run dev/test prediction-only evaluation with the resulting private adapter.
- Import only sanitized evidence and keep strict metrics as authoritative.
- Update `CONTEXT.md`, `reports/final_status.md`, and a concise Human Brief
  with the observed result and limitations.

**Non-Goals:**

- No DPO, GRPO, skill routing, generic chat fine-tuning, GUI action policy
  learning, or full private corpus training.
- No evaluator relaxation, semantic-equivalence scoring, prediction repair,
  prediction replacement, slot normalization, or re-scoring.
- No public release of checkpoint, adapter, model cache, raw logs, private
  override, private path, or full local/private corpus.
- No production-readiness or live-browser benchmark claim.

## Decisions

1. Use the committed readiness config templates as public contracts, and create
   the resolved private override only on A100 under the approved private root.
   This keeps reviewable intent in git without leaking runtime paths.

2. Train only on the current public train split selected by
   `public-sample-20260616T074315Z`. This makes the phase a clean test of the
   merged `form_fill` remediation rows instead of a broader data expansion.

3. Evaluate only dev/test with the existing strict evaluator. Train-split
   diagnostics, DPO, and prompt-policy changes remain separate phases if needed.

4. Treat improvement as observed evidence only when it appears in strict
   `contract_exact_match`, strict `slot_f1`, route/task-type, safety, or
   confirmation metrics. `slot_f1_soft` may appear in reports only as
   diagnostic context.

5. If GPU placement is unsafe, private override creation is ambiguous, training
   fails, or prediction/evaluation fails, stop with a blocked evidence pack
   instead of fabricating or substituting outputs.

## Risks / Trade-offs

- A100 GPU occupancy may be unclear -> stop rather than preempt or risk another
  user's workload.
- The 21 train rows may be too small to move held-out metrics -> report the
  result as observed partial/no recovery, not as failure of the entire project.
- Training can regress non-`form_fill` families -> compare full dev/test ladder
  and residual families, not just confirmation accuracy.
- Private paths may leak through metadata -> sanitize imported metadata and run
  leak scan before commit.
- A single SFT v3 run may be noisy -> avoid overclaiming and preserve configs
  and metadata for later reproducibility.
