## 1. Residual Diagnosis Coverage

- [x] 1.1 Add a focused regression test that requires a public-safe compact-query exact-match residual diagnosis pack.
- [x] 1.2 Verify the test asserts inherited strict metrics, residual family counts, `seed-search-weather-aug-1` slot-shape evidence, strict `normalized_command` mismatches, and non-claim boundaries.

## 2. Evidence Pack

- [x] 2.1 Generate a machine-readable residual diagnosis JSON from the committed compact-query slot-preservation A100 rerun artifacts.
- [x] 2.2 Generate a human-readable Markdown summary, manifest, leak-scan results, and phase validation leak scan.
- [x] 2.3 Generate `docs/human-briefs/2026-06-09-diagnose-compact-query-exact-match-residuals.html` from the OpenSpec artifacts, source evidence, and validation results.

## 3. Validation and Archive

- [x] 3.1 Run the focused regression test, full relevant pytest suite, `ruff`, `mypy`, `openspec validate --all --strict`, and `git diff --check`.
- [x] 3.2 Run Reviewer diff review and fix any in-scope Must Fix items.
- [x] 3.3 Archive the OpenSpec change, rerun strict validation and leak scans, and commit the completed diagnostic phase if guarded auto integration is safe.
