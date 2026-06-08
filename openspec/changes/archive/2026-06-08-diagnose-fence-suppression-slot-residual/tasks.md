## 1. Local Evidence Diagnosis

- [x] 1.1 Inspect the source A100 fence-suppression rerun artifacts and confirm the residual mismatch is exactly one row-level slot mismatch.
- [x] 1.2 Generate `reports/public-sample/fence-suppression-slot-residual-diagnosis/` with diagnosis JSON/Markdown, manifest, and leak scans.
- [x] 1.3 Generate `docs/human-briefs/2026-06-08-diagnose-fence-suppression-slot-residual.html`.

## 2. Tests And Validation

- [x] 2.1 Add focused tests for residual row id, slot mismatch category, strict metric boundaries, source artifact links, privacy boundaries, and no overclaim.
- [x] 2.2 Run focused tests, full `PYTHONPATH=src pytest -q`, `uv run ruff check .`, `uv run mypy src`, public data validation, DPO pair check, leak scans, `git diff --check`, and `openspec validate --all --strict`.
- [x] 2.3 Complete Reviewer pass, fix in-scope Must Fix items only, and rerun required validation.

## 3. Archive And Integration

- [x] 3.1 Archive the OpenSpec change, rerun post-archive validation, and commit the phase under guarded auto integration.
