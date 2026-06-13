## Context

The previous A100 7B public-sample train rerun fixed the compact public-readonly search/weather train rows, but left the three `extract-price` train rows as strict exact-match failures. The observed failures are narrow and contract-shaped:

- one row predicts `extract_page` but writes the target into `slots.query`/`page_url` and uses a longer normalized phrase;
- one paraphrase falls back to public web search for a price-like request;
- one row predicts `extract_page` with `slots.query="价格"` and a non-canonical normalized phrase.

The existing public sample is intentionally small. This phase should test whether making the exact extract-price contract policy explicit can repair the residual before expanding to private data, DPO training, or broader benchmark claims.

## Goals / Non-Goals

**Goals:**
- Encode the current public extract-price/read-page target as a stable contract policy in data and prompts.
- Generate extract-specific hard negatives that reject search fallback and query/page-url slot shapes.
- Regenerate synchronized public SFT, DPO, and manifest artifacts.
- Run one bounded 7B A100 public-sample train rerun and evaluate strict train-split metrics.
- Preserve compact-query recovery while checking whether all extract-price train rows become strict exact matches.
- Publish sanitized evidence and a concise Chinese Human Brief with conservative claim boundaries.

**Non-Goals:**
- No full private corpus training, DPO training, GRPO, dev/test generalization claim, production-readiness claim, live-browser benchmark claim, checkpoint release, adapter release, parser relaxation, evaluator relaxation, semantic-equivalence scoring as a primary metric, prediction repair, prediction replacement, or public full-corpus release.

## Decisions

1. **Fix the extract-price contract policy before adding more data.**
   - Rationale: the residual pattern is consistent: the model confuses current-page price extraction with search or a generic query slot. More data may help later, but the smallest useful test is to remove this contract ambiguity first.
   - Alternative considered: immediately train on the larger private corpus. Rejected because it would mix target-policy repair with data-volume effects and make the result harder to interpret.

2. **Use extract-specific DPO hard negatives, but do not run DPO training in this phase.**
   - Rationale: SFT sees the canonical target, while DPO artifacts record the wrong output families for later preference tuning and dataset validation. Running DPO now would broaden the phase and make a small SFT repair harder to attribute.
   - Alternative considered: run SFT plus DPO. Rejected as too broad for a residual repair phase.

3. **Expose extract policy in shared prompts without leaking row-specific gold targets.**
   - Rationale: the prompt can state the generic rule and use `商品价格` as a public category example, but prediction prompts still must not include hidden row-specific gold contract values that are not already present in the input or policy text.
   - Alternative considered: include the exact gold contract as an example. Rejected because it would contaminate prediction prompts.

4. **Treat strict exact match as the success gate.**
   - Rationale: the residual is about exact `task_type`, `route`, `slots`, and `normalized_command` output. Soft slot F1 remains explanatory only.
   - Alternative considered: mark “页面上的价格” equivalent to “商品价格”. Rejected because it would relax the evaluator rather than proving the model learned the contract target.

5. **Use the same bounded 7B train-split rerun pattern as the archived compact-query phase.**
   - Rationale: keeping model size, split, and evidence structure consistent isolates the new variable to extract-policy repair.

## Risks / Trade-offs

- **Risk: the tiny public sample overfits and still says nothing about held-out data.** -> Mitigation: label the result as train-split/public-sample diagnostic evidence only.
- **Risk: prompt examples accidentally leak exact row targets.** -> Mitigation: add tests that prediction prompts do not include full gold contracts and keep policy text generic to the public category.
- **Risk: DPO hard negatives apply to the wrong task family.** -> Mitigation: gate extract-specific negatives on public-safe `extract`/`extract_page` rows with a target slot.
- **Risk: rerun still fails strict exact match.** -> Mitigation: preserve row-level residual evidence and stop before broadening to private corpus or DPO.
- **Risk: A100 runtime artifacts leak into git.** -> Mitigation: copy back only sanitized predictions, metadata, sidecars, metrics, manifests, reports, and leak scans.

## Migration Plan

1. Add focused tests for extract-specific prompt visibility, DPO hard negatives, validation, and public sample synchronization.
2. Implement minimal dataset, DPO, and formatting changes.
3. Regenerate public-sample SFT/DPO/manifest artifacts.
4. Prepare public-safe A100 7B rerun templates.
5. Inspect A100 GPU occupancy, select an idle GPU, train/predict under `<a100_project_root>`, and copy back sanitized evidence only.
6. Generate strict metrics, residual diagnosis, report, manifest, leak scan, and Chinese Human Brief.
7. Run full local validation and archive only after the evidence is complete.

## Open Questions

- None for this phase. If extract-price remains a residual after this bounded rerun, the next phase should decide between broader data coverage, DPO training, or a deeper target ontology redesign.
