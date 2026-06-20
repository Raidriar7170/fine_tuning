# Step-matched canonical slot ablation comparison

- Status: `observed`
- Decision label: `REGRESSION_OR_GUARDRAIL_FAILURE`
- Gate passed: `False`
- Recommended next step: `design-and-implement-contract-v2; do_not_add_candidates_or_run_dpo`
- Scope: one fixed-seed SFT A/B; step-matched, not token-matched.
- Non-goals: no DPO/GRPO, no evaluator change, no LLM judge, no prediction repair, no semantic-equivalence scoring, no public adapter/checkpoint release.

## dev

| metric | control | treatment | delta |
| --- | ---: | ---: | ---: |
| `contract_exact_match_strict` | 0.835749 | 0.835749 | +0.000000 |
| `strict_slot_f1` | 0.871981 | 0.879227 | +0.007246 |
| `slot_value_exact_f1` | 0.877944 | 0.880342 | +0.002398 |
| `slot_value_normalized_f1` | 0.877944 | 0.880342 | +0.002398 |
| `executable_contract_pass_rate` | 0.855072 | 0.864734 | +0.009662 |
| `schema_validity` | 1.000000 | 1.000000 | +0.000000 |
| `json_valid_rate` | 1.000000 | 1.000000 | +0.000000 |
| `route_accuracy` | 0.975845 | 0.980676 | +0.004831 |
| `task_type_accuracy` | 0.975845 | 0.980676 | +0.004831 |
| `safety_recall` | 1.000000 | 1.000000 | +0.000000 |
| `unsafe_false_negative_rate` | 0.008772 | 0.000000 | -0.008772 |
| `unsafe_false_positive_rate` | 0.000000 | 0.000000 | +0.000000 |
| `requires_confirmation_accuracy` | 0.975845 | 0.980676 | +0.004831 |
| `refusal_or_clarify_accuracy` | 0.888889 | 0.890411 | +0.001522 |

Top family-level deltas:

| family | count | exact | executable | slot exact F1 |
| --- | ---: | ---: | ---: | ---: |
| `search|search_web|public_readonly|confirm:false|slots:query` | 30 | +0.033333 | +0.066667 | +0.066667 |
| `form_fill|fill_form|requires_confirmation|confirm:true|slots:field` | 42 | +0.000000 | +0.023810 | +0.023810 |
| `clarify|clarify|ambiguous_request|confirm:true|slots:ambiguity` | 45 | -0.022222 | -0.022222 | -0.022222 |
| `blocked|deny|unsafe_payment|confirm:true|slots:action,reason` | 27 | +0.000000 | +0.000000 | -0.018519 |
| `extract|extract_page|public_readonly|confirm:false|slots:target` | 36 | +0.000000 | +0.000000 | +0.000000 |
| `navigate|open_url|public_readonly|confirm:false|slots:url` | 27 | +0.000000 | +0.000000 | +0.000000 |

## test

| metric | control | treatment | delta |
| --- | ---: | ---: | ---: |
| `contract_exact_match_strict` | 0.777778 | 0.792271 | +0.014493 |
| `strict_slot_f1` | 0.826892 | 0.823671 | -0.003221 |
| `slot_value_exact_f1` | 0.819328 | 0.820296 | +0.000968 |
| `slot_value_normalized_f1` | 0.819328 | 0.820296 | +0.000968 |
| `executable_contract_pass_rate` | 0.821256 | 0.816425 | -0.004831 |
| `schema_validity` | 1.000000 | 1.000000 | +0.000000 |
| `json_valid_rate` | 1.000000 | 1.000000 | +0.000000 |
| `route_accuracy` | 0.975845 | 0.980676 | +0.004831 |
| `task_type_accuracy` | 0.975845 | 0.980676 | +0.004831 |
| `safety_recall` | 1.000000 | 1.000000 | +0.000000 |
| `unsafe_false_negative_rate` | 0.008333 | 0.008333 | +0.000000 |
| `unsafe_false_positive_rate` | 0.000000 | 0.000000 | +0.000000 |
| `requires_confirmation_accuracy` | 0.995169 | 0.995169 | +0.000000 |
| `refusal_or_clarify_accuracy` | 0.960526 | 0.960526 | +0.000000 |

Top family-level deltas:

| family | count | exact | executable | slot exact F1 |
| --- | ---: | ---: | ---: | ---: |
| `search|search_web|public_readonly|confirm:false|slots:query` | 27 | +0.074074 | +0.074074 | +0.074074 |
| `form_fill|fill_form|requires_confirmation|confirm:true|slots:field` | 45 | -0.044444 | -0.066667 | -0.066667 |
| `blocked|deny|unsafe_payment|confirm:true|slots:reason` | 3 | +0.333333 | +0.000000 | +0.111111 |
| `extract|extract_page|public_readonly|confirm:false|slots:target` | 33 | +0.030303 | +0.030303 | +0.030303 |
| `clarify|clarify|ambiguous_request|confirm:true|slots:ambiguity` | 42 | -0.023810 | -0.023810 | -0.023810 |
| `blocked|deny|unsafe_payment|confirm:true|slots:action,reason` | 30 | +0.000000 | +0.000000 | +0.000000 |
| `navigate|open_url|public_readonly|confirm:false|slots:url` | 27 | +0.074074 | +0.000000 | +0.000000 |

## Required Questions

- Step-matched: yes; both arms use the same explicit max_steps and scheduler step count.
- Examples/tokens: examples are step-matched by optimizer updates; target token exposure is recorded but not matched.
- Canonical data gain: answer is limited to observed treatment-minus-control deltas in comparison.json.
- Search concentration: see family-level-deltas.json for concentration by family.
- Regressions: see paired-row-analysis.json exact/executable/slot regressions.
- Safety and confirmation: see safety and confirmation regression counts plus guardrail deltas.
- Decision label: REGRESSION_OR_GUARDRAIL_FAILURE.
- Next recommendation: design-and-implement-contract-v2; do_not_add_candidates_or_run_dpo.
- Cannot claim: public adapter/checkpoint release, production readiness, safety certification, live-browser improvement, or held-out recovery beyond observed metrics.
