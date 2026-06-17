## Context

The latest current-train-split SFT retry recovered safety recall but introduced confirmation regressions on seven held-out rows. The archived `design-current-retry-confirmation-preservation-candidates` change produced a public-safe design artifact with two reviewed candidate families and explicit design-only boundaries.

Current public sample boundary:

- Manifest: `public-sample-20260616T165835Z`
- Counts: 100 seeds / 256 SFT rows / 864 DPO pairs
- Split counts: train 118 / dev 69 / test 69
- Source design: `reports/public-sample/current-retry-confirmation-preservation-candidate-design/`

This change is the materialization step after design review. It should update the formal public sample and synchronized public artifacts, but it must not train or evaluate a model.

## Goals / Non-Goals

**Goals:**

- Materialize exactly the reviewed confirmation-preservation candidate families as public-safe train seed rows.
- Preserve source design provenance, source row ids, candidate family ids, accepted target sketches, and rejected drift intent.
- Rebuild the committed public manifest, SFT rows, and DPO pairs from the updated public seed traces.
- Publish a materialization evidence pack and refresh status docs.
- Keep the phase auditable as data/materialization evidence only.

**Non-Goals:**

- No A100 training, prediction generation, DPO/GRPO run, prompt change, evaluator relaxation, prediction repair, slot normalization, adapter release, checkpoint release, production-readiness claim, live-browser benchmark claim, or model recovery claim.
- No generic chat fine-tuning, skill routing, or GUI action policy learning.
- No local/private corpus publication.

## Decisions

1. **Use reviewed candidate design as the only materialization source.**
   - Rationale: the design artifact already binds the candidate families to the trade-off diagnosis and records reviewed source rows.
   - Alternative considered: derive new candidates directly from predictions during materialization. Rejected because materialization should not rediscover or broaden candidate scope.

2. **Materialize one seed row per candidate family, with schema-preserving augmentations.**
   - Rationale: each candidate family represents one accepted target shape and several source rows; one public-safe seed plus augmentations is enough for the formal public sample without duplicating held-out rows.
   - Alternative considered: materialize all seven source rows as separate seeds. Rejected because source row ids are held-out evidence references, not necessarily public-safe train seed text.

3. **Merge as train rows and rebuild derived public artifacts.**
   - Rationale: these candidates are intended to teach confirmation preservation in a later retry, so they belong in train and must be reflected in manifest/SFT/DPO artifacts.
   - Alternative considered: keep standalone candidate artifacts only. Rejected because the next useful phase needs a current formal public-sample boundary.

4. **Fail closed on missing, extra, duplicate, unreviewed, or already-merged candidates.**
   - Rationale: prior public-sample phases rely on exact candidate accounting to preserve comparison boundaries.
   - Alternative considered: append whatever candidate rows are present. Rejected because it weakens provenance and reviewability.

## Risks / Trade-offs

- **Risk: candidate wording accidentally leaks private held-out details** -> Use public-safe templates from the design artifact and scan generated artifacts before commit.
- **Risk: materialization is mistaken for model recovery** -> Evidence and docs must repeat that no training or prediction happened.
- **Risk: formal public manifest boundary changes make metric comparisons invalid** -> Update manifest id/counts and `CONTEXT.md` comparison boundary before any later model-quality run.
- **Risk: DPO hard negatives add unintended confirmation drift** -> Treat DPO output as derived public-sample artifacts only; validate counts and provenance, and defer model-effect claims to later strict held-out evaluation.

## Migration Plan

1. Add focused tests for candidate materialization and committed evidence.
2. Implement the materializer/CLI/report writer.
3. Generate candidate seed rows and rebuild public artifacts.
4. Refresh `CONTEXT.md`, `reports/final_status.md`, and Human Brief.
5. Validate tests, ruff, OpenSpec, leak scan, and whitespace.

Rollback is git revert of this phase because all public data changes are committed artifacts.
