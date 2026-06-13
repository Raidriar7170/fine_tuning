## Why

The archived local hardening phase made compact-query exact-match policy visible in data, prompts, validation, and public-safe reporting, but it did not run A100 training or prediction. A small A100 rerun is needed to test whether the current public sample plus hardened prompt/data contract can actually reduce the strict compact-query residual without over-claiming generalization.

## What Changes

- Run a bounded A100 SFT rerun on the committed current public sample only with `Qwen/Qwen2.5-7B-Instruct`, using the archived compact-query exact-match policy and synchronized public SFT/DPO/manifest artifacts.
- Export trained-adapter predictions for the same public-sample train split and preserve raw sanitized model outputs for strict evaluation.
- Generate public-safe evidence containing prompt snapshot, prediction metadata, sanitized predictions, raw decoded/generation sidecars when available, metrics, residual diagnosis, leak scan, manifest, report, and Chinese Human Brief.
- Compare against the prior compact-query exact-match residual family, especially `normalized_command` strict string mismatches and `city/date/topic` versus compact `slots.query`.
- Keep A100 files, private overrides, raw logs, checkpoints, adapters, caches, host details, SSH details, tokens, private paths, and private corpus rows out of git.
- Do not run DPO, full private corpus training, dev/test generalization evaluation, first-phase GRPO, generic chat fine-tuning, skill routing, GUI action policy learning, checkpoint/adapter release, public full-corpus release, parser relaxation, strict evaluator relaxation, semantic-equivalence scoring as a primary metric, prediction repair, prediction replacement, or live-browser benchmark evaluation.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `supervised-contract-tuning`: Add a bounded A100 public-sample SFT rerun using the compact-query exact-match policy and current public manifest.
- `contract-evaluation`: Add public-safe evidence and residual diagnosis requirements for the A100 compact-query exact-match rerun.

## Impact

- Affected systems: local orchestration scripts/configs for 7B A100 execution, A100 private output directory, public evidence under `reports/public-sample/`, and Human Brief under `docs/human-briefs/`.
- Affected code: only if existing CLI/config hooks cannot run the bounded rerun or sanitize evidence correctly.
- Affected tests/validation: focused evidence tests, full local pytest/lint/type checks, public data validation, leak scan, OpenSpec strict validation, and `git diff --check`.
- Remote execution: authorized A100 use under `<a100_project_root>` with explicit GPU selection after occupancy inspection.
