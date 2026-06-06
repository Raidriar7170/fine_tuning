# Design

## Context

The current public-readonly search prompt already requires `task_type="search"`, `route="search_web"`, and object-shaped `slots.query`. It does not yet explicitly forbid `city/date` decomposition, and the public search gold target currently uses a spaced query string (`北京 明天 天气`) while `normalized_command` uses a compact query phrase (`搜索北京明天天气`).

This mismatch makes it unclear whether the next fix should change the model, the target data, or evaluator semantics. This phase chooses a conservative target policy and updates only local targets/prompt guidance/evidence.

## Policy

For public-readonly information lookup and weather-search rows:

1. `slots` MUST be an object with exactly the canonical search query key for the query payload: `{"query": "<compact_query>"}`.
2. The model-visible policy MUST state that it should not split the same search query into `city`, `date`, `topic`, or other ad hoc keys.
3. `<compact_query>` SHOULD omit ASR filler and verb words, and SHOULD avoid artificial token-separating spaces for ordinary Chinese search phrases.
4. `normalized_command` SHOULD be `搜索` + `<compact_query>` for these search rows.
5. This policy is strict target alignment, not evaluator normalization: predictions are still compared exactly.

## Approach

1. Add TDD coverage for:
   - formatting prompt visibility of the compact query/no-`city/date` policy,
   - public sample search targets and DPO chosen/rejected contracts using compact `slots.query`,
   - evidence pack privacy and claim boundaries.
2. Update prompt guidance in `src/voice2task/formatting.py`.
3. Update public sample seed/SFT/DPO search contracts from `北京 明天 天气` to `北京明天天气`.
4. Generate a policy summary artifact from source data and prompt metadata.
5. Generate leak scans and a concise Chinese Human Brief.

## Alternatives Considered

- Accept `city/date` as equivalent to `query`.
  - Rejected because this would change schema/contract interpretation and require evaluator or downstream contract changes.
- Keep spaced `query` strings.
  - Rejected because `normalized_command` and model outputs already use compact query phrases, and the spaces are not semantically required for ordinary Chinese search queries.
- Add evaluator normalization for query spacing.
  - Rejected because this phase must keep strict exact-match metrics unchanged.

## Risks And Mitigations

- Risk: A compact query policy may look like metric relaxation.
  - Mitigation: evidence and Human Brief state that historical predictions are not re-scored and evaluator metrics remain strict.
- Risk: Data changes could hide the prior A100 result.
  - Mitigation: prior A100 artifacts remain unchanged; this phase publishes separate policy evidence only.
- Risk: Prompt guidance could become too narrow.
  - Mitigation: wording is scoped to public-readonly information lookup/search rows, not every task type.
