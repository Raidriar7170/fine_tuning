## Context

The archived `diagnose-normalized-command-string-mismatches` phase produced a public-safe report from committed row-mismatch evidence. It already states that no normalization, semantic-equivalence scoring, repair, replacement, or re-scoring occurred, and it preserves strict metrics including `contract_exact_match=0.0`.

The remaining risk is discoverability and reader interpretation. A reviewer reading the README or evidence directory may see one strict string-only row and the aggregate exact-match failure without understanding that this is strict whole-contract comparison, not a semantic judgment about Chinese query phrases.

## Goals / Non-Goals

**Goals:**

- Make the strict-string interpretation visible from the README and public evidence pack.
- State that `normalized_command` string differences are explanatory row-level evidence only.
- State that `contract_exact_match` remains a strict exact-match metric and is not replaced by semantic equivalence.
- Keep the phase public-safe, local-only, and claim-bounded.
- Add tests and validation to keep the public wording from drifting.

**Non-Goals:**

- No A100 execution.
- No SFT, DPO, GRPO, training, prediction rerun, checkpoint, or adapter creation.
- No prompt, decoder, parser, schema retry, schema, or evaluator metric changes.
- No semantic-equivalence scoring for `搜索/查询` or `明天的天气/明天天气`.
- No normalization, repair, coercion, replacement, or re-scoring of predictions.
- No dev/test held-out generalization, release, production-readiness, public full-corpus, model-quality, or live-browser benchmark claim.

## Decisions

1. **Document the boundary instead of changing evaluator behavior.**
   - Rationale: the prior diagnostic intentionally preserved strict metrics. Any semantic-equivalence metric would change success criteria and needs separate user confirmation.
   - Alternative considered: add a normalized-command semantic match slice. Rejected for this phase because it would change metric interpretation.

2. **Use README plus a small evidence policy note as the implementation surface.**
   - Rationale: README is the project front door, while the evidence directory is where reviewers will inspect the concrete mismatch rows.
   - Alternative considered: regenerate the prior diagnosis report. Rejected to avoid rewriting generated evidence as the source of truth for a later policy clarification.

3. **Test public wording rather than runtime logic.**
   - Rationale: this phase is documentation/policy only; focused tests should pin the discoverability and non-claim boundaries without touching training or prediction paths.
   - Alternative considered: add evaluator regression tests. Rejected because evaluator behavior is intentionally unchanged and already covered by prior tests.

## Risks / Trade-offs

- [Risk] The README note could be interpreted as excusing a failed exact-match metric. -> Mitigation: explicitly say `contract_exact_match` remains strict and failures remain failures.
- [Risk] The evidence policy note could look like a new metric. -> Mitigation: label it as interpretation guidance, not scoring or equivalence.
- [Risk] Public wording could imply model-quality recovery. -> Mitigation: repeat no-A100/no-rerun/no-model-quality boundaries and validate leak/claim scans.
