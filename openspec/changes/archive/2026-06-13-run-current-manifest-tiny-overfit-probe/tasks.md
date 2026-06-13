## 1. Local Contract and Configs

- [x] 1.1 Add focused tests for current-manifest tiny-overfit config templates, row-limit metadata, and evidence boundaries.
- [x] 1.2 Add public-safe 7B SFT and prediction config templates for `public-sample-20260613T072200Z`.
- [x] 1.3 Add minimal row-limit support for the SFT training path so the probe can train on 1 to 3 current train rows and record selected row IDs.

## 2. A100 Probe Execution

- [x] 2.1 Sync code and current public-sample data to the approved private A100 project root.
- [x] 2.2 Inspect GPU/process occupancy and choose an idle GPU explicitly.
- [x] 2.3 Run the tiny 7B SFT probe and train-split prediction export with private overrides, or write a public-safe blocked record if dependencies/GPU/access make execution unsafe.

## 3. Evidence and Closeout

- [x] 3.1 Import only sanitized evidence under `reports/public-sample/current-manifest-tiny-overfit-probe/`.
- [x] 3.2 Generate the phase Human Brief HTML and keep claims bounded to train-internal tiny-overfit evidence.
- [x] 3.3 Run focused pytest, OpenSpec validation, leak scans, and `git diff --check`; then archive the change if complete.
