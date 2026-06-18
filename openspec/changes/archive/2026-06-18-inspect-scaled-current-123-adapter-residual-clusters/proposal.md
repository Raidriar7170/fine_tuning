# inspect-scaled-current-123-adapter-residual-clusters

## Why

The latest scaled-manifest residual diagnosis shows strict failures are
dominated by `slots` and `normalized_command`, but the evidence is still too
coarse to decide whether the next phase should be data design, paired SFT
readiness, policy hardening, or no further training.

Before any data materialization, SFT retry, DPO run, prompt change, evaluator
change, or slot normalization, the project needs a bounded cluster inspection
that turns those dominant residual fields into reviewable, public-safe failure
clusters.

## What Changes

- Generate a public-safe scaled residual-cluster inspection report from the
  committed scaled residual diagnosis evidence.
- Group residuals by actionable cluster dimensions such as task family, source
  family, field path, residual category, and repeated gold/prediction patterns.
- Preserve strict metric authority: `contract_exact_match` and strict
  `slot_f1` remain the headline; `slot_f1_soft` remains diagnostic-only.
- Update `CONTEXT.md`, `reports/final_status.md`, and a concise Chinese Human
  Brief with the cluster-inspection result and the next bounded decision.
- Add focused tests for cluster counts, source-boundary preservation, and
  public-safe claim boundaries.
- Archive this OpenSpec change after validation.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `contract-evaluation`: add requirements for public-safe scaled residual
  cluster inspection without changing evaluator semantics or model artifacts.

## Impact

- Affected evidence:
  `reports/public-sample/scaled-current-123-adapter-residual-cluster-inspection/`.
- Affected docs: `CONTEXT.md`, `reports/final_status.md`, and a new Human Brief.
- Affected tests: focused formal residual-cluster inspection tests.
- No training, prediction rerun, data mutation, prompt change, evaluator
  relaxation, DPO/GRPO run, checkpoint release, adapter release, public full
  corpus release, generic chat fine-tuning, skill routing, GUI action policy
  learning, or live-browser benchmark claim.
