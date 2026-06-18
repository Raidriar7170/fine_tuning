# Design: Scaled Current-123 Adapter Residual Cluster Inspection

## Context

The latest scaled-manifest diagnosis evidence lives under
`reports/public-sample/scaled-current-123-adapter-residual-diagnosis/` and is
bound to `public-sample-20260617T152259Z`. It found `321` residual rows and
dominant residual fields `slots=304` and `normalized_command=194`.

The repository already has a reusable residual-cluster inspection pipeline:

- CLI: `voice2task-eval inspect-formal-heldout-residual-clusters`
- Python entrypoint: `inspect_formal_heldout_residual_clusters`
- report writer: `write_formal_heldout_residual_cluster_inspection_report`
- prior evidence: `reports/public-sample/formal-heldout-residual-cluster-inspection/`

This change should reuse that format for the scaled evidence instead of
creating a parallel report shape.

## Goals / Non-Goals

**Goals:**

- Generate a new public-safe cluster inspection from the scaled residual
  diagnosis JSON.
- Preserve source boundary metadata, especially `public-sample-20260617T152259Z`
  and the scaled A100 recovery prediction evidence pointer.
- Identify the top clusters and repeated mismatch patterns that should guide a
  later data-design or training-readiness decision.
- Keep strict `contract_exact_match` and strict `slot_f1` authoritative.
- Update status docs, Human Brief, focused tests, and OpenSpec archive.

**Non-Goals:**

- No A100 job, training, prediction rerun, data materialization, DPO/GRPO run,
  prompt change, evaluator relaxation, semantic-equivalence scoring, slot
  normalization, prediction repair, checkpoint release, adapter release, public
  full-corpus release, generic chat fine-tuning, skill routing, GUI action
  policy learning, production-readiness claim, or live-browser benchmark claim.

## Decisions

1. **Reuse the existing cluster inspector.**
   The existing inspector already groups formal held-out residual diagnosis
   fields into actionable clusters by task family, source family, field path,
   category, and short pattern. Reusing it keeps this phase comparable with
   older cluster evidence.

2. **Use a new output directory.**
   The scaled cluster evidence will be written under
   `reports/public-sample/scaled-current-123-adapter-residual-cluster-inspection/`
   so it cannot be confused with prior-manifest cluster evidence.

3. **Treat any report manifest path hardcoding as in-scope.**
   If `write_formal_heldout_residual_cluster_inspection_report` still hardcodes
   the old `formal-heldout-residual-cluster-inspection` path, this phase may
   update it to use output-relative public artifact paths. This is not an
   evaluator or metric change; it keeps manifests accurate for reused writers.

4. **Do not pick remediation yet.**
   This phase may recommend a next bounded decision based on top clusters, but
   it must not materialize seed rows, select a training run, or modify evaluator
   semantics.

## Risks / Trade-offs

- Cluster grouping can be descriptive rather than causal -> mitigate by keeping
  cluster evidence separate from remediation decisions.
- The top cluster may be too broad to materialize directly -> mitigate by
  recommending a later design phase when necessary.
- Public report artifacts may accidentally inherit old output paths -> mitigate
  with focused tests and leak scans over the new output directory.
