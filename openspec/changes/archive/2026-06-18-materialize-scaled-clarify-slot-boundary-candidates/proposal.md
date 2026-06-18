## Why

The scaled clarify slot-boundary candidate design identified `3` public-safe
themes covering all `28` source families / `78` source-family incidence in the
selected `clarify/slots` residual cluster. The next safe step is to materialize
reviewable candidate seed/SFT sidecars before changing the formal public sample
or launching any training.

## What Changes

- Add deterministic, public-safe materialization for scaled clarify
  slot-boundary candidates derived from the committed design report.
- Generate standalone candidate seed rows and derived SFT sidecars for the
  three designed themes:
  - `clarify_search_or_extract_ambiguity`
  - `clarify_navigation_or_form_fill_ambiguity`
  - `clarify_pronoun_or_context_missing`
- Publish JSON, Markdown, manifest, and leak-scan evidence under
  `reports/public-sample/scaled-clarify-slot-boundary-candidate-materialization/`.
- Add CLI and focused tests for reproducible candidate generation, candidate
  counts, target-shape invariants, and standalone-only boundaries.
- Update `CONTEXT.md`, `reports/final_status.md`, and a concise Chinese Human
  Brief.
- Do not merge candidates into the formal public sample in this phase.
- Do not rebuild formal public sample manifests, generate formal DPO pairs,
  train, predict, change prompts, change evaluator metrics, normalize slots,
  repair predictions, release checkpoints/adapters, or claim model recovery.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `voice2task-dataset-preparation`: add a requirement for standalone scaled
  clarify slot-boundary candidate materialization before any formal public
  sample merge or paired training retry.

## Impact

- Affected implementation:
  - `src/voice2task/dataset.py`
  - `src/voice2task/cli/data.py`
  - `src/voice2task/reports.py`
- Affected tests:
  - new scaled clarify materialization tests
- Affected public artifacts:
  - `data/public-samples/scaled_clarify_slot_boundary_seed_candidates.jsonl`
  - `reports/public-sample/scaled-clarify-slot-boundary-candidate-materialization/`
  - `docs/human-briefs/2026-06-18-materialize-scaled-clarify-slot-boundary-candidates.html`
- Non-goals:
  - generic chat fine-tuning
  - skill routing
  - GUI action policy learning
  - first-phase GRPO
  - public release of the full local/private corpus
  - formal public sample merge
  - checkpoint, adapter, production-readiness, or live-browser benchmark claims
