## 1. Setup and Explorer

- [x] 1.1 Confirm isolated worktree status, branch, baseline tests, and OpenSpec validity.
- [x] 1.2 Run Explorer read-only analysis for route prompt formatting, current tests, prior failure evidence, and local evidence targets.

## 2. Prompt Ontology Repair

- [x] 2.1 Add focused failing tests for route ontology constraints in SFT training and prediction prompt rendering.
- [x] 2.2 Update prompt formatting so `route` is visible as an execution-channel enum, not a domain/topic/URL/path value.
- [x] 2.3 Record prompt constraint summary flags for route ontology and weather-to-search example visibility.

## 3. Public-Safe Evidence and Human Brief

- [x] 3.1 Generate local public-safe route ontology repair evidence under `reports/public-sample/route-task-ontology-output-repair/`.
- [x] 3.2 Add tests that lock evidence boundaries: no training, no A100/private prediction, no output repair, and no model recovery claim.
- [x] 3.3 Generate a concise Chinese Human Brief HTML with status, changed surfaces, validation, prior evidence links, risks, and next recommendation.

## 4. Validation, Review, Archive, and Integration

- [x] 4.1 Run fresh validation: focused tests, full `PYTHONPATH=src pytest -q`, `uv run ruff check .`, `uv run mypy src`, public data validation, DPO pair check, leak-scan, `git diff --check`, and `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`.
- [x] 4.2 Run Reviewer diff review, fix in-scope Must Fix items, and rerun required validation.
- [x] 4.3 Archive the OpenSpec change, rerun post-archive validation, generate loop closeout report, and apply guarded auto integration when safe.
