## 1. Boundary and Adapter Recovery

- [x] 1.1 Add tests for frozen challenge hash, row count, gold hash, template-disjoint audit, policy hash, action-disabled, normalized-trusted-disabled, and active OpenSpec boundary checks.
- [x] 1.2 Add tests for adapter identity pass, adapter identity mismatch, adapter unavailable, unresolved private root, and private override sanitization.
- [x] 1.3 Implement public-safe adapter discovery, private override loading, identity verification, adapter content hashing, and blocked decision selection.
- [x] 1.4 Generate `adapter-identity-audit.json` with sanitized identity fields and no private paths.

## 2. Canonical Prediction and Hook Evaluation

- [x] 2.1 Add tests proving the canonical `run_sft_prediction_export` path is invoked for challenge prediction and standalone verifier/prediction fabrication is not used.
- [x] 2.2 Implement prediction-only challenge runner for verified adapters with shadow disabled, enabled NullSink, and enabled JsonlSink boundaries.
- [x] 2.3 Prove prediction output hash, parsed contract, evaluator input, exit status, runtime decision, V1 metric, and sidecar path invariance.
- [x] 2.4 If adapters are unavailable or unverifiable, write the bounded `blocked.json` and stop without fabricated predictions.

## 3. Online Sidecars and Offline Audits

- [x] 3.1 Add tests that online sidecars contain no gold, no full input text, no span text, no raw model output, no private path, exact-only trusted provenance, normalized candidate-only, and action disabled.
- [x] 3.2 Implement offline evaluation audit generation after prediction and sidecar artifacts are frozen.
- [x] 3.3 Report duplicate/source-absent/normalization-collision/partial-span/out-of-scope-action false-trust counts, invalid-output fail isolation, and provenance false accepts.
- [x] 3.4 Write public-safe predictions, online sidecars, and evaluation audits under `reports/public-sample/copy-shadow-template-disjoint-challenge-v1/adapter-evaluation/` only when inference runs.

## 4. Metrics, Docs, and Truth Surfaces

- [x] 4.1 Generate `prediction-run-audit.json`, `challenge-evaluation-summary.json/md`, `per-scope-metrics.json`, `per-condition-metrics.json`, `hook-safety-audit.json`, `latency-benchmark.json`, and `recommended-next-change.md`.
- [x] 4.2 Update `docs/copy-shadow-template-disjoint-challenge.md`, README/README_en/CONTEXT/evidence-index, and a Chinese Human Brief with the verifier-fixture boundary and bounded decision.
- [x] 4.3 Select exactly one decision label: `CHALLENGE_V1_VERIFIER_VALIDATED_OBSERVE_ONLY`, `CHALLENGE_V1_VALIDATED_WITH_SCOPE_LIMITATIONS`, `CHALLENGE_V1_HOOK_UNSAFE_OR_INVALID`, `CHALLENGE_EVALUATION_BLOCKED_ADAPTER_UNAVAILABLE`, `CHALLENGE_EVALUATION_BLOCKED_ADAPTER_IDENTITY`, or `CHALLENGE_EVALUATION_BLOCKED_BOUNDARY_MISMATCH`.

## 5. Verification, Review, and Archive

- [x] 5.1 Run `PYTHONPATH=src pytest -q`, `ruff check .`, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`, `python scripts/check_current_truth_surface.py`, `git diff --check`, public leak scan, adapter identity audit check, challenge/policy freeze checks, and prediction output invariance checks when predictions exist.
- [x] 5.2 Run a read-only Reviewer subagent over the final diff and fix Must Fix findings only.
- [x] 5.3 Archive the OpenSpec change and stop without training, policy modification, enforcement, challenge v2 creation, action enablement, or normalized trusted provenance.
