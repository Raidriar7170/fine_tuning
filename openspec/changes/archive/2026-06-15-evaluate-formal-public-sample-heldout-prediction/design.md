## Context

The formal public sample was just expanded to `77` seed rows, `231` SFT rows, and `661` DPO pairs with current manifest id `public-sample-20260615T111316Z`. Prior held-out reports were useful historical evidence, but their prediction configs and manifests refer to earlier public sample versions. This phase asks only whether an existing private 7B adapter can produce useful dev/test predictions on the current formal public sample.

## Goals / Non-Goals

**Goals:**

- Create current-manifest prediction configs for formal public sample dev/test rows.
- Run or record prediction-only execution status without launching SFT or DPO training.
- Evaluate predictions with the existing strict contract ladder, especially `contract_exact_match`.
- Preserve public-safe evidence with sanitized predictions, metrics, schema diagnostics, alignment diagnostics, manifest/report, leak scan, and Human Brief.

**Non-Goals:**

- No dataset mutation, new data generation, DPO generation, or train/dev/test split changes.
- No evaluator relaxation, semantic scoring, slot normalization, prediction repair, or re-scoring.
- No checkpoint release, adapter release, model recovery claim, production-readiness claim, public full-corpus release, private-corpus generalization claim, or live-browser benchmark improvement claim.

## Decisions

1. Use the current formal public sample manifest as the evidence anchor.
   - Rationale: the previous held-out evidence used an older manifest and cannot answer the new post-merge question.
   - Alternative considered: reuse the old held-out metrics as a proxy. Rejected because the row set and family distribution changed.

2. Keep prediction configs public and private overrides out of git.
   - Rationale: committed configs must preserve `<a100_project_root>` placeholders and avoid host, SSH, cache, checkpoint, or adapter details.
   - Alternative considered: commit resolved remote paths for reproducibility. Rejected by the public/private evidence boundary.

3. Treat unavailable remote execution as a first-class blocked evidence state.
   - Rationale: prediction-only evidence is only meaningful if the selected adapter and runtime really exist; otherwise the phase should explain the blocker rather than fabricate metrics.
   - Alternative considered: use fixture predictions as model-quality evidence. Rejected because fixture mode validates the evidence pipeline only and is not a model prediction.

4. Use existing strict evaluator outputs without adding semantic-equivalence scoring.
   - Rationale: the project’s claim boundary relies on strict `contract_exact_match` and field-level diagnostics.
   - Alternative considered: rely on `slot_f1_soft` as the headline. Rejected because it is diagnostic only.

## Risks / Trade-offs

- Remote adapter unavailable -> record a blocked status and stop before quality claims.
- GPU occupancy unsafe -> stop before launch and preserve the reason in private-safe terms.
- New manifest has many more held-out rows -> metrics may drop or expose new residual families; the report will call this diagnosis, not regression proof by itself.
- Sanitization misses private content -> leak scan is mandatory before commit and archive.
