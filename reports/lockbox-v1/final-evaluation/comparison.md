# Lockbox v1 Final Evaluation

Aggregate metrics only. No row-level failure analysis is included in this public report.

| Metric | Base | Final SFT | Delta |
| --- | ---: | ---: | ---: |
| `json_parse_rate` | 1.0000 | 0.9917 | -0.0083 |
| `strict_schema_valid_rate` | 1.0000 | 0.9833 | -0.0167 |
| `semantic_contract_valid_rate` | 0.8250 | 0.8667 | 0.0417 |
| `contract_exact_match` | 0.0167 | 0.0083 | -0.0083 |
| `slot_f1` | 0.0417 | 0.0500 | 0.0083 |
| `slot_f1_soft` | 0.3783 | 0.3867 | 0.0084 |
| `task_type_accuracy` | 0.7917 | 0.8583 | 0.0667 |
| `route_accuracy` | 0.8000 | 0.8583 | 0.0583 |
| `confirmation_accuracy` | 0.7083 | 0.7917 | 0.0833 |
| `safety_precision` | 0.8421 | 1.0000 | 0.1579 |
| `safety_recall` | 1.0000 | 0.9375 | -0.0625 |
| `safety_tp` | 16.0000 | 15.0000 | -1.0000 |
| `safety_fp` | 3.0000 | 0.0000 | -3.0000 |
| `safety_fn` | 0.0000 | 1.0000 | 1.0000 |
| `safety_predicted_positive_support` | 19.0000 | 15.0000 | -4.0000 |
| `safety_gold_positive_support` | 16.0000 | 16.0000 | 0.0000 |

Claim boundary: this is a one-look frozen-lockbox result under the pre-registered prompt, decoding, schema guard, and evaluator. It does not justify post-hoc lockbox tuning.
