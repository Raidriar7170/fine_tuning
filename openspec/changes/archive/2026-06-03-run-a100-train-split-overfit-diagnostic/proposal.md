## Why

The previous preparation phase created public-safe train-split overfit diagnostic surfaces, but the committed evidence is still fixture-mode only. A real private A100 diagnostic is needed to see whether the trained adapter can recover Browser Task Contract schema, route, and slot shape on train-internal rows while preserving prompt, objective, decoding, and row-level evidence.

## What Changes

- Run the bounded A100 train-split overfit diagnostic with a repo-external private override and an idle A100 GPU.
- Keep remote checkpoints, adapters, caches, raw logs, private overrides, host details, SSH details, tokens, private paths, and private corpus rows out of committed artifacts.
- Copy back only sanitized diagnostic predictions, prompt snapshot, raw decoded summary, generation trace, objective inspection, metrics, manifest, report, and leak-scan results.
- Report the observed train-internal recovery status honestly, including schema/route/slot failures if the model still fails.
- Preserve `prediction_split=train`, `overfit_diagnostic=true`, and `generalization_claim=false` in public evidence.
- Non-goals: generic chat fine-tuning, skill routing, GUI action policy learning, first-phase GRPO, public release of the full local/private corpus, checkpoint release, adapter release, production-readiness claims, dev/test generalization claims, and live-browser benchmark improvement claims.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `supervised-contract-tuning`: require the real A100 train-split diagnostic run to use the prepared diagnostic config/sidecar contract and private override boundary.
- `contract-evaluation`: require public-safe reporting of observed train-internal diagnostic evidence without overclaiming generalization or release status.

## Impact

- Affected systems: remote A100 execution under the approved private project root, local sanitized evidence import, contract metrics, report generation, leak scanning, Human Brief HTML, and OpenSpec archive flow.
- Affected artifacts: `reports/public-sample/a100-train-split-overfit-diagnostic/` and the A100 diagnostic Human Brief.
- No public checkpoint, adapter, raw log, private override, host/IP detail, SSH detail, token, secret, private path, or private corpus row may be committed.
