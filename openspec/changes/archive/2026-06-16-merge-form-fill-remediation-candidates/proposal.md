## Why

The previous preview phase proved that 9 reviewed `form_fill` remediation candidate seeds can be built through the public dataset pipeline without mutating the formal public sample. The next bounded step is to promote those train-only candidates into the formal public sample so future held-out prediction phases can use a single manifest boundary.

## What Changes

- Add a formal merge path for the reviewed `form_fill` remediation candidates.
- Rebuild `data/public-samples/seed_traces.jsonl`, `sft_public_sample.jsonl`, `dpo_public_sample.jsonl`, and `manifest_public_sample.json` from the merged public seed.
- Add merge evidence under `reports/public-sample/form-fill-remediation-public-sample-merge/`.
- Add a `voice2task-data merge-form-fill-remediation-candidates` CLI command with evidence output.
- Preserve strict evidence boundaries: no SFT/DPO/GRPO training, no prediction, no A100 execution, no evaluator metric change, no checkpoint/adapter release, no production readiness claim, and no held-out recovery claim.

## Capabilities

### New Capabilities

### Modified Capabilities

- `voice2task-dataset-preparation`: add formal merge support and evidence requirements for reviewed `form_fill` remediation candidate seeds.

## Impact

- Affected code: `src/voice2task/dataset.py`, `src/voice2task/cli/data.py`, `src/voice2task/reports.py`.
- Affected tests: a new focused test module for the `form_fill` formal merge path plus updates to preview expectations after candidates become formal.
- Affected data artifacts: formal public sample seed/SFT/DPO/manifest files.
- Affected reports: new merge evidence and one Human Brief HTML.
- Non-goals: generic chat fine-tuning, skill routing, GUI action policy learning, first-phase GRPO, public release of the full local/private corpus, A100 training, prediction reruns, evaluator relaxation, checkpoint/adapter release, production readiness claims, live-browser benchmark improvement claims, or private-corpus generalization claims.
