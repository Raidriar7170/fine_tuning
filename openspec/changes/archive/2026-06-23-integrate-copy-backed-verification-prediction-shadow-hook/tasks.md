# Tasks

- [x] Add red/green tests for config default-off behavior, NullSink/JsonlSink output invariance, invalid prediction fail isolation, policy/sink/verifier fault isolation, privacy defaults, exact-only trust, normalized candidate-only, action untrusted, and post-artifact private-writer behavior.
- [x] Implement the prediction shadow hook module, outcome model, config parser, Null/JSONL sinks, hash-and-offset sidecar schema, bounded statuses, and deterministic serialization.
- [x] Strengthen frozen scope-policy validation and update existing online shadow interface policy-version/span-retention behavior without changing offline EvaluationAudit semantics.
- [x] Integrate the hook into `run_sft_prediction_export` as an explicit opt-in observe-only post-prediction path that preserves prediction output JSONL and existing metadata behavior.
- [x] Add compact public-safe evidence generation under `reports/public-sample/copy-backed-prediction-shadow-hook/`, including invariance, per-scope metrics, latency, leak scan, deterministic rerun, and final decision label.
- [x] Update `docs/copy-backed-prediction-shadow-hook.md`, README/README_en/CONTEXT/EVIDENCE_INDEX, and a concise Chinese Human Brief with bounded claims and the next recommended change.
- [x] Mechanically fix the two known historical script lint issues or add the smallest justified file-level exception if semantic-preserving lint cleanup is not possible.
- [x] Run full verification: `PYTHONPATH=src pytest -q`, `ruff check .`, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`, `python scripts/check_current_truth_surface.py`, `git diff --check`, public leak scan, output invariance, and deterministic rerun.
