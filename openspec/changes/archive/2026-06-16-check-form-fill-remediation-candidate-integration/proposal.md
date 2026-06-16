## Why

`materialize-form-fill-remediation-cases` produced 9 standalone `form_fill` remediation candidate seeds and 9 candidate SFT rows. Before deciding on any formal public-sample merge or A100 training probe, the project needs a bounded local integration check that proves those candidate seeds can be preview-built through the public dataset builder while preserving the formal public sample boundary.

## What Changes

- Add a local `form_fill` remediation candidate integration check that reads the current formal public sample seed file and the standalone candidate seed file.
- Write a preview public-sample build under a reports directory, including preview seed/SFT/DPO/manifest artifacts, without editing formal public sample files.
- Emit a public-safe JSON/Markdown/manifest evidence pack with formal counts, preview counts, candidate contribution counts, validation status, and claim boundaries.
- Add a `voice2task-data check-form-fill-remediation-candidate-integration` CLI command and focused tests.
- Preserve strict evaluation boundaries: no formal merge, no held-out mutation, no training, no prediction, no A100 job, and no evaluator relaxation.

## Capabilities

### New Capabilities

### Modified Capabilities

- `voice2task-dataset-preparation`: Support a local preview integration check for standalone `form_fill` remediation candidate seeds before later merge/training decisions.

## Impact

- Affected code: `src/voice2task/dataset.py`, `src/voice2task/reports.py`, and `src/voice2task/cli/data.py`.
- Affected tests: focused tests for preview build artifacts, CLI output, committed evidence, public-sample immutability, and DPO preview boundaries.
- Affected reports: new evidence under `reports/public-sample/form-fill-remediation-candidate-integration-preview/` and one Human Brief HTML.
- Non-goals: modifying `data/public-samples/seed_traces.jsonl`, rebuilding formal public sample artifacts in place, A100 execution, model training, prediction, checkpoint/adapter release, held-out recovery claims, production readiness claims, or live-browser benchmark claims.
