## Why

The post-recovery A100 public-sample predictions are JSON-like and contract-like, but still fail the Browser Task Contract schema with path-like `route` values and list-shaped `slots`. The previous diagnostics prove the output mismatch; this change narrows the root-cause evidence across training targets, prompt serialization, and decoding provenance so the next rerun is guided by facts rather than repair-by-reporting.

## What Changes

- Add a public-safe source-alignment diagnostic that audits SFT targets, configured train/prediction splits, prompt constraints, prediction shape symptoms, and decoding metadata availability.
- Strengthen the contract-only system prompt so the model-visible instruction explicitly lists `task_type` and `route` enum values, states that `route` is not a URL/path, and states that `slots` must be a JSON object rather than an array.
- Record future prediction decoding policy metadata, including greedy decoding, `max_new_tokens`, absence of schema repair, and whether raw decoded sidecar evidence is written.
- Generate a bounded public-sample report for the existing post-recovery predictions explaining why path-like routes and list slots are attributed to prompt/data/decoding evidence, not target corruption or evaluator mutation.
- Non-goals: generic chat fine-tuning, skill routing, GUI action policy learning, first-phase GRPO, public release of the full local/private corpus, checkpoint release, adapter release, production-readiness claims, and live-browser benchmark improvement claims.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `supervised-contract-tuning`: expose enum/type constraints and decoding policy in the SFT/prediction surface without repairing model outputs.
- `contract-evaluation`: add public-safe source diagnostics for target/prompt/decoding alignment evidence.

## Impact

- Affected code: `src/voice2task/formatting.py`, `src/voice2task/training.py`, `src/voice2task/evaluation.py`, `src/voice2task/reports.py`, and `src/voice2task/cli/eval.py`.
- Affected tests: formatter/training tests, prediction smoke tests, and evaluator/report tests.
- Affected artifacts: public-sample post-recovery diagnostics and Chinese Human Brief HTML.
- No new runtime dependencies, no private data committed, and no model checkpoint/adapter artifacts copied into git.
