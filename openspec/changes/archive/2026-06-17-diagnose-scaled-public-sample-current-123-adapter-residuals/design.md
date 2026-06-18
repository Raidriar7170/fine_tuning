# Design: Scaled Current-123 Adapter Residual Diagnosis

## Evidence Source

The diagnosis reads only the latest scaled-manifest prediction-only evidence:

- `reports/public-sample/a100-scaled-public-sample-current-123-adapter-prediction-baseline-after-a100-recovery/formal_public_heldout_prediction.json`
- `reports/public-sample/a100-scaled-public-sample-current-123-adapter-prediction-baseline-after-a100-recovery/dev/dev_gold.jsonl`
- `reports/public-sample/a100-scaled-public-sample-current-123-adapter-prediction-baseline-after-a100-recovery/dev/predictions.jsonl`
- `reports/public-sample/a100-scaled-public-sample-current-123-adapter-prediction-baseline-after-a100-recovery/test/test_gold.jsonl`
- `reports/public-sample/a100-scaled-public-sample-current-123-adapter-prediction-baseline-after-a100-recovery/test/predictions.jsonl`

The source evidence already records the comparison boundary: the adapter was
trained on `public-sample-20260617T045941Z`, while the diagnosis target is
`public-sample-20260617T152259Z`.

## Approach

Reuse the existing `diagnose-formal-heldout-residual-families` CLI and report
writer. This keeps the diagnosis aligned with previous residual-family evidence
instead of creating a parallel format.

The output directory is intentionally distinct from older diagnosis artifacts:

`reports/public-sample/scaled-current-123-adapter-residual-diagnosis/`

## Interpretation Rules

1. **Strict metrics stay authoritative.**
   `contract_exact_match` and strict `slot_f1` remain the public headline.
   `slot_f1_soft` remains diagnostic only.

2. **Tiered diagnosis is descriptive, not a new evaluator.**
   The report may say schema/route/safety tiers are comparatively strong and
   strict slot/exact tiers are weak, but it must not replace the existing
   contract ladder.

3. **No automatic remediation.**
   The diagnosis may recommend a next bounded phase, but it must not
   materialize data, change gold labels, train, predict, or change evaluator
   behavior.

4. **Sanitized artifacts only.**
   The committed evidence must omit raw private rows, private paths, host
   details, SSH details, raw logs, private overrides, checkpoints, adapters,
   caches, and secrets.

## Validation

- Focused diagnosis tests.
- Existing formal prediction evidence tests.
- Full pytest.
- Ruff.
- `openspec validate --all --strict`.
- Leak scan over diagnosis evidence, docs, Human Brief, and archive.
- `git diff --check`.
