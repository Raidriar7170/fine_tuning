## Overview

This phase is a dry integration check between standalone candidate materialization and any later formal merge/probe decision.

The check SHALL:

1. Read `data/public-samples/seed_traces.jsonl`.
2. Read `data/public-samples/form_fill_remediation_seed_candidates.jsonl`.
3. Validate that the candidate set is exactly the reviewed 9-row standalone candidate set and that none of those IDs are already in the formal seed file.
4. Convert candidate provenance to a preview-only public seed status in memory.
5. Write preview artifacts under `reports/public-sample/form-fill-remediation-candidate-integration-preview/public-sample-preview/`.
6. Run the normal public dataset builder against the preview seed file in the preview directory.
7. Validate the preview SFT/DPO/manifest artifacts as public-safe.
8. Write integration evidence and a Human Brief.

## Boundary

The preview directory may contain generated preview SFT/DPO artifacts because the point of the check is to verify builder compatibility. Those artifacts are not formal public sample artifacts and do not replace files under `data/public-samples/`.

Evidence must report:

- `formal_public_sample_modified=false`
- `preview_public_sample_generated=true`
- `preview_dpo_pairs_generated=true`
- `training_run=false`
- `prediction_run=false`
- `a100_execution=false`
- `evaluator_metric_change=false`

## Expected Counts

Given the current formal public sample has 77 seed rows and 231 SFT rows, and the candidate file has 9 seed rows with no augmentations, the preview build is expected to contain 86 seed rows and 240 SFT rows.

The normal DPO builder is expected to generate preview DPO pairs for the 9 candidate original rows. These are local preview artifacts only and do not authorize a formal DPO rebuild.

## Claim Boundary

This check proves only that the candidate data is schema-valid, public-safe, and buildable through the existing public dataset builder in a preview directory. It does not prove held-out recovery, model recovery, strict metric improvement, checkpoint release, adapter release, production readiness, private corpus generalization, or live-browser benchmark improvement.

## Next Phase

If this check passes, the next bounded OpenSpec phase may decide between:

- a formal public-sample merge of the reviewed candidates; or
- a no-merge local/A100 probe using the standalone candidates.

That decision must remain separate from this integration check.
