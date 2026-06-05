## 1. Setup and OpenSpec

- [x] 1.1 Confirm branch, git status, active OpenSpec state, validation baseline, and local-only/no-A100 scope.
- [x] 1.2 Run Explorer read-only analysis for README, evidence, spec, and test targets.
- [x] 1.3 Validate the OpenSpec proposal/design/spec/tasks strictly before implementation.

## 2. Public Interpretation Surfaces

- [x] 2.1 Add README wording that keeps `contract_exact_match` strict and rejects automatic semantic equivalence for `normalized_command` string differences.
- [x] 2.2 Add a small public-safe evidence policy note near the normalized-command diagnosis artifacts without rewriting prior generated evidence.
- [x] 2.3 Add focused tests that pin README/evidence wording and no-metric-change/no-semantic-equivalence boundaries.

## 3. Documentation

- [x] 3.1 Generate a concise Chinese Human Brief HTML with project-stage progress, changed surfaces, validation results, remaining risks, and recommended next step.

## 4. Validation, Review, Archive, and Integration

- [x] 4.1 Run fresh validation: focused tests, full `PYTHONPATH=src pytest -q`, `uv run ruff check .`, `uv run mypy src`, public data validation, DPO pair check, leak-scan, `git diff --check`, and `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`.
- [x] 4.2 Run Reviewer diff review, fix in-scope Must Fix items, and rerun required validation.
- [x] 4.3 Archive the OpenSpec change, rerun post-archive validation, generate loop closeout report, and apply guarded auto integration when safe.
