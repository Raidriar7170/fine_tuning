## Context

The repository already contains three bounded A100 phases: a public-sample SFT smoke, a private-adapter prediction/eval smoke, and a local contract-output recovery change. The prediction/eval smoke proved that sanitized private-adapter predictions can be copied back safely, but the model outputs were not Browser Task Contracts and produced `json_valid_rate=0.0000` with 12 schema failures.

The recovery change adjusted real SFT training text and private-adapter prediction prompts to use the same contract-only chat formatting policy. It also made invalid private-adapter output visible as a schema failure instead of collapsing it to fixture, rule-baseline, or gold-contract output. This phase performs the missing remote rerun and records the result.

## Goals / Non-Goals

**Goals:**

- Use the current repository implementation on the A100 machine for a bounded public-sample post-recovery SFT rerun.
- Keep all remote project files, adapters, checkpoints, caches, logs, private configs, and temporary outputs under the approved private A100 root.
- Rerun private-adapter prediction over the committed public sample and copy back only sanitized public-sample evidence.
- Compare post-rerun metrics and controlled smoke against the pre-recovery schema-failure baseline.
- Preserve honest failure reporting if the post-rerun still emits invalid JSON or non-contract JSON.

**Non-Goals:**

- No checkpoint, adapter, raw log, remote cache, full private corpus, host detail, SSH detail, token, secret, or private path publication.
- No generic chat fine-tuning, skill routing, GUI action policy learning, GRPO/rule-reward training, or new inference framework.
- No live-browser benchmark, production-readiness, released-checkpoint, released-adapter, or full-private-corpus claim.

## Decisions

1. Treat this as an evidence rerun, not a new modeling feature.
   - Rationale: the local behavior change is already scoped and archived; this phase should answer whether that change produces better trained-path public-sample evidence.
   - Alternative considered: create a broader model-quality improvement phase. That would change success criteria and invite overclaiming before evidence exists.

2. Use a private A100 override rather than editing committed config templates with real remote paths.
   - Rationale: committed configs remain public-safe placeholders, while remote execution can resolve `output_root`, `base_model`, and `adapter_path` under the approved private root.
   - Alternative considered: commit exact remote run paths for reproducibility. That would leak private infrastructure details and violate the public data posture.

3. Copy back a separate post-recovery evidence directory.
   - Rationale: preserving the old `a100-sft-prediction-eval-smoke` failure pack keeps the baseline auditable, while the new directory can hold post-rerun predictions, metrics, smoke, leak-scan, manifest, and report.
   - Alternative considered: overwrite the failed prediction/eval smoke in place. That would erase the symptom this recovery is meant to compare against.

4. Let metrics and smoke determine the public conclusion.
   - Rationale: schema validity may improve, remain partial, or remain zero; all are valid outcomes if the evidence is honest and public-safe.
   - Alternative considered: require schema recovery as archive success. That would hide useful negative evidence and make the phase depend on model behavior rather than correct execution and reporting.

## Risks / Trade-offs

- [Risk] Remote access, dependencies, or model cache may be unavailable -> Mitigation: record a blocked rerun state without publishing private logs or host details, and stop rather than fabricating evidence.
- [Risk] The rerun may still fail schema validation -> Mitigation: preserve sanitized invalid predictions and publish metrics/smoke as failures.
- [Risk] Sanitized evidence could accidentally include private paths or infrastructure details -> Mitigation: run leak-scan before treating artifacts as commit-ready and use placeholders for remote paths.
- [Risk] The current worktree contains previous uncommitted phase changes -> Mitigation: keep this change scoped, avoid unrelated edits, and review the combined diff before archive or final handoff.
