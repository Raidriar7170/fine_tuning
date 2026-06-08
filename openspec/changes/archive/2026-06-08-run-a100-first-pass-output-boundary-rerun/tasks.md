## 1. Scope And Local Preflight

- [x] 1.1 Confirm current committed repo state, no active unrelated dirty files, and OpenSpec proposal/design/specs validity.
- [x] 1.2 Add or update focused tests for the A100 first-pass output-boundary evidence pack shape, boundary metadata, strict metric preservation, and public-safe non-claims.
- [x] 1.3 Prepare local evidence import expectations and prior baseline links without changing parser or evaluator behavior.

## 2. A100 Runtime Execution

- [x] 2.1 Prepare the A100 runtime under the approved private project root using current committed code and a repo-external private override.
- [x] 2.2 Inspect GPU/process occupancy, choose a safe idle GPU, set `CUDA_VISIBLE_DEVICES`, and run prediction-only train-split rerun without training.
- [x] 2.3 Copy only sanitized public artifacts into `reports/public-sample/a100-first-pass-output-boundary-rerun/`.

## 3. Evidence Import And Human Brief

- [x] 3.1 Generate metrics, schema guard summary, output-boundary comparison diagnosis, manifest, report, and leak scans.
- [x] 3.2 Generate `docs/human-briefs/2026-06-08-run-a100-first-pass-output-boundary-rerun.html`.
- [x] 3.3 Ensure evidence records `prediction_output_boundary` visibility, strict schema-valid counts, Markdown wrapper counts, comparison against prior A100 rerun, and no overclaim boundaries.

## 4. Validation, Review, Archive, Integration

- [x] 4.1 Run focused tests, full `PYTHONPATH=src pytest -q`, `uv run ruff check .`, `uv run mypy src`, public data validation, DPO pair check, public leak scans, `git diff --check`, and `openspec validate --all --strict`.
- [x] 4.2 Complete Reviewer pass in the main thread, fix in-scope Must Fix items only, and rerun required validation.
- [x] 4.3 Archive the OpenSpec change, generate post-archive/final leak scans, rerun post-archive validation, and commit the phase under guarded auto integration.
