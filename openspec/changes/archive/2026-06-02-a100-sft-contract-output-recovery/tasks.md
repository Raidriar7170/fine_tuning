## 1. Contract Formatting Recovery

- [x] 1.1 Add shared formatting helpers for SFT training text and prediction prompts that use tokenizer chat templates when available and deterministic fallback text otherwise.
- [x] 1.2 Strengthen the contract-only system instruction with the required Browser Task Contract fields and explicit non-goals for explanations, Markdown, and GUI actions.
- [x] 1.3 Wire the real SFT training path and private-adapter prediction path through the shared formatting helpers.

## 2. Honest Recovery Evidence

- [x] 2.1 Add tests proving invalid private-adapter predictions remain schema failures rather than being replaced by fixture, rule-baseline, or gold-contract outputs.
- [x] 2.2 Add a public-safe recovery evidence report or template that records pre-recovery schema failures and post-rerun metrics when available.
- [x] 2.3 Update README/runbook wording for contract-output recovery without hostnames, IPs, secrets, SSH details, private paths, checkpoint release claims, or live-browser improvement claims.
- [x] 2.4 Generate a concise Chinese Human Brief HTML for this phase from OpenSpec artifacts, evidence files, and validation output.

## 3. Validation

- [x] 3.1 Run `uv run ruff check .`, `uv run mypy src`, and `uv run pytest`.
- [x] 3.2 Run public dataset validation, DPO pair checks, contract metrics, controlled smoke, leak-scan, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`, and `git diff --check`.
