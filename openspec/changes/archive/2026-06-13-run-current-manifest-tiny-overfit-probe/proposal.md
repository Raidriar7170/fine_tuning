## Why

Current runtime evidence proves that the 7B A100 training path can inspect real assistant-only labels for `public-sample-20260613T072200Z`, but it does not prove the model can memorize even a tiny current-manifest contract slice. Before spending another broad A100 run, we need a bounded train-internal probe that separates "objective path is inspectable" from "7B can learn 1-3 current rows."

## What Changes

- Add public-safe A100 config templates for a 7B current-manifest tiny-overfit probe and its train-split prediction export.
- Run or record the authorized A100 probe only under the approved private project root, using an explicitly selected idle GPU and private overrides outside git.
- Publish only sanitized train-internal evidence: config templates, prediction rows, metrics, sidecars, objective/runtime-label references, leak-scan results, and a concise report/Human Brief.
- Keep the evidence boundary explicit: no DPO, no held-out/dev/test claim, no adapter/checkpoint release, no production-readiness claim, and no live-browser benchmark claim.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `supervised-contract-tuning`: add a bounded 7B current-manifest tiny-overfit probe for 1-3 train rows.
- `contract-evaluation`: add public-safe reporting requirements for the current-manifest tiny-overfit probe.

## Impact

- Affected configs: `configs/sft-a100-current-manifest-tiny-overfit-*.json`.
- Affected evidence: `reports/public-sample/current-manifest-tiny-overfit-probe/`.
- Affected docs: `docs/human-briefs/2026-06-14-run-current-manifest-tiny-overfit-probe.html`.
- Affected tests: focused config/evidence-shape tests and leak-scan validation.
- Remote runtime impact: optional 7B SFT/prediction on the A100 machine; all remote writes stay under `<approved_a100_project_root>` and all private paths remain out of committed artifacts.
