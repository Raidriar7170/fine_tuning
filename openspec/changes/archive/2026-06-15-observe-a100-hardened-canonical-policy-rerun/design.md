# Design

## Decision

Create a new observed evidence directory instead of overwriting
`reports/public-sample/a100-hardened-canonical-policy-rerun/`, because that
directory is linked from the earlier archived blocked phase and its Human Brief.
The previous blocked evidence remains useful as historical proof of why the loop
stopped before adapter restore.

## Execution Shape

Remote execution remains prediction-only:

1. Resolve `<a100_project_root>` in private overrides under the approved remote
   project root.
2. Use the restored `a100-merged-slot-value-heldout-eval` adapter path.
3. Run train/dev/test prediction configs with `CUDA_VISIBLE_DEVICES` set to a
   safe GPU.
4. Generate public-safe local report from sanitized metrics and metadata.

## Report Path Handling

The hardened rerun report writer must derive diagnostic artifact paths from the
requested `output_dir`, so a new observed output directory does not carry stale
hard-coded paths from the earlier blocked report.

## Boundaries

The observed rerun may report strict `contract_exact_match`, JSON-valid rate,
slot F1, prompt-policy flags, residual rows, and comparison to the prior merged
slot-value evidence. It must still state that these are public-sample
prediction-only diagnostics, not model recovery, private-corpus generalization,
production readiness, or live-browser benchmark evidence.
