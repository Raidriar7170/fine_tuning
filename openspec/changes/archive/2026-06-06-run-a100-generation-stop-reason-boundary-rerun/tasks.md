## 1. A100 Preflight

- [x] 1.1 Identify the prior private-adapter prediction command and public-safe artifact template from committed A100 rerun evidence.
- [x] 1.2 Check A100 access, GPU/process occupancy, approved output root, and private override availability before launching any GPU work.

## 2. Prediction-Only Rerun

- [x] 2.1 Run a train-split private-adapter prediction-only export with schema retry enabled and no decoding/parser/metric behavior changes.
- [x] 2.2 Collect sanitized predictions, metrics, prompt snapshot, raw decoded summary, generation trace, prediction metadata, and leak-scan sidecars into a public-safe evidence directory.

## 3. Stop-Boundary Diagnosis

- [x] 3.1 Generate schema guard and stop-boundary diagnosis artifacts summarizing raw/retry trace coverage, new trace fields, strict final metrics, retry wrapper status, and unproven claims.
- [x] 3.2 Publish a manifest and report that compare only to the bounded prior retry-trace rerun and local stop-boundary instrumentation evidence.

## 4. Human Brief And Tests

- [x] 4.1 Add or update tests that assert the A100 stop-boundary rerun evidence pack is public-safe, bounded, and includes the new trace fields.
- [x] 4.2 Generate a concise Chinese Human Brief with project-stage progress, verification results, evidence links, non-claims, and recommended next step.

## 5. Validation And Closeout

- [x] 5.1 Run focused tests, full test suite, lint/type checks, public data validation, DPO pair checks, public-leak scans, `git diff --check`, and `openspec validate --all --strict`.
- [x] 5.2 Complete Reviewer pass, fix Must Fix items only, archive the OpenSpec change, rerun validation, and commit the phase under guarded auto integration.
