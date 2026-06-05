## Context

Current public sample rows already imply a canonical target style:

- Weather/search paraphrases map to `normalized_command="搜索北京明天天气"` even when the input says `查一下北京明天天气` or `搜北京明天的天气`.
- Navigation paraphrases map to `打开示例网站`.
- Form-fill paraphrases map to `填写邮箱并确认`.
- Unsafe payment requests map to `拒绝代替用户付款`.

The prompt currently describes `normalized_command` only as `<Chinese normalized command>` and demonstrates `搜索公开信息` in the one-shot example. That is enough for schema shape, but not enough to explain the target-writing convention that exact-match evaluation uses.

## Goals / Non-Goals

**Goals:**

- Document a conservative canonical target-writing policy for `normalized_command`.
- Make SFT/prediction prompts expose that policy without including row gold targets.
- Keep schema-preserving augmentations tied to the original canonical target.
- Add focused tests that prove the policy is visible and that public sample targets remain stable.
- Preserve strict exact-match evaluation and public evidence boundaries.

**Non-Goals:**

- No A100 execution.
- No SFT, DPO, GRPO, training, prediction rerun, checkpoint, or adapter creation.
- No evaluator metric change, semantic-equivalence scoring, normalized-string metric, prediction repair, coercion, replacement, or re-score.
- No automatic rewriting of existing dataset rows beyond the already committed canonical targets.
- No public full-corpus release, held-out generalization, production-readiness, model-quality, or live-browser benchmark claim.

## Decisions

1. **Define policy at the target-writing layer, not the evaluator layer.**
   - Rationale: exact match should remain strict; the project needs clearer gold targets before any metric discussion.
   - Alternative considered: add semantic-equivalence scoring for `搜索/查询`. Rejected because that changes evaluation success criteria and needs a separate decision.

2. **Expose policy in the shared prompt as general guidance.**
   - Rationale: both SFT training text and prediction prompt share the same `SYSTEM_PROMPT`, so a single visible policy keeps the target surface consistent.
   - Alternative considered: only document in README. Rejected because the model-visible prompt would still lack the canonical target convention.

3. **Keep rules narrow and example-backed.**
   - Rationale: the public sample is small; rules should cover current patterns without pretending to be a full Chinese normalization system.
   - Alternative considered: implement a Chinese text normalization library. Rejected as over-scoped and likely to imply metric behavior changes.

## Risks / Trade-offs

- [Risk] The policy could be mistaken for semantic-equivalence scoring. -> Mitigation: repeat that it is target-writing guidance and exact-match remains strict.
- [Risk] Prompt changes could be interpreted as model recovery. -> Mitigation: no A100/training/rerun; validation is local only.
- [Risk] Rules overfit the four public seeds. -> Mitigation: frame them as first-phase target-writing conventions and require later OpenSpec changes for broader normalization.
