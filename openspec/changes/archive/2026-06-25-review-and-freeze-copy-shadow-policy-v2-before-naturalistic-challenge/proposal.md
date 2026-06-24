## Why

The Policy V2 design phase produced an inactive scope-reduction proposal, but it
is still a review artifact rather than a frozen reference. Before any
naturalistic challenge v2 work, the project needs one bounded review-and-freeze
step that locks the proposed Policy V2 evidence surface while keeping runtime
behavior unchanged.

## What Changes

- Review the committed Policy V2 proposal artifacts for consistency,
  deterministic gate provenance, reviewer-required scope decisions, and
  proposal-only runtime boundaries.
- Emit a frozen public-safe Policy V2 reference artifact derived from the
  reviewed proposal.
- Publish compact freeze evidence that records source hashes, review outcome,
  per-scope frozen statuses, non-goals, and the next allowed bounded phase.
- Refresh status docs and a Human Brief so reviewer-facing truth surfaces no
  longer point at an unfrozen proposal as the current endpoint.
- Keep Policy V1, challenge v1 rows and gold, frozen predictions, sidecars,
  audits, evaluators, prompt/decoding, runtime hooks, model artifacts, and
  training data unchanged.

## Capabilities

### New Capabilities

- `copy-shadow-policy-v2-freeze`: review and freeze an inactive Policy V2
  reference before any naturalistic challenge v2 or runtime integration work.

### Modified Capabilities

None.

## Impact

- Adds a freeze/review script, frozen inactive policy artifact, public-safe
  freeze reports, tests, docs/status refreshes, OpenSpec artifacts, and a
  concise Chinese Human Brief.
- Does not add runtime loading of Policy V2 and does not change prediction or
  evaluation behavior.
- Does not implement generic chat fine-tuning, skill routing, GUI action policy
  learning, first-phase GRPO, public release of the full local/private corpus,
  runtime enforcement, action enablement, normalized trusted provenance,
  naturalistic challenge v2, training, data expansion, schema changes, browser
  automation, or model/executable improvement claims.
