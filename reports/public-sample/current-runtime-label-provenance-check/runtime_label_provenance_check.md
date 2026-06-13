# Voice2Task observed runtime label provenance evidence

Runtime label provenance evidence is objective-path evidence only. It reports whether tokenizer/collator labels were inspectable without publishing private runtime paths, raw logs, checkpoints, adapters, or private corpus rows.

## Boundary

- This is not a checkpoint release.
- This is not an adapter release.
- This is not held-out generalization evidence.
- This makes no production-readiness claim.
- This is not a live-browser benchmark or benchmark-improvement claim.
- This is not model recovery evidence.

## Summary

- Evidence status: `labels_inspected`
- Runtime source kind: `private_a100_runtime`
- Runtime gate: `{'cli_requested_runtime_check': True, 'config_allow_runtime_label_provenance_check': True, 'private_override_resolved': True, 'will_run_runtime_label_provenance_check': True}`
- Output-root policy: `{'approved_policy': 'must_resolve_to_approved_private_a100_project_root', 'public_template_output_root': '<a100_project_root>', 'requested_output': '<private_path>', 'runtime_check_output_dir': '<private_path>', 'status': 'approved_private_root'}`
- Dataset manifest: `public-sample-20260613T072200Z`
- Expected manifest: `public-sample-20260613T072200Z`
- Manifest freshness: `fresh_current_manifest`
- Current-manifest runtime label proof: `True`
- Label source: `actual_training_labels`
- Label source kind: `private_training_runtime`
- Package versions: `{'accelerate': '1.13.0', 'datasets': 'not_installed', 'peft': '0.18.1', 'python': '3.11.4', 'transformers': '5.5.0', 'trl': 'not_installed'}`
- Dependency policy: `{'model_download_allowed': False, 'policy': 'authorized_runtime_tokenizer_collator_check_no_adapter_load_no_training', 'private_adapter_load_allowed': False, 'raw_private_logs_copied_to_git': False}`
- Leak scan ok: `True`
- Label tensor available: `True`
- True label-mask status: `inspectable`
- Prompt tokens masked: `True`
- Assistant tokens carry loss: `True`
- Assistant-only loss-mask claim: `True`
- Recommended next step: `run_1_to_3_row_current_manifest_tiny_overfit_probe`

## Evidence Gaps

- none

## Prior Artifacts

- Stale prior artifacts are historical context only.
- `runtime_label_tiny_overfit_diagnostic`: `reports/public-sample/runtime-label-tiny-overfit-diagnostic/`
- `stale_runtime_label_provenance_check`: `reports/public-sample/runtime-label-provenance-check/`

## Objective Limitations

- If `prompt_tokens_masked=false`, this evidence does not support an assistant-only loss-mask claim.
- `assistant_tokens_carry_loss=true` means assistant target tokens participate in loss, not that the model has learned the contract task.

## Interpretation

- Inspectable real labels can support SFT objective-path interpretation only.
- Fixture or simulated labels remain fixture-only and keep evidence gaps.
- Runtime label evidence does not establish held-out quality, release readiness, or live-browser gains.
