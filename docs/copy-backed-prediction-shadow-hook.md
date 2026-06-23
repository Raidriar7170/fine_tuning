# Copy-backed Prediction Shadow Hook

This document records the bounded prediction-pipeline hook added by
`integrate-copy-backed-verification-prediction-shadow-hook`.

## Integration Point

The hook is attached to `voice2task-train sft-predict` through
`voice2task.training.run_sft_prediction_export`. It runs only after the existing
prediction artifact row has already been determined.

## Feature Flag

The hook is controlled by the prediction config field `copy_backed_shadow`.
Missing config or `enabled=false` keeps previous prediction output and metadata
behavior.

```json
{
  "copy_backed_shadow": {
    "enabled": true,
    "policy_path": "configs/copy-backed-scope-policy-v1.json",
    "sidecar_output_path": "reports/public-sample/example-copy-shadow.jsonl",
    "retain_span_text": false,
    "retain_input_text": false,
    "retain_raw_model_output": false,
    "fail_isolated": true
  }
}
```

## Default Behavior

The default is disabled. Disabled configs create no copy-backed shadow sidecar
file and do not add `copy_backed_shadow` metadata.

## Sidecar Only

Enabled hook output is sidecar-only. `sidecar_output_path=null` computes an
in-memory summary with `NullShadowSink`; a path writes compact JSONL sidecars
through `JsonlShadowSink`. Sidecars are never mixed into prediction JSONL.

## Failure Isolation

Malformed JSON, empty predictions, unsupported prediction values, schema-invalid
BrowserTaskContract V1 objects, policy failures, verifier errors, serialization
errors, and sink write failures are recorded as bounded shadow statuses. The
primary prediction row, caller status, and prediction output file are not
repaired or changed.

## Policy Validation

Before trusted provenance can be emitted, `copy-backed-scope-policy-v1` must pass
full validation: non-empty id/version, expected id, hash algorithm, matching
policy hash, unique and disjoint enabled/disabled triples, unique scope rows,
scope rows equal enabled plus disabled sets, enabled rows equal enabled triples,
disabled rows equal disabled triples, `action_enabled=false`,
`normalized_trusted=false`, and the frozen enabled triples
`search:search_web:query`, `form_fill:fill_form:field`, and
`extract:extract_page:target`.

## Trust Semantics

Trusted provenance is exact-only: `VERIFIED_EXACT_UNIQUE`, exact match kind, one
candidate span, enabled scope, current input hash, valid offsets/hash, and
back-slice equality to the predicted value. `VERIFIED_NORMALIZED_UNIQUE` remains
candidate-only. `action` remains disabled and untrusted.

## Privacy Defaults

Default sidecars are hash-and-offset-only. They omit full input text, raw model
output, full prediction contracts, raw request ids, gold/evaluator fields, and
`source_span.text`. Source spans contain start, end, source text hash, and span
hash. Span text is available only through explicit local debug opt-in.

`retain_input_text` and `retain_raw_model_output` are reserved compatibility
fields in this phase; setting them does not cause input text or raw model output
to be retained. `fail_isolated` is also effectively mandatory: the hook always
isolates shadow failures from the primary prediction path.

## Output Invariance

Public evidence under
`reports/public-sample/copy-backed-prediction-shadow-hook/` shows disabled,
NullSink, and JsonlSink prediction output hashes are identical:
`76ca6ab416293825dc01eac35b7a13cec35ee2f770483e09d3cb00613900c173`. V1 metric
deltas are all 0, contract mutation count is 0, runtime decision delta count is
0, and deterministic rerun is true when ignoring `hook_latency_ms`.

## Latency Boundary

The local latency benchmark is diagnostic only and is not a production SLO. It
measures prediction-result observation, policy lookup, contract read, slot
extraction, exact verification, normalized diagnostic generation, sidecar build,
serialization, and optional local JSONL write.

## Claim Boundary

Source provenance is not task correctness. This hook does not enable runtime
enforcement, prediction repair, action provenance, normalized trusted
provenance, training, evaluator changes, schema migration, model improvement
claims, executable quality claims, production readiness, safety readiness, or
challenge-set generalization claims.

## Evidence

- `reports/public-sample/copy-backed-prediction-shadow-hook/summary.json`
- `reports/public-sample/copy-backed-prediction-shadow-hook/integration-audit.json`
- `reports/public-sample/copy-backed-prediction-shadow-hook/per-scope-metrics.json`
- `reports/public-sample/copy-backed-prediction-shadow-hook/latency-benchmark.json`
- `reports/public-sample/copy-backed-prediction-shadow-hook/sample-online-sidecars.jsonl`

Decision: `PREDICTION_SHADOW_HOOK_READY_OBSERVE_ONLY`.

The only recommended next change is
`evaluate-frozen-copy-shadow-policy-on-template-disjoint-challenge-set`.
