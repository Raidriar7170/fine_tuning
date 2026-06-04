## Why

The SFT objective path now builds pretokenized assistant-only labels, but the committed A100 train-split overfit evidence was generated before that repair. A new explicitly authorized A100 train-split rerun is needed to determine whether the current assistant-only training path changes train-internal Browser Task Contract recovery while preserving the public/private artifact boundary.

## What Changes

- Run a new bounded A100 SFT training pass on the public-sample train split using the current assistant-only loss-mask path.
- Run private-adapter prediction only on `prediction_split=train` with `overfit_diagnostic=true` and `generalization_claim=false`.
- Copy back only sanitized public-sample evidence: adapter metadata, objective/runtime label evidence, predictions, prompt snapshot, sanitized raw decoded summary, generation trace, prediction metadata, metrics, manifest, report, leak-scan result, and Human Brief HTML.
- Preserve invalid, partial, truncated, non-JSON, or wrong-contract outputs as observed failures rather than replacing them with fixtures, rule baselines, or gold contracts.
- Compare the rerun against the earlier train-split diagnostic only as a bounded before/after diagnostic, not as a release or generalization claim.
- Non-goals: generic chat fine-tuning, skill routing, GUI action policy learning, first-phase GRPO, public release of the full local/private corpus, checkpoint release, adapter release, production-readiness claims, dev/test generalization claims, and live-browser benchmark improvement claims.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `supervised-contract-tuning`: require authorized A100 train-split reruns after objective-mask repair to use the current assistant-only SFT label path, explicit heavy-training opt-in, repo-external private overrides, and private artifact boundaries.
- `contract-evaluation`: require public-safe reporting for the assistant-only rerun evidence pack, including objective-mask status, train-internal recovery status, comparison with prior diagnostic evidence, and non-overclaim boundaries.

## Impact

- Affected systems: remote A100 execution under the approved private project root, local sanitized evidence import, contract metrics, evidence pack generation, leak scanning, Human Brief HTML, OpenSpec archive flow, and auto integration.
- Affected artifacts: a new public-safe evidence directory under `reports/public-sample/`, phase Human Brief HTML, OpenSpec deltas, and possibly minimal report/test updates if the existing evidence writer cannot represent the assistant-only rerun cleanly.
- No public checkpoint, adapter, raw log, private override, host/IP detail, SSH detail, token, secret, private path, model cache, or private corpus row may be committed.
