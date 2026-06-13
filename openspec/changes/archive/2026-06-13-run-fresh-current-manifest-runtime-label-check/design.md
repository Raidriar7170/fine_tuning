## Context

The latest runtime-label/tiny-overfit diagnostic ended with a specific gap: the committed current manifest is `public-sample-20260613T072200Z`, while the observed runtime-label and tiny-overfit artifacts were produced for `public-sample-20260601T162313Z`. The project already has a gated `sft-runtime-label-provenance-check` command and a public-safe runtime-label report writer, so this phase should reuse that surface rather than inventing a new training path.

## Goals / Non-Goals

**Goals:**
- Produce current-manifest runtime label provenance evidence for the public train split.
- Record whether the inspected tokenizer/collator labels are real training-path labels, whether prompt tokens are masked, and whether assistant target tokens carry loss.
- Keep all private runtime details out of committed artifacts.
- Use the stale prior runtime-label/tiny-overfit evidence only as context.
- Make the next decision mechanical: if fresh labels are inspectable and assistant-only, recommend a tiny-overfit probe; otherwise stop at the concrete label-path gap.

**Non-Goals:**
- No SFT/DPO/GRPO training.
- No prediction or held-out rerun.
- No private adapter load.
- No checkpoint or adapter release.
- No model recovery, production-readiness, private-corpus generalization, public full-corpus release, or live-browser benchmark claim.
- No evaluator relaxation, prediction repair, semantic equivalence scoring, or slot normalization.

## Decisions

1. **Reuse the existing runtime label provenance path.**
   - Choice: call `voice2task-train sft-runtime-label-provenance-check` and `voice2task-report runtime-label-provenance-check`.
   - Rationale: the existing path already gates private overrides, sanitizes metadata, and records runtime gate/output-root policy.
   - Alternative considered: add a new ad hoc diagnostic command. Rejected because it would duplicate the evidence boundary and make future audits harder.

2. **Use current manifest freshness as the phase success condition.**
   - Choice: the committed evidence must have `dataset_manifest_id=public-sample-20260613T072200Z`.
   - Rationale: the previous phase proved that old observed label evidence is stale for the current rows.
   - Alternative considered: reuse prior `runtime-label-provenance-check/` as enough evidence. Rejected because its manifest ID is older.

3. **Run remotely only when needed, and copy back sanitized summaries only.**
   - Choice: if local dependencies/model are unavailable, run under the approved private A100 project root with explicit GPU selection and copy only sanitized JSON/Markdown/leak-scan artifacts back to git.
   - Rationale: the real tokenizer/collator path may need model files not present locally, but private paths and raw logs must stay remote/private.
   - Alternative considered: download the 7B model locally. Rejected because it is unnecessary and expensive for this phase.

4. **Stop before tiny-overfit.**
   - Choice: this phase may recommend a 1-3 row tiny-overfit probe, but it must not run one.
   - Rationale: tiny-overfit changes the evidence question from label provenance to model learning behavior.

## Risks / Trade-offs

- [Risk] The remote tokenizer path is unavailable or dependency versions fail. -> Mitigation: record a blocked/unavailable runtime-label evidence pack with the exact public-safe gap, then stop rather than inventing success.
- [Risk] Fresh label inspection shows prompt tokens still carry loss. -> Mitigation: treat that as the actionable result and do not proceed to tiny-overfit.
- [Risk] Evidence accidentally includes private paths or host details. -> Mitigation: use existing sanitizers, run leak scans over reports/Human Brief/OpenSpec artifacts, and commit only public-safe files.
- [Risk] A100 occupancy changes between preflight and execution. -> Mitigation: re-run `nvidia-smi` immediately before launching any remote work and choose an idle GPU explicitly.
