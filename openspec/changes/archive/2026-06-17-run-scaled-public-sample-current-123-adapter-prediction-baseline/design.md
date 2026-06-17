## Context

The active public sample manifest is `public-sample-20260617T152259Z` with 240 seed rows, 675 SFT rows, 2046 DPO pairs, and SFT split counts of train 261, dev 207, and test 207. The source adapter for this phase is the private current-123 train split SFT retry runtime `a100-current-train-split-sft-retry`, trained for `public-sample-20260617T045941Z`.

This phase is intentionally prediction-only. It asks how the prior current-123 adapter behaves on the expanded scaled manifest boundary. Any future metric must be labeled as a cross-boundary prediction baseline, not as evidence that the scaled public-sample rows were trained into the adapter.

## Goals / Non-Goals

**Goals:**

- Provide public-safe dev/test config templates for prediction-only export on the scaled target manifest.
- Preserve both boundaries in configs and evidence: target `public-sample-20260617T152259Z`, source adapter `public-sample-20260617T045941Z`.
- Verify local config shape and fixture-mode row selection for 207 dev rows and 207 test rows.
- Keep future committed artifacts sanitized and limited to predictions, sidecars, metrics, manifests, reports, and leak-scan evidence.

**Non-Goals:**

- No A100 execution in the scaffolding pass.
- No SFT, DPO, GRPO, prompt update, dataset mutation, evaluator relaxation, slot normalization, prediction repair, prediction replacement, or prediction re-score.
- No public checkpoint, adapter, raw log, private override, private path, GPU detail, SSH detail, token, cache, private corpus row, or full local corpus publication.
- No production-readiness, held-out recovery, released-model, private-corpus generalization, or live-browser benchmark claim.

## Decisions

1. **Use new config names and evidence directories.** The scaled-target baseline gets distinct config files and a distinct future evidence directory so it cannot be confused with the old `a100-current-train-split-sft-retry-heldout` configs bound to `public-sample-20260617T045941Z`.

2. **Keep `dataset_manifest_id` and `target_dataset_manifest_id` on the scaled target.** Both fields point to `public-sample-20260617T152259Z`, because prediction row selection and evidence interpretation are target-manifest concerns.

3. **Keep source adapter provenance on the old current-123 boundary.** `source_adapter_runtime`, `source_adapter_dataset_manifest_id`, and `requires_paired_training_manifest_id` identify `a100-current-train-split-sft-retry` and `public-sample-20260617T045941Z` so future reports do not imply paired scaled training.

4. **Fail closed if remote execution is unsafe.** Later A100 work must record blocked evidence instead of fabricating predictions or metrics when private adapter, private override, remote dependency, or GPU placement checks fail.

5. **Treat this run as blocked, not observed.** The read-only A100 connectivity preflight timed out before GPU, dependency, private override, or adapter checks could complete. The committed evidence records `prediction_run=false` and `metrics_generated=false`; it must not be interpreted as model quality on the scaled target boundary.

## Risks / Trade-offs

- Cross-boundary evaluation may perform worse on new scaled dev/test rows; report strict metrics directly and do not convert them into model-recovery claims.
- The source adapter was not trained on the scaled target manifest; future reports must make this visible before any comparison.
- A100 resources may be unavailable; blocked evidence is preferable to unsafe execution.
- Private runtime leakage risk remains; committed artifacts need leak scans and placeholder-only public configs.
