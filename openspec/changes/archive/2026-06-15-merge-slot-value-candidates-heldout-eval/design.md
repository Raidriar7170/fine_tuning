## Context

The current formal public sample contains 10 seed rows, 30 SFT rows, and 90 DPO
pairs. A separate slot value candidate dataset contains 4 train seed rows and 12
SFT rows that target the remaining `normalized_command` and `slots` value
drift buckets. The observed A100 candidate probe reached train-split exact
match 1.0 on those 12 rows, but it was intentionally not held-out evidence.

This phase is the approved transition from candidate-only learnability to
formal public sample evaluation. It must preserve existing public `dev` and
`test` rows and evaluate the newly trained adapter on those held-out splits.

## Goals / Non-Goals

**Goals:**

- Merge the reviewed candidate seed rows into the formal public sample as
  train-only public rows.
- Regenerate formal SFT and DPO artifacts from the seed file.
- Produce A100 7B SFT and train/dev/test prediction templates for the merged
  manifest.
- Run the A100 job when GPU placement and private workspace rules are safe.
- Publish sanitized evidence that reports train learnability and dev/test
  strict exact separately.

**Non-Goals:**

- No evaluator relaxation, prediction repair, semantic-equivalence scoring, or
  soft slot F1 promotion.
- No DPO, GRPO, generic chat fine-tuning, skill routing, or GUI action policy
  learning.
- No public release of adapters, checkpoints, raw logs, private overrides,
  private paths, host details, or the full local/private corpus.
- No production-readiness, private-corpus generalization, or live-browser
  benchmark claim.

## Decisions

1. Reuse the current candidate seed definitions instead of hand-copying JSON.
   This keeps provenance, reviewed case-group IDs, and public safety validation
   tied to the materialized candidate design.

2. Add candidates as train-only formal public seeds. Existing public `dev` and
   `test` rows remain unchanged so held-out comparison stays meaningful.

3. Regenerate DPO pairs through the existing hard-negative builder. This keeps
   `wrong_task_type` and residual-specific hard negatives in the same code path
   as all other public sample rows.

4. Use new A100 config names for the merged-candidate phase instead of reusing
   candidate-only or targeted-family configs. The new configs point at
   `manifest_public_sample.json`, not the standalone candidate manifest.

5. Interpret metrics with split boundaries: train exact match is learnability;
   dev/test `contract_exact_match` is the primary held-out signal.

## Risks / Trade-offs

- [Risk] Candidate rows may improve train exact but not held-out strict exact.
  -> Mitigation: publish dev/test metrics separately and avoid recovery claims
  unless strict held-out evidence supports them.
- [Risk] Formal sample count changes can desync derived files.
  -> Mitigation: rebuild SFT/DPO/manifest from seed and add committed count
  tests plus CLI validation.
- [Risk] A100 run may be blocked by SSH, GPU occupancy, dependencies, or output
  placement.
  -> Mitigation: preflight read-only first, use only the approved remote root,
  and record a public-safe blocked status if execution is unsafe.
- [Risk] Public evidence can leak private runtime context.
  -> Mitigation: only import sanitized metadata/metrics, use placeholders, run
  leak scan, and keep raw remote artifacts under private/ignored paths.
