## ADDED Requirements

### Requirement: Run current-123 train split SFT retry after readiness evidence
The system SHALL run at most one bounded private A100 SFT retry on the `public-sample-20260617T045941Z` train split after current-123 readiness evidence is complete.

#### Scenario: Repeat A100 preflight before current-123 retry training
- **WHEN** the current-123 train split SFT retry phase starts
- **THEN** it MUST run fresh A100 connectivity, GPU occupancy, disk/cache/temp, approved-root, dependency, manifest-count, and readiness-evidence checks
- **AND** it MUST select a safe GPU explicitly with `CUDA_VISIBLE_DEVICES` before training
- **AND** it MUST stop with blocked evidence if safe placement cannot be determined without interrupting other users

#### Scenario: Train only from the current formal public train split
- **WHEN** current-123 retry training starts
- **THEN** it MUST use manifest `public-sample-20260617T045941Z` and the train split of 123 SFT rows
- **AND** it MUST use runtime/output label `a100-current-train-split-sft-retry` without overwriting prior public evidence directories
- **AND** it MUST NOT mutate public sample rows, prompts, evaluator metrics, prediction artifacts, or slot values before training

#### Scenario: Keep current-123 retry artifacts private
- **WHEN** current-123 retry training or prediction runs
- **THEN** private overrides, checkpoints, adapters, raw logs, model caches, host details, SSH details, tokens, and private paths MUST remain outside git
- **AND** committed evidence MUST use sanitized summaries and public-safe placeholders

#### Scenario: Preserve non-goals during current-123 retry
- **WHEN** current-123 retry evidence is prepared for commit
- **THEN** it MUST state that no DPO, GRPO, prompt change, evaluator relaxation, semantic-equivalence scoring, slot normalization, prediction repair, prediction replacement, public checkpoint release, public adapter release, private corpus publication, production-readiness claim, or live-browser benchmark claim occurred
