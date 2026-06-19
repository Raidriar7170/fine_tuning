## Why

The archived canonical slot-boundary candidate review classified slot-key alias
and conservative slot-value boundary candidates as eligible only for a later
bounded formal-merge proposal. It also kept normalized-command examples
diagnostic/display-only and preserved excluded non-equivalence cases as blocked
or deferred.

The project should not jump directly from class-level review sketches to formal
public sample mutation. A formal merge needs an explicit row-level candidate
source, comparison-boundary warnings, regenerated derived artifacts, and
fail-closed validation. This phase creates the bounded proposal/readiness
evidence for that future merge and records whether the current repo has enough
exact inputs to mutate formal data.

## What Changes

- Add formal-merge proposal/readiness evidence under
  `reports/public-sample/canonical-slot-boundary-formal-merge-proposal/`.
- Read
  `reports/public-sample/canonical-slot-boundary-candidate-review/summary.json`
  as the source review evidence.
- Classify the currently eligible candidate classes as future merge proposal
  inputs only.
- Record that no exact row-level candidate JSONL pack exists yet for these
  canonical slot-boundary examples, so this phase MUST NOT mutate formal public
  sample data.
- Define the acceptance criteria, required future source artifact, comparison
  boundary, validation commands, and claims not to overstate for any later
  actual formal merge.
- Add focused tests for proposal artifact presence, readiness gating, protected
  data paths, normalized-command exclusion, non-equivalence preservation, and
  public leak-scan cleanliness.
- Generate a concise Chinese Human Brief HTML for the phase.
- Non-goals: editing `data/public-samples/seed_traces.jsonl`, generating JSONL
  seed candidates, generating SFT/DPO rows, rebuilding manifests, changing
  splits, training, prediction reruns, A100 execution, postprocessor
  implementation, prompt/evaluator changes, strict-exact relaxation, LLM
  judging, semantic-equivalence scoring, prediction repair,
  checkpoint/adapter release, held-out recovery claims, model-improvement
  claims, production-readiness claims, safety-readiness claims, and
  live-browser benchmark claims.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `voice2task-dataset-preparation`: add formal-merge proposal/readiness
  evidence requirements for reviewed canonical slot-boundary candidates before
  any future public sample mutation.

## Impact

- New proposal/readiness artifacts under
  `reports/public-sample/canonical-slot-boundary-formal-merge-proposal/`.
- New focused tests under `tests/`.
- Status updates to `CONTEXT.md` / `reports/final_status.md` if the phase
  completes.
- No changes to formal public sample data, generated SFT/DPO artifacts,
  evaluator definitions, model configs, predictions, checkpoints, adapters, or
  A100 workflows.
