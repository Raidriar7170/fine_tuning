## 1. Proposal and Preflight

- [x] 1.1 Add OpenSpec proposal, design, tasks, and spec deltas for observed A100 candidate SFT probe execution.
- [x] 1.2 Validate the change strictly before implementation.
- [x] 1.3 Re-run A100 preflight for SSH, approved root, dependency state, disk/temp/cache placement, and idle GPU selection.

## 2. Report and Test Surface

- [x] 2.1 Add RED tests for observed/blocked A100 candidate probe evidence shape and non-claim boundaries.
- [x] 2.2 Extend report writing/CLI so candidate probe evidence can represent blocked, failed, or completed A100 training and optional train-split prediction.

## 3. Remote Execution

- [x] 3.1 Prepare an isolated remote workspace and dependency environment under the approved private A100 root.
- [x] 3.2 Sync the current project snapshot or required files into the isolated remote workspace without overwriting unrelated remote work.
- [x] 3.3 Run candidate-only 7B SFT on an explicitly selected idle GPU if dependencies and placement are safe.
- [x] 3.4 If SFT completes, run candidate train-split prediction using the private adapter; otherwise record skipped/blocked prediction status.

## 4. Evidence and Closeout

- [x] 4.1 Import sanitized A100 candidate probe metadata/evidence into `reports/public-sample`.
- [x] 4.2 Generate Chinese Human Brief.
- [x] 4.3 Run focused pytest, full pytest, dataset validation, OpenSpec validation, leak scan, and `git diff --check`.
- [x] 4.4 Run reviewer pass and fix Must Fix items in scope.
- [x] 4.5 Archive the change and apply guarded auto integration if complete.
