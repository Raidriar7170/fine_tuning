## Why

The normalized-command mismatch diagnosis is accurate but easy to misread from the project front door: a strict string-only mismatch can look like semantic failure, while `contract_exact_match=0.0` can look like every contract field failed. The project needs a small public-facing interpretation pass before any metric, prompt, training, or A100 rerun decision.

## What Changes

- Clarify in reviewer-facing documentation that `normalized_command` string differences are explanatory row-level evidence, not semantic-equivalence scoring.
- Preserve `contract_exact_match` as a strict exact-match metric; do not soften, normalize, repair, or re-score predictions.
- Add a small public-safe policy note near the existing normalized-command diagnosis evidence so the boundary is visible outside the generated row report.
- Add tests that pin the README/evidence wording and prevent future drift toward semantic-equivalence or metric-change claims.
- Generate a concise Chinese Human Brief and close the OpenSpec phase with fresh validation.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `contract-evaluation`: require public-facing evidence surfaces to explain strict `normalized_command` string mismatches without changing evaluator metrics or marking strings equivalent.

## Impact

- Affected documentation: `README.md`, a public-safe evidence policy note, and a Chinese Human Brief.
- Affected tests: focused public-surface tests that assert the strict-string interpretation boundary.
- Affected OpenSpec artifacts: `contract-evaluation` requirement delta and archived change record.
- No A100 execution, training, prediction rerun, prompt change, decoder change, parser change, schema change, evaluator metric change, checkpoint/adapter publication, dependency change, or semantic-equivalence scoring.
