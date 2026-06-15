## Overview

This change mirrors the existing slot-value candidate materialization pattern for the reviewed `form_fill` remediation case design:

1. Read `reports/public-sample/form-fill-remediation-case-design/form_fill_remediation_case_design.json`.
2. Fail closed unless it is the expected `form_fill_remediation_case_design` evidence with `design_status=design_only_not_materialized`.
3. Require exactly the three reviewed groups:
   - `form-fill-clarify-boundary-protection`
   - `form-fill-confirmation-marker-preservation`
   - `form-fill-field-specificity-preservation`
4. Write standalone candidate seed rows to `data/public-samples/form_fill_remediation_seed_candidates.jsonl`.
5. Write candidate SFT rows and materialization evidence to `reports/public-sample/form-fill-remediation-materialized-candidates/`.

## Data Boundary

The candidate rows are standalone review/probe input, not formal public sample rows. The materializer MUST NOT append to `data/public-samples/seed_traces.jsonl`, rebuild public SFT/DPO artifacts, or update `manifest_public_sample.json`.

All candidate rows use:

- `split="train"`
- `source_mode="form_fill_remediation_candidate_seed"`
- `candidate_status="standalone_not_formal_public_sample"`
- `public_safe=true`
- provenance linking back to the case group, case ID, source bucket, and source design artifact

The candidate SFT rows use the existing `SFTDatasetRow` schema. This phase does not generate augmentations or DPO pairs.

## Canonical Contract Policy

The source case design includes `expected_normalized_command_pattern` values that sometimes focus only on field specificity, such as `填写收货地址`. Current public sample policy requires confirmation-required form-fill targets to use concise fill-and-confirm phrasing. Therefore materialization canonicalizes all `form_fill` remediation contracts to:

- `task_type="form_fill"`
- `route="fill_form"`
- `safety.allow=true`
- `safety.reason="requires_confirmation"`
- `confirmation_required=true`
- `slots={"field": ...}`
- `normalized_command="填写<field>并确认"`

The materialization report preserves the original expected pattern in provenance/report metadata so the design intent remains auditable.

## Claim Boundary

Reports and Human Briefs must state that this phase is candidate data only. It does not prove held-out recovery, model recovery, strict metric improvement, soft-metric promotion, checkpoint release, adapter release, production readiness, private corpus generalization, or live-browser benchmark improvement.

## Next Phase

After materialization, the likely next bounded change is a dry, local candidate integration check or a separate formal merge/probe proposal. Any training or A100 run must remain a later explicit OpenSpec phase.
