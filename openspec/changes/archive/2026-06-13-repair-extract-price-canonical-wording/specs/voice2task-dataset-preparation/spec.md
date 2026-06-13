## ADDED Requirements

### Requirement: Generate extract-price canonical wording hard negatives
The public sample DPO builder SHALL generate extract-price canonical wording hard negatives that reject strict-wrong target synonyms while preserving the canonical accepted contract.

#### Scenario: Build generic price wording negative
- **WHEN** DPO pairs are generated for a public-safe `extract`/`extract_page` row whose accepted contract uses `slots.target="商品价格"` and `normalized_command="提取页面商品价格"`
- **THEN** the builder MUST include a rejected contract whose rejection reason identifies generic price target wording
- **AND** the rejected contract MUST use a plausible but strict-wrong target such as `slots.target="价格"` or `normalized_command="页面价格"`
- **AND** the chosen contract MUST retain `slots.target="商品价格"` and `normalized_command="提取页面商品价格"`

#### Scenario: Build listed-price wording negative
- **WHEN** DPO pairs are generated for a public-safe `extract`/`extract_page` row whose accepted contract uses the canonical商品价格 target
- **THEN** the builder MUST include a rejected contract whose rejection reason identifies listed-price wording drift
- **AND** the rejected contract MUST use a plausible but strict-wrong target such as `slots.target="标价"` or `normalized_command="提取页面标价"`
- **AND** the chosen contract MUST retain the canonical accepted contract

#### Scenario: Build extra-particle normalized-command negative
- **WHEN** DPO pairs are generated for a public-safe `extract`/`extract_page` row whose accepted contract uses the canonical商品价格 target
- **THEN** the builder MUST include a rejected contract whose rejection reason identifies extra-particle extract wording
- **AND** the rejected contract MUST preserve task, route, safety, confirmation, and `slots.target` while changing `normalized_command` to a strict-wrong wording such as `提取页面上的商品价格`

#### Scenario: Limit canonical wording negatives
- **WHEN** DPO pairs are generated for non-extract contracts, non-public rows, or extract rows whose accepted target is not canonical商品价格
- **THEN** the builder MUST NOT invent extract-price canonical wording hard negatives for those rows

### Requirement: Keep extract-price public targets canonical after wording repair
The public sample dataset SHALL keep the original extract-price seed and schema-preserving augmentations aligned to the same canonical accepted contract.

#### Scenario: Inspect extract-price public rows after regeneration
- **WHEN** public sample SFT artifacts are regenerated for the canonical wording phase
- **THEN** all extract-price public rows MUST use `task_type="extract"`, `route="extract_page"`, `slots={"target":"商品价格"}`, and `normalized_command="提取页面商品价格"`
- **AND** they MUST NOT use accepted targets such as `价格`, `标价`, `页面价格`, or `提取页面上的商品价格`
