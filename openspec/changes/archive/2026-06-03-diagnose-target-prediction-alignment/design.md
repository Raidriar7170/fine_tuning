## Context

The schema mismatch phase established that post-recovery A100 public-sample predictions are mostly JSON objects with Browser Task Contract-like field names, but every row still fails strict contract validation. That explains why `json_valid_rate` remains `0.0`, yet it does not fully answer whether the model is close to the gold targets or whether it is emitting a parallel vocabulary such as route paths, task labels like `normalization`, and slot arrays.

The gold public sample target contracts are valid canonical Browser Task Contracts. The diagnostic should therefore compare raw prediction fields with gold target fields without changing validation behavior.

## Goals / Non-Goals

**Goals:**

- Add a public-safe target-vs-prediction alignment diagnostic for schema-invalid but contract-like predictions.
- Show aggregate mismatch counts by field path and row-level examples with sanitized gold/prediction value summaries.
- Generate bounded evidence for the existing A100 post-recovery public-sample predictions.

**Non-Goals:**

- Do not relax or replace `BrowserTaskContract` validation.
- Do not repair invalid predictions, coerce enum labels, map route paths, or convert list slots into objects.
- Do not rerun training or modify A100/private adapter artifacts.
- Do not publish checkpoints, adapters, full private corpora, private paths, or live-browser benchmark claims.
- Do not introduce generic chat fine-tuning, skill routing, GUI action policy learning, or first-phase GRPO.

## Decisions

- Add alignment diagnostics as a sibling to schema diagnostics in evaluation code.
  - Rationale: both features inspect raw predictions and emit public-safe evidence, but neither should change the strict validator or the core metric denominator.
  - Alternative considered: add this to `evaluate_predictions()` failure slices. That would make metrics heavier and still hide gold-vs-prediction value details.

- Compare only canonical top-level and nested contract fields.
  - Rationale: the first diagnostic target is the Browser Task Contract itself: `task_type`, `route`, `safety.allow`, `safety.reason`, `confirmation_required`, `slots`, `normalized_command`, `language`, and `contract_version`.
  - Alternative considered: compute semantic similarity between Chinese commands and normalized commands. That belongs in a later model-quality analysis and risks overclaiming from a tiny public sample.

- Summarize values instead of copying arbitrary raw payloads into Markdown.
  - Rationale: public reports should be readable and leak-resistant. Existing public-sample inputs are sanitized, but future diagnostics should still avoid unbounded raw logs.
  - Alternative considered: dump full gold and prediction objects per row. That is more convenient for debugging but increases report size and privacy risk.

## Risks / Trade-offs

- [Risk] Alignment diagnostics may be mistaken for schema repair. -> Mitigation: reports must state that invalid predictions remain invalid and the diagnostic does not normalize or repair outputs.
- [Risk] Field mismatch counts on schema-invalid objects can double-count a row across multiple fields. -> Mitigation: report both row count and per-field mismatch counts with clear names.
- [Risk] A tiny public sample can reveal failure patterns but cannot prove model quality. -> Mitigation: reports must avoid checkpoint, adapter, production, full-corpus, and live-browser benchmark claims.
