## Why

The latest A100 train-split rerun shows strict final `json_valid_rate=0.0` and `contract_exact_match=0.0`: raw attempts are JSON objects but miss `task_type`, while retry attempts include the missing shape but remain prose/Markdown-wrapped JSON fragments for `3/3` rows. Stop-boundary trace evidence now shows this is not proven to be a max-token truncation problem, so the next narrow local fix is to tighten the retry JSON-only output boundary without relaxing parser or evaluator behavior.

## What Changes

- Strengthen the schema-retry prompt boundary so it states a machine-readable JSON-only contract more redundantly and concretely.
- Add prompt-policy metadata that proves the stricter retry boundary is visible in metadata and prompt snapshots.
- Add focused tests that first fail on the missing stricter boundary signals, then pass after the prompt-policy hardening.
- Publish a public-safe local evidence pack and Human Brief explaining the change, prior A100 context, validation, and non-claims.
- Keep strict parser behavior, evaluator metrics, prediction repair, prediction re-score, semantic-equivalence scoring, slot normalization, training, and A100 prediction reruns out of this phase.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `supervised-contract-tuning`: tighten the local schema-retry prompt/output-boundary policy while preserving strict parsing and prediction behavior.
- `contract-evaluation`: publish a public-safe local evidence pack proving the retry JSON-only boundary hardening and non-claim limits.

## Impact

- Affected code: `src/voice2task/training.py` retry prompt text and retry prompt constraint summary.
- Affected tests: focused retry prompt/metadata evidence tests in `tests/test_a100_sft_prediction_smoke.py`.
- Affected artifacts: a new local evidence pack under `reports/public-sample/tighten-retry-json-only-output-boundary/` and a Chinese Human Brief under `docs/human-briefs/`.
- No dependency changes, no training, no A100 execution, no public full-corpus release, no released checkpoint/adapter, and no live-browser benchmark improvement claim.
