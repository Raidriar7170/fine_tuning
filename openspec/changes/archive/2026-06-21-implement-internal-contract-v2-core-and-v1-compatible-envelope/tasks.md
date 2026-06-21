## 1. Tests First

- [x] 1.1 Add focused failing tests for ContractCoreV2 fields, V1 projection, immutable/no-mutation behavior, and invalid V1 fail-closed handling.
- [x] 1.2 Add focused failing tests for envelope metadata extraction, `preserve_legacy` exact V1 roundtrip, and internal-only provenance.
- [x] 1.3 Add focused failing tests for `derive_display` deterministic rendering, renderer unsupported fail-closed behavior, and old normalized_command isolation.
- [x] 1.4 Add focused failing tests for shadow compatibility aggregate/report gates and V1 evaluator regression zero-delta checks.

## 2. Internal Core And Envelope

- [x] 2.1 Implement `src/voice2task/contract_core_v2.py` with `ContractCoreV2`, `ContractEnvelopeMetadata`, typed errors, projection, validation, canonical JSON, compare, and roundtrip helpers.
- [x] 2.2 Reuse the existing deterministic normalized_command renderer for `derive_display` while keeping external rebuilt contracts V1-compatible.
- [x] 2.3 Implement shadow compatibility checking and aggregate compatibility matrix generation over current public-safe V1 contracts and recovered prediction contracts.

## 3. Minimal Integration And Evidence

- [x] 3.1 Add a minimal `voice2task-eval contract-core-v2-check` command or equivalent script that writes the compact evidence bundle.
- [x] 3.2 Generate `reports/public-sample/internal-contract-v2-core/summary.md`, `summary.json`, `compatibility-matrix.json`, `evaluator-regression.json`, and `decision.md`.
- [x] 3.3 Add `docs/contract-core-v2.md` and a concise Chinese Human Brief for the phase.
- [x] 3.4 Update README, README_en, CONTEXT, evidence index, and current-truth checker only as needed to reflect the internal V2 Core boundary without restating old evidence.

## 4. Validation And Closeout

- [x] 4.1 Verify focused red/green tests and the full suite with `PYTHONPATH=src pytest -q`.
- [x] 4.2 Verify lint with `PYTHONPATH=src ruff check src tests`.
- [x] 4.3 Verify OpenSpec with `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`.
- [x] 4.4 Verify current truth surface with `PYTHONPATH=src python scripts/check_current_truth_surface.py`.
- [x] 4.5 Verify whitespace and public safety with `git diff --check` and a public leak scan over changed public artifacts.
- [x] 4.6 Run a read-only reviewer pass, fix Must Fix items only, archive the OpenSpec change, then stop without starting slot-representation work.
