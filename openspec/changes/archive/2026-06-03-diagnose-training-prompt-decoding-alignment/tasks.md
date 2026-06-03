## 1. Source Diagnostics

- [x] 1.1 Add tests for public-safe source diagnostics that distinguish clean Browser Task Contract targets from path-like route/list-slot prediction symptoms.
- [x] 1.2 Implement source diagnostics and report writers for target shape, prompt constraints, split coverage, prediction symptoms, and decoding evidence gaps.
- [x] 1.3 Add a CLI entry point to generate the source diagnostic report for gold rows, prediction artifacts, training config, and prediction metadata.

## 2. Prompt and Decoding Metadata

- [x] 2.1 Add failing tests that require the SFT system prompt and prediction prompt to expose task type enums, route enums, route non-path semantics, and slots object constraints without leaking gold contracts.
- [x] 2.2 Strengthen the shared SFT prompt while preserving contract-only output and deterministic fallback behavior.
- [x] 2.3 Add tests and implementation for prediction metadata decoding policy fields, including greedy decoding, `max_new_tokens`, raw sidecar availability, and schema repair status.

## 3. Evidence and Closeout

- [x] 3.1 Generate the source diagnostic report for `reports/public-sample/a100-sft-post-recovery-rerun/`.
- [x] 3.2 Run focused tests, full tests, lint, type checks, leak scan, and `openspec validate --all --strict`.
- [x] 3.3 Generate a concise Chinese Human Brief HTML for this phase and a loop-level brief if this autonomous-loop segment stops.
- [x] 3.4 Sync the accepted delta specs into `openspec/specs/` and archive the change after validation passes.
