## Why

The latest runtime label provenance evidence inspected real tokenizer/collator labels and found `assistant_tokens_carry_loss=true` but `prompt_tokens_masked=false`. That means the current SFT path cannot support an assistant-only or completion-only loss-mask claim, and train-split overfit failures should not be reinterpreted as model-quality evidence until the objective path is corrected.

## What Changes

- Replace the full-text causal-LM label path used for real SFT training/objective inspection with an assistant-only loss-mask path that masks system/user/prompt tokens and keeps assistant Browser Task Contract tokens in loss.
- Add tests that fail against the current full-text label behavior and pass only when prompt tokens are `-100` and assistant target tokens carry loss.
- Keep runtime label provenance aligned with the actual SFT training data path, so future A100 evidence can report `prompt_tokens_masked=true` only when the inspected labels prove it.
- Update public-safe runtime label provenance reporting and Human Briefs to describe objective-path repair without overwriting historical A100 observed evidence or claiming model recovery, held-out generalization, checkpoint release, production readiness, or live-browser improvement.
- Non-goals: generic chat fine-tuning, skill routing, GUI action policy learning, first-phase GRPO, public release of the full local corpus, checkpoint release, adapter release, dev/test generalization proof, production readiness, live-browser benchmark improvement, replacing failed predictions with fixtures, or launching a private A100 rerun without a separate explicit execution gate.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `supervised-contract-tuning`: Require the real SFT path and runtime objective inspection to expose assistant-only/completion-only loss masking before objective-path success can be claimed.
- `contract-evaluation`: Require public runtime label provenance evidence to separate objective-mask repair from model-output recovery and train-split/generalization claims.

## Impact

- Affected code: SFT training helpers, runtime objective inspection, label provenance metadata/reporting, and tests around runtime label masks.
- Affected artifacts: updated public-safe runtime label provenance evidence, a phase Human Brief, and archived OpenSpec deltas.
- Dependencies: no new mandatory local dependency; the implementation must keep local tests runnable without downloading models or requiring A100 access.
- Systems not affected: no downstream Voice-to-Browser Agent runtime change, no public dataset expansion, no public model/checkpoint/adapter release, no deployment, and no live-browser benchmark publication.
