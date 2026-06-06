## 1. Baseline And TDD

- [x] 1.1 Re-read the prior A100 stop-boundary evidence and current retry prompt implementation to confirm the failure target is retry wrapper/prose output, not parser or evaluator looseness.
- [x] 1.2 Add focused RED tests for stricter retry JSON-only boundary clauses and prompt constraint visibility.

## 2. Prompt Boundary Implementation

- [x] 2.1 Strengthen `_schema_retry_prompt` with concise exact-output clauses that forbid Markdown, code fences, natural-language prefaces, suffixes, trailing analysis, and second JSON objects.
- [x] 2.2 Extend `schema_retry_prompt_constraint_summary` so metadata/prompt snapshots expose the new retry boundary visibility booleans.
- [x] 2.3 Verify existing strict retry parsing still rejects wrapped JSON fragments without extracting or repairing embedded contracts.

## 3. Local Evidence Pack

- [x] 3.1 Generate a public-safe local evidence pack under `reports/public-sample/tighten-retry-json-only-output-boundary/` with manifest, summary, policy visibility, validation commands, prior A100 context, and non-claims.
- [x] 3.2 Run leak scans over the evidence pack, OpenSpec change, and Human Brief inputs.

## 4. Human Brief And Review

- [x] 4.1 Generate `docs/human-briefs/2026-06-06-tighten-retry-json-only-output-boundary.html` with current status, evidence links, validation, risks, and recommended next A100 rerun decision.
- [x] 4.2 Complete Reviewer pass and fix Must Fix items only.

## 5. Validation And Archive

- [x] 5.1 Run focused tests, full test suite, lint/type checks, public data validation, DPO pair checks, public-leak scans, `git diff --check`, and `openspec validate --all --strict`.
- [x] 5.2 Archive the OpenSpec change, generate post-archive and final leak-scan sidecars, rerun post-archive validation, and commit the phase under guarded auto integration.
