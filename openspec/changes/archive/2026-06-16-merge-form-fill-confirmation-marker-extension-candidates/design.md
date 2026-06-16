## Context

The archived `materialize-form-fill-confirmation-marker-extension-candidates` phase created 12 standalone candidate seed rows. The archived `check-form-fill-confirmation-marker-extension-candidate-integration` phase then proved those rows can be appended to the current formal public seed file and built through the public dataset builder in a report-scoped preview:

- Formal current counts: 86 seeds / 240 SFT rows / 742 DPO pairs.
- Preview counts after appending the 12 candidates: 98 seeds / 252 SFT rows / 850 DPO pairs.
- Preview split counts: train 114 / dev 69 / test 69.
- Candidate contribution: 12 seed rows / 12 SFT rows / 108 DPO pairs.

This phase turns the preview-compatible candidate extension into a formal public-sample update.

## Goals / Non-Goals

**Goals:**

- Validate the 12 candidate seed rows before merge.
- Append the candidate rows to `data/public-samples/seed_traces.jsonl` exactly once.
- Rebuild `sft_public_sample.jsonl`, `dpo_public_sample.jsonl`, and `manifest_public_sample.json` from the updated formal seed file.
- Publish merge evidence with pre/post counts, split counts, candidate contribution counts, formal validation status, and no-recovery claim boundaries.
- Preserve public-safe provenance and fail closed if candidate IDs already exist, candidate rows are unreviewed, or formal artifacts do not validate.

**Non-Goals:**

- No training, prediction, A100 execution, prompt change, evaluator relaxation, checkpoint release, adapter release, production-readiness claim, private-corpus generalization claim, public full-corpus release, or live-browser benchmark improvement claim.
- No changes to held-out evaluation metrics or model-quality claims.
- No merge of unrelated candidate files.

## Decisions

- Reuse the candidate validation and preview evidence from the archived preview phase.
  - Rationale: the candidate file has already passed materialization and preview integration checks.
  - Alternative considered: re-derive candidates from coverage design. Rejected because this phase should merge reviewed artifacts, not regenerate design choices.

- Rebuild formal derived artifacts immediately after seed merge.
  - Rationale: the repository requires public sample seed, SFT, DPO, and manifest synchronization after seed changes.
  - Alternative considered: commit only the updated seed file and ask reviewers to rebuild derived files locally. Rejected because it would violate the public sample synchronization requirement.

- Publish merge evidence in a separate report directory.
  - Rationale: merge evidence should distinguish formal post-merge counts from prior preview counts.
  - Alternative considered: overwrite preview evidence. Rejected because preview evidence is a separate archived phase.

- Treat generated DPO pairs as public dataset construction evidence only.
  - Rationale: formal public DPO rows support reproducible data inspection and smoke validation, but they are not DPO training evidence or model-quality evidence.

## Risks / Trade-offs

- [Risk] Formal merge counts could be mistaken for training or model recovery evidence. -> Mitigation: report and Human Brief must explicitly state no training, prediction, A100, evaluator, held-out recovery, or model recovery claim.
- [Risk] Candidate rows could be merged twice. -> Mitigation: merge command must fail if candidate IDs already exist in the formal seed file.
- [Risk] Derived public artifacts could drift from seed rows. -> Mitigation: rebuild SFT/DPO/manifest in the merge flow and run public artifact validation.
- [Risk] Public sample grows, making smoke tests slightly larger. -> Mitigation: added rows are limited to 12 train-only public-safe examples, increasing DPO by 108 pairs.

## Migration Plan

1. Run the guarded merge command against the current formal seed and reviewed candidate seed file.
2. Rebuild formal public SFT/DPO/manifest artifacts in place.
3. Validate formal public artifacts and DPO summaries.
4. Publish merge evidence and Human Brief.
5. If rollback is needed before commit, restore the four formal public sample files and remove the merge evidence directory.

## Open Questions

- None for this merge phase. Any model-quality evaluation after merge should be a later bounded OpenSpec change.
