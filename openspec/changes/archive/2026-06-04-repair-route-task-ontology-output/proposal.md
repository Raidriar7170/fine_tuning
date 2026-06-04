## Why

The latest constrained-output A100 train-split rerun reached the repaired prompt/parser path but still produced `0/3` schema-valid outputs. The most actionable local failure slice is route/task ontology drift: one raw JSON object used `route="weather"` even though Browser Task Contract `route` is an execution-channel enum, not a domain, topic, URL, or path.

## What Changes

- Strengthen the model-visible SFT training and prediction prompt so `route` is explicitly framed as a Browser Task Contract execution channel.
- Add route ontology examples that keep domain intents such as weather/search targets inside `task_type`, `slots`, and `normalized_command` rather than inventing route values.
- Record public-safe local evidence that this phase updated prompt constraints only and did not run training, private A100 prediction, schema repair, or model-output coercion.
- Add focused tests before implementation to protect the route-ontology prompt boundary and evidence contract.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `supervised-contract-tuning`: model-visible SFT training and prediction prompts must distinguish route execution-channel enums from domain/topic/URL/path values.
- `contract-evaluation`: public reports for local route-ontology repairs must preserve non-claim boundaries and must not imply model recovery without a later authorized rerun.

## Impact

- Affected code: SFT/prediction prompt formatting and prompt constraint metadata.
- Affected tests: focused prompt-formatting and local evidence tests.
- Affected artifacts: public-safe local evidence under `reports/public-sample/` and a Chinese Human Brief under `docs/human-briefs/`.
- Non-goals: no generic chat fine-tuning, no skill routing, no GUI action policy learning, no first-phase GRPO, no public release of the full local corpus, no training, no DPO, no private A100 execution, no checkpoint or adapter release, no production-readiness claim, no dev/test generalization claim, and no live-browser benchmark improvement claim.
