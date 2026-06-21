# Slot Representation Design Boundary

## Current Slot Bottleneck Evidence

The current source of truth is `reports/public-sample/slot-error-mechanism-analysis/summary.json`, generated from recovered metric-reproduced step-matched Control/Treatment prediction contracts and aligned gold contracts under `reports/public-sample/step-matched-canonical-slot-ablation/raw-inputs/`.

The final decision is `MIXED_SLOT_REPRESENTATION_REQUIRED`. The analysis covers 414 dev/test samples, 471 gold slot events, and 942 prediction slot events. Gold exact-or-normalized source-copyability is 50.53%, typed-derivable coverage is 0.00%, source-absent or generation-required coverage is 49.47%, and prediction unsupported-by-source rate is 32.17%. Control/Treatment paired movement is persistent=70, recovered=10, regressed=12, net=-2.

This is analysis evidence only. It does not claim model improvement, executable quality improvement, held-out recovery, safety readiness, production readiness, checkpoint release, adapter release, or live-browser improvement.

## Error Taxonomy

The analyzer uses a deterministic primary slot mechanism plus optional secondary tags. The public taxonomy is listed in `reports/public-sample/slot-error-mechanism-analysis/slot-error-taxonomy.md` and includes exact/normalized correctness, missing or extra keys, alias-key candidates, partial spans, wrong entities/values, source-copy failures, unsupported or generated values, normalization/derived-value failures, clarify ambiguity representation failures, multivalue structure failures, type mismatches, and unclassified slot failures.

Alias-key evidence is diagnostic only. It does not repair strict matches, rewrite predictions, or change evaluator behavior.

## Source Support Results

Gold slot source support:

- Exact source-supported: 48.83%.
- Normalized source-supported: 1.70%.
- Typed-derivable: 0.00%.
- Source absent or generation required: 49.47%.
- Unsupported analysis: 0.00%.

Prediction provenance:

- Source-supported or deterministically derived prediction values: 51.80%.
- Unsupported by source: 32.17%.
- Partial span from source: 16.03%.

Unsupported by source is not automatically interpreted as hallucination. It means the current deterministic source boundary cannot prove the value from the input transcript.

## Slot Path Profile

The slot path profile in `reports/public-sample/slot-error-mechanism-analysis/slot-profile.json` shows mixed needs:

- `query`: high copyability, 82.46%; recommended as copy-or-normalize.
- `field`: high copyability, 89.66%; recommended as copy-or-normalize.
- `target`: high copyability, 85.51%; recommended as copy-or-normalize.
- `action`: high copyability, 80.70%; recommended as copy-or-normalize.
- `ambiguity`: source absent/generation-required by design; recommended as mixed structured representation.
- `reason`: source absent/generation-required by design; recommended as mixed structured representation.
- `url`: mostly not verbatim in source under the bounded rules; recommended as mixed representation with deterministic URL normalization support where available.
- `city`: one low-confidence extra-key regression; schema constraints are the right interpretation, not a broad representation conclusion.

Top task families by movement pressure are `blocked:deny`, `clarify:clarify`, `form_fill:fill_form`, `navigate:open_url`, `search:search_web`, and `extract:extract_page`.

## Representation Boundaries

`COPY_SPAN` fits high-copyability fields such as `query`, `field`, `target`, and `action` when the source span is exact or deterministically normalized.

`COPY_THEN_TYPED_NORMALIZE` remains a future option, but this analysis found 0.00% typed-derivable gold slot coverage in the current recovered inputs. It should not be the first implementation change.

`ENUM_OR_CLASSIFICATION` fits finite decisions only; the current slot residuals do not justify converting open entities or free text into enums.

`TASK_SCHEMA_CONSTRAINED_KEY` fits missing/extra/alias key issues, especially low-frequency extra-key regressions such as `city`, but key constraints alone do not cover the mixed value mechanisms.

`BOUNDED_STRUCTURED_GENERATION` fits `ambiguity` and blocked `reason` fields where values often are not copied from the source but can still be represented with bounded provenance and typed structure.

`LIMITED_FREE_GENERATION` should be reserved for cases that cannot be copied, normalized, classified, or represented structurally.

## Recommended Internal Representation

The recommended next change is `design-hybrid-slot-representation-v1`. A future design may define an internal-only shape like:

```text
SlotValueRepresentation
- value
- value_type
- provenance
- source_span (optional)
- normalization_rule (optional)
```

This stage does not implement that shape. The representation should remain internal and evidence-bound:

- `source_span` only applies to copyable fields.
- `provenance` cannot be freely asserted by the model.
- `normalization_rule` must come from an allowlist.
- unsupported/generated values must remain explicit rather than silently repaired.

## V1 And ContractCoreV2 Compatibility

BrowserTaskContract V1 remains the external schema. ContractCoreV2 remains unchanged. Current training targets remain V1 JSON contracts. Downstream runtime consumers remain V1-compatible.

Any future internal representation must serialize back to the existing V1 `slots` object without changing strict evaluator semantics. It must also avoid changing the internal ContractCoreV2 preserve path, whose current status is `INTERNAL_V2_CORE_READY_RENDERER_PARTIAL`.

## Future Training-Target Implications

Future training-target work would require a separate OpenSpec change. It would need to decide whether the model predicts span/provenance fields directly, whether provenance is computed after prediction, and how strict slot metrics remain comparable to historical V1 evidence.

This analysis does not authorize a new training target, adapter rerun, DPO phase, challenge-set build, or evaluator relaxation.

## Migration Risk

- Internal representation may drift from V1 serialization unless roundtrip compatibility is tested.
- Typed normalization can be mistaken for evaluator relaxation unless it stays outside strict scoring.
- Span provenance can be overclaimed unless source-span checks are deterministic and verifier-owned.
- Structured generation for `ambiguity` and `reason` can become free generation unless bounded value types and schema constraints are explicit.

## Non-Goals

- No BrowserTaskContract V1 change.
- No ContractCoreV2 change.
- No current training target change.
- No downstream runtime migration.
- No prediction repair, alias repair, semantic-equivalence scoring, or LLM judge.
- No model, executable, production, safety, held-out, checkpoint, adapter, DPO, or live-browser improvement claim.
