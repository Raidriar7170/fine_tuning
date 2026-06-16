## Context

The current formal public held-out evidence is tied to manifest `public-sample-20260616T022151Z` and records prediction-only dev/test outcomes. The residual-family diagnosis already identifies 97 residual rows, with high counts in `normalized_command`, `slots`, `task_type`, `route`, and safety fields. It also recommends inspecting residual-family clusters before any data, training, or evaluator change.

The next evidence question is not "did the model recover?" but "which strict residual clusters are most responsible, and which next action is evidence-supported?" This phase should be analysis-only and public-safe.

## Goals / Non-Goals

**Goals:**

- Create a deterministic residual-cluster inspection from committed formal public held-out evidence.
- Group failures by split, task family, field path, category, source family, and representative examples.
- Classify clusters into recommended action candidates such as label canonicalization review, additional boundary data design, safety boundary inspection, or route/task prompt/data inspection.
- Publish a public-safe JSON/Markdown report and concise Human Brief.
- Add focused tests that enforce manifest identity, prediction-only boundaries, public-safety scanning, and strict-metric interpretation.

**Non-Goals:**

- No new prediction run.
- No SFT, DPO, GRPO, or other training.
- No public sample mutation or full private corpus release.
- No evaluator relaxation, semantic-equivalence primary metric, prediction repair, prediction replacement, or prediction re-score.
- No checkpoint or adapter release.
- No production readiness, held-out recovery, private-corpus generalization, or live-browser benchmark improvement claim.

## Decisions

- Derive clusters from committed evidence artifacts only.
  - Rationale: the formal held-out prediction evidence is already observed and public-safe; re-running predictions would conflate inspection with execution.
  - Alternative considered: run another A100 prediction pass with richer logging. Rejected because the residual rows already exist and this phase is analysis-only.

- Keep strict metrics authoritative while allowing diagnostic cluster labels.
  - Rationale: cluster labels help prioritize next work, but they must not become a semantic-equivalence evaluator.
  - Alternative considered: score near-miss normalized commands or slots as partial wins. Rejected because this would change the evidence boundary.

- Publish both machine-readable JSON and Markdown.
  - Rationale: tests and later phases need stable structured fields, while the user needs a quick review surface.
  - Alternative considered: Markdown-only. Rejected because it would make future validation brittle.

- Treat next-action labels as candidates, not implementation authorization.
  - Rationale: a cluster can suggest "label canonicalization review" or "safety boundary inspection" without mutating data or training in the same phase.
  - Alternative considered: automatically generate new remediation data. Rejected because that would change scope and evidence posture.

## Risks / Trade-offs

- [Risk] Cluster labels could sound like root-cause proof. → Mitigation: label them as evidence-backed candidates and keep examples/counts visible.
- [Risk] Reports could overstate soft slot F1. → Mitigation: repeat that `slot_f1_soft` is internal diagnostic-only and strict metrics remain primary.
- [Risk] Public-safe artifacts could accidentally include private runtime details. → Mitigation: derive from committed public-sample reports only and run leak scan before commit.
- [Risk] Cluster grouping may hide individual examples. → Mitigation: include representative row IDs and field-level examples per cluster.
