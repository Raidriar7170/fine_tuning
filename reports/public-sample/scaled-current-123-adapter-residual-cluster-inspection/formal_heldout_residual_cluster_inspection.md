# Voice2Task scaled current-123 adapter residual cluster inspection

This is an analysis-only residual cluster inspection derived from committed formal public held-out evidence. It is not a prediction run, not training, not data mutation, not held-out recovery, and not evaluator relaxation.

## Boundary

- strict `contract_exact_match` remains primary.
- Strict `slot_f1` remains authoritative for slot scoring.
- `slot_f1_soft` remains internal diagnostic-only.
- Predictions are not repaired, replaced, rewritten, normalized, or re-scored.
- This report does not authorize data, training, prompt, or evaluator changes.

## Summary

- Source residual diagnosis kind: `formal_public_heldout_residual_family_diagnosis`
- Source manifest id: `public-sample-20260617T152259Z`
- Source diagnosis artifact: `reports/public-sample/scaled-current-123-adapter-residual-diagnosis/formal_heldout_residual_family_diagnosis.json`
- Strict exact match: `{'dev': 0.2463768115942029, 'test': 0.2028985507246377}`
- Strict slot F1: `{'dev': 0.28743961352657005, 'test': 0.2592592592592593}`
- Soft slot F1: `{'dev': 0.6372298122661537, 'test': 0.6107811374904073}`
- Soft slot F1 primary metric: `False`
- Residual rows: `321`
- Source residual fields: `540`
- Residual clusters: `29`
- Top cluster task family: `clarify|clarify|ambiguous_request|confirm:true|slots:ambiguity`
- Top cluster field path: `slots`
- Top cluster residual rows: `78`
- Top cluster residual fields: `78`
- Source count consistency: `{'expected_residual_rows': 321, 'clustered_residual_rows': 321, 'expected_residual_fields': 540, 'clustered_residual_fields': 540, 'ok': True}`
- Recommended next step: `review_ranked_clusters_before_data_training_or_evaluator_change`

## Aggregates

- By split residual rows: `{'dev': 156, 'test': 165}`
- By field path: `{'confirmation_required': 6, 'normalized_command': 194, 'route': 13, 'safety.allow': 1, 'safety.reason': 9, 'slots': 304, 'task_type': 13}`
- By category: `{'confirmation_required_strict_mismatch': 6, 'normalized_command_strict_string_mismatch': 194, 'route_strict_mismatch': 13, 'safety_field_strict_mismatch': 10, 'slot_strict_mismatch': 304, 'task_type_strict_mismatch': 13}`
- By source family: `{'family-blocked_payment-dev-1': 3, 'family-blocked_payment-dev-2': 7, 'family-blocked_payment-test-1': 6, 'family-blocked_payment-test-2': 3, 'family-blocked_payment-test-3': 5, 'family-clarify-dev-2': 3, 'family-clarify-dev-3': 15, 'family-clarify-test-1': 7, 'family-clarify-test-2': 6, 'family-clarify-test-3': 1, 'family-confirmation-dev-1': 5, 'family-confirmation-dev-2': 6, 'family-confirmation-dev-3': 2, 'family-confirmation-test-2': 4, 'family-confirmation-test-3': 2, 'family-extract-dev-1': 4, 'family-extract-dev-2': 6, 'family-extract-dev-3': 4, 'family-extract-test-1': 6, 'family-extract-test-2': 4, 'family-form_fill-dev-3': 2, 'family-form_fill-test-1': 3, 'family-form_fill-test-3': 7, 'family-navigation-dev-1': 2, 'family-navigation-dev-2': 4, 'family-navigation-dev-3': 3, 'family-navigation-test-1': 3, 'family-navigation-test-2': 4, 'family-navigation-test-3': 5, 'family-search-dev-1': 2, 'family-search-dev-2': 6, 'family-search-dev-3': 4, 'family-search-test-1': 4, 'family-search-test-2': 6, 'family-search-test-3': 6, 'scaled-public-sample-core-blocked_payment-001': 6, 'scaled-public-sample-core-blocked_payment-003': 6, 'scaled-public-sample-core-blocked_payment-004': 6, 'scaled-public-sample-core-blocked_payment-006': 6, 'scaled-public-sample-core-blocked_payment-007': 6, 'scaled-public-sample-core-blocked_payment-009': 6, 'scaled-public-sample-core-blocked_payment-010': 6, 'scaled-public-sample-core-blocked_payment-012': 6, 'scaled-public-sample-core-blocked_payment-013': 6, 'scaled-public-sample-core-blocked_payment-015': 6, 'scaled-public-sample-core-blocked_payment-016': 6, 'scaled-public-sample-core-blocked_payment-018': 6, 'scaled-public-sample-core-blocked_payment-019': 6, 'scaled-public-sample-core-clarify-001': 3, 'scaled-public-sample-core-clarify-003': 3, 'scaled-public-sample-core-clarify-004': 3, 'scaled-public-sample-core-clarify-006': 3, 'scaled-public-sample-core-clarify-007': 3, 'scaled-public-sample-core-clarify-009': 3, 'scaled-public-sample-core-clarify-010': 3, 'scaled-public-sample-core-clarify-012': 3, 'scaled-public-sample-core-clarify-013': 3, 'scaled-public-sample-core-clarify-015': 3, 'scaled-public-sample-core-clarify-016': 3, 'scaled-public-sample-core-clarify-018': 3, 'scaled-public-sample-core-clarify-019': 3, 'scaled-public-sample-core-clarify-021': 3, 'scaled-public-sample-core-clarify-022': 3, 'scaled-public-sample-core-clarify-024': 3, 'scaled-public-sample-core-clarify-025': 3, 'scaled-public-sample-core-clarify-027': 3, 'scaled-public-sample-core-clarify-028': 3, 'scaled-public-sample-core-clarify-030': 3, 'scaled-public-sample-core-clarify-031': 3, 'scaled-public-sample-core-clarify-033': 3, 'scaled-public-sample-core-extract-007': 2, 'scaled-public-sample-core-extract-008': 2, 'scaled-public-sample-core-extract-011': 6, 'scaled-public-sample-core-extract-013': 6, 'scaled-public-sample-core-extract-014': 6, 'scaled-public-sample-core-extract-016': 4, 'scaled-public-sample-core-extract-017': 6, 'scaled-public-sample-core-extract-019': 4, 'scaled-public-sample-core-extract-020': 2, 'scaled-public-sample-core-extract-022': 4, 'scaled-public-sample-core-extract-023': 2, 'scaled-public-sample-core-extract-025': 2, 'scaled-public-sample-core-navigation-001': 6, 'scaled-public-sample-core-navigation-003': 6, 'scaled-public-sample-core-navigation-004': 6, 'scaled-public-sample-core-navigation-006': 6, 'scaled-public-sample-core-navigation-007': 5, 'scaled-public-sample-core-navigation-009': 5, 'scaled-public-sample-core-navigation-010': 5, 'scaled-public-sample-core-navigation-012': 4, 'scaled-public-sample-core-navigation-013': 5, 'scaled-public-sample-core-navigation-015': 5, 'scaled-public-sample-core-navigation-016': 5, 'scaled-public-sample-core-search-002': 4, 'scaled-public-sample-core-search-003': 5, 'scaled-public-sample-core-search-005': 5, 'scaled-public-sample-core-search-006': 5, 'scaled-public-sample-core-search-008': 5, 'scaled-public-sample-core-search-009': 5, 'scaled-public-sample-core-search-011': 6, 'scaled-public-sample-core-search-012': 6, 'scaled-public-sample-core-search-014': 5, 'scaled-public-sample-core-search-015': 5, 'scaled-public-sample-core-search-017': 5, 'scaled-public-sample-core-search-018': 5, 'scaled-public-sample-core-search-020': 3, 'scaled-public-sample-overlay-confirmation-boundary-001': 4, 'scaled-public-sample-overlay-confirmation-boundary-002': 4, 'scaled-public-sample-overlay-confirmation-boundary-004': 4, 'scaled-public-sample-overlay-confirmation-boundary-005': 4, 'scaled-public-sample-overlay-confirmation-boundary-007': 4, 'scaled-public-sample-overlay-confirmation-boundary-008': 4, 'scaled-public-sample-overlay-confirmation-boundary-010': 4, 'scaled-public-sample-overlay-confirmation-boundary-011': 4, 'scaled-public-sample-overlay-confirmation-boundary-013': 4, 'scaled-public-sample-overlay-confirmation-boundary-014': 4, 'scaled-public-sample-overlay-confirmation-boundary-016': 5, 'scaled-public-sample-overlay-confirmation-boundary-017': 4, 'scaled-public-sample-overlay-confirmation-boundary-019': 4, 'scaled-public-sample-overlay-confirmation-boundary-020': 3, 'seed-block-purchase': 3, 'seed-clarify-ambiguous': 3, 'seed-open-example': 6}`

