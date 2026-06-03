## 1. Remote Diagnostic Setup

- [x] 1.1 Confirm the current local git/OpenSpec state and preserve existing task-related untracked Human Briefs.
- [x] 1.2 Identify a safe remote access path using an existing SSH alias or documented local workflow without recording host/IP/private path details in committed artifacts.
- [x] 1.3 Confirm an idle A100 GPU and prepare a repo-external private override under the approved private project root.
- [x] 1.4 Run objective inspection and keep unavailable/mask/loss status honest without claiming assistant-only loss unless labels prove it.

## 2. Real A100 Train-Split Diagnostic

- [x] 2.1 Run the real private-adapter train-split diagnostic prediction with explicit prediction opt-in and `prediction_split=train`.
- [x] 2.2 Generate sanitized predictions, prompt snapshot, raw decoded summary, generation trace, and prediction metadata sidecars without changing prediction values.
- [x] 2.3 Preserve schema-invalid, truncated, non-JSON, or contract-like wrong outputs as failures rather than replacing them with fixture, rule-baseline, or gold contracts.

## 3. Public Evidence Pack

- [x] 3.1 Copy back only sanitized diagnostic evidence into `reports/public-sample/a100-train-split-overfit-diagnostic/`.
- [x] 3.2 Generate metrics, manifest, report, and leak-scan results with `overfit_diagnostic=true` and `generalization_claim=false`.
- [x] 3.3 Verify the evidence pack contains no raw private rows, local or remote private paths, secrets, private IPs, SSH details, raw logs, checkpoints, adapters, caches, or oversized generated corpora.

## 4. Validation and Closeout

- [x] 4.1 Run fresh validation covering dataset build/validate, schema metrics, DPO pair checks, focused A100 diagnostic tests, full tests, lint, type checks, public-leak scan, `git diff --check`, and `openspec validate --all --strict`.
- [x] 4.2 Generate a concise Chinese Human Brief HTML for this phase with observed metrics and explicit non-overclaim boundaries.
- [x] 4.3 Run Reviewer diff review, fix in-scope Must Fix items, rerun required validation, sync accepted specs into `openspec/specs/`, and archive the change if validation passes.
