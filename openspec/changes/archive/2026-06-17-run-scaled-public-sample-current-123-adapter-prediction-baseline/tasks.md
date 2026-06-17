## 1. Local Scaffolding

- [x] 1.1 Add public-safe dev/test prediction config templates for the scaled target manifest and current-123 source adapter boundary.
- [x] 1.2 Add focused tests for prediction-only config shape, public-safe placeholders, boundary fields, and 207-row dev/test fixture selection.
- [x] 1.3 Add OpenSpec proposal/design/spec/tasks and a Human Brief draft that does not claim metrics.

## 2. Prediction-Only Execution

- [x] 2.1 Attempt read-only A100 connectivity preflight; fail closed before GPU/process, dependency, and private adapter checks because the configured SSH alias timed out.
- [x] 2.2 Do not prepare repo-external private overrides while remote access is blocked; record that no private override was created.
- [x] 2.3 Do not run dev prediction-only export; record blocked evidence with `dev_predictions_written=false`.
- [x] 2.4 Do not run test prediction-only export; record blocked evidence with `test_predictions_written=false`.
- [x] 2.5 Do not evaluate dev/test predictions; record blocked evidence with `metrics_generated=false`.

## 3. Public Evidence

- [x] 3.1 Import public-safe blocked evidence, manifest, report, A100 preflight status, and leak-scan results; no predictions, sidecars, or metrics were produced.
- [x] 3.2 Record target manifest `public-sample-20260617T152259Z`, source adapter runtime `a100-current-train-split-sft-retry`, source adapter manifest `public-sample-20260617T045941Z`, and split counts of 261 train / 207 dev / 207 test.
- [x] 3.3 Refresh `CONTEXT.md`, `reports/final_status.md`, and the Human Brief with blocked results.

## 4. Validation And Closeout

- [x] 4.1 Run focused tests around config/formal public held-out prediction.
- [x] 4.2 Run OpenSpec strict validation, ruff, leak scan, and `git diff --check`.
- [x] 4.3 Review the diff for private-path leakage, overclaiming, stale manifest comparisons, and unrelated edits.
- [x] 4.4 Archive only after prediction evidence or blocked evidence has been produced and validated in a later phase.
