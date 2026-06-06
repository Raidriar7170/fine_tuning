# A100 public-readonly search policy train-split rerun

Status: train-internal public-readonly search policy observation. This is not a benchmark, not a release, and no held-out generalization claim is made.

## Result

The rerun produced `3` train predictions from the private A100 adapter path. The prediction metadata shows `public_readonly_search_policy_visible=True`, `public_readonly_safety_reason_visible=True`, `search_query_slot_guidance_visible=True`, and `task_type_not_route_enum_visible=True`.

Observed strict final-contract `json_valid_rate=0.0000` and `contract_exact_match=0.0000`.
All three raw outputs emitted the public-readonly field bundle (`route=search_web`, `safety.reason=public_readonly`, `confirmation_required=false`, and `slots.query`), but all three also remained strict schema-invalid because the raw JSON was malformed and `task_type` still used the route enum value `search_web`.
Compared with the previous normalized-command rerun, this is not full train-row recovery; strict JSON validity regressed from `1/3` to `0/3` while preserving useful field-level negative evidence.

## Public Artifacts

- Predictions: `reports/public-sample/a100-public-readonly-search-policy-train-split-rerun/predictions.jsonl`
- Train gold subset used for metrics: `reports/public-sample/a100-public-readonly-search-policy-train-split-rerun/train_split_gold.jsonl`
- Metrics: `reports/public-sample/a100-public-readonly-search-policy-train-split-rerun/metrics.json` / `reports/public-sample/a100-public-readonly-search-policy-train-split-rerun/metrics.md`
- Schema guard summary: `reports/public-sample/a100-public-readonly-search-policy-train-split-rerun/schema_guard_summary.json` / `reports/public-sample/a100-public-readonly-search-policy-train-split-rerun/schema_guard_summary.md`
- Public-readonly search policy diagnosis: `reports/public-sample/a100-public-readonly-search-policy-train-split-rerun/public_readonly_search_policy_diagnosis.json` / `reports/public-sample/a100-public-readonly-search-policy-train-split-rerun/public_readonly_search_policy_diagnosis.md`
- Prompt snapshot: `reports/public-sample/a100-public-readonly-search-policy-train-split-rerun/prompt_snapshot.json`
- Raw decoded summary: `reports/public-sample/a100-public-readonly-search-policy-train-split-rerun/raw_decoded_summary.jsonl`
- Generation trace: `reports/public-sample/a100-public-readonly-search-policy-train-split-rerun/generation_trace.jsonl`
- Prediction metadata: `reports/public-sample/a100-public-readonly-search-policy-train-split-rerun/prediction_metadata.json`
- Manifest: `reports/public-sample/a100-public-readonly-search-policy-train-split-rerun/manifest.json`

## Boundary

The evidence pack contains sanitized public-sample contract predictions, aggregate metrics, schema guard summaries, row-level public-readonly search diagnosis, and leak-scan status. It does not copy raw logs, checkpoints, adapters, remote caches, private configs, host details, tokens, SSH details, or private corpus rows into git.

No semantic-equivalence scoring, slot normalization, normalized-command normalization, evaluator metric relaxation, prediction repair, re-score, SFT/DPO/GRPO training, checkpoint release, adapter release, production-readiness claim, held-out generalization claim, model-quality claim, or live-browser benchmark improvement claim is made.
