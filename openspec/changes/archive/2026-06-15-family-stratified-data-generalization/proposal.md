## Why

The current 7B SFT path can memorize the train split, but held-out `dev`/`test`
exact-match remains uneven. The next useful data step is to expand
family-stratified, public-safe SFT candidates while preserving the existing
formal public-sample evaluation boundary.

This change makes the next generalization data step concrete without launching
A100 training, broad DPO expansion, evaluator relaxation, or model-quality
claims.

## What Changes

- Add a deterministic, public-safe family-stratified candidate dataset covering
  the first text/ASR-to-contract families: search, navigation, clarify,
  form-fill, extraction, unsafe payment blocking, and confirmation.
- Keep the generated candidate dataset independent from the formal public sample
  so current `train/dev/test = 30/6/6` evidence remains interpretable.
- Record family-level split counts, seed/SFT row counts, coverage targets, and
  explicit non-claims in a manifest and Markdown report.
- Add a CLI command to regenerate the candidate dataset and report.
- Add tests that prove family split separation, minimum held-out coverage,
  public-safety, and formal public-sample non-mutation.
- Generate a concise Chinese Human Brief for the phase.

## Non-Goals

- Do not edit `data/public-samples/seed_traces.jsonl`,
  `sft_public_sample.jsonl`, `dpo_public_sample.jsonl`, or
  `manifest_public_sample.json`.
- Do not merge the candidate dataset into the formal public sample in this
  phase.
- Do not generate DPO pairs, run SFT/DPO/GRPO, or run A100 prediction.
- Do not add visual-reference or multimodal grounding data in this phase.
- Do not change strict evaluator semantics, normalized-command scoring,
  prediction repair, or semantic-equivalence scoring.
- Do not claim held-out generalization recovery, model recovery, adapter release,
  checkpoint release, production readiness, private-corpus generalization, or
  live-browser benchmark improvement.
- Do not expand into generic chat fine-tuning, skill routing, GUI action policy
  learning, first-phase GRPO, or public release of the full local corpus.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `voice2task-dataset-preparation`: add an independent family-stratified
  generalization candidate dataset path that preserves formal public-sample
  train/dev/test evidence boundaries.

## Impact

- `src/voice2task/dataset.py`: add deterministic family-stratified candidate
  generation and summary metadata.
- `src/voice2task/reports.py`: add public-safe report/manifest writer for the
  family-stratified candidate dataset.
- `src/voice2task/cli/data.py`: add a regeneration CLI command.
- `tests/`: add focused TDD coverage for candidate generation, CLI, public
  safety, split separation, and non-mutation boundaries.
- `data/public-samples/`: add an independent candidate seed JSONL file.
- `reports/public-sample/`: add candidate SFT rows and evidence.
- `docs/human-briefs/`: add the phase brief.
