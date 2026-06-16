## Context

`materialize-form-fill-remediation-cases` created 9 reviewed train-only `form_fill` remediation candidate seeds. `check-form-fill-remediation-candidate-integration` then preview-built those candidates into a report-scoped public sample with counts 86 seed rows, 240 SFT rows, 742 DPO pairs, and split counts train=102/dev=69/test=69.

The candidates remain standalone today, so future formal held-out prediction work would need either a custom preview manifest or a formal merge. This change makes the public sample boundary explicit by promoting the reviewed candidates into `data/public-samples/*`.

## Goals / Non-Goals

**Goals:**

- Promote exactly the 9 reviewed `form_fill` remediation candidates into the formal public sample train split.
- Preserve existing slot-value and family-stratified formal public sample provenance.
- Rebuild formal seed/SFT/DPO/manifest artifacts and record merge evidence.
- Make the new formal counts and DPO deltas auditable in tests and reports.

**Non-Goals:**

- No SFT/DPO/GRPO training.
- No prediction or A100 execution.
- No evaluator metric change or soft-metric promotion.
- No checkpoint, adapter, production readiness, held-out recovery, private-corpus generalization, or live-browser benchmark claim.
- No dev/test held-out mutation beyond rebuilding derived artifacts from unchanged dev/test seeds.

## Decisions

1. **Use a formal seed merge, not a custom training manifest.**
   - Rationale: the preview phase already proved builder compatibility; a formal merge creates one durable public sample boundary for later prediction-only evaluation.
   - Alternative considered: keep candidates standalone and run no-merge probes. That preserves the previous manifest but forces later evidence to explain custom data plumbing.

2. **Promote only train-split candidates.**
   - Rationale: the 9 reviewed cases are remediation data, not held-out evaluation cases. Dev/test counts stay at 69/69.
   - Alternative considered: add dev/test form-fill cases. That would change held-out semantics and belongs in a separate case-design phase.

3. **Mirror the family-stratified merge evidence pattern.**
   - Rationale: existing reports already distinguish formal public data changes from training/prediction evidence.
   - Alternative considered: rely only on `manifest_public_sample.json`. That loses phase-local claims and artifact policy evidence.

4. **Fail closed on duplicate/already-merged candidate IDs.**
   - Rationale: rerunning the merge should not silently duplicate candidates or mutate provenance twice.
   - Alternative considered: idempotent no-op merge. That would make it harder to distinguish a fresh merge from an already-mutated public sample.

## Risks / Trade-offs

- New formal manifest ID can make earlier public held-out metrics non-comparable by default -> Reports must state that later held-out predictions use the new public sample boundary.
- DPO pair count increases by 81 but this is data construction, not DPO training evidence -> Merge report and Human Brief must state this boundary.
- Existing preview tests assumed candidates were absent from formal public seed -> Update preview tests to use a formal-sample-without-form-fill fixture when checking pre-merge behavior.
- Formal public sample mutation is larger than preview-only evidence -> Keep changes scoped to reviewed train-only candidates and validate public safety.
