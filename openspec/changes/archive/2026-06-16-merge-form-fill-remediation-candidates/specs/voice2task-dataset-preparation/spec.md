## ADDED Requirements

### Requirement: Merge reviewed form-fill remediation candidates into formal public sample
The system SHALL support a formal public-sample merge for the reviewed train-only `form_fill` remediation candidate seeds after preview integration has passed.

#### Scenario: Rebuild formal public sample with form-fill candidates
- **WHEN** the merge command is run with the reviewed form-fill remediation candidate seed file and the current formal public seed file
- **THEN** the system MUST append exactly 9 formalized candidate seed rows
- **AND** it MUST rebuild formal seed, SFT, DPO, and manifest artifacts in place
- **AND** the rebuilt formal public sample MUST contain 86 seed rows, 240 SFT rows, and 742 DPO pairs
- **AND** the rebuilt SFT split counts MUST be `train=102`, `dev=69`, and `test=69`

#### Scenario: Preserve candidate provenance
- **WHEN** form-fill remediation candidates are promoted into the formal public sample
- **THEN** each promoted seed MUST preserve `public_safe=true`
- **AND** each promoted seed MUST set `candidate_status=formal_public_sample`
- **AND** each promoted seed MUST identify the source candidate seed artifact
- **AND** the formal manifest MUST summarize form-fill remediation candidate counts and affected source case groups

#### Scenario: Reject unsafe or duplicate merge inputs
- **WHEN** candidate seed rows are missing, extra, duplicated, unreviewed, not train split, not standalone, not public-safe, or already present in the formal seed
- **THEN** the merge MUST fail before rewriting formal public sample artifacts

### Requirement: Record form-fill remediation merge evidence without model-quality claims
The system SHALL record public-safe evidence for the formal form-fill remediation candidate merge while preserving evaluation and execution boundaries.

#### Scenario: Write merge evidence artifacts
- **WHEN** the form-fill remediation candidate merge completes
- **THEN** the system MUST write JSON, Markdown, and manifest evidence under `reports/public-sample/form-fill-remediation-public-sample-merge/`
- **AND** the evidence MUST record formal counts, split counts, candidate source, candidate seed rows, candidate SFT rows, candidate DPO contribution, and source case groups

#### Scenario: Preserve execution and claim boundaries
- **WHEN** merge artifacts, reports, or Human Briefs describe the phase
- **THEN** they MUST state that strict `contract_exact_match` remains the primary metric
- **AND** they MUST state that no training, prediction, A100 execution, evaluator metric change, checkpoint release, or adapter release occurred
- **AND** they MUST NOT claim held-out recovery, model recovery, production readiness, private-corpus generalization, public full-corpus release, or live-browser benchmark improvement
