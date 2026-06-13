## Design

The diagnostic uses only committed public-safe artifacts:

- `data/public-samples/sft_public_sample.jsonl`
- `data/public-samples/manifest_public_sample.json`
- `reports/public-sample/current-manifest-tiny-overfit-probe/manifest.json`
- `reports/public-sample/current-tiny-adapter-heldout-prediction/manifest.json`
- split-level alignment/schema diagnostics from the current tiny held-out phase

It will compute:

1. Dataset family coverage by `source_id`, split, task type, route, safety
   reason, confirmation behavior, and slot keys.
2. Tiny-adapter training subset coverage from the prior tiny-overfit manifest.
3. Held-out residual families by split and source family, using existing
   alignment/schema diagnostics without repairing predictions.
4. A strategy recommendation with claim boundaries.

## Strategy Semantics

The recommendation is evidence-only. It may say that targeted coverage is the
best next hypothesis, but it must not generate rows or modify training configs.
It must also distinguish:

- dataset-level coverage exists in train rows
- tiny-adapter subset coverage did not include those families
- held-out exact-match remains failed

## Public Safety

The output is a small JSON/Markdown evidence pack plus Human Brief. It must not
include private paths, remote paths, raw logs, checkpoints, adapters, caches,
private rows, tokens, host details, or SSH details.
