# Design

## Context

The source phase `run-a100-retry-template-boundary-rerun` is already archived. Its sanitized public artifacts show that retry-template boundary behavior restored schema-valid final outputs on the bounded train split, while strict exact match remains unrecovered because all three rows still fail the slot slice.

This phase must explain that residual mismatch shape only. It must not relabel the source metrics, normalize slot values, rerun predictions, or claim model-quality improvement.

## Approach

1. Load existing public-safe source artifacts:
   - `train_split_gold.jsonl`
   - `predictions.jsonl`
   - `metrics.json`
   - `schema_guard_summary.json`
   - `retry_template_boundary_diagnosis.json`
   - `manifest.json`
2. Reuse field-level alignment comparison against schema-valid prediction objects.
3. Add a narrow retry-template slot exact-match classifier:
   - `city_date_slots_instead_of_query` when gold slots are `query` and prediction slots expose `city`/`date`,
   - `query_slot_strict_string_mismatch` when both sides use `query` but exact strings differ,
   - `normalized_command_strict_string_mismatch` as secondary context when the only non-slot mismatch is normalized command.
4. Write a machine-readable diagnosis, Markdown report, manifest, leak-scan results, and Human Brief.
5. Validate that source strict metrics and non-claim boundaries are preserved.

## Alternatives Considered

- Treat `city/date` as semantically equivalent to `query`.
  - Rejected because this would add semantic-equivalence scoring and blur the strict evaluator boundary.
- Normalize spaces in `query` values before comparison.
  - Rejected because this would be slot normalization and would change exact-match interpretation.
- Run another A100 prediction pass immediately.
  - Rejected because the next useful step is understanding residual exact-match shape before changing data or policy.

## Risks And Mitigations

- Risk: Readers may infer that schema-valid recovery means quality recovery.
  - Mitigation: diagnosis and Human Brief state that exact match and slot F1 remain unrecovered.
- Risk: The report may look like a recommendation to relax evaluator metrics.
  - Mitigation: claims explicitly reject metric relaxation, semantic equivalence, and slot normalization.
- Risk: Public artifacts may accidentally include private runtime details.
  - Mitigation: run leak scans over evidence, Human Brief, and OpenSpec artifacts.
