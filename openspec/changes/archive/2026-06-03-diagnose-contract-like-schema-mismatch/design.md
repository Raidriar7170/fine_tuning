## Context

The current post-recovery evidence pack records that all 12 public-sample private-adapter predictions fail schema validation, even though the predictions are mostly JSON objects with Browser Task Contract-like field names. `evaluate_predictions()` correctly treats them as schema failures, but it only records a single `schema` slice, so the next investigation cannot distinguish missing fields from invalid enum labels, wrong container types, empty required strings, or safety/confirmation mismatches.

## Goals / Non-Goals

**Goals:**

- Add a public-safe diagnostic surface that explains why contract-like prediction objects fail the Browser Task Contract schema.
- Reuse the existing schema constants and validators so diagnostics describe the actual contract, not a second schema.
- Generate a bounded report for the existing A100 post-recovery public-sample predictions.

**Non-Goals:**

- Do not relax the Browser Task Contract schema.
- Do not normalize invalid private-adapter predictions into valid contracts.
- Do not rerun training, publish checkpoints or adapters, claim model-quality improvement, or claim live-browser benchmark improvement.
- Do not introduce generic chat fine-tuning, skill routing, GUI action policy learning, first-phase GRPO, or public release of the full local/private corpus.

## Decisions

- Add diagnostics alongside evaluation instead of changing the schema validator.
  - Rationale: `BrowserTaskContract.from_dict()` should remain strict and fail fast for runtime/evaluation correctness. Diagnostics can collect multiple public-safe reasons for human analysis without weakening validation.
  - Alternative considered: make `from_dict()` collect all errors. That would change the semantics of the authoritative validator and increase risk outside this small phase.

- Report both aggregate issue counts and per-row issue lists.
  - Rationale: aggregate counts show the dominant failure pattern, while row-level examples preserve traceability to the public-sample evidence.
  - Alternative considered: only add more failure slices to metrics. That would still hide exactly which fields and values caused failure.

- Keep diagnostics local to sanitized public artifacts.
  - Rationale: the existing predictions are already public-safe, and this phase should not require copying private A100 logs, configs, paths, checkpoints, adapters, or caches.

## Risks / Trade-offs

- [Risk] Diagnostics could be mistaken for an automatic repair path. -> Mitigation: reports must state that invalid predictions remain invalid and no model-quality improvement is claimed.
- [Risk] A parallel diagnostic schema could drift from the real validator. -> Mitigation: use existing constants such as `TASK_TYPES`, `ROUTES`, and required field names from the current contract implementation.
- [Risk] Row-level reports may leak raw private details if future prediction artifacts are not sanitized. -> Mitigation: use the existing public leak scan on generated reports and keep this phase scoped to committed public-sample evidence.
