## Context

The current public manifest is `public-sample-20260616T074315Z`. The archived
blocked-payment repair candidate design identified two reviewed repair families:
`refund_confirmation_or_processing` and
`subscription_charge_confirmation`. Those records are not seed rows yet and
cannot affect public sample validation, SFT rows, DPO pairs, or later held-out
evaluation until materialized.

This phase is the bridge between design evidence and data evidence. It
materializes only public-safe candidate seed rows and rebuilds public derived
artifacts. It remains separate from model training, prediction, and quality
claims.

## Goals / Non-Goals

**Goals:**

- Convert the reviewed blocked-payment repair candidates into public-safe seed
  trace rows with `blocked/deny` contracts and `unsafe_payment` safety labels.
- Rebuild public sample derived artifacts from the updated seed traces.
- Publish materialization evidence with candidate provenance, pre/post row
  counts, validation status, DPO family counts, and no-claim boundaries.
- Update `CONTEXT.md`, `reports/final_status.md`, and a concise Human Brief so
  the next phase can decide whether to run a bounded training/evaluation retry.

**Non-Goals:**

- No SFT, DPO, GRPO, A100 execution, prediction generation, evaluator
  relaxation, semantic-equivalence scoring, prediction repair, prompt change,
  checkpoint/adapter release, production-readiness claim, public full-corpus
  release, generic chat fine-tuning, skill routing, GUI action policy learning,
  or live-browser benchmark claim.

## Decisions

1. **Materialize from archived candidate design, not from ad hoc rows.**
   - Rationale: candidate provenance remains traceable to the safety regression
     diagnosis and reviewed design evidence.
   - Alternative considered: manually editing public seed rows from memory.
     Rejected because it weakens reproducibility and reviewer traceability.

2. **One materialized seed per repair family, with augmentations carrying the
   reviewed templates.**
   - Rationale: this preserves compact public-sample growth while still covering
     the observed refund and subscription-charge patterns.
   - Alternative considered: one seed row per source row. Rejected for this
     phase because it would overfit the public sample to four residual ids and
     make candidate counts harder to review.

3. **Regenerate derived public artifacts immediately after seed mutation.**
   - Rationale: `seed_traces.jsonl`, SFT rows, DPO pairs, and manifest must stay
     synchronized; stale derived files previously caused review failures.
   - Alternative considered: commit seed rows only and defer rebuild. Rejected
     because it leaves the repository inconsistent.

4. **Keep model-quality claims blocked until a later held-out evaluation.**
   - Rationale: materialization changes data artifacts, not model behavior.
   - Alternative considered: treating data coverage as safety improvement.
     Rejected because no prediction or strict held-out evidence is produced in
     this phase.

## Risks / Trade-offs

- [Risk] Materialized templates may be too close to residual wording.
  → Mitigation: include provenance and public-safe template lists, and defer
  model-quality claims until later held-out evaluation.
- [Risk] Public sample DPO pair counts may change unexpectedly.
  → Mitigation: run public data validation and DPO family count checks before
  archive.
- [Risk] Seed rows could imply payment action execution instead of blocking.
  → Mitigation: require `blocked/deny`, `safety.allow=false`,
  `safety.reason=unsafe_payment`, and `confirmation_required=false` in tests and
  evidence.
