## Context

The latest public truth surface is the SFT v3 retry evidence under
`reports/public-sample/a100-form-fill-remediation-sft-v3-retry-after-ssh-recovery/`.
It uses the current formal public manifest `public-sample-20260616T074315Z` and
the same dev/test split counts as the prediction-only baseline under
`reports/public-sample/a100-formal-public-heldout-prediction-after-a100-recovery/`.

The retry improved dev `contract_exact_match` and strict `slot_f1`, but dev
`safety_recall` moved from `0.6667` to `0.5556`. Because safety false
negatives are a stronger project risk than slot wording differences, the next
phase should diagnose the regression before any new training or data change.

## Goals / Non-Goals

**Goals:**

- Identify gold stop rows in the current formal public dev/test splits.
- Compare baseline and SFT v3 retry predictions for safety false negatives and
  false positives.
- Summarize regressions, recoveries, and unchanged safety misses by row id,
  task family, task type, route, and sanitized command/slot summaries.
- Produce public-safe machine-readable and human-readable evidence.
- Recommend a next bounded action based on observed failure clusters.

**Non-Goals:**

- No training, prediction generation, prompt change, data mutation, evaluator
  change, semantic-equivalence scoring, prediction repair, or safety policy
  rewrite.
- No public adapter/checkpoint release, private corpus release, live-browser
  benchmark, or production-readiness claim.

## Decisions

1. **Use existing artifacts only.**
   The diagnosis reads committed gold rows, baseline predictions/metrics, and
   SFT v3 retry predictions/metrics. It does not touch A100 or load a model.
   This keeps the phase fast, reproducible, and reviewable.

2. **Diagnose at row level, report publicly at sanitized level.**
   Row ids, task families, safety labels, and concise public-sample command
   snippets are acceptable. Private paths, raw logs, private overrides, and
   adapter metadata remain out of the report.

3. **Separate regression from absolute weakness.**
   A row can be:
   - `regressed`: baseline was safety-correct, retry is safety-wrong.
   - `recovered`: baseline was safety-wrong, retry is safety-correct.
   - `persistent_miss`: both are safety-wrong.
   - `stable_correct`: both are safety-correct.
   This prevents treating all current false negatives as caused by SFT v3.

4. **Keep recommendations bounded.**
   The output may recommend a future data/policy/training phase, but it must
   not materialize data or launch training as part of this diagnosis.

## Risks / Trade-offs

- Small dev/test safety support can make deltas noisy -> report support counts
  alongside rates.
- Public-sample commands are sanitized but still row-level -> keep summaries
  concise and rely on leak scan before commit.
- A regression can be caused by sampling composition rather than `form_fill`
  remediation itself -> report this as evidence, not causal proof.
