## 1. Formal Public Sample Merge

- [x] 1.1 Add a public-safe dataset merge path for reviewed slot value candidate seeds.
- [x] 1.2 Merge the candidate seeds into `data/public-samples/seed_traces.jsonl` and regenerate formal SFT/DPO/manifest artifacts.
- [x] 1.3 Add tests for formal counts, candidate inclusion, split preservation, DPO hard negatives, and leak-scan boundaries.

## 2. A100 Training And Held-Out Evaluation

- [x] 2.1 Add merged-candidate A100 7B SFT and train/dev/test prediction configs with private placeholders.
- [x] 2.2 Add report generation for merged-candidate train/dev/test evidence and claim boundaries.
- [x] 2.3 Run local dry-run/config/report tests and public sample validation.
- [x] 2.4 If A100 preflight is safe, run the private 7B SFT plus train/dev/test prediction/eval and import only sanitized evidence; otherwise record a public-safe blocked status.

## 3. Review, Brief, Archive

- [x] 3.1 Generate the Chinese Human Brief with project-stage progress and non-claim boundaries.
- [x] 3.2 Run focused tests, full pytest, `openspec validate --all --strict`, leak scan, and `git diff --check`.
- [x] 3.3 Run Reviewer pass, fix in-scope Must Fix items, archive the change, and commit.
