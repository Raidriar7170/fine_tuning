## Context

The archived scaled-sample design records the current public boundary as
`102` seed rows / `261` SFT rows / `881` DPO pairs and recommends a later
materialization phase for a `240` seed milestone. The current public sample is
imbalanced: `form_fill` already has `42` seeds, while `search`, `extract`, and
`clarify` are much smaller. The latest model evidence is a partial strict signal
with stable JSON, recovered safety recall, but weak strict exact match.

This phase turns the design into public-safe standalone candidate artifacts.
It deliberately does not merge the candidates into the formal public sample and
does not run model training or prediction.

## Goals / Non-Goals

**Goals:**

- Materialize a deterministic candidate seed set aligned with the archived
  scaled-sample target:
  - `118` core-family candidates to close the current core-family gaps toward
    the `220` core target.
  - `20` confirmation-boundary overlay candidates.
  - `138` total candidate seed rows, so a later merge could move from `102`
    formal seeds to the `240` seed milestone.
- Generate SFT candidate sidecars and machine/human-readable materialization
  evidence.
- Record family targets, current counts, candidate counts, split counts,
  augmentation-depth guidance, and claim boundaries.
- Add tests and CLI coverage so the materialization is reproducible and cannot
  overwrite the formal public sample files by accident.

**Non-Goals:**

- No formal public sample merge in this phase.
- No rebuild of `seed_traces.jsonl`, `sft_public_sample.jsonl`,
  `dpo_public_sample.jsonl`, or `manifest_public_sample.json`.
- No DPO pair generation for the new candidates.
- No A100 training, prediction, prompt change, evaluator change, slot
  normalization, prediction repair, checkpoint/adapter release, production
  readiness claim, or live-browser benchmark claim.
- No generic chat fine-tuning, skill routing, GUI action policy learning,
  first-phase GRPO, or public full local/private corpus release.

## Decisions

1. **Use deterministic templates rather than an LLM batch.**

   Rationale: this phase must be reviewable and reproducible inside git. The
   current scope is public-safe candidate generation, not private corpus
   expansion. Deterministic templates also keep slot values invariant across
   augmentations.

   Alternative considered: call an LLM to generate additional spoken variants.
   Rejected because it would introduce non-determinism and require separate
   review and provenance gates.

2. **Keep candidates standalone.**

   Rationale: the archived design says materialize candidates after review, but
   the next formal public manifest boundary should be created by a later merge
   phase. Standalone candidates allow tests, leak scans, and human review
   without changing the formal evaluation boundary.

   Alternative considered: directly merge to the formal sample and rebuild
   SFT/DPO. Rejected for this phase because it would change the comparison
   boundary and make the materialization harder to review.

3. **Use `118` core candidates plus `20` overlay candidates.**

   Rationale: current core counts are `102` seeds. The design target is `220`
   core seeds plus `20` confirmation-boundary overlay seeds. The core deltas are
   search `20`, navigation `17`, form_fill `3`, extract `25`, clarify `33`, and
   blocked_payment `20`, totaling `118`. Adding the overlay `20` yields `138`
   standalone candidate seeds.

4. **Keep confirmation-boundary overlay separate from core-family counts.**

   Rationale: overlay examples contrast otherwise similar requests by
   confirmation marker; they help diagnose confirmation preservation but should
   not distort task-family target accounting.

## Risks / Trade-offs

- **[Risk] Template candidates may be less diverse than LLM candidates.** →
  Mitigation: use multiple families and augmentation variants per seed, and
  record this as candidate evidence rather than final model-quality evidence.
- **[Risk] Reviewers may confuse candidate materialization with a formal sample
  merge.** → Mitigation: candidate status, manifest, report, and Human Brief
  explicitly say standalone-only and no formal public sample mutation.
- **[Risk] The next phase could overclaim model improvement from data-only
  artifacts.** → Mitigation: reports state that no training/prediction happened
  and that strict `contract_exact_match` / strict `slot_f1` remain the headline
  metrics for later evaluation.
- **[Risk] The `240` milestone could be misread as current formal sample size.**
  → Mitigation: evidence records current counts, candidate counts, and the
  later-merge interpretation separately.
