## Context

The compact-query slot-preservation A100 rerun is already committed as public-safe evidence and shows strict JSON/schema-valid output for all three train rows, while `contract_exact_match` remains `0.0`. The next safe step is a local diagnostic phase that reads those sanitized artifacts and explains the exact-match residual families before any training, data, prompt, decoding, parser, or evaluator behavior change is considered.

## Goals / Non-Goals

**Goals:**

- Derive row-level exact-match residual evidence from the latest compact-query slot-preservation rerun artifacts.
- Separate compact-query slot-shape residuals from strict `normalized_command` string residuals.
- Preserve the source strict metrics and source predictions as historical evidence.
- Publish a machine-readable JSON summary, human-readable Markdown report, manifest, leak-scan results, and Chinese Human Brief.

**Non-Goals:**

- No A100 execution, local training, prediction rerun, prompt change, decoding change, parser relaxation, evaluator metric change, semantic-equivalence scoring, slot normalization, prediction repair, prediction replacement, or re-score.
- No checkpoint release, adapter release, held-out generalization claim, production-readiness claim, public full-corpus release, model-quality improvement claim, model recovery claim, or live-browser benchmark improvement claim.
- No generic chat fine-tuning, skill routing, GUI action policy learning, or first-phase GRPO work.

## Decisions

- **Use committed sanitized rerun artifacts as the only data source.** This keeps the diagnosis reproducible and public-safe, and avoids remote/private runtime dependencies.
- **Classify residuals by exact field evidence, not semantic equivalence.** Rows with matching slots but different `normalized_command` strings remain strict exact-match mismatches; rows with compact-query slot mismatch are reported separately.
- **Generate evidence files rather than changing evaluator behavior.** The strict `contract_exact_match` metric remains inherited from the source rerun; the diagnostic explains why rows failed without reinterpreting the metric.
- **Reuse the existing evidence-pack style.** The phase follows prior report directories under `reports/public-sample/`, with leak scans, manifest links, validation commands, and bounded claims.

## Risks / Trade-offs

- **Risk: The diagnosis is only three train rows.** → Mitigation: label it as local public-sample train-split diagnosis and avoid held-out or model-quality claims.
- **Risk: Strict string differences may look semantically equivalent to a human.** → Mitigation: explicitly preserve strict exact-match semantics and do not add normalization or semantic-equivalence scoring.
- **Risk: Public reports could overstate recovery.** → Mitigation: include explicit non-claims in JSON, Markdown, manifest, Human Brief, and loop report.
- **Risk: Source artifacts may change in a future rerun.** → Mitigation: record source report paths, inherited metrics, and row ids in the manifest for traceability.
