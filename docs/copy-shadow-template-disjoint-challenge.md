# Copy-Shadow Template-Disjoint Challenge

This document records the bounded `evaluate-frozen-copy-shadow-policy-on-template-disjoint-challenge-set` phase.

## Status

Decision: `CHALLENGE_V1_HOOK_UNSAFE_OR_INVALID` for the recovered step-matched adapter challenge run.

The challenge rows and audits were frozen, hook hardening was implemented, and the recovered runner executed the frozen challenge on content-hash-verified private Control/Treatment step-matched adapters in the A100 environment. Public artifacts contain only sanitized adapter identity fields, predictions, sidecars, audits, and summaries; they do not contain private adapter paths, override configs, caches, host details, or raw A100 logs.

Authoritative artifacts:

- Challenge rows: [`../data/public-samples/copy-shadow-template-disjoint-challenge-v1.jsonl`](../data/public-samples/copy-shadow-template-disjoint-challenge-v1.jsonl)
- Summary: [`../reports/public-sample/copy-shadow-template-disjoint-challenge-v1/challenge-summary.json`](../reports/public-sample/copy-shadow-template-disjoint-challenge-v1/challenge-summary.json)
- Freeze-phase blocked evidence: [`../reports/public-sample/copy-shadow-template-disjoint-challenge-v1/blocked.json`](../reports/public-sample/copy-shadow-template-disjoint-challenge-v1/blocked.json)
- Recovered-adapter runner report: [`../reports/public-sample/copy-shadow-template-disjoint-challenge-v1/adapter-evaluation/challenge-evaluation-summary.json`](../reports/public-sample/copy-shadow-template-disjoint-challenge-v1/adapter-evaluation/challenge-evaluation-summary.json)
- Hook safety audit: [`../reports/public-sample/copy-shadow-template-disjoint-challenge-v1/adapter-evaluation/hook-safety-audit.json`](../reports/public-sample/copy-shadow-template-disjoint-challenge-v1/adapter-evaluation/hook-safety-audit.json)
- Prediction run audit: [`../reports/public-sample/copy-shadow-template-disjoint-challenge-v1/adapter-evaluation/prediction-run-audit.json`](../reports/public-sample/copy-shadow-template-disjoint-challenge-v1/adapter-evaluation/prediction-run-audit.json)
- Offline evaluation audits: [`../reports/public-sample/copy-shadow-template-disjoint-challenge-v1/adapter-evaluation/evaluation-audits.jsonl`](../reports/public-sample/copy-shadow-template-disjoint-challenge-v1/adapter-evaluation/evaluation-audits.jsonl)
- Template audit: [`../reports/public-sample/copy-shadow-template-disjoint-challenge-v1/template-disjoint-audit.json`](../reports/public-sample/copy-shadow-template-disjoint-challenge-v1/template-disjoint-audit.json)

## Challenge Purpose

Challenge v1 is a copy-shadow verifier adversarial fixture, not a naturalistic language benchmark or speech/ASR generalization benchmark. It evaluates whether frozen observe-only copy-backed provenance evidence can generalize beyond templates used for scope selection, policy design, verifier design, model training, and dev/test debugging.

This phase does not train, repair predictions, change policy scopes, change prompts, change decoding, change evaluators, change schemas, enable runtime enforcement, enable action provenance, or trust normalized provenance.

## Template-Disjoint Definition

Accepted rows must have no overlap with current train/dev/test rows by:

- sample id;
- exact input text;
- canonical template signature;
- slot-value-stripped template signature.

Near-duplicate thresholds are deterministic: accepted rows stay below character 3-gram Jaccard `0.80` and normalized edit similarity `0.85`. The v1 audit accepted all 120 rows with 0 overlap counts.

## Freeze Flow

1. Load and validate frozen `copy-backed-scope-policy-v1`.
2. Materialize deterministic public-safe rows.
3. Validate each `gold_contract` as BrowserTaskContract V1.
4. Verify gold feasibility against the frozen policy expectation.
5. Write the challenge JSONL and report bundle.
6. Attempt frozen adapter identity discovery from a private override or environment variables.
7. If no adapter is loadable and identity-verifiable, write `CHALLENGE_EVALUATION_BLOCKED` and stop.
8. If both adapters are content-hash verified, run the canonical prediction exporter for Control/Treatment with the shadow hook disabled, enabled with NullSink, and enabled with JsonlSink.
9. Freeze predictions and online sidecars, then generate public-safe offline evaluation audits and summary metrics.

## Scope Coverage

The frozen v1 challenge has 120 rows:

- `search:search_web:query`: 30 rows.
- `form_fill:fill_form:field`: 30 rows.
- `extract:extract_page:target`: 30 rows.
- `blocked:deny:action`: 30 disabled negative-control rows.

Condition tags cover exact unique, duplicate exact, source absent, multiple entity distractor, partial span trap, normalization candidate, normalization collision, long input, ASR-style noise, synthetic PII, out-of-scope action, and invalid/unparseable output fault injection.

## Prediction Boundary

Observed challenge prediction may only use the canonical `voice2task-train sft-predict` entrypoint or library-equivalent `voice2task.training.run_sft_prediction_export`. The bounded runner is [`../scripts/run_recovered_adapter_challenge_evaluation.py`](../scripts/run_recovered_adapter_challenge_evaluation.py); it writes public-safe audits under `adapter-evaluation/` and keeps private adapter override paths out of committed artifacts.

No standalone verifier script may be used as the primary online-sidecar result. In the recovered A100 run, both Control and Treatment adapters passed config/model content-hash checks, and each adapter produced 120 predictions in disabled, NullSink, and JsonlSink modes. Prediction output hashes and parsed prediction contracts are invariant across hook modes for each adapter role.

## Provenance And Correctness Split

Online sidecars remain gold-free and privacy-preserving. They may record hashes, policy metadata, hook status, write status, and slot diagnostics.

Gold correctness belongs only in offline challenge audits after prediction and sidecar artifacts are frozen. The recovered run writes 252 offline evaluation audit rows because observed model predictions can contain more than one audited slot event. Online sidecars remain gold-free, retain no full input text, retain no span text, and retain no raw model output.

## Trust Rules

- Exact unique copy-backed provenance is the only trusted path.
- Normalized matches are candidate-only and never trusted.
- Action provenance remains disabled.
- Source spans must pass full offset/hash/back-slice validation.
- Sidecar path conflicts are isolated and never fallback-written.

## Privacy Defaults

Sidecars default to hash-and-offset-only retention. `retain_input_text=true`, `retain_raw_model_output=true`, and `fail_isolated=false` are rejected as invalid shadow config.

The challenge rows are public-safe synthetic text. Synthetic PII tags are labels for test coverage, not real personal data.

## Decision Gate

The only possible non-blocked labels for observed challenge prediction remain observe-only. Runtime enforcement cannot be recommended in this phase.

This run selected `CHALLENGE_V1_HOOK_UNSAFE_OR_INVALID`. The canonical prediction path, sidecar privacy, and hook invariance gates passed, but adversarial false-trust gates failed: source-absent false trust is 3, normalization-collision false trust is 6, and partial-span false trust is 3. Normalized trusted count, action trusted count, provenance false accepts, contract mutations, runtime decision deltas, sidecar unmatched count, policy drift count, and prediction hash mismatch count are all 0. This result does not prove naturalistic generalization, task correctness, model improvement, slot accuracy improvement, runtime enforcement safety, production readiness, or safety readiness.
