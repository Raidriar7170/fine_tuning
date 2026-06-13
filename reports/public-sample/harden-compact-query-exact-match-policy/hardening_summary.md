# Compact Query Exact-Match Policy Hardening

## Conclusion

This phase locally fixes the P1 review issues around public sample synchronization, compact-query prompt policy, DPO `wrong_task_type` validation, PEFT merge compatibility, markdown fence suppression, and public-safe reporting boundaries. It does not claim A100 recovery, production readiness, or model-quality improvement.

## What Changed

- Public-safe seed fixtures were expanded to 6 rows and the derived public SFT/DPO/manifest artifacts were regenerated to `18` SFT rows and `46` DPO pairs.
- `wrong_task_type` hard negatives now validate that the rejected contract changes `task_type`; the public DPO sample contains `6` such pairs.
- The SFT training prompt now exposes compact exact-match guidance: `normalized_command` should be `搜索` plus the same compact phrase used in `slots.query`, without adding extra `的`, and without decomposing into `city/date/topic`.
- Prediction prompt comparison now treats the prediction-only one-shot as non-core when checking SFT target-template alignment.
- Markdown fence suppression keeps tokenizer-derived multi-token `bad_words_ids`.
- Real PEFT adapters are merged only when `merge_and_unload` exists, preserving local fake-model tests.
- `slot_f1_soft` remains an internal diagnostic; strict `slot_f1` and `contract_exact_match` remain authoritative.

## Key Files

- `src/voice2task/formatting.py`
- `src/voice2task/dataset.py`
- `src/voice2task/dpo.py`
- `src/voice2task/evaluation.py`
- `src/voice2task/training.py`
- `data/public-samples/manifest_public_sample.json`
- `reports/experiment_report.md`
- `openspec/changes/harden-compact-query-exact-match-policy/`

## Validation

- `PYTHONPATH=src pytest -q tests/test_evaluator_reports.py::test_source_diagnostics_include_sft_target_template_alignment_evidence tests/test_a100_sft_prediction_smoke.py::test_compact_query_slot_preservation_pack_is_public_safe_and_bounded`: `2 passed`
- `PYTHONPATH=src pytest -q tests/test_formatting_training.py tests/test_dataset_builder.py tests/test_dpo_validation.py tests/test_a100_sft_prediction_smoke.py::test_compact_query_slot_preservation_pack_is_public_safe_and_bounded`: `32 passed`
- `PYTHONPATH=src pytest -q`: `195 passed`
- `uv run ruff check .`: `All checks passed`
- `uv run mypy src`: `Success: no issues found in 16 source files`
- Public data validation: `ok=true`, `sft_rows=18`, `dpo_pairs=46`
- DPO check: `total_pairs=46`, `wrong_task_type=6`, `decomposed_search_slots=1`
- Leak scan over report/data/OpenSpec evidence: `ok=true`, `findings=[]`
- `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`: `5 passed, 0 failed`
- `git diff --check`: passed

## Boundaries

- No A100 execution, training, prediction rerun, checkpoint release, adapter release, parser relaxation, prediction repair, prediction replacement, semantic-equivalence scoring as a primary metric, or strict metric relaxation was performed.
- Existing A100/private artifacts remain historical evidence only.
- This evidence pack is a local phase companion; OpenSpec artifacts remain the authoritative scope and lifecycle record.
