# Route Ontology Diagnosis

Status: route ontology improved on these train rows, but the Browser Task Contract remains schema-invalid because `confirmation_required` is absent in all final predictions.

## Route Ontology Counts

- Route value counts: `{'search_web': 3}`
- Task type value counts: `{'search': 3}`
- Route enum-valid count: `3/3`
- Task type enum-valid count: `3/3`
- Raw route ontology / gold-route match: `3/3`
- Missing `confirmation_required`: `3/3`
- Final schema-valid count: `0/3`
- Strict final route accuracy remains `0.0000` because the strict evaluator only grants route credit after final Browser Task Contract validation.

## Interpretation

The previous weather/domain route symptom is not present in this rerun: observed `route` values are `search_web`, and all three raw route values match the gold route. This does not prove model recovery because strict Browser Task Contract validation still rejects every prediction.

## Boundary

This is train-internal evidence only, with no held-out generalization claim and no release or production-readiness claim.
