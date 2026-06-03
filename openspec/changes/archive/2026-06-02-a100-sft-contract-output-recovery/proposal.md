## Why

The A100 trained-path prediction/evaluation smoke produced sanitized public-sample predictions, but every prediction failed schema validation (`json_valid_rate=0.0000`) and all 12 public-sample rows landed in the schema failure slice. This change recovers the contract-output path by making SFT training and private-adapter prediction use a consistent contract-only chat format, preserving honest failure reporting, and creating a public-safe rerun/evidence path for the next A100 smoke.

## What Changes

- Align the real SFT training text and private-adapter prediction prompt so both use the tokenizer chat template when available, with a deterministic fallback for local tests and minimal environments.
- Strengthen the contract-only output instructions with the exact required Browser Task Contract fields and strict "JSON object only" boundaries.
- Add tests that prove the formatted training target and prediction prompt stay contract-focused and do not drift into generic normalization/task-description schemas.
- Keep invalid private-adapter outputs visible as schema failures rather than replacing them with rule, fixture, or gold-contract fallbacks.
- Add a public-safe recovery evidence path that records pre-recovery failure evidence, post-rerun metrics when available, leak-scan results, and explicit claim boundaries.
- Non-goals: generic chat fine-tuning, Hermes-style skill routing, GUI action policy learning, first-phase GRPO/rule reward training, publishing the full local/private corpus, publishing model checkpoints/adapters, hiding failed model outputs, or claiming live-browser benchmark improvement before controlled evidence exists.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `supervised-contract-tuning`: require consistent contract-only chat formatting for real SFT training and trained-adapter prediction, plus an output-recovery runbook for rerunning the A100 public-sample SFT path.
- `contract-evaluation`: require public-safe schema-failure recovery evidence that preserves failed outputs, compares recovery metrics when rerun evidence exists, and rejects private artifact leakage.

## Impact

- Affects SFT formatting helpers, real SFT training text construction, private-adapter prediction prompt construction, A100 public-sample config/runbook wording, recovery evidence reports, and tests.
- Uses the existing Transformers + PEFT + TRL stack and does not add a new inference framework or force a remote A100 run from local validation.
- Requires any future heavy rerun outputs to remain under the approved private A100 project root, with only sanitized predictions, metrics, manifests, leak-scan summaries, and claim-bounded reports copied into the repo.
