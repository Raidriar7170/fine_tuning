# Observe A100 Hardened Canonical Policy Rerun

## Why

The previous hardened canonical policy rerun phase was blocked because the
required `a100-merged-slot-value-heldout-eval` adapter was missing on the A100
machine. The follow-up restore phase regenerated that prerequisite adapter and
archived public-safe evidence that it is available.

## What Changes

- Run the existing hardened canonical policy prediction-only configs on A100 for
  train/dev/test using the restored merged slot-value adapter.
- Publish a new observed public-safe report directory, leaving the earlier
  blocked evidence intact for historical traceability.
- Record sanitized metrics, prompt-policy metadata, interpretation, and leak
  scan evidence without copying raw predictions, private overrides, raw logs,
  adapter weights, checkpoints, host details, SSH details, or remote paths.

## Out Of Scope

- No SFT, DPO, GRPO, adapter continuation training, or model merge.
- No dataset mutation, evaluator relaxation, prediction repair, normalization,
  or semantic-equivalence re-scoring.
- No public adapter/checkpoint release and no production-readiness claim.
- No claim that private-corpus or live-browser generalization is solved.

## Expected Evidence

- `reports/public-sample/a100-hardened-canonical-policy-rerun-observed/`
  containing sanitized observed rerun evidence.
- `docs/human-briefs/2026-06-15-observe-a100-hardened-canonical-policy-rerun.html`
  summarizing the phase.
