# Voice2Task form-fill remediation candidate integration preview

This is a preview-only integration check: it proves the standalone form-fill remediation candidate seeds can be consumed by the public dataset builder in a report-scoped directory. It does not rewrite formal public sample files.

## Boundary

- Preview seed/SFT/DPO/manifest artifacts live only under this report directory.
- Formal public sample seed, SFT, DPO, and manifest files are not rewritten.
- Preview DPO pairs are data-construction evidence only, not DPO training evidence.
- No SFT/DPO/GRPO training, prediction run, or A100 execution is performed.
- strict `contract_exact_match` remains primary.
- Soft slot F1 and semantic equivalence remain diagnostic-only.
- This is not a model recovery, held-out recovery, checkpoint, adapter, production, or live-browser claim.

## Counts

- Formal public sample counts before: `{'dpo_pairs': 661, 'seed_rows': 77, 'sft_rows': 231}`
- Preview counts: `{'seed_rows': 86, 'sft_rows': 240, 'dpo_pairs': 742}`
- Preview split counts: `{'train': 102, 'dev': 69, 'test': 69}`
- Candidate seed rows: `9`
- Candidate SFT rows: `9`
- Candidate preview DPO pairs: `81`

## Validation

- Public preview validation ok: `True`
- Validation counts: `{'sft_rows': 240, 'dpo_pairs': 742}`
- Validation failures: `[]`

## Recommended Next Step

Use a later bounded OpenSpec phase to decide whether to formally merge the candidates or run a no-merge candidate probe. Keep formal merge, A100 training, prediction, and recovery claims separate.
