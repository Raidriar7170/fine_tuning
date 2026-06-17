## Why

The current formal public sample is only `102` seeds / `261` SFT rows, with just
`123` train rows. The latest strict held-out evidence shows stable JSON and
recovered safety recall, but strict `contract_exact_match` and strict `slot_f1`
remain partial; the archived scaled-sample design recommends expanding the
reviewed public candidate pool before another training retry.

## What Changes

- Add a deterministic, public-safe scaled public-sample candidate materializer.
- Produce standalone candidate seed rows and derived SFT sidecar evidence for the
  archived `240` seed milestone design.
- Materialize the delta from the current `102` formal seeds to the designed
  `240` milestone as reviewable candidates: `118` core family candidates plus
  `20` confirmation-boundary overlay candidates.
- Add a CLI command and tests for candidate generation, validation boundaries,
  and public-safe evidence.
- Generate a public evidence pack and Human Brief for the materialization phase.
- Do not merge candidates into the formal public sample in this phase.
- Do not train, predict, change prompts, change evaluator metrics, normalize
  slots, repair predictions, release checkpoints/adapters, or claim model
  recovery.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `voice2task-dataset-preparation`: add a requirement for scaled public-sample
  candidate materialization that remains standalone until a later explicit merge
  phase.

## Impact

- Affected implementation:
  - `src/voice2task/dataset.py`
  - `src/voice2task/cli/data.py`
  - `src/voice2task/reports.py`
- Affected tests:
  - new scaled-candidate materialization tests
- Affected public artifacts:
  - `data/public-samples/scaled_public_sample_seed_candidates.jsonl`
  - `reports/public-sample/scaled-public-sample-candidate-materialization/`
  - `docs/human-briefs/2026-06-17-materialize-scaled-public-sample-candidates.html`
- Non-goals:
  - generic chat fine-tuning
  - skill routing
  - GUI action policy learning
  - first-phase GRPO
  - public release of the full local/private corpus
  - checkpoint, adapter, or live-browser benchmark claims
