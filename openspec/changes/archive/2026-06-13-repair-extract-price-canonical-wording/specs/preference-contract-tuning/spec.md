## ADDED Requirements

### Requirement: Validate extract-price canonical wording hard negatives
The system SHALL validate extract-price canonical wording hard negatives so that strict-wrong target synonyms cannot be mislabeled or silently accepted as canonical outputs.

#### Scenario: Accept generic price wording negative
- **WHEN** a DPO pair is labeled as generic extract-price wording drift
- **THEN** the chosen contract MUST be a public-safe `extract`/`extract_page` contract with `slots.target="商品价格"` and `normalized_command="提取页面商品价格"`
- **AND** the rejected contract MUST differ in `slots.target`, `normalized_command`, or both
- **AND** validation MUST fail if the rejected contract is identical to the canonical accepted contract

#### Scenario: Accept listed-price wording negative
- **WHEN** a DPO pair is labeled as listed-price wording drift
- **THEN** the chosen contract MUST be the canonical public-safe extract-price contract
- **AND** the rejected contract MUST contain a strict-wrong listed-price target or normalized command such as `标价` or `提取页面标价`

#### Scenario: Accept extra-particle normalized-command negative
- **WHEN** a DPO pair is labeled as extract-price extra-particle wording drift
- **THEN** the chosen contract MUST be the canonical public-safe extract-price contract
- **AND** the rejected contract MUST preserve `slots.target="商品价格"` while changing `normalized_command` away from `提取页面商品价格`

#### Scenario: Summarize canonical wording negatives by slice
- **WHEN** DPO slice summaries are generated
- **THEN** extract-price canonical wording negatives MUST count in the slot slice when `slots.target` changes
- **AND** they MUST count in a normalized-command slice when only `normalized_command` changes
