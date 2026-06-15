## Why

The formal held-out residual-family diagnosis identified 97 strict residual
rows, but the project still needs a bounded, evidence-backed decision about
which residual family should be remediated first. This change turns the
diagnosis into a public-safe next-target selection report before any data,
training, DPO, or evaluator-policy change.

## What Changes

- Add a formal held-out remediation-target selection artifact that ranks
  residual task families using existing committed diagnosis evidence.
- Recommend exactly one first remediation target, with explicit reasons,
  non-goals, and follow-up acceptance boundaries.
- Preserve strict `contract_exact_match` and strict `slot_f1` as primary
  metrics; keep `slot_f1_soft` diagnostic-only.
- Do not launch A100 jobs, generate data, retrain, run DPO, rewrite gold labels,
  repair predictions, or change evaluator behavior.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `contract-evaluation`: add requirements for publishing a public-safe
  remediation-target selection report from formal held-out residual diagnosis.

## Impact

- Affected code/artifacts: report generation, committed public-safe evidence
  under `reports/public-sample/`, a concise Chinese Human Brief, and tests.
- No model checkpoints, adapters, private paths, private corpus rows, raw logs,
  secrets, or A100 host details are added.
- No runtime dependencies or public APIs change.