## Ranked Residual Clusters

### `clarify` / `clarify|clarify|ambiguous_request|confirm:true|slots:ambiguity / slots`

- Category: `slot_strict_mismatch`
- Mismatch category: `value_mismatch`
- Residual rows: `78`
- Residual rows by split: `{'dev': 42, 'test': 36}`
- Residual fields: `78`
- Source family counts: `{'family-clarify-dev-2': 3, 'family-clarify-dev-3': 3, 'family-clarify-test-1': 1, 'family-clarify-test-2': 1, 'family-clarify-test-3': 1, 'scaled-public-sample-core-clarify-001': 3, 'scaled-public-sample-core-clarify-003': 3, 'scaled-public-sample-core-clarify-004': 3, 'scaled-public-sample-core-clarify-006': 3, 'scaled-public-sample-core-clarify-007': 3, 'scaled-public-sample-core-clarify-009': 3, 'scaled-public-sample-core-clarify-010': 3, 'scaled-public-sample-core-clarify-012': 3, 'scaled-public-sample-core-clarify-013': 3, 'scaled-public-sample-core-clarify-015': 3, 'scaled-public-sample-core-clarify-016': 3, 'scaled-public-sample-core-clarify-018': 3, 'scaled-public-sample-core-clarify-019': 3, 'scaled-public-sample-core-clarify-021': 3, 'scaled-public-sample-core-clarify-022': 3, 'scaled-public-sample-core-clarify-024': 3, 'scaled-public-sample-core-clarify-025': 3, 'scaled-public-sample-core-clarify-027': 3, 'scaled-public-sample-core-clarify-028': 3, 'scaled-public-sample-core-clarify-030': 3, 'scaled-public-sample-core-clarify-031': 3, 'scaled-public-sample-core-clarify-033': 3, 'seed-clarify-ambiguous': 3}`
- Recommended action candidate: `route_intent_boundary_inspection_before_data_or_training`

Representative examples:

- `dev / seed-clarify-ambiguous / slots`: gold object with keys: ambiguity; prediction object with keys: ambiguity
- `dev / seed-clarify-ambiguous-aug-1 / slots`: gold object with keys: ambiguity; prediction object with keys: ambiguity
- `dev / seed-clarify-ambiguous-aug-2 / slots`: gold object with keys: ambiguity; prediction object with keys: ambiguity
- `dev / family-clarify-dev-2 / slots`: gold object with keys: ambiguity; prediction object with keys: ambiguity
- `dev / family-clarify-dev-2-aug-1 / slots`: gold object with keys: ambiguity; prediction object with keys: ambiguity

### `blocked` / `blocked|deny|unsafe_payment|confirm:true|slots:action,reason / slots`

