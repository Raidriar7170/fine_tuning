## Context

The latest current-manifest model evidence is
`reports/public-sample/a100-current-train-split-sft-retry/`. It trained a
private adapter on the current 118-row train split and evaluated dev/test with
the strict contract ladder. The observed signal is mixed: safety recall
recovered and strict slot F1 improved, while dev exact match, confirmation
accuracy, and test route/confirmation regressed relative to the
current-manifest prediction-only baseline.

The project status contract now says the next bounded step should diagnose
these residuals and trade-offs before any additional training, DPO, evaluator
change, or release claim.

## Goals / Non-Goals

**Goals:**

- Compare current retry outputs against the current-manifest prediction-only
  baseline on matching dev/test row ids.
- Categorize confirmation regressions, exact-match regressions, route/task-type
  regressions, safety changes, and remaining slot residuals.
- Produce a public-safe diagnosis evidence pack, refreshed status docs, and a
  concise Chinese Human Brief.
- Preserve strict `contract_exact_match` and strict `slot_f1` as headline
  metrics while keeping `slot_f1_soft` diagnostic-only.

**Non-Goals:**

- No training, prediction generation, DPO, GRPO, evaluator relaxation, slot
  normalization, prediction repair, prompt change, or dataset mutation.
- No checkpoint/adapter release, full private corpus release, live-browser
  benchmark claim, held-out recovery claim, or production-readiness claim.
- No broad residual remediation design beyond the next bounded recommendation.

## Decisions

1. Diagnosis reads committed public-safe evidence only.
   - Rationale: the current question is about observed trade-offs, not hidden
     training internals.
   - Alternative considered: inspect private remote logs/adapters. Rejected
     because it widens scope and is unnecessary for row-level output comparison.

2. Use row-id aligned comparison between baseline and retry predictions.
   - Rationale: dev/test row ids are stable under the current manifest, so
     row-level deltas can identify regressions and recoveries without changing
     metrics.
   - Alternative considered: aggregate-only comparison. Rejected because it
     cannot explain confirmation and exact-match regressions.

3. Keep the phase report-oriented unless a reusable report writer is needed.
   - Rationale: minimal code changes are preferred. If code is added, it should
     be small, tested, and focused on deterministic diagnosis output.
   - Alternative considered: ad hoc notebooks or private scripts. Rejected
     because committed evidence should be reproducible by repo tooling.

## Risks / Trade-offs

- [Risk] The diagnosis may identify multiple plausible next actions. ->
  Mitigation: record the strongest row-level evidence and recommend only one
  bounded next OpenSpec phase.
- [Risk] Soft slot diagnostics could be overread as semantic recovery. ->
  Mitigation: label `slot_f1_soft` diagnostic-only in every public artifact.
- [Risk] Public artifacts could leak private paths or raw logs. -> Mitigation:
  run the existing leak scan and keep inputs limited to committed evidence.
