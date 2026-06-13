## Context

The current public sample manifest is `public-sample-20260613T072200Z`. The latest runtime-label provenance evidence shows that the 7B A100 tokenizer/collator path can inspect actual assistant-only labels for that manifest: prompt tokens are masked and assistant contract tokens carry loss. That evidence does not establish that the model can memorize current train rows.

Earlier tiny/train-split evidence is not enough for this question because some artifacts used an older manifest or 0.5B model. This phase therefore narrows the next action to a 7B, current-manifest, train-internal tiny-overfit probe.

## Goals / Non-Goals

**Goals:**
- Create public-safe 7B config templates for a current-manifest tiny-overfit training run and train-split prediction export.
- Execute or honestly block the A100 probe with all remote writes under the approved private project root.
- Publish sanitized public evidence that states whether 1-3 current train rows were used, whether prediction was train-only, and whether contract metrics improved on that tiny train slice.
- Keep runtime label provenance, tiny-overfit metrics, and held-out generalization as separate evidence layers.

**Non-Goals:**
- No DPO, GRPO, private-corpus training, or broad rerun.
- No dev/test or held-out generalization claim.
- No evaluator relaxation, prediction repair, schema coercion, or semantic-equivalence scoring.
- No checkpoint, adapter, full dataset, production-readiness, or live-browser benchmark release claim.

## Decisions

1. Use a dedicated current-manifest probe rather than reusing older train-split evidence.
   - Rationale: old evidence can be stale by manifest, model size, or objective path. The recommended next step explicitly asks for a fresh 1-3 row current-manifest probe.
   - Alternative considered: rerun the broader held-out repair. Rejected because it would spend A100 time before proving the model can memorize a tiny current slice.

2. Keep committed configs as templates with placeholders.
   - Rationale: public repo artifacts must not expose private A100 paths, host details, caches, raw logs, or SSH details.
   - Alternative considered: committing the private override. Rejected by repository privacy policy.

3. Publish sanitized evidence only after train and prediction artifacts exist.
   - Rationale: a completed training command alone is not evidence of contract learning. The evidence pack must include metrics and failure slices from prediction rows.
   - Alternative considered: reporting loss curves only. Rejected because loss is training telemetry, not the contract evaluation ladder.

4. Treat dependency or GPU unavailability as a bounded blocked result.
   - Rationale: the previous runtime-label check showed `datasets` and `trl` may be absent in the default remote environment. A blocked public-safe record is preferable to implying progress.
   - Alternative considered: silently changing environments or writing outside the approved root. Rejected by the A100 rules.

## Risks / Trade-offs

- Remote training dependencies are missing -> record the exact public-safe blocked status and do not claim tiny-overfit execution.
- GPU availability is unclear -> stop before launching and keep the phase blocked rather than interfering with other users.
- Tiny train recovery succeeds but held-out remains unknown -> report only train-internal memorization and open a separate held-out phase later.
- Tiny train recovery fails -> treat this as a learning/objective/decoding diagnosis result, not as proof that more data alone will fix the issue.
