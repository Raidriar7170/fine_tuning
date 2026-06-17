## Why

The current formal public sample advanced to `public-sample-20260617T045941Z` after current-retry confirmation-preservation materialization, but the latest model evidence remains bound to the prior evaluated manifest. The readiness phase shows the 123-row train split is ready for a bounded A100 SFT retry, so the next step is to train a paired private adapter and evaluate it with the strict contract ladder.

## What Changes

- Run one bounded A100 SFT retry on the current formal public train split for `public-sample-20260617T045941Z`.
- Use fresh A100 GPU preflight, select an idle GPU, and keep all private runtime outputs under the approved private A100 project root.
- Run strict dev/test prediction evaluation with the adapter trained for the same target manifest.
- Publish only sanitized public-sample evidence: aggregate metrics, sidecars, manifests, reports, and a Human Brief.
- Preserve comparison boundaries: prior-manifest metrics remain context only, and current-manifest claims require the new paired adapter evidence.
- Do not run DPO/GRPO, change prompts, relax evaluator metrics, normalize slots, mutate data, publish checkpoints/adapters, publish private corpora, or claim production/live-browser improvement.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `supervised-contract-tuning`: Add requirements for a bounded current-123-row A100 SFT retry run with private outputs and paired target-manifest adapter evidence.
- `contract-evaluation`: Add requirements for strict dev/test evaluation and public-safe reporting for the current-123-row SFT retry.

## Impact

- Affected configs: `configs/sft-a100-current-train-split-retry.json`, `configs/sft-a100-current-train-split-retry-dev-prediction.json`, and `configs/sft-a100-current-train-split-retry-test-prediction.json`.
- Affected public evidence: a new `reports/public-sample/a100-current-123-train-split-sft-retry/` evidence pack and a Human Brief.
- Affected remote runtime: a private A100 training/prediction run under the approved private A100 project root, with no raw logs, adapters, checkpoints, caches, SSH details, GPU identifiers, or private corpus rows committed to git.
