## ADDED Requirements

### Requirement: Encode public extract-price targets canonically
The public sample dataset SHALL encode current-page price extraction requests with a canonical extract-page contract target instead of search fallback or generic query slots.

#### Scenario: Build public extract-price rows
- **WHEN** the public sample dataset is generated or inspected for the current extract-price seed and its schema-preserving augmentations
- **THEN** those rows MUST use `task_type="extract"` and `route="extract_page"`
- **AND** they MUST use `safety.allow=true`, `safety.reason="public_readonly"`, and `confirmation_required=false`
- **AND** they MUST use `slots={"target":"商品价格"}` and `normalized_command="提取页面商品价格"`
- **AND** they MUST NOT encode the target as `slots.query`, `slots.page_url`, or a public web search route

### Requirement: Generate extract-price hard negatives
The public sample DPO builder SHALL generate extract-specific hard negatives that reject search fallback and query/page-url slot shapes for current-page price extraction targets.

#### Scenario: Build extract search-fallback hard negative
- **WHEN** DPO pairs are generated for a public-safe `extract`/`extract_page` row whose chosen contract uses `slots.target`
- **THEN** the builder MUST include a rejected contract with a distinct rejection reason for extract search fallback
- **AND** the rejected contract MUST change the output toward a plausible but wrong `search`/`search_web` contract
- **AND** the chosen contract MUST retain `task_type="extract"`, `route="extract_page"`, `slots.target`, and the canonical normalized command

#### Scenario: Build extract query-slot hard negative
- **WHEN** DPO pairs are generated for a public-safe `extract`/`extract_page` row whose chosen contract uses `slots.target`
- **THEN** the builder MUST include a rejected contract with a distinct rejection reason for query-slot extraction drift
- **AND** the rejected contract MUST replace the accepted `slots.target` shape with a wrong query/page-url style slot shape
- **AND** the chosen contract MUST retain `slots.target` and the canonical normalized command

#### Scenario: Limit extract hard-negative scope
- **WHEN** DPO pairs are generated for non-extract contracts or extract contracts without a public-safe target slot
- **THEN** the builder MUST NOT invent extract-price search-fallback or query-slot rejected contracts for those rows
