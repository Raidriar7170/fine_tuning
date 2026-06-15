## Why

The slot value candidate probe proved that 7B SFT can learn the reviewed
candidate rows on train split, but those rows are still outside the formal
public sample and therefore have not tested held-out improvement. This phase
turns the approved candidate set into formal public data and measures whether
the resulting 7B adapter improves public `dev`/`test` strict contract behavior.

## What Changes

- Merge the reviewed slot value generalization candidate seeds into
  `data/public-samples/seed_traces.jsonl`.
- Regenerate `sft_public_sample.jsonl`, `dpo_public_sample.jsonl`, and
  `manifest_public_sample.json` from the formal seed file.
- Preserve candidate provenance while changing candidate status from standalone
  probe data to formal public-sample rows.
- Add A100 SFT and split-specific prediction configs for the merged public
  sample.
- Publish public-safe train/dev/test held-out evidence, including strict
  metrics and claim boundaries.
- Generate a concise Chinese Human Brief for the phase.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `voice2task-dataset-preparation`: formalize reviewed slot value candidates
  as public sample seed/SFT/DPO rows after explicit approval.
- `supervised-contract-tuning`: run a bounded 7B A100 SFT rerun on the merged
  public sample and split-specific train/dev/test predictions.
- `contract-evaluation`: publish public-safe evidence for the merged-candidate
  held-out evaluation without release or production claims.

## Impact

- `src/voice2task/dataset.py` and `src/voice2task/cli/data.py`: public sample
  candidate merge path.
- `data/public-samples/`: formal seed, SFT, DPO, and manifest artifacts.
- `configs/`: A100 7B training and prediction templates with private
  placeholders.
- `src/voice2task/reports.py`, `src/voice2task/cli/report.py`, and
  `reports/public-sample/`: sanitized evidence report generation.
- `tests/`: focused coverage for counts, candidate inclusion, DPO hard
  negatives, configs, evidence boundaries, and public leak scanning.

Non-goals: generic chat fine-tuning, skill routing, GUI action policy learning,
first-phase GRPO, DPO training, public release of the full local/private
corpus, checkpoint or adapter release, production-readiness claims, and
live-browser benchmark improvement claims.
