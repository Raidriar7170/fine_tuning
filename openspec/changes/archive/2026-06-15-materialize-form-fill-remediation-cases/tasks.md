## 1. OpenSpec And Dataset Logic

- [x] 1.1 Add an OpenSpec spec delta for standalone `form_fill` remediation materialization.
- [x] 1.2 Add fail-closed dataset helpers that accept only the reviewed case design and expected groups.
- [x] 1.3 Materialize 9 train-split candidate seed rows and 9 candidate SFT rows without changing formal public sample files.

## 2. Reporting, CLI, And Evidence

- [x] 2.1 Add a public-safe materialization report writer for JSON, Markdown, manifest, and candidate SFT JSONL.
- [x] 2.2 Add a `voice2task-data materialize-form-fill-remediation-candidates` CLI command.
- [x] 2.3 Generate committed candidate artifacts under `data/public-samples/` and `reports/public-sample/`.
- [x] 2.4 Generate a concise Chinese Human Brief HTML for the phase.

## 3. Validation And Closeout

- [x] 3.1 Add focused tests for the materializer, CLI, committed evidence, canonical contract policy, and public-sample immutability.
- [x] 3.2 Run focused tests, full tests, ruff, OpenSpec strict validation, leak scan, and `git diff --check`.
- [x] 3.3 Archive the OpenSpec change after tasks complete.
