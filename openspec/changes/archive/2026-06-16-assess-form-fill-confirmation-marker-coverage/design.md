## Context

The archived `define-form-fill-confirmation-field-policy` phase established that `missing_confirmation_marker` is the largest current form-fill policy section, with 27 cluster-row incidences and 27 residual fields in the formal public held-out residual evidence. However, the repository already contains a previous form-fill remediation chain:

- `reports/public-sample/form-fill-remediation-case-design/`
- `reports/public-sample/form-fill-remediation-materialized-candidates/`
- `reports/public-sample/form-fill-remediation-public-sample-merge/`
- `reports/public-sample/form-fill-remediation-candidate-integration-preview/`
- `reports/public-sample/...evaluate-form-fill...` evidence through archived OpenSpec changes

This phase assesses coverage between the new confirmation-marker policy and that existing remediation chain. It is a decision and evidence phase only.

## Goals / Non-Goals

**Goals:**

- Read only committed public-safe artifacts.
- Compare the `confirmation_markers` policy section with existing form-fill remediation case design and materialized candidate artifacts.
- Record coverage signals such as candidate case count, represented field labels, whether candidates include explicit confirmation wording, whether materialization/merge already occurred, and whether held-out evaluation still shows confirmation-marker residuals.
- Produce JSON, Markdown, manifest, and Human Brief artifacts with a bounded recommended next action.
- Add tests that enforce public-safety boundaries, source consistency, and no data/training/evaluator changes.

**Non-Goals:**

- No new candidate rows, seed traces, public sample splits, SFT rows, DPO pairs, or held-out gold labels.
- No prompt change, gold policy change, evaluator change, prediction repair, prediction replacement, or prediction re-score.
- No A100 job, SFT, DPO, GRPO, prediction run, or live-browser smoke.
- No model recovery, held-out recovery, checkpoint release, adapter release, production readiness, private-corpus generalization, public full-corpus release, or live-browser benchmark improvement claim.

## Decisions

- Use existing public-safe artifacts as the only inputs.
  - Rationale: the goal is coverage assessment, not a new diagnosis or data-generation pass.
  - Alternative considered: reread raw predictions and public sample rows. Rejected because it would expand scope and duplicate prior residual analyses.

- Keep the assessment focused on confirmation markers only.
  - Rationale: this is the largest policy section and has a direct candidate action from the previous phase.
  - Alternative considered: assess all three policy sections in one phase. Rejected to avoid another broad remediation plan.

- Treat existing remediation artifacts as evidence, not as authorization.
  - Rationale: prior candidate materialization and merge already happened, but this assessment must not modify those artifacts or claim recovery from them.
  - Alternative considered: automatically expand materialized candidates if coverage is thin. Rejected because data mutation needs a later OpenSpec phase.

- Emit a bounded next-action decision.
  - Rationale: the loop needs a concrete next phase, but this phase should not silently choose data/prompt/training changes.
  - Alternative considered: stop after a descriptive report. Rejected because the opsx auto loop should continue when the next step can be bounded.

## Risks / Trade-offs

- [Risk] Existing candidate coverage may be confused with model recovery. -> Mitigation: report materialization and held-out metrics separately, and require new prediction/evaluation before any recovery claim.
- [Risk] Confirmation coverage may be overcounted by candidate cases that share wording but not field diversity. -> Mitigation: report represented field labels and source family overlap instead of a single pass/fail.
- [Risk] The assessment may push toward data mutation. -> Mitigation: output only a recommended next OpenSpec phase and preserve unsupported changes.
- [Risk] Public artifacts may accidentally include private paths or raw logs. -> Mitigation: derive from committed public-safe reports and run leak scan over outputs, Human Brief, and OpenSpec archive.
