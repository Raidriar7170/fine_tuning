## Why

The new form-fill policy identifies `missing_confirmation_marker` as the largest observed policy section, but the repository already contains an older form-fill remediation design, materialization, merge, and held-out evaluation chain. Before creating more data, changing prompts, or retraining, the project needs a public-safe coverage assessment that compares the new confirmation-marker policy evidence with the existing remediation artifacts.

## What Changes

- Add a deterministic coverage assessment that reads the committed form-fill confirmation policy and existing form-fill remediation design/materialization/merge/evaluation artifacts.
- Report whether the existing remediation chain covers the confirmation-marker policy surface, where it is thin, and which bounded next action is justified.
- Publish JSON, Markdown, and manifest artifacts under `reports/public-sample/`.
- Generate a concise Human Brief for this coverage-assessment phase.
- Preserve assessment-only boundaries: no new candidate rows, no dataset mutation, no prompt change, no prediction run, no training, no evaluator relaxation, no prediction repair/re-score, and no checkpoint/adapter release.

## Capabilities

### New Capabilities

### Modified Capabilities

- `contract-evaluation`: require a public-safe confirmation-marker coverage assessment before any further confirmation-marker data, prompt, training, or evaluator remediation.

## Impact

- Affected code: evaluation/report helpers and CLI entry point for the confirmation-marker coverage assessment.
- Affected reports: add a new public-safe coverage report under `reports/public-sample/`.
- Affected tests: add focused tests for source artifact consistency, coverage decision boundaries, public-safety scanning, and claim boundaries.
- Affected specs: extend `contract-evaluation` with a confirmation-marker coverage-assessment evidence requirement.
- Non-goals: generic chat fine-tuning, skill routing, GUI action policy learning, first-phase GRPO, public release of the full local corpus, any new prediction/training run, dataset materialization, prompt change, evaluator relaxation, prediction repair, checkpoint release, adapter release, production readiness, live-browser benchmark improvement, private-corpus generalization, or public full-corpus release claims.
