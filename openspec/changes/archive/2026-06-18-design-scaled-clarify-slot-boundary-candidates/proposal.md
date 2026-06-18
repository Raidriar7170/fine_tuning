# design-scaled-clarify-slot-boundary-candidates

## Why

The scaled residual target-selection evidence selected `clarify/slots` as the
first remediation target: 78 strict residual rows in the
`clarify|clarify|ambiguous_request|confirm:true|slots:ambiguity` cluster.

Before materializing new seed rows or retraining, the project needs a bounded
candidate-design artifact that explains what clarify slot-boundary examples
would look like and what drift they are meant to prevent.

## What Changes

- Add a design-only evidence pack for scaled clarify slot-boundary candidate
  sketches derived from the committed target-selection and cluster-inspection
  evidence.
- Group source clarify families into reviewable candidate themes and record
  accepted target sketches for `clarify/clarify` ambiguous requests.
- Record rejected drift sketches for common failure modes such as converting
  ambiguous requests into `search`, `navigate`, `form_fill`, or `blocked`
  contracts.
- Update `CONTEXT.md`, `reports/final_status.md`, and a concise Chinese Human
  Brief with the candidate-design result and claim boundaries.
- Do not materialize seed rows, rebuild public sample artifacts, train, run
  DPO/GRPO, generate predictions, change prompts, or change evaluator metrics
  in this phase.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `voice2task-dataset-preparation`: add a requirement for publishing
  public-safe scaled clarify slot-boundary candidate designs before candidate
  materialization or paired-adapter training.

## Impact

- Affected code: public report/evidence generation helpers and eval CLI if a
  reusable writer is needed.
- Affected docs/evidence: `CONTEXT.md`, `reports/final_status.md`,
  `reports/public-sample/`, `docs/human-briefs/`, and OpenSpec archives.
- No dependency, model, checkpoint, adapter, remote runtime, prompt, evaluator,
  public manifest, or dataset-builder behavior changes are intended.
- Non-goals: generic chat fine-tuning, skill routing, GUI action policy
  learning, first-phase GRPO, public full-corpus release, checkpoint/adapter
  release, live-browser benchmark claims, and production-readiness claims.
