## Why

The current formal public held-out baseline is a partial signal, and the
selected residual target is `form_fill` with 29 residual rows and 49 residual
fields. The previous readiness phase proved that the current public train split
contains 21 merged `form_fill` remediation rows and can safely feed a bounded
A100 SFT v3 run.

## What Changes

- Run one explicitly bounded A100 SFT v3 training job using the committed
  `public-sample-20260616T074315Z` manifest and train split.
- Keep all model artifacts, checkpoints, logs, caches, and private overrides
  under the approved private A100 project root and out of git.
- Run prediction-only dev/test evaluation with the SFT v3 private adapter and
  the existing strict contract evaluator.
- Commit only sanitized evidence: adapter metadata summary, dev/test metrics,
  run manifest, leak scan, and a concise Human Brief.
- Preserve the current evaluator semantics: strict `contract_exact_match` and
  strict `slot_f1` remain authoritative, and `slot_f1_soft` stays diagnostic
  only.
- Non-goals: generic chat fine-tuning, skill routing, GUI action policy
  learning, first-phase GRPO, DPO reruns, evaluator relaxation, public release
  of the full local/private corpus, public checkpoint or adapter release, and
  live-browser benchmark improvement claims.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `supervised-contract-tuning`: authorize and bound the private A100 SFT v3
  execution phase after readiness evidence exists.
- `contract-evaluation`: authorize and bound the sanitized prediction-only
  held-out evidence import for the SFT v3 adapter.

## Impact

- Affected configs: `configs/sft-a100-form-fill-remediation-v3*.json`.
- Affected runtime: remote A100 SFT and `sft-predict` execution under the
  approved private project root.
- Affected evidence: a new public-safe evidence directory under
  `reports/public-sample/` and a Human Brief under `docs/human-briefs/`.
- Affected specs: `supervised-contract-tuning` and `contract-evaluation`.
