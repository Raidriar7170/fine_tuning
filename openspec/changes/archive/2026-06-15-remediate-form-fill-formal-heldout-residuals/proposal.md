## Why

The formal held-out target selection report identified `form_fill` as the first
bounded remediation target: 29 strict residual rows and 49 residual fields. The
project needs to split those failures into actionable remediation buckets before
changing data, training, gold policy, or evaluator behavior.

## What Changes

- Add a plan-only `form_fill` remediation diagnosis that classifies the selected
  residuals into canonical confirmation wording, field-name specificity, and
  clarify/route-boundary buckets.
- Recommend a bounded next implementation phase with acceptance criteria for
  any future data or training change.
- Publish public-safe JSON/Markdown evidence and a concise Chinese Human Brief.
- Preserve strict `contract_exact_match` and strict `slot_f1` as primary
  metrics; keep `slot_f1_soft` diagnostic-only.
- Do not generate new seeds, modify held-out splits, rewrite gold labels,
  retrain, run DPO, run A100 prediction, or change evaluator metrics.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `contract-evaluation`: add requirements for publishing a public-safe,
  plan-only `form_fill` remediation diagnosis from the selected formal held-out
  residual target.

## Impact

- Affected code/artifacts: evaluation/report helpers, eval CLI, tests,
  committed public-safe evidence under `reports/public-sample/`, and one Human
  Brief.
- No checkpoints, adapters, private paths, private corpus rows, raw logs,
  secrets, remote host details, or GPU jobs are introduced.
- No runtime browser behavior, public API, model weights, or evaluator metric
  semantics change.