- Category: `slot_strict_mismatch`
- Mismatch category: `value_mismatch`
- Residual rows: `51`
- Residual rows by split: `{'dev': 21, 'test': 30}`
- Residual fields: `51`
- Source family counts: `{'family-blocked_payment-dev-2': 3, 'family-blocked_payment-test-1': 3, 'family-blocked_payment-test-2': 3, 'family-blocked_payment-test-3': 3, 'scaled-public-sample-core-blocked_payment-001': 3, 'scaled-public-sample-core-blocked_payment-003': 3, 'scaled-public-sample-core-blocked_payment-004': 3, 'scaled-public-sample-core-blocked_payment-006': 3, 'scaled-public-sample-core-blocked_payment-007': 3, 'scaled-public-sample-core-blocked_payment-009': 3, 'scaled-public-sample-core-blocked_payment-010': 3, 'scaled-public-sample-core-blocked_payment-012': 3, 'scaled-public-sample-core-blocked_payment-013': 3, 'scaled-public-sample-core-blocked_payment-015': 3, 'scaled-public-sample-core-blocked_payment-016': 3, 'scaled-public-sample-core-blocked_payment-018': 3, 'scaled-public-sample-core-blocked_payment-019': 3}`
- Recommended action candidate: `dedicated_safety_boundary_inspection_before_data_or_training`

Representative examples:

- `dev / family-blocked_payment-dev-2 / slots`: gold object with keys: action, reason; prediction object with keys: action, reason
- `dev / family-blocked_payment-dev-2-aug-1 / slots`: gold object with keys: action, reason; prediction object with keys: action, reason
- `dev / family-blocked_payment-dev-2-aug-2 / slots`: gold object with keys: action, reason; prediction object with keys: action, reason
- `dev / scaled-public-sample-core-blocked_payment-003 / slots`: gold object with keys: action, reason; prediction object with keys: action, reason
- `dev / scaled-public-sample-core-blocked_payment-003-aug-1 / slots`: gold object with keys: action, reason; prediction object with keys: action, reason

### `search` / `search|search_web|public_readonly|confirm:false|slots:query / slots`

- Category: `slot_strict_mismatch`
- Mismatch category: `value_mismatch`
- Residual rows: `51`
- Residual rows by split: `{'dev': 25, 'test': 26}`
- Residual fields: `51`
- Source family counts: `{'family-search-dev-1': 1, 'family-search-dev-2': 3, 'family-search-dev-3': 2, 'family-search-test-1': 2, 'family-search-test-2': 3, 'family-search-test-3': 3, 'scaled-public-sample-core-search-002': 2, 'scaled-public-sample-core-search-003': 3, 'scaled-public-sample-core-search-005': 3, 'scaled-public-sample-core-search-006': 3, 'scaled-public-sample-core-search-008': 3, 'scaled-public-sample-core-search-009': 3, 'scaled-public-sample-core-search-011': 3, 'scaled-public-sample-core-search-012': 3, 'scaled-public-sample-core-search-014': 3, 'scaled-public-sample-core-search-015': 3, 'scaled-public-sample-core-search-017': 3, 'scaled-public-sample-core-search-018': 3, 'scaled-public-sample-core-search-020': 2}`
- Recommended action candidate: `label_canonicalization_review_before_data_or_training`

Representative examples:

- `dev / family-search-dev-1-aug-1 / slots`: gold object with keys: query; prediction object with keys: query
- `dev / family-search-dev-2 / slots`: gold object with keys: query; prediction object with keys: query
- `dev / family-search-dev-2-aug-1 / slots`: gold object with keys: query; prediction object with keys: query
- `dev / family-search-dev-2-aug-2 / slots`: gold object with keys: query; prediction object with keys: query
- `dev / family-search-dev-3-aug-1 / slots`: gold object with keys: query; prediction object with keys: query

### `form_fill` / `form_fill|fill_form|requires_confirmation|confirm:true|slots:field / slots`

- Category: `slot_strict_mismatch`
- Mismatch category: `value_mismatch`
- Residual rows: `50`
- Residual rows by split: `{'dev': 25, 'test': 25}`
- Residual fields: `50`
- Source family counts: `{'family-confirmation-dev-1': 1, 'family-confirmation-dev-2': 1, 'family-confirmation-dev-3': 1, 'family-confirmation-test-2': 2, 'family-confirmation-test-3': 1, 'family-form_fill-dev-3': 1, 'family-form_fill-test-1': 1, 'family-form_fill-test-3': 1, 'scaled-public-sample-overlay-confirmation-boundary-001': 3, 'scaled-public-sample-overlay-confirmation-boundary-002': 3, 'scaled-public-sample-overlay-confirmation-boundary-004': 3, 'scaled-public-sample-overlay-confirmation-boundary-005': 3, 'scaled-public-sample-overlay-confirmation-boundary-007': 3, 'scaled-public-sample-overlay-confirmation-boundary-008': 3, 'scaled-public-sample-overlay-confirmation-boundary-010': 3, 'scaled-public-sample-overlay-confirmation-boundary-011': 3, 'scaled-public-sample-overlay-confirmation-boundary-013': 3, 'scaled-public-sample-overlay-confirmation-boundary-014': 3, 'scaled-public-sample-overlay-confirmation-boundary-016': 3, 'scaled-public-sample-overlay-confirmation-boundary-017': 3, 'scaled-public-sample-overlay-confirmation-boundary-019': 3, 'scaled-public-sample-overlay-confirmation-boundary-020': 2}`
- Recommended action candidate: `inspect_form_fill_boundary_and_field_specificity_before_new_data_or_training`

Representative examples:

- `dev / family-form_fill-dev-3-aug-2 / slots`: gold object with keys: field; prediction object with keys: field
- `dev / family-confirmation-dev-1-aug-2 / slots`: gold object with keys: field; prediction object with keys: ambiguity
- `dev / family-confirmation-dev-2-aug-2 / slots`: gold object with keys: field; prediction object with keys: ambiguity
- `dev / family-confirmation-dev-3-aug-2 / slots`: gold object with keys: field; prediction object with keys: field
- `dev / scaled-public-sample-overlay-confirmation-boundary-001 / slots`: gold object with keys: field; prediction object with keys: field

### `blocked` / `blocked|deny|unsafe_payment|confirm:true|slots:action,reason / normalized_command`

