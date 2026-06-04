## Why

The repository's core public evidence paths pass leak-scan, but the full public-surface scan still fails on one historical Human Brief that contains an illustrative A100 private-root path pattern. That means the committed companion documentation cannot currently be scanned end-to-end with the same privacy gate used for evidence artifacts.

## What Changes

- Sanitize the historical Human Brief text so it describes remote private-root rejection without embedding a path-like private A100 example.
- Add an OpenSpec clarification that committed Human Briefs and loop reports are part of the public report surface and must pass the same no-private-path boundary as evidence packs.
- Generate a concise Chinese Human Brief for this cleanup phase and record fresh validation.
- Non-goals: generic chat fine-tuning, skill routing, GUI action policy learning, first-phase GRPO, public release of the full local corpus, checkpoint release, adapter release, held-out generalization proof, production readiness, live-browser benchmark improvement, changing prior A100 evidence outcomes, weakening leak-scan rules, or editing private runtime artifacts.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `contract-evaluation`: Clarify that committed Human Brief HTML and loop reports are public documentation surfaces that must not contain private local or remote path patterns.

## Impact

- Affected artifacts: one historical Human Brief, one cleanup Human Brief, OpenSpec change files, and archived spec sync after acceptance.
- Affected validation: full public-surface leak-scan over `README.md`, `CONTEXT.md`, `data/public-samples`, `reports/public-sample`, `reports/templates`, `docs/human-briefs`, and `openspec`; full tests and OpenSpec strict validation.
- Systems not affected: no training code, dataset rows, predictions, metrics, A100 remote files, model artifacts, downstream Voice-to-Browser Agent runtime, deployment, or release posture.
