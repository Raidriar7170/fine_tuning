## Context

The previous `prepare-runtime-label-provenance-check` phase added a public-safe config template, prep metadata, and evidence pack, but it intentionally reported `runtime_check_status=blocked_unresolved_private_override` and `true_label_mask_status=unavailable`. The repository also has local SFT label provenance inspection that can describe unavailable, fixture, or simulated label sources, and an A100 train-split diagnostic whose interpretation remains blocked by the absence of real tokenizer/collator label-mask evidence.

This phase is the authorized private/A100 execution step. It may use private overrides and remote runtime files, but committed artifacts must contain only sanitized summaries, public sample row identifiers, aggregate statuses, public-safe placeholders, and claim boundaries. The remote write boundary is the approved private A100 project root, represented in committed artifacts as `<approved_a100_project_root>`, with raw logs, caches, checkpoints, adapters, model snapshots, private overrides, host details, and private paths kept out of git.

## Goals / Non-Goals

**Goals:**

- Execute a real tokenizer/collator SFT label provenance check in the authorized A100 environment using an idle GPU and repo-external private override.
- Reuse the same formatting/collator path used for real SFT examples where feasible, so the inspected labels are not merely fixture evidence.
- Produce a sanitized metadata/evidence pack that records runtime execution status, real label tensor availability, label source, tokenizer/template status, collator status, prompt mask status, assistant-target loss status, evidence gaps, package/runtime policy, and non-claim boundaries.
- Add local tests for the public-safe evidence writer and fail-closed sanitization so reviewers can validate the committed evidence without A100 access.
- Archive the OpenSpec change after local validation, leak scan, and reviewer fixes pass.

**Non-Goals:**

- No generic chat fine-tuning, skill routing, GUI action policy learning, first-phase GRPO, public release of the full local corpus, checkpoint release, adapter release, held-out generalization claim, production-readiness claim, live-browser benchmark claim, publishing raw remote logs, committing private overrides, or documenting SSH/host/IP details.

## Decisions

1. Add an executed-runtime evidence shape instead of mutating the prep evidence contract.
   - Rationale: prep and observed runtime proof answer different questions. Keeping separate `runtime_check_status` values avoids turning readiness into evidence by accident.
   - Alternative considered: overwrite `runtime-label-provenance-prep` artifacts. Rejected because it would erase the audit trail and make fixture/prep/real evidence harder to distinguish.

2. Sanitize at the report boundary and leak-scan every committed evidence path.
   - Rationale: the A100 run may necessarily see private paths and raw runtime details, but git-backed artifacts must not.
   - Alternative considered: copy a compact remote log and redact it. Rejected because structured evidence is smaller, deterministic, and easier to validate.

3. Treat a successful runtime label inspection as objective-path evidence only.
   - Rationale: real label masks can show whether the training objective includes the assistant target and masks prompts, but they do not prove model quality or generalization.
   - Alternative considered: use runtime label evidence to reinterpret previous A100 prediction failures as training success/failure. Rejected because prediction quality still requires separate model-output evidence.

4. Make A100 execution recoverable but not mandatory for local tests.
   - Rationale: local CI and reviewers should validate the evidence contract without private infrastructure; the real run remains recorded through sanitized outputs.
   - Alternative considered: require A100 for all validation. Rejected because it would make ordinary review impossible and expand private-infra dependence.

## Risks / Trade-offs

- [Risk] Remote runtime details leak into committed evidence -> Mitigation: use structured sanitized summaries, placeholders for private paths, and run leak-scan over evidence, Human Brief, and OpenSpec artifacts.
- [Risk] The inspected path differs from real SFT training -> Mitigation: record label source kind, tokenizer/template status, collator status, and evidence gaps; do not overclaim if the path is partial.
- [Risk] A100 access or dependencies are unavailable -> Mitigation: stop with a blocked loop report if the real run cannot execute without exposing private details or changing scope.
- [Risk] Runtime labels are still unavailable or ambiguous -> Mitigation: publish the observed unavailable/ambiguous state honestly and keep model-quality claims blocked.
- [Risk] The phase grows into retraining or prediction repair -> Mitigation: limit this change to label provenance inspection and public-safe evidence packaging.
