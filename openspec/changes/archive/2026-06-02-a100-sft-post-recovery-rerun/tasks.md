## 1. Remote Preflight

- [x] 1.1 Identify an existing SSH alias or approved access path without writing hostnames, IPs, SSH details, tokens, or secrets into repo artifacts.
- [x] 1.2 Select an idle A100 GPU without killing or interrupting other users' processes.
- [x] 1.3 Prepare a private remote project workspace and config overrides under `<a100_project_root>/voice2task-post-recovery-rerun`.

## 2. Post-Recovery A100 Rerun

- [x] 2.1 Run public-sample SFT with `voice2task-train sft --run-training`, the recovered contract-only formatting policy, and private outputs under the approved remote project root.
- [x] 2.2 Run private-adapter public-sample prediction with `voice2task-train sft-predict --run-prediction`, preserving invalid outputs as sanitized schema-failure candidates if the model still fails.
- [x] 2.3 Copy back only sanitized public-sample predictions, prediction metadata, and aggregate command/status summaries; leave checkpoints, adapters, raw logs, caches, private configs, and private paths on the A100 machine.

## 3. Public Evidence Pack

- [x] 3.1 Write post-recovery predictions, prediction metadata, metrics, controlled smoke result, leak-scan result, manifest, and report under `reports/public-sample/a100-sft-post-recovery-rerun/`.
- [x] 3.2 Compare post-recovery metrics and controlled smoke status against the pre-recovery `json_valid_rate=0.0000` and 12-schema-failure baseline.
- [x] 3.3 Update the recovery evidence template or report slot so it points to the real post-rerun artifacts and keeps all claim boundaries explicit.

## 4. Documentation And Validation

- [x] 4.1 Generate `docs/human-briefs/2026-06-02-a100-sft-post-recovery-rerun.html` from OpenSpec artifacts, evidence files, and validation output.
- [x] 4.2 Run focused checks for formatting/prediction recovery behavior and evidence boundaries.
- [x] 4.3 Run `uv run ruff check .`, `uv run mypy src`, and `uv run pytest`.
- [x] 4.4 Run public dataset validation, DPO pair checks, post-recovery metrics, controlled smoke, leak-scan, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`, and `git diff --check`.
