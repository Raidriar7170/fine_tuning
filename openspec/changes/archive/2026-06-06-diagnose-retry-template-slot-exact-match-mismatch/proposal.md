# diagnose-retry-template-slot-exact-match-mismatch

## Why

The archived A100 retry-template boundary rerun now shows `json_valid_rate=1.0` and `validated_output_schema_valid_count=3`, but strict final recovery is still incomplete: `contract_exact_match=0.0` and `slot_f1=0.0`. The remaining failures need a small public-safe diagnosis that explains why schema-valid Browser Task Contracts still miss exact match.

## What Changes

- Publish a local evidence-only row-level diagnosis derived from `reports/public-sample/a100-retry-template-boundary-rerun/`.
- Classify slot mismatch shape for each train row:
  - `city/date` slot shape emitted instead of gold `query`,
  - `query` slot emitted with strict string spacing mismatch,
  - normalized-command exact-string mismatch when present.
- Preserve the source strict metrics, schema guard evidence, retry-template boundary interpretation, and no-repair/no-normalization boundaries.
- Add focused tests, leak-scan results, and a concise Chinese Human Brief.

## Non-Goals

- No A100 execution.
- No training, fine-tuning, prediction rerun, prompt change, decoding change, retry change, schema change, parser change, evaluator change, or metric relaxation.
- No slot normalization, normalized-command normalization, semantic-equivalence scoring, prediction repair, prediction replacement, or re-score.
- No held-out generalization, model-quality improvement, production-readiness, checkpoint-release, adapter-release, public full-corpus, or live-browser benchmark claim.

## Impact

- Affected spec: `contract-evaluation`
- Affected code: row-level evaluation/report helper and focused tests only.
- Affected evidence: a new public-safe directory under `reports/public-sample/retry-template-slot-exact-match-mismatch-diagnosis/`.