- Category: `normalized_command_strict_string_mismatch`
- Mismatch category: `value_mismatch`
- Residual rows: `47`
- Residual rows by split: `{'dev': 21, 'test': 26}`
- Residual fields: `47`
- Source family counts: `{'family-blocked_payment-dev-2': 3, 'family-blocked_payment-test-1': 3, 'family-blocked_payment-test-3': 2, 'scaled-public-sample-core-blocked_payment-001': 3, 'scaled-public-sample-core-blocked_payment-003': 3, 'scaled-public-sample-core-blocked_payment-004': 3, 'scaled-public-sample-core-blocked_payment-006': 3, 'scaled-public-sample-core-blocked_payment-007': 3, 'scaled-public-sample-core-blocked_payment-009': 3, 'scaled-public-sample-core-blocked_payment-010': 3, 'scaled-public-sample-core-blocked_payment-012': 3, 'scaled-public-sample-core-blocked_payment-013': 3, 'scaled-public-sample-core-blocked_payment-015': 3, 'scaled-public-sample-core-blocked_payment-016': 3, 'scaled-public-sample-core-blocked_payment-018': 3, 'scaled-public-sample-core-blocked_payment-019': 3}`
- Recommended action candidate: `dedicated_safety_boundary_inspection_before_data_or_training`

Representative examples:

- `dev / family-blocked_payment-dev-2 / normalized_command`: gold string(10): 拒绝代替用户订阅付款; prediction string(8): 拒绝代替用户订阅
- `dev / family-blocked_payment-dev-2-aug-1 / normalized_command`: gold string(10): 拒绝代替用户订阅付款; prediction string(8): 拒绝代替用户付款
- `dev / family-blocked_payment-dev-2-aug-2 / normalized_command`: gold string(10): 拒绝代替用户订阅付款; prediction string(8): 拒绝订阅扣款确认
- `dev / scaled-public-sample-core-blocked_payment-003 / normalized_command`: gold string(12): 拒绝代替用户支付操作03; prediction string(8): 拒绝代替用户付款
- `dev / scaled-public-sample-core-blocked_payment-003-aug-1 / normalized_command`: gold string(12): 拒绝代替用户支付操作03; prediction string(8): 拒绝代替用户付款

### `navigate` / `navigate|open_url|public_readonly|confirm:false|slots:url / slots`

- Category: `slot_strict_mismatch`
- Mismatch category: `value_mismatch`
- Residual rows: `41`
- Residual rows by split: `{'dev': 19, 'test': 22}`
- Residual fields: `41`
- Source family counts: `{'family-navigation-dev-2': 2, 'family-navigation-dev-3': 1, 'family-navigation-test-2': 2, 'family-navigation-test-3': 2, 'scaled-public-sample-core-navigation-001': 3, 'scaled-public-sample-core-navigation-003': 3, 'scaled-public-sample-core-navigation-004': 3, 'scaled-public-sample-core-navigation-006': 3, 'scaled-public-sample-core-navigation-007': 3, 'scaled-public-sample-core-navigation-009': 3, 'scaled-public-sample-core-navigation-010': 3, 'scaled-public-sample-core-navigation-012': 3, 'scaled-public-sample-core-navigation-013': 3, 'scaled-public-sample-core-navigation-015': 3, 'scaled-public-sample-core-navigation-016': 3, 'seed-open-example': 1}`
- Recommended action candidate: `label_canonicalization_review_before_data_or_training`

Representative examples:

- `dev / seed-open-example-aug-1 / slots`: gold object with keys: url; prediction object with keys: ambiguity
- `dev / family-navigation-dev-2 / slots`: gold object with keys: url; prediction object with keys: url
- `dev / family-navigation-dev-2-aug-2 / slots`: gold object with keys: url; prediction object with keys: url
- `dev / family-navigation-dev-3-aug-1 / slots`: gold object with keys: url; prediction object with keys: url
- `dev / scaled-public-sample-core-navigation-003 / slots`: gold object with keys: url; prediction object with keys: url

### `search` / `search|search_web|public_readonly|confirm:false|slots:query / normalized_command`

- Category: `normalized_command_strict_string_mismatch`
- Mismatch category: `value_mismatch`
- Residual rows: `41`
- Residual rows by split: `{'dev': 20, 'test': 21}`
- Residual fields: `41`
- Source family counts: `{'family-search-dev-1': 1, 'family-search-dev-2': 3, 'family-search-dev-3': 2, 'family-search-test-1': 2, 'family-search-test-2': 3, 'family-search-test-3': 3, 'scaled-public-sample-core-search-002': 2, 'scaled-public-sample-core-search-003': 2, 'scaled-public-sample-core-search-005': 2, 'scaled-public-sample-core-search-006': 2, 'scaled-public-sample-core-search-008': 2, 'scaled-public-sample-core-search-009': 2, 'scaled-public-sample-core-search-011': 3, 'scaled-public-sample-core-search-012': 3, 'scaled-public-sample-core-search-014': 2, 'scaled-public-sample-core-search-015': 2, 'scaled-public-sample-core-search-017': 2, 'scaled-public-sample-core-search-018': 2, 'scaled-public-sample-core-search-020': 1}`
- Recommended action candidate: `label_canonicalization_review_before_data_or_training`

Representative examples:

- `dev / family-search-dev-1-aug-1 / normalized_command`: gold string(11): 搜索成都博物馆开放时间; prediction string(11): 搜索成都博物馆开门时间
- `dev / family-search-dev-2 / normalized_command`: gold string(10): 搜索南京今天空气质量; prediction string(10): 搜索南京今日空气质量
- `dev / family-search-dev-2-aug-1 / normalized_command`: gold string(10): 搜索南京今天空气质量; prediction string(8): 搜索南京空气质量
- `dev / family-search-dev-2-aug-2 / normalized_command`: gold string(10): 搜索南京今天空气质量; prediction string(10): 搜索南京今日空气质量
- `dev / family-search-dev-3-aug-1 / normalized_command`: gold string(8): 搜索苏州园林门票; prediction string(10): 搜索苏州园林门票价格

