## 1. Setup and Explorer

- [x] 1.1 Confirm branch, clean git status, no active OpenSpec conflicts, validation baseline, and local-only/no-A100 scope.
- [x] 1.2 Run Explorer read-only analysis for normalized-command data, prompt, spec, and test targets.
- [x] 1.3 Validate the OpenSpec proposal/design/spec/tasks strictly before implementation.

## 2. Canonicalization Policy Surface

- [x] 2.1 Add a small target-writing policy surface for `normalized_command` that distinguishes canonical gold targets from evaluator-side normalization or semantic equivalence.
- [x] 2.2 Make SFT training text and prediction prompts expose the canonical target policy without leaking row gold targets into prediction prompts.
- [x] 2.3 Add focused tests for public-sample canonical target stability, prompt visibility, and no metric/re-score/A100 boundary wording.

## 3. Documentation

- [x] 3.1 Generate a concise Chinese Human Brief HTML with project-stage progress, changed surfaces, validation results, remaining risks, and recommended next step.

## 4. Validation, Review, Archive, and Integration

- [x] 4.1 Run fresh validation: focused tests, full `PYTHONPATH=src pytest -q`, `uv run ruff check .`, `uv run mypy src`, public data validation, DPO pair check, leak-scan, `git diff --check`, and `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`.
- [x] 4.2 Run Reviewer diff review, fix in-scope Must Fix items, and rerun required validation.
- [x] 4.3 Archive the OpenSpec change, rerun post-archive validation, generate loop closeout report, and apply guarded auto integration when safe.
