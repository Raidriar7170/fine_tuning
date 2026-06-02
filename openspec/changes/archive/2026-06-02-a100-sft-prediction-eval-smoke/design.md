## Context

The previous A100 smoke phase produced sanitized metadata proving the public-sample SFT training command completed once on the A100 machine. The current public evidence intentionally did not copy model predictions, checkpoints, adapters, raw logs, or private remote paths into git, so the repository cannot yet show whether the trained adapter can emit schema-valid public-sample contracts that pass the existing contract ladder and controlled smoke.

This change bridges that gap with a bounded evidence path. The private A100 side may load the trained adapter and generate predictions, but the repository only receives sanitized prediction rows, aggregate metrics, controlled smoke status, and evidence manifests.

## Goals / Non-Goals

**Goals:**

- Add a prediction export interface that can run against a trained adapter only with explicit opt-in.
- Keep the committed prediction artifact small, public-sample-only, and free of private infrastructure details.
- Reuse the existing evaluator for contract metrics and controlled smoke rather than inventing a separate scoring layer.
- Extend leak-scan and tests so public evidence cannot accidentally contain raw logs, checkpoints, adapters, private paths, secrets, or oversized generated corpora.
- Generate a concise Chinese Human Brief HTML for the phase from the resulting artifacts and validation outputs.

**Non-Goals:**

- No checkpoint, adapter, or model-card release.
- No full local/private corpus training or prediction publication.
- No generic chat fine-tuning, skill routing, GUI action policy learning, or first-phase GRPO/rule reward training.
- No live-browser benchmark improvement claim; controlled smoke remains separate from live-browser success.
- No requirement to rerun full private training if an existing private A100 adapter path is already available.

## Decisions

1. Public predictions use the same prediction file shape already accepted by `voice2task-eval metrics`.

   Rationale: the evaluator already expects gold rows plus prediction rows and can compute contract ladder metrics. Reusing that shape keeps the phase small and testable.

   Alternative considered: introduce a new prediction schema. That would add review overhead without improving first-phase evidence.

2. Prediction export is explicit and fail-closed.

   Rationale: loading a trained adapter is a heavy/private operation. The CLI path must require an explicit `--run-prediction` style opt-in or a clearly named fixture mode so local tests cannot accidentally load private models.

   Alternative considered: auto-run predictions after training. That risks copying private paths/logs into evidence and makes validation less bounded.

3. Evidence is split into sanitized predictions, metrics, controlled smoke, manifest, and report.

   Rationale: reviewers need to inspect outputs and metrics, while privacy checks need concrete files to scan. Keeping these artifacts separate makes overclaim and leakage easier to audit.

   Alternative considered: one large report file. That is harder to validate and more likely to mix raw evidence with prose.

4. The committed smoke can use a deterministic trained-path fixture when the private adapter is unavailable locally, but the report must label its source honestly.

   Rationale: local CI should verify the evidence pipeline without requiring the A100 machine or model files. Actual private A100 prediction execution remains a separate command recorded in sanitized metadata.

   Alternative considered: block all local validation unless the private adapter exists. That would make the repository difficult to review and would not improve public safety.

## Risks / Trade-offs

- Private adapter path unavailable during local validation -> Use fixture-mode tests for the repository pipeline and reserve private model loading for the A100 runbook.
- Prediction artifact overstates model quality -> Reports must label results as public-sample prediction/eval smoke, not benchmark or production readiness.
- Sanitized predictions accidentally include prompts, logs, or paths -> Leak-scan covers prediction/evidence directories and rejects local absolute paths, secrets, private IPs, SSH details, raw private rows, oversized JSONL corpora, checkpoints, and adapters.
- Controlled smoke is mistaken for live-browser success -> Report controlled smoke separately from contract metrics and include explicit non-claim wording.
- ModelSource ambiguity from Hugging Face vs ModelScope -> Metadata records the source label without exposing private cache paths.
