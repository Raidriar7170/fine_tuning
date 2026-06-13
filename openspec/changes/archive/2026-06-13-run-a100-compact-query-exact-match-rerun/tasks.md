## 1. Local Preparation

- [x] 1.1 Reconfirm current public sample manifest, SFT rows, DPO pairs, and compact-query prompt constraint metadata.
- [x] 1.2 Add or update focused local tests for the new rerun evidence-pack contract and non-claim boundaries.
- [x] 1.3 Prepare public-safe 7B A100 run and prediction templates plus repo-external private override instructions with unresolved private paths excluded from git.

## 2. A100 Execution

- [x] 2.1 On the A100 machine, inspect `nvidia-smi`, choose a safe idle GPU, and set `CUDA_VISIBLE_DEVICES` explicitly.
  - Blocked 2026-06-13: configured A100 SSH alias timed out before remote command execution, so GPU occupancy could not be inspected safely.
  - Resumed 2026-06-13 after company VPN/proxy was enabled: GPU 3 was selected from idle GPUs 3-7 and verified with `CUDA_VISIBLE_DEVICES=3`.
- [x] 2.2 Run bounded public-sample SFT under `<a100_project_root>` using the current public manifest and compact-query exact-match training prompt policy.
- [x] 2.3 Export sanitized train-split trained-adapter predictions and sidecars: prompt snapshot, prediction metadata, raw decoded summary, generation trace, schema guard summary, and metrics when available.

## 3. Evidence And Diagnostics

- [x] 3.1 Copy back only public-safe sanitized evidence; keep raw logs, checkpoints, adapters, caches, private overrides, private paths, host details, SSH details, tokens, and private corpus rows out of git.
- [x] 3.2 Generate residual-family diagnosis comparing strict `contract_exact_match`, strict `slot_f1`, `normalized_command` exact strings, and compact `slots.query` shape against prior compact-query residual evidence.
- [x] 3.3 Generate evidence JSON, Markdown report, manifest, leak scan, and concise Chinese Human Brief for the A100 rerun.

## 4. Validation, Review, And Archive

- [x] 4.1 Run focused evidence tests, full `PYTHONPATH=src pytest -q`, `uv run ruff check .`, `uv run mypy src`, public data validation, DPO pair check, leak scan, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`, and `git diff --check`.
- [x] 4.2 Run Reviewer diff review, fix any in-scope Must Fix items, and rerun required validation.
  - Review note: current multi-agent tool policy requires explicit user authorization before spawning subagents, so this pass was completed as a main-thread read-only diff review. Must Fix: none.
- [x] 4.3 Archive the OpenSpec change after user review, rerun post-archive validation, and report the bounded conclusion without claiming model recovery unless strict evidence supports it.
  - Archive is executed under `/opsx auto`; post-archive validation is recorded in the final response and evidence report.
