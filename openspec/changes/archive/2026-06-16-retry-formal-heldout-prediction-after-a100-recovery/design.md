## Context

The archived change `run-formal-heldout-prediction-after-confirmation-marker-merge` established the current public sample boundary, but it could only publish blocked evidence because A100 SSH preflight timed out. Its archived requirement already records the expected strict metrics, manifest id `public-sample-20260616T074315Z`, split counts of train 114/dev 69/test 69, and source counts of 98 seed rows, 252 SFT rows, and 850 DPO pairs.

This change retries the runtime-dependent portion after A100 access is restored. It must not overwrite the blocked evidence directory, because the blocked archive is valid evidence about an unavailable dependency at that time.

## Goals / Non-Goals

**Goals:**

- Retry prediction-only dev/test evaluation against the current formal public sample manifest.
- Keep private A100 runtime details, adapters, checkpoints, raw logs, caches, private paths, and SSH details outside git.
- Commit only sanitized public-sample artifacts: predictions, prediction metadata or sidecars when available, metrics, failure slices, manifest/report, leak-scan output, and a Human Brief.
- Make the retry boundary explicit: the phase may report observed current-manifest metrics, but not claim model recovery from the blocked phase.

**Non-Goals:**

- No SFT, DPO, GRPO, adapter continuation, prompt update, evaluator relaxation, semantic-equivalence scoring, prediction repair, prediction replacement, or prediction re-score.
- No checkpoint or adapter release.
- No production readiness, public full-corpus release, private-corpus generalization, or live-browser benchmark claim.
- No mutation of the formal public sample during this phase.

## Decisions

1. **Publish to a new retry evidence directory.**
   - Decision: write the recovered retry under `reports/public-sample/a100-formal-public-heldout-prediction-after-a100-recovery/`.
   - Rationale: the blocked archive and the successful/failed retry answer different evidence questions.

2. **Use the existing selected private adapter.**
   - Decision: reuse the adapter referenced by the formal-heldout prediction configs unless preflight shows it is unavailable.
   - Rationale: the phase isolates runtime recovery and avoids introducing new training variables.

3. **Fail closed again if execution becomes unsafe.**
   - Decision: if no idle GPU, adapter path, private override, or remote environment is safely available, publish blocked evidence rather than fabricate metrics.
   - Rationale: evidence integrity remains more important than filling a report slot.

## Risks / Trade-offs

- **Boundary confusion** -> Mitigation: report the manifest id, split counts, blocked-evidence path, and a clear warning that this is a retry after runtime recovery, not a model-training change.
- **Private runtime leakage** -> Mitigation: sanitize copied artifacts, commit no private override, run leak scans, and use placeholders in public configs/reports.
- **GPU contention** -> Mitigation: inspect GPU occupancy, choose only a clearly idle GPU, and stop if placement is unsafe.
- **Metrics regress or remain weak** -> Mitigation: report observed values directly; do not frame prediction-only evidence as recovery or production readiness.
