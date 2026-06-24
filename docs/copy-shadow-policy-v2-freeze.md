# Copy-shadow Policy V2 freeze

Policy V2 has been frozen as an inactive reference in
`configs/copy-backed-scope-policy-v2.frozen.json`.

Current decision:
`POLICY_V2_FROZEN_INACTIVE_REFERENCE_READY_FOR_NATURALISTIC_CHALLENGE_DESIGN`.

Authoritative freeze artifacts:

- `configs/copy-backed-scope-policy-v2.frozen.json`
- `reports/public-sample/copy-shadow-policy-v2-freeze/summary.json`
- `reports/public-sample/copy-shadow-policy-v2-freeze/freeze-input-audit.json`
- `reports/public-sample/copy-shadow-policy-v2-freeze/frozen-scope-decisions.json`
- `reports/public-sample/copy-shadow-policy-v2-freeze/recommended-next-change.md`

## Frozen status

The frozen reference records `status=frozen_reference`, `active=false`,
`runtime_loaded=false`, and `enforcement_enabled=false`.

Frozen scope decisions:

- `form_fill:fill_form:field`: `PROPOSE_DISABLE`
- `search:search_web:query`: `INSUFFICIENT_EVIDENCE`
- `extract:extract_page:target`: `INSUFFICIENT_EVIDENCE`

Every frozen scope has `reviewer_required=true` and
`execution_eligible=false`.

## Source boundary

The freeze validates the inactive proposed Policy V2 artifact and its design
evidence by content hash before writing the frozen reference. It preserves the
source Policy V1 hash, challenge v1 hash, diagnosis artifact hash, and gate
version. Any drift writes only `blocked.json` and does not emit a frozen
policy.

## Runtime boundary

This frozen reference is not runtime enforcement, not action eligibility, not normalized trust, not training, not naturalistic challenge v2, not data expansion, not prediction repair, not browser automation, not model improvement, not production readiness, and not a safety readiness claim.

No runtime loader, prediction hook, evaluator, prompt, decoding, training, or
dataset path reads `configs/copy-backed-scope-policy-v2.frozen.json` as an
active policy.

Recommended next change:
`design-and-materialize-naturalistic-copy-shadow-challenge-v2`
