# Design

## Boundary
The canonical prediction surface is `voice2task-train sft-predict`, implemented by `voice2task.training.run_sft_prediction_export`. The hook runs after each prediction artifact has already been determined and written or after the completed prediction JSONL is available for legacy/private writer paths. It observes the existing prediction value and the matching `SFTDatasetRow.input_text`; it never repairs, replaces, suppresses, or rewrites the prediction.

## Configuration
Prediction configs MAY include:

```json
{
  "copy_backed_shadow": {
    "enabled": false,
    "policy_path": "configs/copy-backed-scope-policy-v1.json",
    "sidecar_output_path": null,
    "retain_span_text": false,
    "retain_input_text": false,
    "retain_raw_model_output": false,
    "fail_isolated": true
  }
}
```

Absent or malformed config defaults to disabled behavior. No environment variable enables the hook implicitly.

## Hook Outcome
The hook returns a bounded outcome with:
- `hook_status`
- optional `sidecar`
- optional `error_code`
- `trusted_provenance_count`
- `candidate_provenance_count`
- `sidecar_write_status`
- `main_prediction_unchanged`
- `exception_isolated`

Errors are mapped to bounded codes and do not expose tracebacks in public sidecars or reports.

## Sidecar Retention
Default sidecars retain hashes, offsets, policy identifiers, verification statuses, provenance booleans, and bounded failure reasons. They do not retain full input text, raw model output, full prediction contract, raw request ids, gold fields, or span text. `retain_span_text=true` is a local fixture/debug opt-in and remains false in public evidence.

## Trust Gate
Trusted provenance requires all of:
- `VERIFIED_EXACT_UNIQUE`
- `match_kind=exact`
- frozen policy enabled for the exact `(task_type, route, slot_path)`
- `candidate_span_count=1`
- `verify_source_span(source_text, span)` passes
- span hash and current input hash match
- back-sliced source text equals the predicted string value
- action disabled and normalized trusted disabled
- policy validation passed

`VERIFIED_NORMALIZED_UNIQUE` is candidate-only. All other statuses are untrusted.

## Evidence
The phase writes compact public-safe evidence under `reports/public-sample/copy-backed-prediction-shadow-hook/` and docs under `docs/copy-backed-prediction-shadow-hook.md`. Evidence reports invariance hashes, per-scope metrics, latency measurements, policy id/version/hash, privacy defaults, and the final bounded decision label.
