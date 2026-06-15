# Voice2Task slot value generalization materialized candidates

This is candidate data only: it materializes reviewed slot value generalization cases into a standalone public-safe candidate dataset, not merged into seed_traces.jsonl and not used as training evidence yet.

## Boundary

- Candidate rows are not formal public sample rows yet.
- Formal public sample seed, SFT, DPO, and manifest files are not rewritten.
- No DPO pairs, SFT training, prediction run, or A100 execution is performed.
- strict `contract_exact_match` remains primary.
- Soft slot F1 and semantic equivalence remain diagnostic-only.
- This is not a model recovery, held-out recovery, checkpoint, adapter, production, or live-browser claim.

## Summary

- Candidate groups: `4`
- Candidate seed rows: `4`
- Candidate SFT rows: `12`
- Formal public sample seed rows: `10`
- Formal public sample SFT rows: `30`
- Formal public sample DPO pairs: `90`
- Public sample modified: `False`
- Recommended next step: `decide_candidate_merge_or_local_sft_probe`

## Candidate Case Groups

### `blocked-payment-normalized-command-paraphrase`

- Candidate seed: `candidate-blocked-payment-canonical-command`
- Candidate SFT rows: `['candidate-blocked-payment-canonical-command', 'candidate-blocked-payment-canonical-command-aug-1', 'candidate-blocked-payment-canonical-command-aug-2']`
- Source family: `seed-block-purchase`
- Residual bucket: `normalized_command_paraphrase_drift`
- Affected fields: `['normalized_command']`
- Canonical gold values: `[{'field_path': 'normalized_command', 'value': '拒绝代替用户付款'}]`

### `clarify-ambiguous-slot-value-canonical-phrase`

- Candidate seed: `candidate-clarify-ambiguous-canonical-scope`
- Candidate SFT rows: `['candidate-clarify-ambiguous-canonical-scope', 'candidate-clarify-ambiguous-canonical-scope-aug-1', 'candidate-clarify-ambiguous-canonical-scope-aug-2']`
- Source family: `seed-clarify-ambiguous`
- Residual bucket: `slot_value_canonical_phrase_drift`
- Affected fields: `['slots']`
- Canonical gold values: `[{'field_path': 'slots', 'value': {'ambiguity': '目标不明确，未指定具体网站或页面'}}]`

### `form-email-slot-value-language-variant`

- Candidate seed: `candidate-form-email-canonical-field`
- Candidate SFT rows: `['candidate-form-email-canonical-field', 'candidate-form-email-canonical-field-aug-1', 'candidate-form-email-canonical-field-aug-2']`
- Source family: `seed-form-email`
- Residual bucket: `slot_value_language_variant`
- Affected fields: `['slots']`
- Canonical gold values: `[{'field_path': 'slots', 'value': {'field': '邮箱'}}]`

### `navigate-open-url-normalized-command-paraphrase`

- Candidate seed: `candidate-navigate-open-url-canonical-command`
- Candidate SFT rows: `['candidate-navigate-open-url-canonical-command', 'candidate-navigate-open-url-canonical-command-aug-1', 'candidate-navigate-open-url-canonical-command-aug-2']`
- Source family: `seed-open-example`
- Residual bucket: `normalized_command_paraphrase_drift`
- Affected fields: `['normalized_command']`
- Canonical gold values: `[{'field_path': 'normalized_command', 'value': '打开示例网站'}]`

## Recommended Next Step

Decide in a later bounded OpenSpec phase whether to merge the candidates into the formal public sample or run a small local/A100 SFT probe. That later phase should keep DPO, evaluator relaxation, and model-quality claims separate unless explicitly approved.
