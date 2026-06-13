## Why

The previous diagnostic found that the current public manifest has fresh SFT target spans, but the only observed runtime-label and tiny-overfit artifacts belong to an older manifest. We need a fresh, bounded runtime label provenance check for `public-sample-20260613T072200Z` before deciding whether a tiny-overfit probe or any training rerun is meaningful.

## What Changes

- Run or record a current-manifest SFT runtime label provenance check for the public train split.
- Generate a public-safe evidence pack that proves whether the real tokenizer/collator path inspected labels for the current manifest.
- Record prompt-token masking, assistant-token loss, label source kind, runtime gate status, package policy, and evidence gaps without exposing private paths or logs.
- Compare the fresh evidence against the stale prior runtime-label artifact only as historical context.
- Generate a concise Chinese Human Brief and archive the change after validation.
- Non-goals: no generic chat fine-tuning, no skill routing, no GUI action policy learning, no first-phase GRPO, no full private-corpus release, no checkpoint or adapter release, no model-quality recovery claim, no prediction rerun, and no tiny-overfit probe in this phase.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `contract-evaluation`: Require current-manifest runtime label provenance evidence to explicitly distinguish fresh current evidence from stale prior artifacts and preserve non-claim boundaries.
- `supervised-contract-tuning`: Require bounded current-manifest runtime label checks to avoid training, prediction, adapter loading, or model download beyond the local/private tokenizer needed for label inspection.

## Impact

- Affected code: likely test/report glue around runtime label provenance evidence freshness; existing training/report CLIs should be reused where possible.
- Affected artifacts: a new report directory under `reports/public-sample/`, one phase Human Brief under `docs/human-briefs/`, and OpenSpec archive/spec deltas.
- Affected systems: local repo validation and, if local dependencies/model are unavailable, authorized A100 execution under the approved private project root only.