### `navigate` / `navigate|open_url|public_readonly|confirm:false|slots:url / normalized_command`

- Category: `normalized_command_strict_string_mismatch`
- Mismatch category: `value_mismatch`
- Residual rows: `40`
- Residual rows by split: `{'dev': 18, 'test': 22}`
- Residual fields: `40`
- Source family counts: `{'family-navigation-dev-1': 2, 'family-navigation-dev-2': 2, 'family-navigation-dev-3': 2, 'family-navigation-test-1': 3, 'family-navigation-test-2': 2, 'family-navigation-test-3': 3, 'scaled-public-sample-core-navigation-001': 3, 'scaled-public-sample-core-navigation-003': 3, 'scaled-public-sample-core-navigation-004': 3, 'scaled-public-sample-core-navigation-006': 3, 'scaled-public-sample-core-navigation-007': 2, 'scaled-public-sample-core-navigation-009': 2, 'scaled-public-sample-core-navigation-010': 2, 'scaled-public-sample-core-navigation-012': 1, 'scaled-public-sample-core-navigation-013': 2, 'scaled-public-sample-core-navigation-015': 2, 'scaled-public-sample-core-navigation-016': 2, 'seed-open-example': 1}`
- Recommended action candidate: `label_canonicalization_review_before_data_or_training`

Representative examples:

- `dev / seed-open-example-aug-1 / normalized_command`: gold string(6): 打开示例网站; prediction string(6): 请求澄清目标
- `dev / family-navigation-dev-1-aug-1 / normalized_command`: gold string(6): 打开新闻页面; prediction string(8): 打开新闻示例站点
- `dev / family-navigation-dev-1-aug-2 / normalized_command`: gold string(6): 打开新闻页面; prediction string(6): 打开新闻网站
- `dev / family-navigation-dev-2-aug-1 / normalized_command`: gold string(6): 打开商店首页; prediction string(6): 打开商品页面
- `dev / family-navigation-dev-2-aug-2 / normalized_command`: gold string(6): 打开商店首页; prediction string(8): 打开公开读写商店

### `extract` / `extract|extract_page|public_readonly|confirm:false|slots:target / slots`

- Category: `slot_strict_mismatch`
- Mismatch category: `value_mismatch`
- Residual rows: `31`
- Residual rows by split: `{'dev': 16, 'test': 15}`
- Residual fields: `31`
- Source family counts: `{'family-extract-dev-1': 2, 'family-extract-dev-2': 2, 'family-extract-dev-3': 1, 'family-extract-test-1': 2, 'family-extract-test-2': 1, 'scaled-public-sample-core-extract-007': 1, 'scaled-public-sample-core-extract-008': 1, 'scaled-public-sample-core-extract-011': 3, 'scaled-public-sample-core-extract-013': 3, 'scaled-public-sample-core-extract-014': 3, 'scaled-public-sample-core-extract-016': 2, 'scaled-public-sample-core-extract-017': 3, 'scaled-public-sample-core-extract-019': 2, 'scaled-public-sample-core-extract-020': 1, 'scaled-public-sample-core-extract-022': 2, 'scaled-public-sample-core-extract-023': 1, 'scaled-public-sample-core-extract-025': 1}`
- Recommended action candidate: `extract_target_canonicalization_review_before_data_or_training`

Representative examples:

- `dev / family-extract-dev-1-aug-1 / slots`: gold object with keys: target; prediction object with keys: target
- `dev / family-extract-dev-1-aug-2 / slots`: gold object with keys: target; prediction object with keys: target
- `dev / family-extract-dev-2-aug-1 / slots`: gold object with keys: target; prediction object with keys: query
- `dev / family-extract-dev-2-aug-2 / slots`: gold object with keys: target; prediction object with keys: target
- `dev / family-extract-dev-3-aug-1 / slots`: gold object with keys: target; prediction object with keys: query

### `extract` / `extract|extract_page|public_readonly|confirm:false|slots:target / normalized_command`

- Category: `normalized_command_strict_string_mismatch`
- Mismatch category: `value_mismatch`
- Residual rows: `31`
- Residual rows by split: `{'dev': 16, 'test': 15}`
- Residual fields: `31`
- Source family counts: `{'family-extract-dev-1': 2, 'family-extract-dev-2': 2, 'family-extract-dev-3': 1, 'family-extract-test-1': 2, 'family-extract-test-2': 1, 'scaled-public-sample-core-extract-007': 1, 'scaled-public-sample-core-extract-008': 1, 'scaled-public-sample-core-extract-011': 3, 'scaled-public-sample-core-extract-013': 3, 'scaled-public-sample-core-extract-014': 3, 'scaled-public-sample-core-extract-016': 2, 'scaled-public-sample-core-extract-017': 3, 'scaled-public-sample-core-extract-019': 2, 'scaled-public-sample-core-extract-020': 1, 'scaled-public-sample-core-extract-022': 2, 'scaled-public-sample-core-extract-023': 1, 'scaled-public-sample-core-extract-025': 1}`
- Recommended action candidate: `extract_target_canonicalization_review_before_data_or_training`

Representative examples:

- `dev / family-extract-dev-1-aug-1 / normalized_command`: gold string(8): 提取页面作者姓名; prediction string(8): 提取页面作者信息
- `dev / family-extract-dev-1-aug-2 / normalized_command`: gold string(8): 提取页面作者姓名; prediction string(8): 提取页面作者信息
- `dev / family-extract-dev-2-aug-1 / normalized_command`: gold string(8): 提取页面客服电话; prediction string(6): 搜索客服热线
- `dev / family-extract-dev-2-aug-2 / normalized_command`: gold string(8): 提取页面客服电话; prediction string(8): 提取页面联系号码
- `dev / family-extract-dev-3-aug-1 / normalized_command`: gold string(8): 提取页面优惠信息; prediction string(6): 搜索优惠活动

### `form_fill` / `form_fill|fill_form|requires_confirmation|confirm:true|slots:field / normalized_command`

