# Tighten retry JSON-only output boundary

Status: local prompt-policy hardening only. This phase records no A100 execution, no training, no parser relaxation, no evaluator metric change, no prediction repair, no prediction re-score, and no model recovery or quality claim.

## Prior A100 context

The prior A100 generation stop-boundary rerun is linked from `reports/public-sample/a100-generation-stop-reason-boundary-rerun/`. Its strict final metrics remain `json_valid_rate=0.0` and `contract_exact_match=0.0` on the 3-row train-split rerun. This local phase does not prove any change in trained-adapter output behavior until a later real A100 rerun is performed.

## Local retry prompt hardening

The retry prompt constraint summary now exposes these machine-readable visibility booleans:

- `exact_json_only_output_visible`
- `no_text_outside_root_json_object_visible`
- `no_natural_language_wrapper_or_preamble_visible`
- `machine_readable_only_retry_response_visible`
- existing no-Markdown, no prefix/suffix, no trailing analysis, no second JSON object, and strict-parser rejection warnings

## Boundary

This pack observes prompt text and metadata propagation only. It does not extract embedded JSON fragments, repair historical predictions, normalize fields, re-score outputs, rerun A100, train a model, release an adapter/checkpoint, or claim model recovery.

Recommended next step: run a later prediction-only A100 rerun if the user wants evidence that the trained adapter actually follows the stricter retry JSON-only boundary.
