## 1. Rerun Setup

- [x] 1.1 Confirm worktree git status, branch, OpenSpec state, baseline evidence, and local validation before private execution.
- [x] 1.2 Identify the existing A100 access path without recording host/IP/private path details in committed artifacts.
- [x] 1.3 Prepare a repo-external private A100 override under the approved private project root with explicit heavy-training and prediction opt-ins.
- [x] 1.4 Confirm an idle A100 GPU and avoid interrupting other users' processes.

## 2. Required-Field Repair A100 Execution

- [x] 2.1 Run the current SFT training entrypoint on the public-sample train split with assistant-only labels and required-field prompt skeleton.
- [x] 2.2 Run runtime/objective label provenance on the current tokenizer/collator path and record prompt-mask plus assistant-loss status.
- [x] 2.3 Run private-adapter prediction on `prediction_split=train` with schema guard/retry enabled, `overfit_diagnostic=true`, and `generalization_claim=false`.
- [x] 2.4 Preserve raw attempts, retry attempts, schema guard metadata, schema-invalid outputs, partial outputs, truncated outputs, non-JSON outputs, and wrong-contract outputs as observed model evidence.

## 3. Public-Safe Evidence Pack

- [x] 3.1 Copy back only sanitized public-sample evidence into a new required-field repair rerun evidence directory.
- [x] 3.2 Generate metrics, manifest, report, and comparison context against the prior assistant-only train-split rerun and required-field repair metadata.
- [x] 3.3 Run leak-scan over the new evidence pack and reject raw private rows, private paths, secrets, IPs, SSH details, raw logs, checkpoints, adapters, caches, and oversized generated corpora.
- [x] 3.4 Add or update focused tests if the rerun evidence, schema guard report shape, or manifest shape introduces new committed behavior.

## 4. Validation, Review, Archive, and Integration

- [x] 4.1 Run fresh validation: focused tests, full `PYTHONPATH=src pytest -q`, `uv run ruff check .`, `uv run mypy src`, public data validation, DPO pair check, leak-scan, `git diff --check`, and `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`.
- [x] 4.2 Generate a concise Chinese Human Brief HTML with project-stage progress, observed metrics, A100 evidence links, validation results, and non-overclaim limits.
- [x] 4.3 Run Reviewer diff review, fix in-scope Must Fix items, and rerun required validation.
- [x] 4.4 Archive the OpenSpec change, rerun post-archive validation, update the loop report, and apply auto integration when safe.
