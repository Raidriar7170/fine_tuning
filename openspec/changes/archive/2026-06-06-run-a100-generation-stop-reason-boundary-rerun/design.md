## Context

The archived `instrument-generation-stop-reason-boundary` phase added stop-boundary evidence fields to future trained-adapter `generation_trace.jsonl` rows. The prior A100 retry generation trace rerun recorded raw/retry attempts, but it predates those new fields, so it cannot show whether real A100 rows now expose `max_new_tokens_hit`, `finish_state_basis`, `stop_reason_evidence`, `actual_stop_reason_recorded`, and `actual_stop_reason`.

This phase is a bounded A100 prediction-only rerun. It observes the existing private adapter on the public train split, records sanitized public-sample evidence, and keeps all private runtime material under the approved A100 project root.

## Goals / Non-Goals

**Goals:**

- Run a train-split private-adapter prediction export on an idle A100 GPU using the existing prediction path and stop-boundary instrumentation.
- Preserve strict final metrics and raw/retry generation observations as separate evidence.
- Publish a public-safe evidence pack with:
  - predictions, metrics, prompt snapshot, raw decoded summary, generation trace, schema guard summary, stop-boundary diagnosis, manifest, leak scans, and Human Brief
  - per-row raw/retry stop-boundary field availability and values
  - explicit non-claim boundaries

**Non-Goals:**

- No training, checkpoint release, adapter release, decoding change, retry prompt change, parser relaxation, evaluator metric change, output repair, prediction re-score, semantic-equivalence scoring, slot normalization, public full-corpus release, or live-browser benchmark claim.
- No generic chat fine-tuning, skill routing, GUI action policy learning, or first-phase GRPO.
- No private paths, host details, raw logs, private overrides, caches, checkpoints, adapters, SSH details, tokens, or private corpus rows in committed artifacts.

## Decisions

1. Use a prediction-only train-split rerun, not a training rerun.
   - Rationale: the instrumentation question is about exported generation trace evidence, and training would change more variables than needed.
   - Alternative rejected: retrain or tune decoding before observing the new fields. That would conflate instrumentation evidence with behavior change.

2. Keep strict metrics and generation-trace observations separate.
   - Rationale: stop-boundary trace fields can explain what was observed during generation; they do not make invalid predictions valid.
   - Alternative rejected: summarize the rerun as model recovery or quality improvement. That would overclaim the evidence.

3. Use the A100 only under the approved runtime boundary.
   - Rationale: AGENTS allows suitable GPU-heavy work on A100, but files created by this phase must stay under the AGENTS-defined approved A100 root, GPU occupancy must be checked first, and public artifacts must be sanitized.
   - Alternative rejected: local fixture rerun only. That would not answer the real private-adapter observation question.

## Risks / Trade-offs

- [Risk] No GPU is safely idle. -> Mitigation: stop before launching if occupancy or process ownership is unclear.
- [Risk] Remote access or private override is unavailable. -> Mitigation: stop with a hard-stop reason rather than inventing fixture evidence.
- [Risk] Outputs remain schema-invalid. -> Mitigation: preserve the failure evidence and avoid parser repair or model recovery claims.
- [Risk] Stop-boundary fields remain insufficient to prove actual stop reason. -> Mitigation: report `actual_stop_reason_recorded` directly and keep any next decoding-policy work as a separate decision.
