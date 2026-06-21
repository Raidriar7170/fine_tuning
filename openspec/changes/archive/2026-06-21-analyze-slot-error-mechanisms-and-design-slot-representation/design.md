## Context

The current Voice2Task truth surface says the one-seed step-matched canonical-slot SFT ablation has no stable broad benefit, the recovered-input Contract V2 projection has only partial schema/display-field benefit, and the internal ContractCoreV2 preserve path is V1-compatible but not a slot-error solution. Core slot failures remain the dominant residual, so the next useful question is slot mechanism analysis rather than another training, prediction, evaluator, or schema migration phase.

This change uses only recovered, metric-reproduced public-safe artifacts under `reports/public-sample/step-matched-canonical-slot-ablation/raw-inputs/`. It treats `prediction_contract` and `gold_contract` as immutable inputs and reports deterministic diagnostics only.

## Goals / Non-Goals

**Goals:**

- Validate the recovered-input boundary before any analysis and fail closed with `ANALYSIS_BLOCKED_INVALID_INPUT` if it is not projection-ready.
- Flatten and align nested slot values by stable slot paths across gold, Control predictions, and Treatment predictions.
- Classify slot-level residuals into deterministic mechanisms, with source-support and prediction-provenance labels.
- Quantify persistent, recovered, and introduced slot errors between Control and Treatment on the same sample and slot path.
- Recommend exactly one next bounded change and document the slot representation design boundary in `docs/slot-representation.md`.
- Produce compact public-safe artifacts and a Chinese Human Brief without changing authoritative source evidence.

**Non-Goals:**

- No SFT, DPO, GRPO, A100, SSH, GPU work, prediction rerun, checkpoint or adapter release.
- No train/dev/test split change, new/merged data, gold contract mutation, recovered prediction mutation, or prediction repair.
- No strict or layered evaluator change, exact-match relaxation, LLM judge, semantic-equivalence scoring, or automatic canonicalization.
- No BrowserTaskContract V1 change, ContractCoreV2 change, downstream runtime migration, or current training-target change.
- No claim that slot performance, executable quality, held-out recovery, safety readiness, production readiness, or live browser behavior improved.

## Decisions

1. **Independent deterministic module.** Add `src/voice2task/slot_error_analysis.py` rather than extending `contract_core_v2.py`, evaluators, or schemas. This keeps the analysis read-only and prevents accidental coupling to current runtime or evaluator semantics.

2. **Fail-closed boundary validation.** The report generator first checks `artifact-manifest.json`, `boundary-verification.json`, `metric-reproduction.json`, required JSONL files, row counts, sample-id parity, gold hash matches, recovered provenance, and no blocked artifact. If the boundary fails, it writes only `blocked.json` and stops.

3. **Path-level alignment without repair.** Slot objects are flattened into deterministic paths such as `query`, `items[0].name`, or `address.city`. Same paths align directly. Canonical alias policy is used only to record `alias_key_candidate`; alias matches do not repair, rewrite, or count as strict success.

4. **Bounded normalization and provenance.** Text normalization is deterministic NFKC/case/punctuation/spacing cleanup plus named allowlisted typed rules for URLs, email, phone, dates, times, amounts, booleans, and numeric strings. No LLM, embeddings, fuzzy semantic model, or broad paraphrase matching is used.

5. **Primary mechanism with secondary tags.** Each gold slot receives one primary mechanism and optional secondary tags. Extra prediction-only keys are reported as extra key events and included in paired movement and feasibility metrics without inventing gold values.

6. **Compact evidence surface.** The report directory contains only the bounded files requested by the change: `summary.md`, `summary.json`, `slot-error-taxonomy.md`, `slot-profile.json`, `paired-error-movement.json`, `representation-feasibility.json`, `recommended-next-change.md`, and `blocked.json` only when blocked.

7. **Design-only representation proposal.** `docs/slot-representation.md` can describe a future internal `SlotValueRepresentation` shape and migration implications, but this change must not implement or wire it into BrowserTaskContract V1, ContractCoreV2, training, or runtime.

## Risks / Trade-offs

- **Risk: deterministic source-support rules undercount values that humans would consider copied.** → Mitigation: label those cases `source_absent_or_generation_required` or `unsupported_analysis` and keep the decision confidence explicit.
- **Risk: alias policy could be mistaken for prediction repair.** → Mitigation: store alias evidence as candidate metadata only and state that strict metrics are unchanged.
- **Risk: public examples could leak raw private content.** → Mitigation: use existing schema privacy regexes, include only sample ids plus truncated sanitized summaries, and run leak scan.
- **Risk: one-seed Control/Treatment movement can be overinterpreted.** → Mitigation: report movement counts as explanation of existing A/B output only, not treatment success or model improvement.
- **Risk: representation recommendation can become an implementation claim.** → Mitigation: separate `docs/slot-representation.md` from runtime code and make the next change recommendation explicit but unexecuted.
