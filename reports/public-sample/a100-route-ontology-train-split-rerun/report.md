# A100 Route Ontology Train-Split Rerun

Status: train-internal route ontology diagnostic evidence. This is not a benchmark, not a release, and no held-out generalization claim is made.

## Result

The rerun produced `3` train predictions from the private A100 adapter path. The prompt constraints include route execution-channel visibility `True`, route domain/topic exclusion `True`, and the weather-to-search route example `True`.

Observed strict final-contract Browser Task Contract `json_valid_rate=0.0000`, `contract_exact_match=0.0000`, and `route_accuracy=0.0000`. This strict final-contract route accuracy is computed only after strict schema validation, so schema-invalid final predictions do not receive route credit.

raw route ontology / gold-route match: `3/3`. Raw route value counts are `{'search_web': 3}`, and route enum-valid predictions are `3/3`.

Schema guard observed raw schema-valid `0/3`, retry schema-valid `0/3`, and final validated schema-valid `0/3`. All final predictions remain invalid because the raw attempt omits `confirmation_required`; no schema repair or output coercion was applied.

## What Changed Versus Baseline

- The route ontology prompt repair reached the A100 prediction path.
- The previous weather/domain route symptom is not present in these final predictions: observed route values are `search_web`.
- The remaining failure is required-field/schema completeness, not route enum selection.

## Public Artifacts

- Predictions: `reports/public-sample/a100-route-ontology-train-split-rerun/predictions.jsonl`
- Train gold subset used for metrics: `reports/public-sample/a100-route-ontology-train-split-rerun/train_split_gold.jsonl`
- Metrics: `reports/public-sample/a100-route-ontology-train-split-rerun/metrics.json` / `reports/public-sample/a100-route-ontology-train-split-rerun/metrics.md`
- Schema guard summary: `reports/public-sample/a100-route-ontology-train-split-rerun/schema_guard_summary.json` / `reports/public-sample/a100-route-ontology-train-split-rerun/schema_guard_summary.md`
- Route ontology diagnosis: `reports/public-sample/a100-route-ontology-train-split-rerun/route_ontology_diagnosis.json` / `reports/public-sample/a100-route-ontology-train-split-rerun/route_ontology_diagnosis.md`
- Prompt snapshot: `reports/public-sample/a100-route-ontology-train-split-rerun/prompt_snapshot.json`
- Raw decoded summary: `reports/public-sample/a100-route-ontology-train-split-rerun/raw_decoded_summary.jsonl`
- Generation trace: `reports/public-sample/a100-route-ontology-train-split-rerun/generation_trace.jsonl`
- Prediction metadata: `reports/public-sample/a100-route-ontology-train-split-rerun/prediction_metadata.json`
- Manifest: `reports/public-sample/a100-route-ontology-train-split-rerun/manifest.json`

## Boundary

The evidence pack contains sanitized public-sample contract predictions, aggregate metrics, schema guard summaries, route ontology diagnosis, and leak-scan status. It does not copy raw logs, checkpoints, adapters, remote caches, private configs, host details, tokens, SSH details, or private corpus rows into git.

Claim boundaries: no checkpoint release, no adapter release, no held-out generalization claim, no production-readiness claim, no public full-corpus release, no model-quality claim, and no live-browser benchmark improvement claim.

## Recommended Next Step

Reviewer re-review passed after the route-metric consistency fix. The next small phase should target required-field emission for `confirmation_required` under the route-ontology prompt path, but it should be proposed as a separate bounded OpenSpec change rather than mixed into this A100 evidence phase.
