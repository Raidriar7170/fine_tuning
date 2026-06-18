# Voice2Task scaled clarify slot-boundary candidate design

This is a public-safe candidate-design report for the selected scaled `clarify/slots` residual cluster. It is design evidence only: it does not materialize seed rows, generate SFT or DPO rows, rebuild manifests, train, generate predictions, change prompts, or change evaluator metrics.

## Boundary

- strict `contract_exact_match` remains primary.
- Strict `slot_f1` remains authoritative for slot scoring.
- `slot_f1_soft` remains diagnostic-only.
- Semantic equivalence is not introduced as a primary metric.
- No public sample data, private corpus, prompt, evaluator, adapter, checkpoint, or A100 job changed.
- This is not a model recovery, held-out recovery, safety improvement, production-readiness, or live-browser claim.
- Blocked-payment residuals remain deferred to a dedicated safety boundary phase.

## Summary

- Source manifest id: `public-sample-20260617T152259Z`
- Selected target: `clarify`
- Selected task family: `clarify|clarify|ambiguous_request|confirm:true|slots:ambiguity`
- Selected field path: `slots`
- Selected residual rows: `78`
- Selected residual fields: `78`
- Source families: `28`
- Source family incidence total: `78`
- Candidate themes: `['clarify_search_or_extract_ambiguity', 'clarify_navigation_or_form_fill_ambiguity', 'clarify_pronoun_or_context_missing']`
- Recommended next change: `materialize-scaled-clarify-slot-boundary-candidates`
- Recommended next step: `review_then_materialize_scaled_clarify_slot_boundary_candidates_in_one_later_bounded_phase`

## Source Count Consistency

- Selected cluster matches source cluster: `True`
- Themes cover all source families: `True`
- Themes cover all source-family incidence: `True`

## Candidate Themes

### `clarify_search_or_extract_ambiguity`

- Description: information or extraction request with an underspecified target/source
- Source family count: `10`
- Source family incidence total: `28`
- Source families: `['family-clarify-dev-2', 'family-clarify-test-2', 'scaled-public-sample-core-clarify-003', 'scaled-public-sample-core-clarify-007', 'scaled-public-sample-core-clarify-012', 'scaled-public-sample-core-clarify-016', 'scaled-public-sample-core-clarify-021', 'scaled-public-sample-core-clarify-025', 'scaled-public-sample-core-clarify-030', 'seed-clarify-ambiguous']`
- Accepted target sketch: `{'task_type': 'clarify', 'route': 'clarify', 'safety': {'allow': True, 'reason': 'ambiguous_request'}, 'confirmation_required': True, 'slots': {'ambiguity': '用户想查询或提取信息，但目标、来源或对象不明确，需要先追问。'}}`
- Rejected drift sketches: `[{'task_type': 'search', 'route': 'search_web', 'drift_reason': 'ambiguous request incorrectly treated as a searchable query'}, {'task_type': 'navigate', 'route': 'open_url', 'drift_reason': 'ambiguous destination incorrectly treated as a known URL target'}, {'task_type': 'form_fill', 'route': 'fill_form', 'drift_reason': 'missing field/value details incorrectly treated as a fillable form task'}, {'task_type': 'blocked', 'route': 'deny', 'drift_reason': 'ambiguous but not unsafe request incorrectly denied'}]`
- Suggested public utterance templates: `['帮我查一下这个的最新情况', '把那个页面里的价格提取出来', '看看这条内容具体讲了什么']`
- Intended later action: `review_before_seed_materialization`

### `clarify_navigation_or_form_fill_ambiguity`

- Description: navigation or form-fill action missing destination, field, or value details
- Source family count: `9`
- Source family incidence total: `25`
- Source families: `['family-clarify-dev-3', 'family-clarify-test-3', 'scaled-public-sample-core-clarify-004', 'scaled-public-sample-core-clarify-009', 'scaled-public-sample-core-clarify-013', 'scaled-public-sample-core-clarify-018', 'scaled-public-sample-core-clarify-022', 'scaled-public-sample-core-clarify-027', 'scaled-public-sample-core-clarify-031']`
- Accepted target sketch: `{'task_type': 'clarify', 'route': 'clarify', 'safety': {'allow': True, 'reason': 'ambiguous_request'}, 'confirmation_required': True, 'slots': {'ambiguity': '用户给出打开或填写动作，但缺少目标网站、字段或要填写的值，需要先确认。'}}`
- Rejected drift sketches: `[{'task_type': 'search', 'route': 'search_web', 'drift_reason': 'ambiguous request incorrectly treated as a searchable query'}, {'task_type': 'navigate', 'route': 'open_url', 'drift_reason': 'ambiguous destination incorrectly treated as a known URL target'}, {'task_type': 'form_fill', 'route': 'fill_form', 'drift_reason': 'missing field/value details incorrectly treated as a fillable form task'}, {'task_type': 'blocked', 'route': 'deny', 'drift_reason': 'ambiguous but not unsafe request incorrectly denied'}]`
- Suggested public utterance templates: `['打开那个官网', '把这个填到表单里', '帮我提交一下那项信息']`
- Intended later action: `review_before_seed_materialization`

### `clarify_pronoun_or_context_missing`

- Description: deictic or context-dependent wording without enough prior context
- Source family count: `9`
- Source family incidence total: `25`
- Source families: `['family-clarify-test-1', 'scaled-public-sample-core-clarify-001', 'scaled-public-sample-core-clarify-006', 'scaled-public-sample-core-clarify-010', 'scaled-public-sample-core-clarify-015', 'scaled-public-sample-core-clarify-019', 'scaled-public-sample-core-clarify-024', 'scaled-public-sample-core-clarify-028', 'scaled-public-sample-core-clarify-033']`
- Accepted target sketch: `{'task_type': 'clarify', 'route': 'clarify', 'safety': {'allow': True, 'reason': 'ambiguous_request'}, 'confirmation_required': True, 'slots': {'ambiguity': '用户使用这个、那里、刚才那个等指代词，但当前上下文不足以确定对象。'}}`
- Rejected drift sketches: `[{'task_type': 'search', 'route': 'search_web', 'drift_reason': 'ambiguous request incorrectly treated as a searchable query'}, {'task_type': 'navigate', 'route': 'open_url', 'drift_reason': 'ambiguous destination incorrectly treated as a known URL target'}, {'task_type': 'form_fill', 'route': 'fill_form', 'drift_reason': 'missing field/value details incorrectly treated as a fillable form task'}, {'task_type': 'blocked', 'route': 'deny', 'drift_reason': 'ambiguous but not unsafe request incorrectly denied'}]`
- Suggested public utterance templates: `['帮我处理一下刚才那个', '看一下这里的信息', '把它整理出来']`
- Intended later action: `review_before_seed_materialization`

## Recommended Next Step

Use this report as reviewable input for one later bounded materialization phase. That later phase may generate candidate seed/SFT/DPO artifacts, but this design phase does not do so and does not claim any model-quality improvement.
