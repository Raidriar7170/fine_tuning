## 1. Readiness

- [x] 1.1 Verify local repo status, active OpenSpec status, current manifest id/counts, formal-heldout config templates, archived blocked evidence, and retry output directory plan.
- [x] 1.2 Run an Explorer pass or local pattern review for prediction export, evaluation, report, leak-scan, and A100 evidence import patterns.
- [x] 1.3 Inspect A100 GPU/process occupancy and private adapter availability under the approved private project root without writing public artifacts or exposing private paths.

## 2. Prediction-Only Execution

- [x] 2.1 Prepare private, repo-external A100 dev/test prediction configs or overrides resolving placeholders to approved private paths and the selected adapter.
- [x] 2.2 Run dev/test prediction-only exports with explicit `CUDA_VISIBLE_DEVICES`, no training flags, and sidecars needed for public-safe evidence.
- [x] 2.3 If prediction cannot safely run, write blocked-status evidence instead of predictions or model-quality metrics. Outcome: not needed because A100 prediction executed safely and observed evidence was generated.

## 3. Public Evidence

- [x] 3.1 Import or generate sanitized dev/test predictions, prediction metadata, prompt/decoded sidecars where available, metrics, failure slices, manifest, and Markdown report under the distinct retry evidence directory.
- [x] 3.2 Ensure reports record manifest id `public-sample-20260616T074315Z`, dev/test split row counts, 98/252/850 source counts, strict metric authority, retry-after-recovery semantics, and no training/evaluator-relaxation boundary.
- [x] 3.3 Generate `docs/human-briefs/2026-06-16-retry-formal-heldout-prediction-after-a100-recovery.html`.

## 4. Validation And Review

- [x] 4.1 Run focused tests or report-generation checks for the new evidence, plus public dataset validation, DPO check, leak scan, `ruff check .`, `PYTHONPATH=src python -m pytest -q`, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`, and `git diff --check`.
- [x] 4.2 Run a Reviewer pass and fix in-scope Must Fix items.
- [x] 4.3 Archive the OpenSpec change after tasks complete and validation passes.
