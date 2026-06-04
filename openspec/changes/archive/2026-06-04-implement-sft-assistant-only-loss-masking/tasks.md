## 1. Tests First

- [x] 1.1 Add focused failing tests proving that the current runtime/full-text SFT label path leaves prompt tokens unmasked.
- [x] 1.2 Add tests for the desired assistant-only behavior: prompt/system/user labels are `-100`, assistant contract tokens carry loss, and ambiguous target spans fail closed.
- [x] 1.3 Verify the new tests fail for the expected reason before implementation.

## 2. Objective Mask Implementation

- [x] 2.1 Implement assistant-only label construction from rendered SFT training text, tokenizer offsets, and assistant target boundary.
- [x] 2.2 Align runtime objective inspection with the same label path and provenance fields used by real SFT training.
- [x] 2.3 Update real SFT training integration or fail-closed metadata so the trainer path does not silently claim assistant-only labels when the installed TRL API cannot use them.

## 3. Evidence, Brief, and Review

- [x] 3.1 Update public-safe runtime label provenance reporting for the repaired objective path, and preserve historical observed A100 evidence instead of overwriting it without a new runtime run.
- [x] 3.2 Generate a concise Chinese Human Brief with project-stage progress, changed files, validation results, remaining A100 rerun boundary, and non-overclaim limits.
- [x] 3.3 Run Worker validation, Reviewer diff review, fix in-scope Must Fix items, and rerun required validation.

## 4. Validation and Closeout

- [x] 4.1 Run fresh validation: focused tests, full `PYTHONPATH=src pytest -q`, `uv run ruff check .`, `uv run mypy src`, public data validation, DPO pair check, full public-surface leak-scan, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`, and `git diff --check`.
- [x] 4.2 Archive the change when local validation and review pass, rerun post-archive validation, and apply auto integration policy when safe.
- [x] 4.3 Stop before real private A100 retraining/prediction unless a separate execution gate is explicitly satisfied and sanitized evidence handling is ready.
