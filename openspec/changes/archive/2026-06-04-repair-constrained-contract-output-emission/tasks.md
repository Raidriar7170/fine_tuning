## 1. Setup and Baseline

- [x] 1.1 Confirm isolated worktree status, branch, OpenSpec state, and baseline focused validation.
- [x] 1.2 Run Explorer read-only analysis and fold findings into the scoped implementation plan.

## 2. Prompt and Schema-Guard Repair

- [x] 2.1 Add failing tests for first-pass canonical one-shot visibility, whole-object boundaries, and prediction-prompt gold-target exclusion.
- [x] 2.2 Add or update tests proving wrapped retry fragments remain invalid and schema-valid whole-object raw output is accepted.
- [x] 2.3 Implement the minimal prompt/output constraint repair without post-hoc coercion or metric repair.

## 3. Public-Safe Evidence and Documentation

- [x] 3.1 Generate a local constrained-output repair evidence pack with prompt constraint coverage and non-claim boundaries.
- [x] 3.2 Run leak-scan over the evidence pack and reject private paths, secrets, raw logs, checkpoints, adapters, caches, and oversized generated corpora.
- [x] 3.3 Generate a concise Chinese Human Brief HTML with project-stage progress, validation results, remaining risks, and recommended next step.

## 4. Validation, Review, Archive, and Integration

- [x] 4.1 Run fresh validation: focused tests, full `PYTHONPATH=src pytest -q`, `uv run ruff check .`, `uv run mypy src`, public data validation, DPO pair check, leak-scan, `git diff --check`, and `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`.
- [x] 4.2 Run Reviewer diff review, fix in-scope Must Fix items, and rerun required validation.
- [x] 4.3 Archive the OpenSpec change, rerun post-archive validation, update the loop report, and apply auto integration when safe.
