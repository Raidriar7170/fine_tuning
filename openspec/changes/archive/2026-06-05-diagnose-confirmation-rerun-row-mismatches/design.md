## Context

The archived `run-a100-confirmation-required-train-split-rerun` phase recorded a real private-adapter prediction-only train-split rerun. It produced three sanitized public evidence rows with `prediction_source_kind=private_a100_adapter`, `prediction_split=train`, `generalization_claim=false`, `json_valid_rate=0.6667`, and `contract_exact_match=0.0000`.

The evidence already shows three different residual patterns:

- `seed-search-weather`: raw JSON object still omits `confirmation_required`; retry emits a JSON fragment wrapped in prose/Markdown and remains invalid.
- `seed-search-weather-aug-1`: final output is schema-valid, but the model selects `task_type=form_fill`, `route=open_url`, and `safety.reason=form_fill` instead of the gold weather-search contract.
- `seed-search-weather-aug-2`: final output is schema-valid and route/task type match, but strict exact match still fails because at least `normalized_command` differs from gold.

This phase turns that into an explicit public-safe diagnosis so the next phase can decide whether the remaining gap is prompt, training-target, decoding, or evaluation-explanation work.

## Goals / Non-Goals

**Goals:**
- Produce row-level field mismatch evidence for the three committed train rows.
- Separate schema invalidity, semantic field mismatch, and strict exact-match string mismatch.
- Preserve the original prediction rows and strict evaluator output unchanged.
- Link the diagnosis back to the prior A100 confirmation-required rerun evidence.
- Run fresh local validation, leak scans, Reviewer review, OpenSpec archive, and guarded commit.

**Non-Goals:**
- No A100 execution.
- No SFT, DPO, GRPO, retraining, checkpoint or adapter creation.
- No prompt, decoder, schema, parser, retry, or evaluator metric changes.
- No rule-baseline, fixture, or gold-contract substitution.
- No dev/test or full-public-sample rerun.
- No release, production-readiness, public full-corpus, model-quality, or live-browser benchmark claim.

## Decisions

1. **Generate evidence locally from committed artifacts.**
   - Rationale: the source predictions, gold train rows, metrics, and prior diagnosis are already public-safe and committed.
   - Alternative considered: rerun A100 to gather more rows. Rejected because the immediate question is interpretation of existing evidence.

2. **Classify mismatches by failure family.**
   - Rationale: one aggregate exact-match number hides materially different issues: missing required field, wrong execution channel/task type, and normalized string mismatch.
   - Alternative considered: only add narrative Markdown. Rejected because machine-readable counts make future tests and Reviewer checks sharper.

3. **Do not change evaluator behavior.**
   - Rationale: strict exact match is doing its job; this phase explains it rather than weakening it.
   - Alternative considered: normalize `normalized_command` or ignore some fields for exact match. Rejected as an evaluation-scope change that would need separate user confirmation.

## Risks / Trade-offs

- [Risk] Diagnosis accidentally sounds like a model fix. -> Mitigation: every report states it is evidence-only and no output was repaired or replaced.
- [Risk] Public artifacts leak private runtime details from inherited metadata. -> Mitigation: read only committed sanitized artifacts and run leak scans over evidence, Human Briefs, archived OpenSpec, and synced specs.
- [Risk] A later phase overreacts to exact-match `0.0`. -> Mitigation: explicitly separate exact-match string mismatch from schema and route/task mismatch.
- [Risk] Static evidence generation becomes a second source of truth. -> Mitigation: derive counts from committed predictions, train gold, and existing metrics; tests assert consistency with source artifacts.
