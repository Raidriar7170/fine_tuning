## Why

The repository can now prepare a runtime label provenance check, but public evidence still cannot show whether labels from the real tokenizer/collator SFT path mask prompts and expose assistant contract targets correctly. The user has explicitly authorized an A100 phase, so the next bounded step is to run that check privately and commit only a sanitized evidence summary.

## What Changes

- Add a bounded, explicitly authorized A100 runtime label provenance execution path that resolves private overrides outside git, selects an idle GPU, and keeps all private files under the approved A100 project root.
- Extend runtime label provenance metadata/reporting so the executed result can record real label tensor availability, label source kind, tokenizer/template status, collator status, prompt mask status, assistant-target loss status, package/version policy, and claim boundaries.
- Generate a public-safe runtime label provenance evidence pack under `reports/public-sample/` from sanitized A100 outputs only.
- Generate a concise Chinese Human Brief for this phase and link the prior prep, local label provenance, target-template alignment, and train-split diagnostic evidence.
- Non-goals: generic chat fine-tuning, skill routing, GUI action policy learning, first-phase GRPO, public release of the full local corpus, checkpoint release, adapter release, held-out generalization proof, production readiness, live-browser benchmark improvement, publishing private A100 details, or committing raw logs/checkpoints/adapters/caches/private overrides.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `supervised-contract-tuning`: Add the authorized runtime label provenance execution requirement for real tokenizer/collator labels while preserving private artifact boundaries.
- `contract-evaluation`: Add the public-safe observed runtime label provenance evidence requirement for sanitized A100 summaries and non-overclaim reporting.

## Impact

- Affected code: training/objective inspection helpers, train/report CLIs, report writers, leak-scan coverage, and tests for executed runtime evidence.
- Affected artifacts: a new sanitized evidence directory under `reports/public-sample/`, the phase Human Brief, and archived OpenSpec deltas.
- Dependencies: no new mandatory local dependency; A100 execution may use existing optional training dependencies already required by the private runtime path.
- Systems not affected: no downstream Voice-to-Browser Agent runtime change, no public dataset expansion, no public model/checkpoint/adapter release, and no deployment or benchmark publication.
