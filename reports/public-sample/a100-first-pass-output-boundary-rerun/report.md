# A100 first-pass output-boundary rerun

## Conclusion

The A100 prediction-only rerun confirms `prediction_output_boundary` is visible, but all 3 train-split predictions remain Markdown-wrapped fragments and strict schema-valid output remains 0/3.

## Evidence

- predictions: `reports/public-sample/a100-first-pass-output-boundary-rerun/predictions.jsonl`
- prediction_metadata: `reports/public-sample/a100-first-pass-output-boundary-rerun/prediction_metadata.json`
- prompt_snapshot: `reports/public-sample/a100-first-pass-output-boundary-rerun/prompt_snapshot.json`
- raw_decoded_summary: `reports/public-sample/a100-first-pass-output-boundary-rerun/raw_decoded_summary.jsonl`
- generation_trace: `reports/public-sample/a100-first-pass-output-boundary-rerun/generation_trace.jsonl`
- metrics_json: `reports/public-sample/a100-first-pass-output-boundary-rerun/metrics.json`
- schema_guard_summary: `reports/public-sample/a100-first-pass-output-boundary-rerun/schema_guard_summary.json`
- output_boundary_rerun_diagnosis: `reports/public-sample/a100-first-pass-output-boundary-rerun/output_boundary_rerun_diagnosis.json`

## Boundary

- A100 prediction-only, train-split-only evidence.
- No training, parser relaxation, evaluator metric change, prediction repair, prediction re-score, slot normalization, semantic-equivalence scoring, checkpoint release, or adapter release.
- Do not claim held-out generalization, production readiness, live-browser benchmark improvement, model recovery, or model-quality improvement.