- Category: `normalized_command_strict_string_mismatch`
- Mismatch category: `value_mismatch`
- Residual rows: `28`
- Residual rows by split: `{'dev': 13, 'test': 15}`
- Residual fields: `28`
- Source family counts: `{'family-confirmation-dev-1': 1, 'family-confirmation-dev-2': 2, 'family-confirmation-dev-3': 1, 'family-confirmation-test-2': 2, 'family-confirmation-test-3': 1, 'family-form_fill-dev-3': 1, 'family-form_fill-test-1': 2, 'family-form_fill-test-3': 3, 'scaled-public-sample-overlay-confirmation-boundary-001': 1, 'scaled-public-sample-overlay-confirmation-boundary-002': 1, 'scaled-public-sample-overlay-confirmation-boundary-004': 1, 'scaled-public-sample-overlay-confirmation-boundary-005': 1, 'scaled-public-sample-overlay-confirmation-boundary-007': 1, 'scaled-public-sample-overlay-confirmation-boundary-008': 1, 'scaled-public-sample-overlay-confirmation-boundary-010': 1, 'scaled-public-sample-overlay-confirmation-boundary-011': 1, 'scaled-public-sample-overlay-confirmation-boundary-013': 1, 'scaled-public-sample-overlay-confirmation-boundary-014': 1, 'scaled-public-sample-overlay-confirmation-boundary-016': 2, 'scaled-public-sample-overlay-confirmation-boundary-017': 1, 'scaled-public-sample-overlay-confirmation-boundary-019': 1, 'scaled-public-sample-overlay-confirmation-boundary-020': 1}`
- Recommended action candidate: `inspect_form_fill_boundary_and_field_specificity_before_new_data_or_training`

Representative examples:

- `dev / family-form_fill-dev-3-aug-2 / normalized_command`: gold string(9): 填写发票抬头并确认; prediction string(9): 填写发票信息并确认
- `dev / family-confirmation-dev-1-aug-2 / normalized_command`: gold string(9): 填写预约时间并确认; prediction string(6): 请求确认时间
- `dev / family-confirmation-dev-2 / normalized_command`: gold string(9): 填写配送方式并确认; prediction string(9): 选择配送方式并确认
- `dev / family-confirmation-dev-2-aug-2 / normalized_command`: gold string(9): 填写配送方式并确认; prediction string(6): 请求澄清目标
- `dev / family-confirmation-dev-3-aug-2 / normalized_command`: gold string(9): 填写发票邮箱并确认; prediction string(9): 填写发票信息并确认

### `clarify` / `clarify|clarify|ambiguous_request|confirm:true|slots:ambiguity / normalized_command`

- Category: `normalized_command_strict_string_mismatch`
- Mismatch category: `value_mismatch`
- Residual rows: `6`
- Residual rows by split: `{'dev': 3, 'test': 3}`
- Residual fields: `6`
- Source family counts: `{'family-clarify-dev-3': 3, 'family-clarify-test-1': 2, 'family-clarify-test-2': 1}`
- Recommended action candidate: `route_intent_boundary_inspection_before_data_or_training`

Representative examples:

- `dev / family-clarify-dev-3 / normalized_command`: gold string(6): 请求澄清目标; prediction string(7): 填写表格并确认
- `dev / family-clarify-dev-3-aug-1 / normalized_command`: gold string(6): 请求澄清目标; prediction string(7): 填写表格并确认
- `dev / family-clarify-dev-3-aug-2 / normalized_command`: gold string(6): 请求澄清目标; prediction string(7): 填写表单并确认
- `test / family-clarify-test-1 / normalized_command`: gold string(6): 请求澄清目标; prediction string(8): 请求澄清目标城市
- `test / family-clarify-test-1-aug-1 / normalized_command`: gold string(6): 请求澄清目标; prediction string(4): 搜索天气

### `clarify` / `clarify|clarify|ambiguous_request|confirm:true|slots:ambiguity / task_type`

- Category: `task_type_strict_mismatch`
- Mismatch category: `value_mismatch`
- Residual rows: `5`
- Residual rows by split: `{'dev': 3, 'test': 2}`
- Residual fields: `5`
- Source family counts: `{'family-clarify-dev-3': 3, 'family-clarify-test-1': 1, 'family-clarify-test-2': 1}`
- Recommended action candidate: `route_intent_boundary_inspection_before_data_or_training`

Representative examples:

- `dev / family-clarify-dev-3 / task_type`: gold string(7): clarify; prediction string(9): form_fill
- `dev / family-clarify-dev-3-aug-1 / task_type`: gold string(7): clarify; prediction string(9): form_fill
- `dev / family-clarify-dev-3-aug-2 / task_type`: gold string(7): clarify; prediction string(9): form_fill
- `test / family-clarify-test-1-aug-1 / task_type`: gold string(7): clarify; prediction string(6): search
- `test / family-clarify-test-2-aug-1 / task_type`: gold string(7): clarify; prediction string(7): blocked

### `clarify` / `clarify|clarify|ambiguous_request|confirm:true|slots:ambiguity / route`

- Category: `route_strict_mismatch`
- Mismatch category: `value_mismatch`
- Residual rows: `5`
- Residual rows by split: `{'dev': 3, 'test': 2}`
- Residual fields: `5`
- Source family counts: `{'family-clarify-dev-3': 3, 'family-clarify-test-1': 1, 'family-clarify-test-2': 1}`
- Recommended action candidate: `route_intent_boundary_inspection_before_data_or_training`

Representative examples:

- `dev / family-clarify-dev-3 / route`: gold string(7): clarify; prediction string(9): fill_form
- `dev / family-clarify-dev-3-aug-1 / route`: gold string(7): clarify; prediction string(9): fill_form
- `dev / family-clarify-dev-3-aug-2 / route`: gold string(7): clarify; prediction string(9): fill_form
- `test / family-clarify-test-1-aug-1 / route`: gold string(7): clarify; prediction string(10): search_web
- `test / family-clarify-test-2-aug-1 / route`: gold string(7): clarify; prediction string(4): deny

