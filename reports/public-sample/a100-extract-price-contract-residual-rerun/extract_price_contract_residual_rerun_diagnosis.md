# A100 extract-price contract residual rerun diagnosis

Overall interpretation: `extract_price_route_recovered_but_strict_exact_match_residual_remains`.

## Key counts

- Compact-query exact match: `3/3`
- Extract-price exact match: `0/3`
- Extract-price task+route correct: `3/3`
- Extract-price target-slot exact: `1/3`
- Extract-price search fallback: `0`
- Extract-price query/page_url slot drift: `0`

The residual is now strict canonical target wording, not schema, task type, route, safety, or confirmation.
