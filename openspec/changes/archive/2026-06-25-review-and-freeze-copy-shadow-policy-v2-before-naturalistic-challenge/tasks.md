## 1. Tests First

- [x] 1.1 Add focused tests for successful Policy V2 freeze output, inactive frozen policy invariants, per-scope frozen statuses, source hash recording, and recommended next change.
- [x] 1.2 Add focused fail-closed tests for drifted or executable proposal inputs and ensure no frozen policy is emitted on blocked validation.
- [x] 1.3 Add focused public-boundary tests for docs/report text and leak-scan coverage.

## 2. Freeze Implementation

- [x] 2.1 Implement a bounded Policy V2 freeze module that validates proposal/design inputs and writes blocked output on drift.
- [x] 2.2 Add a runner script that emits `configs/copy-backed-scope-policy-v2.frozen.json` and `reports/public-sample/copy-shadow-policy-v2-freeze/`.
- [x] 2.3 Ensure the frozen artifact remains inactive and no runtime loader, prediction hook, evaluator, prompt, decoding, training, or dataset path reads it as an active policy.

## 3. Evidence and Truth Surfaces

- [x] 3.1 Generate the frozen policy reference and compact freeze evidence from committed Policy V2 design artifacts.
- [x] 3.2 Refresh `CONTEXT.md`, README status surfaces, copy-shadow docs, evidence index artifacts, and the recommended-next-change surface.
- [x] 3.3 Generate `docs/human-briefs/2026-06-25-review-and-freeze-copy-shadow-policy-v2-before-naturalistic-challenge.html`.

## 4. Validation

- [x] 4.1 Run focused freeze tests and adjacent Policy V2 design/false-trust tests.
- [x] 4.2 Run `PYTHONPATH=src pytest -q`, `ruff check .`, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`, `PYTHONPATH=src python scripts/check_current_truth_surface.py`, `git diff --check`, and a public leak scan over README/CONTEXT/docs/reports/configs.
- [x] 4.3 Confirm Policy V1, challenge v1 rows/gold, predictions, sidecars, audits, evaluator behavior, runtime hooks, prompts/decoding, training data, and model artifacts were not modified.
- [x] 4.4 Stop after freeze evidence without creating naturalistic challenge v2, runtime enforcement, action enablement, normalized trusted provenance, training, data expansion, prediction repair, browser automation, or model/executable improvement claims.
