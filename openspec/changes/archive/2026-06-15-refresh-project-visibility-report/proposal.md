## Why

The repository now contains a more authoritative formal public held-out
prediction evidence pack for manifest `public-sample-20260615T111316Z`, but the
top-level README and experiment report still foreground older dev128 and
small-public-sample results. That makes the project look stronger and narrower
than the current evidence supports.

## What Changes

- Refresh the Chinese and English README current-status sections to point at
  `reports/public-sample/a100-formal-public-heldout-prediction/`.
- Rewrite `reports/experiment_report.md` around the formal public held-out
  dev/test evidence and demote the old dev128 SFT v2 run to historical context.
- Keep strict `contract_exact_match` and strict `slot_f1` as primary evidence,
  with `slot_f1_soft` labeled as an internal diagnostic only.
- Generate a concise Chinese Human Brief for the documentation refresh phase.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `contract-evaluation`: clarify that public project summary documents must stay
  aligned with the latest committed formal held-out evidence and conservative
  claim boundaries.

## Impact

- Affected docs: `README.md`, `README_en.md`,
  `reports/experiment_report.md`, and one Human Brief HTML.
- Affected specs: `contract-evaluation` documentation/evidence boundary.
- Non-goals: no dataset mutation, no SFT/DPO training, no prediction rerun, no
  evaluator semantic change, no soft-metric promotion, no checkpoint/adapter
  release claim, no production-readiness claim, and no live-browser benchmark
  claim.
