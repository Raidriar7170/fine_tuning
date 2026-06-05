## Why

The previous strict-string phases clarified that `normalized_command` mismatches remain exact-match failures, but the project still lacks an explicit target-writing policy for what the gold `normalized_command` should look like. Without that policy, a future prompt or A100 rerun can keep oscillating between valid-looking phrases such as `搜索北京明天天气`, `查询北京明天天气`, and `搜索北京明天的天气`.

## What Changes

- Define a public-safe `normalized_command` canonicalization policy for gold Browser Task Contract targets.
- Make the existing prompt/formatting surface expose the policy as target guidance, not as evaluator relaxation.
- Add tests that pin the current public-sample canonical targets and model-visible prompt policy.
- Preserve strict evaluator behavior: no semantic-equivalence scoring, no normalized-string metric, no prediction repair, no re-score, and no A100 execution.
- Generate a concise Chinese Human Brief and archived OpenSpec record for the phase.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `voice2task-dataset-preparation`: define `normalized_command` as a stable canonical intent phrase retained across schema-preserving augmentations.
- `supervised-contract-tuning`: expose the same canonicalization policy in SFT training text and trained-adapter prediction prompts.

## Impact

- Affected code: small prompt/formatting policy constants and summaries in `src/voice2task/formatting.py`.
- Affected tests: focused dataset/formatting/project-surface tests for canonical target policy and non-metric boundaries.
- Affected docs/evidence: README or public policy note plus Chinese Human Brief/loop report.
- No A100 execution, training, prediction rerun, evaluator metric change, semantic-equivalence scoring, prediction repair, checkpoint/adapter publication, dependency change, or public full-corpus release.
