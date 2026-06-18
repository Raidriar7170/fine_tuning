## Why

The residual-driven target selection found one current unsafe false-negative
signal in layered evaluation. Even though the count is small, safety mistakes
have higher execution risk than ordinary slot wording residuals, so the next
bounded phase should design public-safe safety repair candidates before any
data merge, prediction rerun, or training.

## What Changes

- Add design-only safety repair candidate evidence under
  `reports/public-sample/safety-repair-candidate-design/`.
- Read the committed remediation target-selection, layered-eval, and
  residual-diagnosis artifacts as current public-safe evidence.
- Propose public-safe safety-boundary candidate themes for unsafe downgrade,
  confirmation-drop, and clarify-vs-blocked drift patterns.
- Record accepted target sketches, rejected drift sketches, source evidence
  counts, allowed follow-up operations, non-goals, and claim boundaries.
- Add tests that enforce design-only scope and public leak-scan cleanliness.
- Non-goals: generic chat fine-tuning, skill routing, GUI action policy
  learning, first-phase GRPO, public release of the full local corpus,
  materializing seed rows, mutating public samples, changing train/dev/test
  splits, training, prediction reruns, evaluator relaxation, LLM judging,
  semantic-equivalence scoring, prediction repair, checkpoint/adapter release,
  production-readiness claims, safety-readiness claims, held-out recovery
  claims, and live-browser benchmark claims.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `voice2task-dataset-preparation`: add public-safe safety repair candidate
  design evidence before any future materialization or training phase.

## Impact

- New or updated design-report code under `src/voice2task/`.
- New public-safe design artifacts under
  `reports/public-sample/safety-repair-candidate-design/`.
- New focused tests under `tests/`.
- New OpenSpec archive material and a Human Brief HTML for this phase.
