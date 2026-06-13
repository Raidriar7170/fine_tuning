## Why

The archived public held-out residual repair phase showed that the 7B SFT-only rerun did not even strictly memorize the new public train repair rows (`train contract_exact_match=0.3333`) and still failed on public `dev/test` (`contract_exact_match=0.0`). Before adding more data, running DPO, or launching another A100 rerun, the project needs a bounded diagnosis of whether the SFT training path is actually applying loss to the assistant contract target with enough target-token signal.

## What Changes

- Add a public-safe SFT contract learning-signal diagnostic that inspects committed public SFT rows, rendered training prompts, assistant target spans, target-token pressure, and prior repair evidence.
- Reuse or extend the existing local label-provenance and formatting utilities without downloading models, loading private adapters, or starting heavy training by default.
- Produce a compact evidence pack under `reports/public-sample/sft-contract-learning-signal/` with JSON, Markdown, leak-scan results, and a concise Chinese Human Brief.
- Add tests that prove the diagnostic distinguishes structural assistant target evidence from true runtime label evidence and keeps claims bounded.
- Keep interpretation conservative: this phase may identify training-signal risk and recommend a later runtime/A100 or DPO phase, but it does not claim model recovery, private-corpus generalization, checkpoint release, adapter release, production readiness, or live-browser benchmark improvement.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `supervised-contract-tuning`: add a bounded SFT contract learning-signal diagnostic over public SFT rows, rendered prompts, assistant targets, token-pressure summaries, and label-mask evidence availability.
- `contract-evaluation`: add public-safe reporting boundaries for the learning-signal evidence pack and its relation to prior negative repair evidence.

## Impact

- Affected code: likely `src/voice2task/training.py`, report helpers or a small diagnostic CLI path, and tests around A100/SFT smoke evidence.
- Affected artifacts: `reports/public-sample/sft-contract-learning-signal/`, `docs/human-briefs/YYYY-MM-DD-diagnose-sft-contract-learning-signal.html`, and OpenSpec archive/spec sync.
- Affected tests: focused unit tests for learning-signal diagnostics, evidence-boundary tests, and existing validation checks.
- Non-goals: generic chat fine-tuning, skill routing, GUI action policy learning, first-phase GRPO, private full-corpus evaluation, public release of the full local corpus, prediction repair/replacement, evaluator relaxation, semantic-equivalence scoring, checkpoint/adapter release claims, and live-browser benchmark claims.
