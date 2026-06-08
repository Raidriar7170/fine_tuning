## Why

The A100 first-pass fence-suppression rerun improved the wrapper/schema boundary on the three train rows, but strict exact match remains `2/3` because one row still emits `city/date/topic` slots instead of the gold compact `query` slot. The next smallest step is a local evidence-only diagnosis that explains the remaining row-level mismatch without changing metrics or model behavior.

## What Changes

- Generate a public-safe local diagnosis from `reports/public-sample/a100-first-pass-fence-suppression-rerun/`.
- Identify the residual row, gold/predicted slot shape, strict metric impact, and why this is still a strict exact-match failure.
- Preserve the successful wrapper/schema observation separately from the remaining slot mismatch.
- Add tests that lock the evidence boundaries, privacy boundary, and no-overclaim wording.
- Keep A100 reruns, training, parser/evaluator changes, slot normalization, prediction repair, semantic-equivalence scoring, and release claims out of scope.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `contract-evaluation`: add public-safe row-level diagnosis requirements for residual slot exact-match mismatch after first-pass fence suppression.

## Impact

- Affected evidence: new public-safe directory under `reports/public-sample/fence-suppression-slot-residual-diagnosis/` and a Chinese Human Brief under `docs/human-briefs/`.
- No runtime code, model, parser, evaluator, dataset, or remote A100 changes.
