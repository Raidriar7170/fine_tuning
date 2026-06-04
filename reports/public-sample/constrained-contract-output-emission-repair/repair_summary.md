# Constrained contract output emission repair summary

Status: local shared-prompt and whole-string prediction parsing repair only. This is not A100 improvement evidence.

## What changed

- Added a valid canonical Browser Task Contract one-shot example to the shared SFT prediction prompt.
- Added whole-object JSON output boundaries: first non-whitespace character must be `{`, and last non-whitespace character must be `}`.
- Kept the prompt change on the shared chat template so future training, prediction, and DPO formatting stay aligned.
- Kept prediction prompts target-safe: the current row's gold contract is still excluded from the prediction prompt.
- Preserved strict schema behavior: accepted predictions must pass `BrowserTaskContract.from_dict()`.
- Made first-pass raw prediction parsing whole-string JSON only, so Markdown/prose-wrapped raw fragments remain invalid.
- Preserved strict retry behavior: Markdown/prose-wrapped retry fragments still remain invalid.

## Prior evidence context

- Prior A100 strict-retry train-split rerun produced `0/3` schema-valid validated outputs.
- The same rerun proved strict retry rejected `3/3` wrapped JSON fragments.
- This phase prepares a stronger local first-pass output contract for a future rerun; it does not reinterpret old A100 artifacts.

## Focused validation

- `PYTHONPATH=src pytest -q tests/test_formatting_training.py::test_sft_prediction_prompt_includes_canonical_one_shot_and_whole_object_boundaries_without_gold_contract tests/test_a100_sft_prediction_smoke.py::test_sft_prediction_export_requires_explicit_opt_in_and_adapter_config`: 2 passed.
- `PYTHONPATH=src pytest -q tests/test_formatting_training.py tests/test_a100_sft_prediction_smoke.py::test_real_sft_prediction_retries_schema_invalid_missing_required_fields tests/test_a100_sft_prediction_smoke.py::test_real_sft_prediction_rejects_markdown_wrapped_retry_even_when_fragment_is_valid tests/test_a100_sft_prediction_smoke.py::test_real_sft_prediction_skips_retry_when_raw_attempt_is_valid tests/test_a100_sft_prediction_smoke.py::test_schema_retry_prompt_declares_canonical_json_only_contract_shape`: 16 passed.
- `PYTHONPATH=src pytest -q tests/test_a100_sft_prediction_smoke.py::test_real_sft_prediction_rejects_markdown_wrapped_raw_attempt_even_when_fragment_is_valid tests/test_a100_sft_prediction_smoke.py::test_real_sft_prediction_skips_retry_when_raw_attempt_is_valid tests/test_a100_sft_prediction_smoke.py::test_real_sft_prediction_rejects_markdown_wrapped_retry_even_when_fragment_is_valid tests/test_a100_sft_prediction_smoke.py::test_real_sft_prediction_retries_schema_invalid_missing_required_fields`: 4 passed.

## Full validation

- `PYTHONPATH=src pytest -q`: 132 passed.
- `uv run ruff check .`: All checks passed.
- `uv run mypy src`: Success, 16 source files.
- `voice2task.cli.data validate --public`: ok, 12 SFT rows, 26 DPO pairs.
- `voice2task.cli.data dpo-check`: ok, 26 DPO pairs.
- `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`: 4 passed, 0 failed after archive.
- `git diff --check`: passed.
- `voice2task.cli.report leak-scan`: ok, 0 findings.

## Boundaries

- No A100 training or private prediction was run in this phase.
- No checkpoint or adapter was released.
- No held-out generalization, production readiness, public full-corpus release, or live-browser benchmark improvement claim is made.
- A future A100 rerun still needs explicit user authorization.
