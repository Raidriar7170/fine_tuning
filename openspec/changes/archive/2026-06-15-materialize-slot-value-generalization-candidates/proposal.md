## Why

The slot value generalization case design has already identified four reviewed residual families, but they still exist only as design evidence. To make the next learning step testable without contaminating held-out public rows, we need a bounded materialization phase that writes public-safe candidate data separately from the current public sample.

This solves the immediate data question without claiming model recovery, changing evaluator semantics, or launching A100 training.

## What Changes

- Add deterministic materialization from the archived slot value case design into a standalone candidate seed JSONL file.
- Generate schema-compatible candidate SFT rows and a public-safe materialization report/manifest.
- Add a CLI command for regenerating the candidate data and report from the design artifact.
- Add tests that prove the candidate data covers the four reviewed case groups and does not mutate `seed_traces.jsonl`, `sft_public_sample.jsonl`, `dpo_public_sample.jsonl`, or `manifest_public_sample.json`.
- Generate a concise Chinese Human Brief with project-stage progress and non-claim boundaries.

## Non-Goals

- Do not merge candidates into `data/public-samples/seed_traces.jsonl`.
- Do not rebuild the formal public sample SFT/DPO artifacts from the candidate rows.
- Do not generate DPO pairs, run SFT/DPO/GRPO, or run A100 prediction.
- Do not change strict evaluator semantics, slot normalization, or exact-match scoring.
- Do not claim held-out generalization recovery, private-corpus generalization, production readiness, adapter release, checkpoint release, or live-browser benchmark improvement.
- Do not expand into generic chat fine-tuning, skill routing, GUI action policy learning, first-phase GRPO, or public release of the full local corpus.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `voice2task-dataset-preparation`: add a bounded candidate materialization path for reviewed slot value generalization cases that remains separate from the formal public sample.

## Impact

- `src/voice2task/dataset.py`: add deterministic candidate materialization and summary generation.
- `src/voice2task/reports.py`: add a public-safe report writer and manifest for materialized candidates.
- `src/voice2task/cli/data.py`: add a local CLI command to regenerate candidate artifacts.
- `tests/`: add focused materialization tests and CLI/report boundary tests.
- `data/public-samples/`: add an independent candidate seed JSONL file.
- `reports/public-sample/`: add materialization evidence.
- `docs/human-briefs/`: add the phase brief.
