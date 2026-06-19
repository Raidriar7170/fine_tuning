## Why

The archived `propose-canonical-slot-boundary-formal-merge-after-review`
phase failed closed because no exact reviewed row-level canonical
slot-boundary candidate source existed. It identified the next bounded step:
materialize that exact row-level source before any future formal public sample
merge.

This phase turns the reviewed eligible candidate classes into a standalone
row-level candidate seed file. It still does not merge the formal public
sample, rebuild formal SFT/DPO artifacts, or claim model improvement.

## What Changes

- Add `data/public-samples/canonical_slot_boundary_seed_candidates.jsonl` as a
  standalone, public-safe row-level candidate source.
- Materialize exactly the reviewed eligible classes from the archived review:
  `slot_key_aliases` and `slot_value_boundaries`.
- Exclude normalized-command display diagnostics and excluded
  non-equivalence cases from row-level candidates.
- Publish materialization evidence under
  `reports/public-sample/canonical-slot-boundary-row-level-candidates/`.
- Generate report-local SFT candidate preview rows and a manifest for review,
  without touching formal public sample files.
- Add focused tests for schema validity, candidate counts, provenance,
  train-only split labels, excluded class boundaries, protected formal data
  paths, and public leak-scan cleanliness.
- Generate a concise Chinese Human Brief HTML for the phase.
- Non-goals: formal public sample merge, editing `seed_traces.jsonl`,
  generating formal SFT/DPO rows, rebuilding formal manifests, changing splits
  for formal data, training, prediction reruns, A100 execution, postprocessor
  implementation, prompt/evaluator changes, strict-exact relaxation, LLM
  judging, semantic-equivalence scoring, prediction repair,
  checkpoint/adapter release, held-out recovery claims, model-improvement
  claims, production-readiness claims, safety-readiness claims, and
  live-browser benchmark claims.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `voice2task-dataset-preparation`: add standalone row-level canonical
  slot-boundary candidate source materialization before any future formal
  public sample merge.

## Impact

- New standalone candidate source:
  `data/public-samples/canonical_slot_boundary_seed_candidates.jsonl`.
- New report artifacts under
  `reports/public-sample/canonical-slot-boundary-row-level-candidates/`.
- New focused tests under `tests/`.
- Status updates to `CONTEXT.md` / `reports/final_status.md` if the phase
  completes.
- No changes to formal public sample data, formal SFT/DPO artifacts, evaluator
  definitions, model configs, predictions, checkpoints, adapters, or A100
  workflows.
