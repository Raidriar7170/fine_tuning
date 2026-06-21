## Why

The latest recovered-input Contract V2 projection shows limited schema-burden value, especially around derived display fields, but no model-quality or executable-quality improvement. This change implements the smallest internal boundary needed to separate core contract fields from deterministic V1-compatible envelope fields while keeping BrowserTaskContract V1 authoritative externally.

## What Changes

- Add an internal ContractCoreV2 DTO containing only `task_type`, `route`, `safety`, `confirmation_required`, and `slots`.
- Add internal envelope metadata for `language`, `contract_version`, `normalized_command`, and internal-only `normalized_command_provenance`.
- Add pure V1 projection, V1 metadata extraction, V1-compatible envelope building, canonical core serialization, roundtrip comparison, and shadow compatibility checks.
- Add a minimal shadow compatibility report path over current committed public-safe V1 contracts and recovered step-matched prediction contracts.
- Add concise documentation and evidence artifacts for the internal boundary.
- Preserve all external BrowserTaskContract V1 interfaces, training data, evaluator semantics, gold contracts, predictions, prompts, decoding, splits, and downstream runtime behavior.
- Do not train, rerun predictions, repair predictions, relax strict exact, publish adapters/checkpoints, or claim model/executable-quality improvement.

## Capabilities

### New Capabilities
- `internal-contract-core-v2`: Internal ContractCoreV2 projection, V1-compatible deterministic envelope construction, and shadow compatibility diagnostics.

### Modified Capabilities
- None.

## Impact

- Affected code: new internal core/envelope module, a small compatibility report/CLI entry point, focused tests, and concise docs.
- Affected artifacts: `reports/public-sample/internal-contract-v2-core/`, `docs/contract-core-v2.md`, current snapshot docs, and a Human Brief.
- No new runtime dependency.
- No breaking external API or schema change; V1 remains the default and authoritative external contract.
