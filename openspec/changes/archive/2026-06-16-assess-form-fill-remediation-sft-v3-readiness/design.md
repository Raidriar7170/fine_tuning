## Boundary

This phase is readiness-only. It prepares a later SFT v3 decision but does not
perform training, prediction, data mutation, or metric changes.

## Inputs

- Current formal public manifest:
  `data/public-samples/manifest_public_sample.json`
- Current A100 prediction-only baseline:
  `reports/public-sample/a100-formal-public-heldout-prediction-after-a100-recovery/`
- Current `form_fill` residual target:
  `reports/public-sample/formal-heldout-remediation-target-selection/`
- Current `form_fill` remediation plan/design/merge evidence:
  `reports/public-sample/form-fill-remediation-plan/`,
  `reports/public-sample/form-fill-remediation-case-design/`,
  `reports/public-sample/form-fill-remediation-public-sample-merge/`, and
  `reports/public-sample/form-fill-confirmation-marker-extension-public-sample-merge/`.

## Approach

1. Add public-safe config templates that keep all private A100 paths as
   `<a100_project_root>` placeholders.
2. Run local SFT dry-run row selection only, using the current formal public
   manifest and the later-run config.
3. Write a readiness report that records:
   - current strict formal held-out metrics;
   - current selected `form_fill` residual counts;
   - merged `form_fill` train-row counts from the manifest source summary;
   - dry-run row count and source-id coverage;
   - training/prediction not-run boundaries;
   - the recommended next bounded OpenSpec change.
4. Add a Human Brief and validation evidence.

## Interpretation

Readiness evidence can justify opening a later SFT v3 execution phase, but it
must not be described as model improvement. The later execution phase must still
perform A100 GPU preflight, use a private override outside git, run training
under the approved A100 project root, and publish only sanitized public evidence.
