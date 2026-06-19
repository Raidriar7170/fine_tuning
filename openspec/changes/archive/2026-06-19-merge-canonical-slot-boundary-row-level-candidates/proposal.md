## Why

The archived `materialize-canonical-slot-boundary-row-level-candidates` phase
created the exact reviewed row-level source required by the earlier
formal-merge readiness packet:
`data/public-samples/canonical_slot_boundary_seed_candidates.jsonl`.

The next bounded step is to promote those seven reviewed standalone candidates
into the formal public sample so future evaluation or training phases can bind
to an explicit new manifest boundary. This must be a data/evidence phase only:
no model training, prediction, evaluator relaxation, postprocessor work, or
model-quality claim.

## What Changes

- Add a guarded formal merge path for
  `data/public-samples/canonical_slot_boundary_seed_candidates.jsonl`.
- Promote exactly seven reviewed canonical slot-boundary candidate seeds into
  `data/public-samples/seed_traces.jsonl`.
- Rebuild synchronized formal `sft_public_sample.jsonl`,
  `dpo_public_sample.jsonl`, and `manifest_public_sample.json` from the
  updated formal seed file.
- Publish merge evidence under
  `reports/public-sample/canonical-slot-boundary-formal-merge/`.
- Record the new formal sample comparison boundary so old metrics are not
  compared directly to future metrics.
- Add focused tests for merge counts, provenance promotion, duplicate or
  unreviewed row rejection, validation, public leak-scan cleanliness, and
  fail-closed claims.
- Generate a concise Chinese Human Brief HTML for the phase.
- Non-goals: training, prediction reruns, A100 execution, postprocessor
  implementation, prompt/evaluator changes, strict-exact relaxation, LLM
  judging, semantic-equivalence scoring, prediction repair,
  checkpoint/adapter release, held-out recovery claims, model-improvement
  claims, production-readiness claims, safety-readiness claims, and
  live-browser benchmark claims.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `voice2task-dataset-preparation`: add a guarded formal merge path for
  reviewed canonical slot-boundary row-level candidates with explicit
  comparison-boundary warnings.

## Impact

- Affected code:
  - `src/voice2task/dataset.py`
  - `src/voice2task/cli/data.py`
  - `src/voice2task/reports.py`
- Affected tests:
  - new or updated tests under `tests/`.
- Affected artifacts:
  - `data/public-samples/seed_traces.jsonl`
  - `data/public-samples/sft_public_sample.jsonl`
  - `data/public-samples/dpo_public_sample.jsonl`
  - `data/public-samples/manifest_public_sample.json`
  - `reports/public-sample/canonical-slot-boundary-formal-merge/`
  - `docs/human-briefs/2026-06-19-merge-canonical-slot-boundary-row-level-candidates.html`
