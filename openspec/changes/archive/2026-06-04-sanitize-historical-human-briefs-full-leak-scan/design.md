## Context

Public evidence packs already reject raw private rows, local absolute paths, private remote paths, secrets, private IP addresses, SSH details, checkpoints, adapters, caches, raw logs, and oversized generated corpora. During the project audit, the broader public-surface scan found a single historical Human Brief line that used a path-like private A100 example while describing sanitizer behavior.

The finding is not a leaked live secret or raw runtime artifact, but keeping the literal path pattern in committed HTML weakens the repository's "scan every public-facing artifact" posture. This phase treats the historical brief as a public documentation surface and cleans it without changing the underlying failed A100 model-output evidence.

## Goals / Non-Goals

**Goals:**

- Remove the path-like private A100 example from the historical Human Brief while preserving the intended meaning: public evidence must reject private remote roots.
- Clarify in OpenSpec that committed Human Brief HTML and loop reports are scanned public documentation surfaces.
- Run fresh leak-scan, tests, OpenSpec strict validation, and whitespace checks.
- Generate a concise Chinese Human Brief with project-stage progress and the remaining model-quality gap.

**Non-Goals:**

- No model retraining, DPO work, prediction repair, schema normalization, new A100 execution, public checkpoint release, private corpus publication, live-browser benchmark claim, or rewrite of historical evidence outcomes.

## Decisions

1. Edit only the unsafe illustrative text, not the historical evidence status.
   - Rationale: the prior phase result remains historically useful; the cleanup target is public-surface hygiene.
   - Alternative considered: delete the old Human Brief. Rejected because it would remove audit trail context.

2. Keep leak-scan strict instead of adding an allowlist for documentation examples.
   - Rationale: committed public-facing artifacts are easier to trust when the same privacy gate applies uniformly.
   - Alternative considered: allow placeholder examples under `docs/human-briefs`. Rejected because similar examples can drift into real paths.

3. Treat this as a small OpenSpec change.
   - Rationale: it modifies public evidence posture and archived project documentation, so it should be traceable even though the code diff is tiny.

## Risks / Trade-offs

- [Risk] The cleanup could appear to rewrite the past A100 result -> Mitigation: do not change metrics, manifests, prediction rows, or the failure interpretation.
- [Risk] Human Briefs become a second source of truth -> Mitigation: the new brief links back to OpenSpec, reports, and validation commands only; it does not replace authoritative artifacts.
- [Risk] The phase expands into SFT objective fixes -> Mitigation: keep this change scoped to public-surface hygiene; objective repair belongs to the next OpenSpec change.
