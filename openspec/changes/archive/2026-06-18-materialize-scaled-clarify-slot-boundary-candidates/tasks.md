## 1. Candidate Materialization

- [x] 1.1 Add deterministic scaled clarify slot-boundary candidate materialization from the committed candidate-design report.
- [x] 1.2 Write standalone candidate seed rows, SFT sidecars, JSON evidence, Markdown evidence, manifest, and leak-scan result without touching formal public sample files.
- [x] 1.3 Add CLI support for `materialize-scaled-clarify-slot-boundary-candidates`.

## 2. Evidence And Documentation

- [x] 2.1 Generate committed standalone candidate seed rows and evidence under the scaled clarify materialization report directory.
- [x] 2.2 Update `CONTEXT.md` and `reports/final_status.md` to point at the new materialization evidence while preserving strict metric boundaries.
- [x] 2.3 Add a concise Chinese Human Brief HTML for this phase.

## 3. Validation And Archive

- [x] 3.1 Add focused tests for candidate counts, target-shape invariants, split accounting, standalone-only boundaries, and committed evidence.
- [x] 3.2 Run focused tests, full tests, ruff, public dataset validation where applicable, OpenSpec strict validation, leak scan, candidate-count checks, and `git diff --check`.
- [x] 3.3 Review the diff for overclaiming, private-path leakage, and unrelated changes.
- [x] 3.4 Archive the OpenSpec change and record guarded auto-integration readiness for the outer `/opsx auto` integration step.
