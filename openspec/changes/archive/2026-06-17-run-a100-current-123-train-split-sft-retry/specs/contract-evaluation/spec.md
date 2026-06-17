## ADDED Requirements

### Requirement: Publish current-123 train split SFT retry strict held-out evidence
The system SHALL publish public-safe dev/test strict evaluation evidence for the private current-123 train split SFT retry adapter trained for `public-sample-20260617T045941Z`.

#### Scenario: Report observed current-123 retry metrics
- **WHEN** current-123 retry training and dev/test prediction-only evaluation complete
- **THEN** the evidence MUST report strict dev/test metrics using the existing contract ladder, including `json_valid_rate`, `task_type_accuracy`, `route_accuracy`, `safety_precision`, `safety_recall`, `confirmation_accuracy`, strict `slot_f1`, diagnostic-only `slot_f1_soft`, and `contract_exact_match`
- **AND** it MUST record manifest id `public-sample-20260617T045941Z`, split counts of 123 train / 69 dev / 69 test, and the paired adapter runtime `a100-current-train-split-sft-retry`
- **AND** it MUST keep strict `contract_exact_match` and strict `slot_f1` as public headline metrics while labeling `slot_f1_soft` diagnostic-only

#### Scenario: Preserve current-manifest comparison boundary
- **WHEN** reports or Human Briefs compare current-123 retry evidence with prior model evidence
- **THEN** they MUST state that prior metrics were bound to `public-sample-20260616T165835Z`
- **AND** they MUST NOT present old/new values as clean improvement or regression unless the manifest boundary is explicit
- **AND** they MUST NOT interpret prediction configs as current-manifest model evidence unless the adapter was trained for `public-sample-20260617T045941Z`

#### Scenario: Report blocked or failed current-123 retry safely
- **WHEN** training, prediction, evaluation, GPU preflight, dependency setup, private override setup, or output-root policy cannot safely complete
- **THEN** the evidence MUST record blocked or failed status without fabricating predictions, metrics, adapters, or model-quality claims
- **AND** committed artifacts MUST omit raw logs, host details, SSH details, private paths, checkpoints, adapters, caches, tokens, and private corpus rows

#### Scenario: Preserve current-123 retry public evidence boundaries
- **WHEN** current-123 retry evidence is prepared for commit
- **THEN** leak scan MUST reject raw private rows, absolute local paths, private remote paths, host details, SSH details, secrets, tokens, raw logs, checkpoints, adapters, caches, and oversized generated corpora
- **AND** reports MUST NOT claim production readiness, private-corpus generalization, public checkpoint release, public adapter release, released model quality, or live-browser benchmark improvement
