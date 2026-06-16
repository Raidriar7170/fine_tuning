# Voice2Task form-fill confirmation-marker extension materialized candidates

This is candidate data only: it materializes reviewed form-fill confirmation-marker extension cases into standalone public-safe candidate seed and SFT rows. The standalone candidate artifacts written by this materialization report remain candidate-only; the current formal sample state is recorded separately by the merge evidence.

## Boundary

- Current formal public sample already includes the reviewed confirmation-marker extension candidates; use the merge report as the authoritative current-state evidence.
- This materialization command does not rewrite formal public sample seed, SFT, DPO, or manifest files.
- No DPO pairs, SFT training, prediction run, A100 execution, or evaluator relaxation is performed.
- Strict `contract_exact_match` and strict `slot_f1` remain authoritative.
- `slot_f1_soft` is diagnostic-only and not a primary metric.
- Family-level candidate labels are public-safe placeholders, not recovered gold text.
- This is not a model recovery, held-out recovery, checkpoint, adapter, production, private-corpus, public-full-corpus, or live-browser improvement claim.

## Summary

- Candidate cases: `12`
- Candidate seed rows: `12`
- Candidate SFT rows: `12`
- Derived field-label rows: `3`
- Family-level candidate-label rows: `9`
- Formal public sample seed rows: `98`
- Formal public sample SFT rows: `252`
- Formal public sample DPO pairs: `850`
- Formal public sample modified: `False`
- Seed traces modified: `False`
- Recommended next step: `use_formal_merge_report_as_current_public_sample_state`

## Candidate Cases

### `ff-confirm-marker-extension-family-confirmation-dev-1`

- Source family: `family-confirmation-dev-1`
- Source bucket: `missing_confirmation_marker`
- Candidate seed: `candidate-form-fill-confirmation-marker-extension-ff-confirm-marker-extension-family-confirmation-dev-1`
- Candidate SFT row: `candidate-form-fill-confirmation-marker-extension-ff-confirm-marker-extension-family-confirmation-dev-1`
- Field-label derivation: `not_derivable_from_committed_coverage_policy_artifacts`
- Field-label provenance: `public_safe_family_level_candidate_label_not_recovered_gold_text`
- Expected marker: `并确认`

### `ff-confirm-marker-extension-family-confirmation-dev-2`

- Source family: `family-confirmation-dev-2`
- Source bucket: `missing_confirmation_marker`
- Candidate seed: `candidate-form-fill-confirmation-marker-extension-ff-confirm-marker-extension-family-confirmation-dev-2`
- Candidate SFT row: `candidate-form-fill-confirmation-marker-extension-ff-confirm-marker-extension-family-confirmation-dev-2`
- Field-label derivation: `not_derivable_from_committed_coverage_policy_artifacts`
- Field-label provenance: `public_safe_family_level_candidate_label_not_recovered_gold_text`
- Expected marker: `并确认`

### `ff-confirm-marker-extension-family-confirmation-dev-3`

- Source family: `family-confirmation-dev-3`
- Source bucket: `missing_confirmation_marker`
- Candidate seed: `candidate-form-fill-confirmation-marker-extension-ff-confirm-marker-extension-family-confirmation-dev-3`
- Candidate SFT row: `candidate-form-fill-confirmation-marker-extension-ff-confirm-marker-extension-family-confirmation-dev-3`
- Field-label derivation: `not_derivable_from_committed_coverage_policy_artifacts`
- Field-label provenance: `public_safe_family_level_candidate_label_not_recovered_gold_text`
- Expected marker: `并确认`

### `ff-confirm-marker-extension-family-confirmation-test-1`

- Source family: `family-confirmation-test-1`
- Source bucket: `missing_confirmation_marker`
- Candidate seed: `candidate-form-fill-confirmation-marker-extension-ff-confirm-marker-extension-family-confirmation-test-1`
- Candidate SFT row: `candidate-form-fill-confirmation-marker-extension-ff-confirm-marker-extension-family-confirmation-test-1`
- Field-label derivation: `not_derivable_from_committed_coverage_policy_artifacts`
- Field-label provenance: `public_safe_family_level_candidate_label_not_recovered_gold_text`
- Expected marker: `并确认`

### `ff-confirm-marker-extension-family-confirmation-test-2`

- Source family: `family-confirmation-test-2`
- Source bucket: `missing_confirmation_marker`
- Candidate seed: `candidate-form-fill-confirmation-marker-extension-ff-confirm-marker-extension-family-confirmation-test-2`
- Candidate SFT row: `candidate-form-fill-confirmation-marker-extension-ff-confirm-marker-extension-family-confirmation-test-2`
- Field-label derivation: `not_derivable_from_committed_coverage_policy_artifacts`
- Field-label provenance: `public_safe_family_level_candidate_label_not_recovered_gold_text`
- Expected marker: `并确认`

