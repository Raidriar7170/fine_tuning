## Why

The previous `design-form-fill-remediation-cases` phase produced a public-safe, design-only artifact with 3 `form_fill` remediation groups and 9 candidate cases. The next bounded step is to make those cases executable as standalone candidate data without changing the formal public sample, held-out splits, evaluator metrics, or model claims.

This keeps the evidence ladder explicit: case design first, candidate dataset materialization second, and any formal public-sample merge or training probe in a later OpenSpec change.

## What Changes

- Add a `form_fill` remediation materializer that reads the reviewed case-design artifact and emits public-safe candidate seed rows plus candidate SFT rows.
- Add a public-safe materialization report writer, CLI command, committed candidate artifacts, focused tests, and Human Brief HTML.
- Preserve the formal public sample boundary: do not edit `seed_traces.jsonl`, public SFT/DPO artifacts, or the public manifest.
- Preserve model/evaluation boundaries: no DPO, no training, no prediction run, no A100 job, no evaluator metric change, no held-out recovery or model recovery claim.
- Apply the existing public form-fill canonical target policy: confirmation-required candidate contracts keep `confirmation_required=true`, `safety.reason=requires_confirmation`, and use a canonical `填写...并确认` normalized command even when the design case focuses on field specificity.

## Capabilities

### New Capabilities

### Modified Capabilities

- `voice2task-dataset-preparation`: Require standalone, public-safe materialization for reviewed `form_fill` remediation candidates before any later formal public-sample merge or training probe.

## Impact

- Affected code: `src/voice2task/dataset.py`, `src/voice2task/reports.py`, and `src/voice2task/cli/data.py`.
- Affected tests: new focused tests for `form_fill` candidate materialization, CLI output, committed evidence, and public-sample immutability.
- Affected data/reports: new candidate seed JSONL and materialization evidence under `data/public-samples/` and `reports/public-sample/`.
- Non-goals: formal public sample merge, held-out mutation, DPO pair generation, training, prediction, A100 execution, evaluator relaxation, checkpoint/adapter release, production readiness, private corpus release, or live-browser benchmark claims.
