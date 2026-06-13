## ADDED Requirements

### Requirement: Validate extract-price hard negatives
The system SHALL validate extract-specific DPO hard negatives so that mislabeled search fallback or query-slot pairs cannot silently enter preference training data.

#### Scenario: Accept extract search-fallback negative
- **WHEN** a DPO pair is labeled as extract search fallback
- **THEN** the chosen contract MUST be a public-safe `extract`/`extract_page` contract with a `target` slot
- **AND** the rejected contract MUST change to `task_type="search"` and `route="search_web"`
- **AND** validation MUST fail if the rejected contract keeps the extract task and route unchanged

#### Scenario: Accept extract query-slot negative
- **WHEN** a DPO pair is labeled as extract query-slot drift
- **THEN** the chosen contract MUST be a public-safe `extract`/`extract_page` contract with a `target` slot
- **AND** the rejected contract MUST remove `slots.target` and use a wrong query/page-url style slot shape
- **AND** validation MUST fail if the rejected contract keeps the same accepted slot shape

#### Scenario: Summarize extract hard negatives by slice
- **WHEN** DPO slice summaries are generated
- **THEN** extract search-fallback pairs MUST count in the task-type slice
- **AND** extract query-slot pairs MUST count in the slot slice
