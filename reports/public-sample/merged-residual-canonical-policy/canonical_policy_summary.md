# Voice2Task merged residual canonical policy

This is local prompt/policy hardening only. No A100 execution was performed, no
training or prediction rerun was performed, no evaluator metric was changed, and
no historical prediction was repaired or re-scored.

## Boundary

- strict `contract_exact_match` remains primary.
- Strict slot F1 remains authoritative for slot scoring.
- Soft slot F1 remains internal diagnostic-only.
- Exact canonical phrases are shared public policy text, not row-specific full
  gold target contracts.
- This is not held-out recovery, model recovery, production readiness, a
  checkpoint release, an adapter release, or a live-browser benchmark claim.

## Source Residuals

- Source prior phase: `reports/public-sample/merged-slot-value-residual-diagnosis`
- Residual rows: `4`
- Residual categories: `{"normalized_command_strict_string_mismatch": 1, "slot_value_strict_mismatch_soft_match": 3}`
- Strict exact match: `{"dev": 0.5, "test": 0.8333333333333334}`

## Hardened Canonical Policy

- Ambiguous clarify canonical phrase count: `3`
- Unsafe payment canonical command count: `1`
- Prompt exposes `slots.ambiguity="目标不明确，未指定具体网站或页面"`: `true`
- Prompt exposes `normalized_command="拒绝代替用户付款"`: `true`
- Prompt marks shorter ambiguity variants and order-refusal wording as strict-wrong: `true`

## Validation

- pytest: `274 passed`
- ruff: `All checks passed!`
- mypy: `Success: no issues found in 16 source files`
- OpenSpec all strict: `pass`
- leak scan: `pass`
- git diff check: `pass`
- Max public-sample SFT training text length: `2039 / 2048`

## Recommended Next Step

If this local policy hardening is accepted, the next separate phase should be a
bounded 7B A100 prediction/evaluation rerun that measures train/dev/test strict
metrics with the hardened prompt policy. That later phase should not be treated
as already proven by this local evidence.
