## 1. Inputs And Boundary

- [x] 1.1 Validate OpenSpec status, local git status, and source candidate design paths.
- [x] 1.2 Load `reports/public-sample/blocked-payment-safety-repair-candidate-design/` and current public sample manifest/counts.
- [x] 1.3 Confirm this phase is materialization-only: no SFT, DPO, GRPO, A100 execution, prediction generation, evaluator relaxation, semantic scoring, prediction repair, prompt change, checkpoint/adapter release, public full-corpus release, production-readiness claim, model-quality claim, or live-browser benchmark claim.

## 2. Public Candidate Materialization

- [x] 2.1 Implement or run a reproducible materialization pass that converts reviewed blocked-payment repair candidates into public-safe seed rows.
- [x] 2.2 Ensure each materialized contract uses `blocked/deny`, `safety.allow=false`, `safety.reason=unsafe_payment`, and `confirmation_required=false`.
- [x] 2.3 Rebuild public sample derived artifacts (`manifest_public_sample.json`, `sft_public_sample.jsonl`, `dpo_public_sample.jsonl`) from the updated seed traces.
- [x] 2.4 Publish JSON and Markdown materialization evidence under `reports/public-sample/` with candidate provenance, pre/post counts, validation status, DPO family counts, and machine-readable no-claim flags.

## 3. Project Visibility

- [x] 3.1 Refresh `CONTEXT.md` and `reports/final_status.md` with the new manifest/count boundary and recommended next phase.
- [x] 3.2 Generate a concise Chinese Human Brief for the materialization phase.

## 4. Validation And Archive

- [x] 4.1 Add or update focused tests for materialized seed shape, provenance, derived counts, and no-claim flags.
- [x] 4.2 Run focused tests, full tests, ruff, OpenSpec strict validation, public data validation, DPO pair count check, leak scan, and `git diff --check`.
- [x] 4.3 Review the diff for overclaiming, private-path leakage, stale derived artifacts, and unrelated changes.
- [x] 4.4 Archive the OpenSpec change if validation passes.
