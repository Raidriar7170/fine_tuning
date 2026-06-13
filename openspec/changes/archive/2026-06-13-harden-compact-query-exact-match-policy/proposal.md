## Why

The latest residual diagnosis shows that strict schema validity is recovered for the three public train rows, but full-contract exact match still fails on two strict `normalized_command` string differences and one compact-query slot-shape mismatch. A narrow local hardening phase is needed before another A100 rerun so the model-visible policy explicitly ties `normalized_command` and `slots.query` to the same compact query phrase while preserving strict evaluator semantics.

## What Changes

- Harden the shared SFT training and trained-adapter prediction prompt policy for public-readonly search/weather contracts.
- Add non-row-specific guidance that `normalized_command` should be `搜索` plus the same compact query phrase used in `slots.query`, without inserting extra particles such as `的`.
- Add non-row-specific positive and rejected examples that contrast compact `slots.query` with decomposed `city/date/topic` slots.
- Keep public sample seed-derived SFT/DPO artifacts synchronized when public-safe seeds are expanded.
- Add a `wrong_task_type` hard-negative family and validation that verifies the rejected contract actually changes `task_type`.
- Add `slot_f1_soft` only as an internal diagnostic metric alongside strict `slot_f1` and `contract_exact_match`; it must not replace or relax strict metrics.
- Repair local trained-adapter prediction loading so merged PEFT adapters are used when available without breaking local fake-model tests.
- Keep DPO training compatible with the current TRL `DPOConfig` API and optional SFT-adapter initialization.
- Publish a local public-safe evidence pack proving the prompt/data policy visibility, source residual links, validation results, and non-claim boundaries.
- Generate a concise Chinese Human Brief for this phase.
- Do not run A100, train, rerun predictions, relax parser or strict evaluator metrics, normalize slots or `normalized_command`, apply semantic-equivalence scoring, repair predictions, replace predictions, or re-score outputs.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `supervised-contract-tuning`: Adds explicit compact-query exact-match prompt policy for `normalized_command` and `slots.query` alignment.
- `voice2task-dataset-preparation`: Keeps expanded public seed fixtures and derived SFT/DPO artifacts synchronized.
- `preference-contract-tuning`: Adds `wrong_task_type` hard-negative coverage and validation.
- `contract-evaluation`: Adds public-safe local evidence and an internal-only soft slot diagnostic without reinterpreting prior predictions or strict metrics.

## Impact

- Affected code: prompt policy constants and prompt constraint metadata in `src/voice2task/formatting.py`, public dataset/DPO helpers, internal evaluation diagnostics, and local training/prediction compatibility paths.
- Affected scripts: seed generation, generated-seed validation, and slot-value normalization helpers.
- Affected tests: focused prompt-policy, DPO validation, public dataset, prediction-loading, and evidence-boundary tests.
- Affected reports: public-safe experiment summary and, when the phase is completed, a new public-safe local evidence directory under `reports/public-sample/` plus a phase Human Brief under `docs/human-briefs/`.
- New optional dependency: `anthropic` under the dataset extra for seed-generation helper scripts.
- No public API, A100 execution, checkpoint/adapter release, parser relaxation, strict evaluator replacement, private data exposure, or production-readiness claim.