### `ff-confirm-marker-extension-family-confirmation-test-3`

- Source family: `family-confirmation-test-3`
- Source bucket: `missing_confirmation_marker`
- Candidate seed: `candidate-form-fill-confirmation-marker-extension-ff-confirm-marker-extension-family-confirmation-test-3`
- Candidate SFT row: `candidate-form-fill-confirmation-marker-extension-ff-confirm-marker-extension-family-confirmation-test-3`
- Field-label derivation: `not_derivable_from_committed_coverage_policy_artifacts`
- Field-label provenance: `public_safe_family_level_candidate_label_not_recovered_gold_text`
- Expected marker: `并确认`

### `ff-confirm-marker-extension-family-form_fill-dev-1`

- Source family: `family-form_fill-dev-1`
- Source bucket: `missing_confirmation_marker`
- Candidate seed: `candidate-form-fill-confirmation-marker-extension-ff-confirm-marker-extension-family-form_fill-dev-1`
- Candidate SFT row: `candidate-form-fill-confirmation-marker-extension-ff-confirm-marker-extension-family-form_fill-dev-1`
- Field-label derivation: `derived_from_committed_coverage_examples`
- Field-label provenance: `derived_from_committed_public_artifacts`
- Expected marker: `并确认`

### `ff-confirm-marker-extension-family-form_fill-dev-2`

- Source family: `family-form_fill-dev-2`
- Source bucket: `missing_confirmation_marker`
- Candidate seed: `candidate-form-fill-confirmation-marker-extension-ff-confirm-marker-extension-family-form_fill-dev-2`
- Candidate SFT row: `candidate-form-fill-confirmation-marker-extension-ff-confirm-marker-extension-family-form_fill-dev-2`
- Field-label derivation: `derived_from_committed_coverage_examples`
- Field-label provenance: `derived_from_committed_public_artifacts`
- Expected marker: `并确认`

### `ff-confirm-marker-extension-family-form_fill-dev-3`

- Source family: `family-form_fill-dev-3`
- Source bucket: `missing_confirmation_marker`
- Candidate seed: `candidate-form-fill-confirmation-marker-extension-ff-confirm-marker-extension-family-form_fill-dev-3`
- Candidate SFT row: `candidate-form-fill-confirmation-marker-extension-ff-confirm-marker-extension-family-form_fill-dev-3`
- Field-label derivation: `derived_from_committed_coverage_examples`
- Field-label provenance: `derived_from_committed_public_artifacts`
- Expected marker: `并确认`

### `ff-confirm-marker-extension-family-form_fill-test-1`

- Source family: `family-form_fill-test-1`
- Source bucket: `missing_confirmation_marker`
- Candidate seed: `candidate-form-fill-confirmation-marker-extension-ff-confirm-marker-extension-family-form_fill-test-1`
- Candidate SFT row: `candidate-form-fill-confirmation-marker-extension-ff-confirm-marker-extension-family-form_fill-test-1`
- Field-label derivation: `not_derivable_from_committed_coverage_policy_artifacts`
- Field-label provenance: `public_safe_family_level_candidate_label_not_recovered_gold_text`
- Expected marker: `并确认`

### `ff-confirm-marker-extension-family-form_fill-test-2`

- Source family: `family-form_fill-test-2`
- Source bucket: `missing_confirmation_marker`
- Candidate seed: `candidate-form-fill-confirmation-marker-extension-ff-confirm-marker-extension-family-form_fill-test-2`
- Candidate SFT row: `candidate-form-fill-confirmation-marker-extension-ff-confirm-marker-extension-family-form_fill-test-2`
- Field-label derivation: `not_derivable_from_committed_coverage_policy_artifacts`
- Field-label provenance: `public_safe_family_level_candidate_label_not_recovered_gold_text`
- Expected marker: `并确认`

### `ff-confirm-marker-extension-family-form_fill-test-3`

- Source family: `family-form_fill-test-3`
- Source bucket: `missing_confirmation_marker`
- Candidate seed: `candidate-form-fill-confirmation-marker-extension-ff-confirm-marker-extension-family-form_fill-test-3`
- Candidate SFT row: `candidate-form-fill-confirmation-marker-extension-ff-confirm-marker-extension-family-form_fill-test-3`
- Field-label derivation: `not_derivable_from_committed_coverage_policy_artifacts`
- Field-label provenance: `public_safe_family_level_candidate_label_not_recovered_gold_text`
- Expected marker: `并确认`

## Recommended Next Step

Use the formal public-sample merge report as the authoritative current-state evidence. This materialization report remains standalone candidate-generation evidence, not training, prediction, or held-out recovery evidence.
