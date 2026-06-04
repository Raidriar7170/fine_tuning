## 1. Runtime Evidence Contract

- [x] 1.1 Add focused failing tests for observed runtime label provenance evidence shape, safe-claim defaults, hostile metadata sanitization, and private-path rejection.
- [x] 1.2 Implement an observed runtime label provenance evidence writer/CLI path that keeps prep evidence separate from executed runtime evidence.
- [x] 1.3 Add or update runtime metadata helpers so real tokenizer/collator label provenance can be recorded without exposing private paths, host details, raw logs, checkpoints, adapters, or private rows.

## 2. Authorized A100 Execution

- [x] 2.1 Resolve the private runtime override outside git, select an idle A100 GPU, and keep all created/modified remote files under `<approved_a100_project_root>`.
- [x] 2.2 Execute the bounded runtime label provenance check against the committed public-sample SFT manifest using the real training tokenizer/collator path where available.
- [x] 2.3 Copy back only sanitized runtime metadata/evidence artifacts and record blocked/ambiguous states honestly if real labels are unavailable.

## 3. Evidence, Brief, and Review

- [x] 3.1 Generate a public-safe evidence pack under `reports/public-sample/runtime-label-provenance-check/` and link prior prep, label-provenance, target-template, and train-split diagnostic evidence.
- [x] 3.2 Generate a concise Chinese Human Brief with project-stage progress, A100 execution status, validation results, remaining gaps, and non-overclaim boundaries.
- [x] 3.3 Run Reviewer diff review, fix in-scope Must Fix items, and rerun required validation.

## 4. Validation and OpenSpec Closeout

- [x] 4.1 Run fresh validation: focused tests, full `PYTHONPATH=src pytest -q`, `ruff check .`, `mypy src`, public dataset validate, DPO pair checks, schema metrics smoke, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`, leak-scan, and `git diff --check`.
- [x] 4.2 Archive the change, sync accepted specs, regenerate loop closeout HTML, rerun post-archive validation, and apply auto integration policy when safe.
