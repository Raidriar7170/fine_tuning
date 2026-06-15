## 1. Proposal And Configs

- [x] 1.1 Validate the OpenSpec proposal, design, and delta spec.
- [x] 1.2 Add current-manifest dev/test prediction config templates for formal public sample held-out evaluation.
- [x] 1.3 Add or update tests that prove the configs point at the current manifest and preserve prediction-only/private-override boundaries.

## 2. Prediction Evidence

- [x] 2.1 Run local dry-run or fixture checks to verify dev/test row selection against the current manifest.
- [x] 2.2 If remote A100 execution is safe and the private adapter is available, run prediction-only dev/test export; otherwise generate a blocked evidence record.
- [x] 2.3 Produce metrics, schema diagnostics, alignment diagnostics, manifest/report, and leak-scan evidence when predictions are available, or blocked evidence when they are not.

## 3. Closeout

- [x] 3.1 Generate the Chinese Human Brief for this phase.
- [x] 3.2 Run focused tests, full test suite, ruff, public validation, leak scan, OpenSpec validation, and diff checks.
- [x] 3.3 Archive the OpenSpec change, commit, and push if validation passes.
