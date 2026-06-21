# Internal Contract Core V2

This document describes the internal ContractCoreV2 boundary added for Voice2Task. It is an implementation note, not a public schema migration.

## Relationship To External V1

BrowserTaskContract V1 remains the authoritative external schema. Current training targets, gold contracts, predictions, evaluator metrics, downstream runtime inputs, and controlled smoke fixtures remain V1-compatible.

ContractCoreV2 is internal only:

```text
BrowserTaskContract V1
  -> parse / validate
ContractCoreV2
  -> validate / consume
V1-compatible deterministic envelope
  -> BrowserTaskContract V1
```

## Core Fields

ContractCoreV2 contains exactly:

- `task_type`
- `route`
- `safety`
- `confirmation_required`
- `slots`

It deliberately excludes `normalized_command`, `language`, and `contract_version`. It also excludes fields not present in V1, including `allowed_actions`, `success_criteria`, `policy_tags`, and `runtime_hints`.

## Envelope Metadata

The internal envelope metadata contains:

- `language`
- `contract_version`
- `normalized_command`
- `normalized_command_provenance`

`normalized_command_provenance` is internal-only and is not serialized into V1 JSON.

## Build Modes

`preserve_legacy` is the default compatibility mode. It keeps V1 `normalized_command`, `language`, and `contract_version` metadata and rebuilds canonical V1 JSON exactly.

`derive_display` is an experimental deterministic display-field mode. It uses the existing deterministic normalized-command renderer and emits V1-compatible `language="zh-CN"` and `contract_version="v1"`. Unsupported renderer shapes fail closed and do not fall back to free generation or legacy command text.

## Compatibility Evidence

Current evidence is under `reports/public-sample/internal-contract-v2-core/`.

- Decision: `INTERNAL_V2_CORE_READY_RENDERER_PARTIAL`
- Contracts checked: 2185
- Preserve roundtrip exact rate: 1.0
- Safety preservation rate: 1.0
- Confirmation preservation rate: 1.0
- Slots preservation rate: 1.0
- V1 evaluator metric deltas: all 0
- Derive-display renderer support: 99.77%, with 5 unsupported cases

## Claim Boundary

This implementation does not prove model improvement, executable quality improvement, slot-error resolution, safety readiness, production readiness, a public V2 schema, a V2 training target, or downstream runtime migration. The next technical question is `analyze-slot-error-mechanisms-and-design-slot-representation`.
