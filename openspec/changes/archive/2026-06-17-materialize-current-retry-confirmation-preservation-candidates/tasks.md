## 1. Input Validation

- [x] 1.1 Load the current-retry confirmation-preservation candidate design and verify it is bound to `public-sample-20260616T165835Z`.
- [x] 1.2 Validate exactly two reviewed candidate families and reject missing, extra, duplicate, unreviewed, or already-merged candidates.
- [x] 1.3 Confirm the phase does not require A100 execution, training, prediction generation, prompt changes, evaluator changes, slot normalization, adapter/checkpoint release, or private corpus publication.

## 2. Materialization And Public Artifacts

- [x] 2.1 Add focused tests for candidate seed materialization, accepted target contracts, provenance, and boundary flags.
- [x] 2.2 Implement the materializer and CLI/report path for confirmation-preservation candidate materialization.
- [x] 2.3 Materialize public-safe train seed rows for unsafe-payment confirmation preservation and public-navigation non-confirmation preservation.
- [x] 2.4 Rebuild `seed_traces.jsonl`, `manifest_public_sample.json`, `sft_public_sample.jsonl`, and `dpo_public_sample.jsonl` with updated counts and provenance.
- [x] 2.5 Publish a public-safe materialization evidence pack with pre/post counts, candidate contribution counts, source design provenance, and leak scan result.

## 3. Status Surfaces

- [x] 3.1 Refresh `CONTEXT.md` with the new manifest boundary, materialization result, and strict claim boundaries.
- [x] 3.2 Refresh `reports/final_status.md` with materialization evidence and the next bounded recommendation.
- [x] 3.3 Generate a concise Chinese Human Brief under `docs/human-briefs/`.

## 4. Validation And Archive

- [x] 4.1 Run focused tests for candidate materialization and committed evidence.
- [x] 4.2 Run full tests, ruff, OpenSpec strict validation, DPO pair checks, public leak scan, and `git diff --check`.
- [x] 4.3 Review the diff for overclaiming, private-path leakage, unrelated changes, and comparison-boundary drift.
- [x] 4.4 Archive the OpenSpec change, then stage/commit/push under the guarded auto-integration policy.
