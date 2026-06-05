# Normalized-command canonicalization policy

This note describes the first-phase target-writing policy for gold `normalized_command` values. It is not a model run, not a new evaluator metric, and not semantic-equivalence scoring.

## Policy

- `normalized_command` gold targets are canonical Chinese intent phrases, not verbatim transcripts or ASR text.
- Schema-preserving paraphrases keep the same target contract, including the same `normalized_command`.
- Search/information targets prefer `搜索` plus a concise query phrase, for example `搜索北京明天天气`.
- Navigation targets use concise open-site intent phrases such as `打开示例网站`.
- Confirmation-required form-fill targets use concise fill-and-confirm phrases such as `填写邮箱并确认`.
- Unsafe payment denial targets use concise refusal phrases such as `拒绝代替用户付款`.

## Boundaries

- `contract_exact_match` remains a strict full-contract exact-match metric.
- This policy does not normalize predictions, mark `搜索/查询` or `明天的天气/明天天气` equivalent, repair predictions, or re-score prior evidence.
- No A100 execution, training, prediction rerun, evaluator metric change, checkpoint release, adapter release, held-out generalization, production-readiness claim, public full-corpus release, model-quality claim, or live-browser benchmark claim occurred in this phase.
