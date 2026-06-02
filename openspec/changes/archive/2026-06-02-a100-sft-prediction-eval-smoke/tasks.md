## 1. Prediction Export

- [x] 1.1 Add a trained-path public-sample prediction export surface that requires explicit opt-in and fails closed without private adapter configuration.
- [x] 1.2 Add a deterministic fixture-mode prediction path for local tests and public evidence generation without loading private model artifacts.
- [x] 1.3 Add tests proving prediction export does not copy checkpoints, adapters, raw logs, private paths, caches, or secrets into committed artifacts.

## 2. Evidence Pack

- [x] 2.1 Generate sanitized public-sample trained-path prediction JSONL under `reports/public-sample/`.
- [x] 2.2 Run contract metrics and controlled execution smoke against the sanitized trained-path predictions.
- [x] 2.3 Write a machine-readable manifest and human-readable report that record prediction provenance, metrics, controlled smoke status, leak-scan status, release status, and claim boundaries.
- [x] 2.4 Extend leak-scan validation to cover the trained-prediction evidence pack and reject oversized generated corpora or private artifact leakage.

## 3. Documentation And Validation

- [x] 3.1 Update README/runbook wording for the trained-prediction smoke without hostnames, IPs, secrets, SSH details, private paths, checkpoint release claims, or live-browser improvement claims.
- [x] 3.2 Generate a concise Chinese Human Brief HTML for this phase from OpenSpec artifacts, evidence files, and validation output.
- [x] 3.3 Run `uv run ruff check .`, `uv run mypy src`, and `uv run pytest`.
- [x] 3.4 Run public dataset validation, DPO pair checks, contract metrics, controlled smoke, leak-scan, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`, and `git diff --check`.
