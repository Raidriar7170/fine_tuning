## 1. Scope and Cleanup

- [x] 1.1 Confirm the current public-surface leak-scan finding and identify the exact historical Human Brief line.
- [x] 1.2 Sanitize the historical Human Brief wording without changing prior A100 evidence outcomes, metrics, manifests, or non-claim boundaries.
- [x] 1.3 Add an OpenSpec delta clarifying that committed Human Briefs and loop reports are public documentation surfaces covered by no-private-path boundaries.

## 2. Brief and Review

- [x] 2.1 Generate a concise Chinese Human Brief for this cleanup phase with project-stage progress, changed files, validation results, remaining risks, and next recommended phase.
- [x] 2.2 Run Reviewer diff review, fix in-scope Must Fix items, and rerun required validation.

## 3. Validation and Closeout

- [x] 3.1 Run fresh validation: full public-surface leak-scan over `README.md`, `CONTEXT.md`, `data/public-samples`, `reports/public-sample`, `reports/templates`, `docs/human-briefs`, and `openspec`; `PYTHONPATH=src pytest -q`; `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`; and `git diff --check`.
- [x] 3.2 Archive the change, rerun post-archive validation, create the loop report or update it with this phase, and apply auto integration policy when safe.
