## Why

The archived A100 public held-out diagnostic showed that the previous 7B train-split recovery did not generalize: public `dev` and `test` predictions were schema-valid but had `contract_exact_match=0.0` and `slot_f1=0.0`. This phase repairs the narrow public held-out residual families with explicit target policy and hard negatives before any broader private-corpus or release claim is considered.

## What Changes

- Add public-safe target-policy coverage for the held-out residual families: ambiguous `clarify`, unsafe payment `blocked`, confirmation-required `form_fill`, and canonical `navigate` URL/open-site outputs.
- Add dedicated public DPO hard-negative categories for the observed drifts: clarify-to-search/navigate, blocked-payment-to-search/navigate, form confirmation/slot/safety drift, and navigation URL/normalized-command drift.
- Regenerate the committed public sample SFT/DPO/manifest artifacts so the public training sample and DPO slice counts reflect the repair data.
- Add SFT prompt visibility tests, DPO validation tests, dataset-builder tests, and public evidence tests that keep the repair bounded to strict contract behavior.
- Prepare and run a bounded A100 public-sample rerun/evaluation path only after local validation passes, preserving public-safe sidecars and claim boundaries.
- Keep all claims conservative: this phase may report train/dev/test public-sample metrics but does not imply private-corpus generalization, checkpoint/adapter release, production readiness, or live-browser benchmark improvement.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `voice2task-dataset-preparation`: public sample generation includes held-out residual repair hard negatives and keeps regenerated SFT/DPO/manifest artifacts synchronized.
- `preference-contract-tuning`: DPO validation and slice reporting recognize the new held-out residual hard-negative categories.
- `supervised-contract-tuning`: SFT and prediction prompts expose held-out residual contract policies without leaking row-specific gold targets into prediction prompts.
- `contract-evaluation`: public-safe repair evidence reports split metrics and bounded interpretation after rerun.

## Impact

- Affected code: `src/voice2task/dataset.py`, `src/voice2task/dpo.py`, `src/voice2task/formatting.py`, and report/evidence generation scripts as needed.
- Affected public artifacts: `data/public-samples/*`, public A100 rerun config templates, `reports/public-sample/repair-public-heldout-contract-residuals/`, and a concise Chinese Human Brief.
- Affected tests: dataset builder, DPO validation, formatting prompt policy, A100 smoke/evidence boundary tests, and validation/leak-scan checks.
- Non-goals: generic chat fine-tuning, skill routing, GUI action policy learning, first-phase GRPO, evaluator normalization, semantic-equivalence scoring, prediction repair/replacement, private full-corpus evaluation, released checkpoint/adapter claims, and live-browser benchmark claims.
