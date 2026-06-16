## ADDED Requirements

### Requirement: Retry post-confirmation-marker-merge formal held-out prediction after A100 recovery
The system SHALL support a public-safe prediction-only retry after a blocked A100 formal held-out prediction phase, while preserving the blocked archive, changed manifest boundary, and strict evaluation semantics.

#### Scenario: Evaluate current formal held-out splits after runtime recovery
- **WHEN** sanitized private-adapter predictions are available for the current formal public sample dev and test splits after A100 runtime recovery
- **THEN** the system MUST evaluate them with the existing strict contract ladder, including `json_valid_rate`, `task_type_accuracy`, `route_accuracy`, `safety_precision`, `safety_recall`, `confirmation_accuracy`, `slot_f1`, `slot_f1_soft`, and `contract_exact_match`
- **AND** the evidence MUST record manifest id `public-sample-20260616T074315Z`, 69 dev SFT rows, 69 test SFT rows, and the source formal sample counts of 98 seed rows, 252 SFT rows, and 850 DPO pairs

#### Scenario: Preserve retry and blocked-evidence boundaries
- **WHEN** reports or Human Briefs describe the A100-recovery retry metrics
- **THEN** they MUST publish those metrics in a distinct evidence directory from both the earlier formal held-out prediction evidence and the archived blocked post-confirmation-marker-merge evidence
- **AND** they MUST state that the retry was a runtime-recovery prediction-only rerun, not a training change, evaluator relaxation, prediction repair, or model-recovery claim

#### Scenario: Preserve prediction-only and public-safety boundaries
- **WHEN** A100-recovery retry evidence is prepared for commit
- **THEN** committed artifacts MUST state that no SFT training, DPO training, GRPO training, dataset mutation, evaluator relaxation, semantic-equivalence scoring, slot normalization, prediction repair, prediction replacement, or prediction re-score was performed
- **AND** committed artifacts MUST NOT claim held-out recovery, model recovery, checkpoint release, adapter release, production readiness, public full-corpus release, private-corpus generalization, or live-browser benchmark improvement
- **AND** leak-scan validation MUST reject raw private rows, absolute local paths, private remote paths, host details, SSH details, secrets, tokens, raw logs, checkpoints, adapters, caches, and oversized generated corpora

#### Scenario: Record retry execution as blocked if safety preflight fails
- **WHEN** the prediction-only A100 retry cannot safely execute because the private adapter, private override, remote dependency, or idle GPU state is unavailable
- **THEN** the evidence MUST record a blocked status without writing fabricated predictions or model-quality metrics
- **AND** committed artifacts MUST omit raw logs, host details, SSH details, private paths, checkpoints, adapters, caches, tokens, and private corpus rows
