# A100 Constrained-Output Schema Guard Summary

This summary separates raw attempt parsing, retry attempt parsing, schema validity, and final validated output source. It does not repair or replace model outputs.

## Counts

- Predictions: `3`
- Raw attempt schema-valid: `0/3`
- Retry attempt schema-valid: `0/3`
- Final validated schema-valid: `0/3`
- Retry fragments rejected by strict parser: `3/3`

## Prompt Constraints

- `canonical_json_one_shot_visible`: `True`
- `required_field_checklist_visible`: `True`
- `required_field_skeleton_visible`: `True`
- `route_enum_visible`: `True`
- `route_not_url_or_path_visible`: `True`
- `slots_object_not_array_visible`: `True`
- `task_type_enum_visible`: `True`
- `whole_object_boundary_visible`: `True`

## Parse Status Counts

### Raw Attempt

- `json_object`: `1`
- `non_json`: `2`

### Retry Attempt

- `json_fragment_object`: `3`

## Interpretation

- The constrained-output prompt reached the A100 prediction path: canonical one-shot and whole-object boundary rules are visible.
- The adapter still produced `0/3` schema-valid final Browser Task Contracts on the train split.
- The main remaining failures are invalid route/task shape in raw outputs and Markdown/prose-wrapped retry fragments.
- This is train-internal diagnostic evidence only, not a generalization or model-quality claim.
