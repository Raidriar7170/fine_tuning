## Why

The 12 standalone form-fill confirmation-marker extension candidates have been materialized and validated through a report-scoped preview dataset. The next bounded step is to decide and execute their formal public-sample merge so future public dataset builds include this confirmation-marker coverage without treating preview artifacts as formal evidence.

## What Changes

- Merge the reviewed `form_fill_confirmation_marker_extension_seed_candidates.jsonl` rows into the formal public seed file.
- Rebuild formal public SFT, DPO, and manifest artifacts from the updated seed file.
- Publish merge evidence under `reports/public-sample/` with pre/post counts, split counts, candidate contribution counts, validation status, and public-safety boundaries.
- Add a `voice2task-data` CLI command for the formal merge flow.
- Preserve evidence boundaries: no training, no prediction, no A100 execution, no evaluator relaxation, no checkpoint or adapter release, and no held-out/model recovery claim.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `voice2task-dataset-preparation`: require a guarded formal merge path for reviewed form-fill confirmation-marker extension candidates after preview validation.

## Impact

- Affected code: `src/voice2task/dataset.py`, `src/voice2task/cli/data.py`, and `src/voice2task/reports.py`.
- Affected tests: focused tests for formal confirmation-marker extension candidate merge.
- Affected artifacts: formal public sample seed/SFT/DPO/manifest files and a new merge evidence report.
- Non-goals: generic chat fine-tuning, skill routing, GUI action policy learning, first-phase GRPO, public release of the full local corpus, prompt change, evaluator relaxation, prediction run, SFT/DPO/GRPO training, checkpoint release, adapter release, production readiness, private-corpus generalization, public full-corpus release, or live-browser benchmark improvement claims.