### `clarify` / `clarify|clarify|ambiguous_request|confirm:true|slots:ambiguity / safety.reason`

- Category: `safety_field_strict_mismatch`
- Mismatch category: `value_mismatch`
- Residual rows: `5`
- Residual rows by split: `{'dev': 3, 'test': 2}`
- Residual fields: `5`
- Source family counts: `{'family-clarify-dev-3': 3, 'family-clarify-test-1': 1, 'family-clarify-test-2': 1}`
- Recommended action candidate: `route_intent_boundary_inspection_before_data_or_training`

Representative examples:

- `dev / family-clarify-dev-3 / safety.reason`: gold string(17): ambiguous_request; prediction string(21): requires_confirmation
- `dev / family-clarify-dev-3-aug-1 / safety.reason`: gold string(17): ambiguous_request; prediction string(21): requires_confirmation
- `dev / family-clarify-dev-3-aug-2 / safety.reason`: gold string(17): ambiguous_request; prediction string(21): requires_confirmation
- `test / family-clarify-test-1-aug-1 / safety.reason`: gold string(17): ambiguous_request; prediction string(19): information_request
- `test / family-clarify-test-2-aug-1 / safety.reason`: gold string(17): ambiguous_request; prediction string(14): unsafe_payment

### `blocked` / `blocked|deny|unsafe_payment|confirm:true|slots:action,reason / confirmation_required`

- Category: `confirmation_required_strict_mismatch`
- Mismatch category: `value_mismatch`
- Residual rows: `4`
- Residual rows by split: `{'dev': 4}`
- Residual fields: `4`
- Source family counts: `{'family-blocked_payment-dev-1': 3, 'family-blocked_payment-dev-2': 1}`
- Recommended action candidate: `dedicated_safety_boundary_inspection_before_data_or_training`

Representative examples:

- `dev / family-blocked_payment-dev-1 / confirmation_required`: gold bool: True; prediction bool: False
- `dev / family-blocked_payment-dev-1-aug-1 / confirmation_required`: gold bool: True; prediction bool: False
- `dev / family-blocked_payment-dev-1-aug-2 / confirmation_required`: gold bool: True; prediction bool: False
- `dev / family-blocked_payment-dev-2-aug-2 / confirmation_required`: gold bool: True; prediction bool: False

### `extract` / `extract|extract_page|public_readonly|confirm:false|slots:target / task_type`

- Category: `task_type_strict_mismatch`
- Mismatch category: `value_mismatch`
- Residual rows: `4`
- Residual rows by split: `{'dev': 2, 'test': 2}`
- Residual fields: `4`
- Source family counts: `{'family-extract-dev-2': 1, 'family-extract-dev-3': 1, 'family-extract-test-1': 1, 'family-extract-test-2': 1}`
- Recommended action candidate: `extract_target_canonicalization_review_before_data_or_training`

Representative examples:

- `dev / family-extract-dev-2-aug-1 / task_type`: gold string(7): extract; prediction string(6): search
- `dev / family-extract-dev-3-aug-1 / task_type`: gold string(7): extract; prediction string(6): search
- `test / family-extract-test-1-aug-1 / task_type`: gold string(7): extract; prediction string(6): search
- `test / family-extract-test-2-aug-1 / task_type`: gold string(7): extract; prediction string(6): search

### `extract` / `extract|extract_page|public_readonly|confirm:false|slots:target / route`

- Category: `route_strict_mismatch`
- Mismatch category: `value_mismatch`
- Residual rows: `4`
- Residual rows by split: `{'dev': 2, 'test': 2}`
- Residual fields: `4`
- Source family counts: `{'family-extract-dev-2': 1, 'family-extract-dev-3': 1, 'family-extract-test-1': 1, 'family-extract-test-2': 1}`
- Recommended action candidate: `extract_target_canonicalization_review_before_data_or_training`

Representative examples:

- `dev / family-extract-dev-2-aug-1 / route`: gold string(12): extract_page; prediction string(10): search_web
- `dev / family-extract-dev-3-aug-1 / route`: gold string(12): extract_page; prediction string(10): search_web
- `test / family-extract-test-1-aug-1 / route`: gold string(12): extract_page; prediction string(10): search_web
- `test / family-extract-test-2-aug-1 / route`: gold string(12): extract_page; prediction string(10): search_web

### `form_fill` / `form_fill|fill_form|requires_confirmation|confirm:true|slots:field / task_type`

- Category: `task_type_strict_mismatch`
- Mismatch category: `value_mismatch`
- Residual rows: `3`
- Residual rows by split: `{'dev': 2, 'test': 1}`
- Residual fields: `3`
- Source family counts: `{'family-confirmation-dev-1': 1, 'family-confirmation-dev-2': 1, 'family-form_fill-test-3': 1}`
- Recommended action candidate: `inspect_form_fill_boundary_and_field_specificity_before_new_data_or_training`

Representative examples:

- `dev / family-confirmation-dev-1-aug-2 / task_type`: gold string(9): form_fill; prediction string(7): clarify
- `dev / family-confirmation-dev-2-aug-2 / task_type`: gold string(9): form_fill; prediction string(7): clarify
- `test / family-form_fill-test-3-aug-2 / task_type`: gold string(9): form_fill; prediction string(7): clarify

### `form_fill` / `form_fill|fill_form|requires_confirmation|confirm:true|slots:field / route`

- Category: `route_strict_mismatch`
- Mismatch category: `value_mismatch`
- Residual rows: `3`
- Residual rows by split: `{'dev': 2, 'test': 1}`
- Residual fields: `3`
- Source family counts: `{'family-confirmation-dev-1': 1, 'family-confirmation-dev-2': 1, 'family-form_fill-test-3': 1}`
- Recommended action candidate: `inspect_form_fill_boundary_and_field_specificity_before_new_data_or_training`

Representative examples:

- `dev / family-confirmation-dev-1-aug-2 / route`: gold string(9): fill_form; prediction string(7): clarify
- `dev / family-confirmation-dev-2-aug-2 / route`: gold string(9): fill_form; prediction string(7): clarify
- `test / family-form_fill-test-3-aug-2 / route`: gold string(9): fill_form; prediction string(7): clarify

