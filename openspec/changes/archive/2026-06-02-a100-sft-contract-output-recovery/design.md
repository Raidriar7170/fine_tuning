## Context

The previous A100 trained-path prediction/evaluation smoke proved that the evidence pipeline can run and stay public-safe, but the private adapter predictions were not Browser Task Contract JSON. The committed prediction rows show generic normalization/task-description structures and `"{}"` values, and the metrics report records `json_valid_rate=0.0000` with 12 schema failures. The current training and prediction code formats conversations as plain `role: content` text; Qwen-family instruction models are more likely to follow structured output when training and inference share the tokenizer chat template.

## Goals / Non-Goals

**Goals:**

- Make real SFT training and trained-adapter prediction use consistent contract-only conversation formatting.
- Preserve a local deterministic fallback so tests and dry-run validation do not need model downloads.
- Keep evaluation honest: failed model outputs remain schema failures unless a real rerun produces valid contracts.
- Add recovery evidence surfaces that can compare the failed pre-recovery smoke with post-rerun public-sample metrics without leaking private paths, host details, checkpoints, adapters, caches, or raw logs.

**Non-Goals:**

- No generic chat fine-tuning, skill routing, GUI action policy learning, or first-phase GRPO/rule reward training.
- No checkpoint, adapter, full private corpus, or remote log publication.
- No rule-normalizer or fixture fallback that makes private adapter outputs appear better than they are.
- No live-browser benchmark, production-readiness, or released-model-quality claim.

## Decisions

1. Use tokenizer chat templates when available for both SFT training text and prediction prompts.
   - Rationale: the same message structure should reach the model during training and inference, and Qwen-family instruction models already define a chat serialization contract.
   - Alternative considered: keep plain `system: ...` / `user: ...` text and only strengthen the system prompt. This is less invasive, but it leaves the training/inference format mismatch with the base model's instruction format unresolved.

2. Keep a deterministic plain-text fallback.
   - Rationale: local tests, dry-run metadata, and minimal runtimes should not require downloading tokenizers or installing heavy training dependencies.
   - Alternative considered: require chat-template-capable tokenizers everywhere. That would make local validation too dependent on remote model availability.

3. Improve contract instructions, not post-hoc success masking.
   - Rationale: schema failures are model-output evidence. They should be fixed by the training/prediction path and rerun evidence, not hidden by converting invalid predictions to fixtures or rule-normalized contracts.
   - Alternative considered: add a contract repair layer. That may be useful later for production resilience, but it would blur model-output quality and needs a separate scoped change.

4. Treat recovery evidence as an honest comparison surface.
   - Rationale: reviewers need to see that the old smoke failed schema validation and whether a later rerun actually improves it. The report should record pre-recovery metrics, post-rerun metrics when present, controlled smoke, leak-scan status, and claim boundaries.
   - Alternative considered: overwrite the previous evidence pack. Keeping a named recovery pack avoids losing the failure history.

## Risks / Trade-offs

- [Risk] Chat-template serialization differs by tokenizer implementation -> Mitigation: isolate formatting helpers and test both a fake chat-template tokenizer and the fallback path.
- [Risk] A local implementation cannot prove a remote A100 rerun improves schema validity -> Mitigation: separate local code validation from rerun evidence and avoid improvement claims until post-rerun metrics exist.
- [Risk] Stronger instructions still may not recover a tiny public-sample adapter -> Mitigation: preserve failure slices and make the next evidence pack explicit about model-output limitations.
- [Risk] Public reports could overstate the phase -> Mitigation: keep release status `not_released`, scan public artifacts, and explicitly exclude checkpoint, production, and live-browser benchmark claims.
