# diagnose-scaled-public-sample-current-123-adapter-residuals

## Why

The A100 recovery retry produced observed prediction-only evidence on the
scaled formal public sample manifest `public-sample-20260617T152259Z`.
The structural tiers remain stable (`json_valid_rate=1.0`, route accuracy above
0.96, safety recall 1.0), but strict `contract_exact_match` and strict
`slot_f1` dropped sharply on the scaled dev/test splits.

Before any paired SFT retry, data materialization, prompt change, DPO run, or
evaluator change, the project needs a bounded diagnosis that identifies which
families and field paths dominate the new scaled-boundary strict residuals.

## What Changes

- Generate public-safe formal held-out residual-family diagnosis from the
  latest scaled-manifest A100 recovery prediction evidence.
- Preserve a tiered interpretation of the scaled metrics: schema/route/safety
  are strong, strict slot and full-contract exact are weak.
- Update `CONTEXT.md`, `reports/final_status.md`, and a short Chinese Human
  Brief with the diagnosis result and recommended next bounded decision.
- Add focused tests for the diagnosis evidence and claim boundaries.
- Archive this OpenSpec change after validation.

## Out of Scope

- No SFT or DPO training.
- No new seed rows, candidate rows, DPO pairs, or manifest rebuild.
- No A100 job, prediction rerun, prompt change, evaluator metric change, slot
  normalization, prediction repair, or prediction replacement.
- No checkpoint/adapter release, production-readiness claim, private-corpus
  generalization claim, or live-browser benchmark claim.

## Impact

- Affected evidence: `reports/public-sample/scaled-current-123-adapter-residual-diagnosis/`.
- Affected docs: `CONTEXT.md`, `reports/final_status.md`, and a new Human Brief.
- Affected capability: `contract-evaluation` public-safe residual diagnosis
  evidence for the scaled formal public sample boundary.