### `form_fill` / `form_fill|fill_form|requires_confirmation|confirm:true|slots:field / safety.reason`

- Category: `safety_field_strict_mismatch`
- Mismatch category: `value_mismatch`
- Residual rows: `3`
- Residual rows by split: `{'dev': 2, 'test': 1}`
- Residual fields: `3`
- Source family counts: `{'family-confirmation-dev-1': 1, 'family-confirmation-dev-2': 1, 'family-form_fill-test-3': 1}`
- Recommended action candidate: `inspect_form_fill_boundary_and_field_specificity_before_new_data_or_training`

Representative examples:

- `dev / family-confirmation-dev-1-aug-2 / safety.reason`: gold string(21): requires_confirmation; prediction string(17): ambiguous_request
- `dev / family-confirmation-dev-2-aug-2 / safety.reason`: gold string(21): requires_confirmation; prediction string(17): ambiguous_request
- `test / family-form_fill-test-3-aug-2 / safety.reason`: gold string(21): requires_confirmation; prediction string(17): ambiguous_request

### `blocked` / `blocked|deny|unsafe_payment|confirm:true|slots:reason / slots`

- Category: `slot_strict_mismatch`
- Mismatch category: `value_mismatch`
- Residual rows: `2`
- Residual rows by split: `{'test': 2}`
- Residual fields: `2`
- Source family counts: `{'seed-block-purchase': 2}`
- Recommended action candidate: `dedicated_safety_boundary_inspection_before_data_or_training`

Representative examples:

- `test / seed-block-purchase-aug-1 / slots`: gold object with keys: reason; prediction object with keys: action, reason
- `test / seed-block-purchase-aug-2 / slots`: gold object with keys: reason; prediction object with keys: action, reason

### `blocked` / `blocked|deny|unsafe_payment|confirm:true|slots:reason / normalized_command`

- Category: `normalized_command_strict_string_mismatch`
- Mismatch category: `value_mismatch`
- Residual rows: `1`
- Residual rows by split: `{'test': 1}`
- Residual fields: `1`
- Source family counts: `{'seed-block-purchase': 1}`
- Recommended action candidate: `dedicated_safety_boundary_inspection_before_data_or_training`

Representative examples:

- `test / seed-block-purchase-aug-1 / normalized_command`: gold string(8): 拒绝代替用户付款; prediction string(10): 拒绝代替用户下单付款

### `clarify` / `clarify|clarify|ambiguous_request|confirm:true|slots:ambiguity / confirmation_required`

- Category: `confirmation_required_strict_mismatch`
- Mismatch category: `value_mismatch`
- Residual rows: `1`
- Residual rows by split: `{'test': 1}`
- Residual fields: `1`
- Source family counts: `{'family-clarify-test-1': 1}`
- Recommended action candidate: `route_intent_boundary_inspection_before_data_or_training`

Representative examples:

- `test / family-clarify-test-1-aug-1 / confirmation_required`: gold bool: True; prediction bool: False

### `clarify` / `clarify|clarify|ambiguous_request|confirm:true|slots:ambiguity / safety.allow`

- Category: `safety_field_strict_mismatch`
- Mismatch category: `value_mismatch`
- Residual rows: `1`
- Residual rows by split: `{'test': 1}`
- Residual fields: `1`
- Source family counts: `{'family-clarify-test-2': 1}`
- Recommended action candidate: `route_intent_boundary_inspection_before_data_or_training`

Representative examples:

- `test / family-clarify-test-2-aug-1 / safety.allow`: gold bool: True; prediction bool: False

### `navigate` / `navigate|open_url|public_readonly|confirm:false|slots:url / task_type`

- Category: `task_type_strict_mismatch`
- Mismatch category: `value_mismatch`
- Residual rows: `1`
- Residual rows by split: `{'dev': 1}`
- Residual fields: `1`
- Source family counts: `{'seed-open-example': 1}`
- Recommended action candidate: `label_canonicalization_review_before_data_or_training`

Representative examples:

- `dev / seed-open-example-aug-1 / task_type`: gold string(8): navigate; prediction string(7): clarify

### `navigate` / `navigate|open_url|public_readonly|confirm:false|slots:url / route`

- Category: `route_strict_mismatch`
- Mismatch category: `value_mismatch`
- Residual rows: `1`
- Residual rows by split: `{'dev': 1}`
- Residual fields: `1`
- Source family counts: `{'seed-open-example': 1}`
- Recommended action candidate: `label_canonicalization_review_before_data_or_training`

Representative examples:

- `dev / seed-open-example-aug-1 / route`: gold string(8): open_url; prediction string(7): clarify

### `navigate` / `navigate|open_url|public_readonly|confirm:false|slots:url / safety.reason`

- Category: `safety_field_strict_mismatch`
- Mismatch category: `value_mismatch`
- Residual rows: `1`
- Residual rows by split: `{'dev': 1}`
- Residual fields: `1`
- Source family counts: `{'seed-open-example': 1}`
- Recommended action candidate: `label_canonicalization_review_before_data_or_training`

Representative examples:

- `dev / seed-open-example-aug-1 / safety.reason`: gold string(15): public_readonly; prediction string(17): ambiguous_request

### `navigate` / `navigate|open_url|public_readonly|confirm:false|slots:url / confirmation_required`

- Category: `confirmation_required_strict_mismatch`
- Mismatch category: `value_mismatch`
- Residual rows: `1`
- Residual rows by split: `{'dev': 1}`
- Residual fields: `1`
- Source family counts: `{'seed-open-example': 1}`
- Recommended action candidate: `label_canonicalization_review_before_data_or_training`

Representative examples:

- `dev / seed-open-example-aug-1 / confirmation_required`: gold bool: False; prediction bool: True

## Recommended Next Step

Use this cluster inspection to choose one bounded OpenSpec follow-up. Any data, training, prompt, or evaluator change must be proposed separately with its own success boundary.
