# Route/task ontology output repair summary

Status: local prompt repair only. This is not A100 improvement evidence and does not prove model recovery.

## What changed

- Strengthened the shared Voice2Task prompt so `route` is described as a Browser Task Contract execution-channel enum.
- Added an explicit boundary that `route` is not a domain, topic, intent, URL, or path value.
- Added a weather example that keeps the weather intent in `task_type`, `slots`, and `normalized_command`: weather requests use `task_type=search` and `route=search_web`.
- Kept prediction prompts target-safe: the current row's gold contract is still excluded from the prediction prompt.
- Did not add schema aliases, output repair, or output coercion.

## Prior evidence context

- Prior A100 constrained-output train-split rerun: `reports/public-sample/a100-constrained-output-train-split-rerun/`.
- The row `seed-search-weather` produced a JSON object with invalid `route` value `weather`.
- The corresponding public-safe gold row uses `task_type=search`, `route=search_web`, and weather details in `slots` / `normalized_command`.
- That prior run remained `0/3` schema-valid and must not be reinterpreted as recovered by this local phase.

## Prompt constraints

- `task_type_enum_visible`: true
- `route_enum_visible`: true
- `route_not_url_or_path_visible`: true
- `route_execution_channel_visible`: true
- `route_domain_values_not_route_visible`: true
- `weather_to_search_route_example_visible`: true
- `slots_object_not_array_visible`: true
- `required_field_skeleton_visible`: true
- `required_field_checklist_visible`: true
- `canonical_json_one_shot_visible`: true
- `whole_object_boundary_visible`: true

## Validation

- `PYTHONPATH=src pytest -q` focused route ontology/evidence tests: 4 passed.
- `PYTHONPATH=src pytest -q tests/test_formatting_training.py tests/test_a100_sft_prediction_smoke.py`: 52 passed.
- `PYTHONPATH=src pytest -q`: 136 passed.
- `uv run ruff check .`: All checks passed.
- `uv run mypy src`: Success, 16 source files.
- `voice2task.cli.data validate --public`: ok, 12 SFT rows, 26 DPO pairs.
- `voice2task.cli.data dpo-check`: ok, 26 DPO pairs.
- `PYTHONPATH=src python -m voice2task.cli.report leak-scan reports/public-sample/route-task-ontology-output-repair docs/human-briefs/2026-06-04-repair-route-task-ontology-output.html openspec/changes/repair-route-task-ontology-output --output reports/public-sample/route-task-ontology-output-repair/leak_scan_result.json`: ok true, 0 findings.
- `git diff --check`: passed.
- `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`: 5 passed, 0 failed before archive.
- `OPENSPEC_TELEMETRY=0 openspec archive repair-route-task-ontology-output -y`: specs updated, change archived.
- `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`: 4 passed, 0 failed after archive.

## Boundary

- This phase did not train.
- This phase did not run private prediction or A100 execution.
- This phase did not repair or coerce model outputs.
- This phase does not prove model recovery.
- This phase does not prove held-out generalization, checkpoint release, adapter release, production readiness, public full-corpus release, or live-browser benchmark improvement.

## Recommended next step

After archive and guarded integration, a later separately authorized A100 rerun can test whether the prompt repair changes actual adapter outputs.
