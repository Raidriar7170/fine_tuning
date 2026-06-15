## 1. Proposal and Contract

- [x] 1.1 Add OpenSpec proposal, design, tasks, and spec delta for bounded candidate materialization.
- [x] 1.2 Validate the change strictly before implementation.

## 2. Candidate Materialization

- [x] 2.1 Add RED tests for candidate coverage, schema validity, committed evidence, and public-sample non-mutation.
- [x] 2.2 Implement deterministic candidate seed and SFT-row materialization from the reviewed design artifact.
- [x] 2.3 Add a public-safe report writer and data CLI command.

## 3. Evidence and Brief

- [x] 3.1 Generate committed candidate seed JSONL plus JSON, Markdown, and manifest evidence.
- [x] 3.2 Generate a concise Chinese Human Brief with project-stage progress and recommended next decision.

## 4. Validation and Closeout

- [x] 4.1 Run focused pytest, related regression tests, dataset validation, OpenSpec validation, leak scan, and `git diff --check`.
- [x] 4.2 Run a reviewer pass over the diff and fix Must Fix items in scope.
- [x] 4.3 Archive the change if complete and apply guarded auto integration.
