## Context

The current public sample boundary is `public-sample-20260617T045941Z` after current-retry confirmation-preservation materialization. The latest model evidence remains bound to `public-sample-20260616T165835Z`, where the private current-train-split SFT retry trained on 118 rows and showed a mixed partial signal: safety recovered, but confirmation and exact-match trade-offs remained.

The next safe step is not another training run by default. The repository first needs a public-safe readiness-only evidence pack confirming that the 123-row train split, SFT retry config, prediction config templates, and latest baseline references are internally consistent.

## Goals / Non-Goals

**Goals:**

- Generate current-123-row readiness evidence for `public-sample-20260617T045941Z`.
- Confirm the dry-run selects all 123 train rows.
- Record representation of prior form-fill repair rows, blocked-payment repair rows, and new current-retry confirmation-preservation rows.
- Preserve comparison boundaries: latest model metrics remain bound to the prior manifest until a later bounded training/evaluation phase runs.
- Produce a concise Human Brief and refresh status surfaces.

**Non-Goals:**

- No A100 training, DPO, GRPO, or prediction generation.
- No prompt change, evaluator metric change, slot normalization, prediction repair, or semantic-equivalence scoring.
- No checkpoint, adapter, raw log, private override, private corpus, or cache release.
- No production-readiness, held-out recovery, model-quality improvement, safety improvement, or live-browser benchmark claim.

## Decisions

1. Use readiness-only evidence before A100 retry.
   - Rationale: the manifest changed through train-only materialization, so a readiness pass can catch config/manifest drift before launching GPU work.
   - Alternative considered: run A100 SFT immediately. Rejected because it would skip the explicit boundary check and make failures harder to interpret.

2. Reuse existing dry-run SFT and readiness report paths.
   - Rationale: `run_sft(..., dry_run=True)` already validates manifest/config alignment without touching A100 resources.
   - Alternative considered: create a new readiness implementation. Rejected unless validation reveals a metadata gap.

3. Keep a separate evidence directory for this manifest boundary.
   - Rationale: the previous readiness pack is bound to a 118-row train split and should remain historical evidence.
   - Alternative considered: overwrite the prior readiness pack. Rejected because it would blur comparison boundaries.

## Risks / Trade-offs

- [Risk] The existing readiness report may not explicitly count the new current-retry rows. -> Mitigation: add focused evidence/test coverage if the dry-run metadata does not expose enough row-family detail.
- [Risk] Readiness evidence could be mistaken for model improvement. -> Mitigation: repeat no-training/no-prediction/non-claim boundaries in the report, Human Brief, and status docs.
- [Risk] Existing prediction configs may imply an adapter already trained for the new manifest. -> Mitigation: record that the configs require a later paired training phase before prediction-only evaluation can be interpreted as current-manifest model evidence.
