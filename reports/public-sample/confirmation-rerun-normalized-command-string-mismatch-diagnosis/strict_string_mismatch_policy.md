# Strict string mismatch policy

This note explains how to read the committed normalized-command string mismatch diagnosis. It is interpretation guidance for reviewers, not a new metric or a rerun result.

## Policy

- `contract_exact_match` remains a hard full-contract exact-match metric.
- `normalized_command` string-mismatch diagnostics are explanatory row-level evidence only.
- The evidence does not relax, normalize, semantically score, repair, replace, or re-score predictions.
- Chinese phrase differences such as `搜索/查询` or `明天的天气/明天天气` are not automatically marked equivalent.
- Any future semantic-equivalence or normalized-string metric would require a separately scoped OpenSpec change and explicit user approval.

## Boundaries

- No A100 execution was performed for this policy clarification.
- No training, prediction rerun, prompt change, decoding change, parser change, schema change, or evaluator metric change was performed.
- This note does not claim checkpoint release, adapter release, held-out generalization, production readiness, public full-corpus release, model-quality improvement, or live-browser benchmark improvement.
