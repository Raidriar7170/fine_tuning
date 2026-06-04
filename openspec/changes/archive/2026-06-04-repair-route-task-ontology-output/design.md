## Context

Voice2Task's first-phase target is speech-to-contract normalization: a Chinese spoken command or ASR transcript becomes a schema-valid Browser Task Contract. The current prompt already exposes legal `task_type` and `route` values, but the latest A100 constrained-output train-split rerun showed a remaining ontology failure: a JSON-shaped output used a domain label (`weather`) as `route`, even though the schema expects execution-channel enum values such as `search_web`.

This phase is local and bounded. It changes prompt constraints and public-safe evidence only; it does not launch private A100 execution, retrain, or repair existing predictions.

## Goals / Non-Goals

**Goals:**

- Make SFT training text and trained-adapter prediction prompts explicitly state that `route` is an execution channel from the allowed enum.
- Make domain/topic/intent examples visible enough that weather-style requests map to `task_type="search"` and `route="search_web"` with details in `slots` and `normalized_command`.
- Record evidence that the local prompt repair is ready for a later rerun but is not itself model recovery.
- Keep validation focused on prompt rendering, prompt constraint metadata, public-safe evidence, and OpenSpec requirements.

**Non-Goals:**

- No training, DPO, GRPO, private A100 prediction, checkpoint release, adapter release, public model upload, production-readiness claim, held-out generalization claim, or live-browser benchmark claim.
- No schema coercion, alias repair, fixture-mode replacement, rule-baseline replacement, or gold-contract substitution for model outputs.
- No changes to the Browser Task Contract schema enum itself.

## Decisions

1. **Repair prompt ontology before rerunning A100.**
   - Rationale: the observed `route="weather"` failure is cheaper and safer to address locally than with another remote run. A rerun before local constraints are testable would spend private infrastructure on an avoidable prompt ambiguity.
   - Alternative considered: immediately rerun A100. Rejected for this phase because it would not isolate whether the ontology instruction itself is present.

2. **Keep `route` enum unchanged.**
   - Rationale: downstream consumers already validate a fixed Browser Task Contract route enum. Adding domain-specific route values would loosen the contract and hide the original schema failure.
   - Alternative considered: accept `weather` as a route alias. Rejected because alias repair would be post-hoc coercion and would overstate model correctness.

3. **Use tests and metadata instead of manual prose only.**
   - Rationale: prompt instructions are easy to regress. Focused tests should assert the route ontology wording and summary flags in both training and prediction rendering paths.
   - Alternative considered: only update a report or Human Brief. Rejected because documentation alone would not protect future reruns.

4. **Publish local repair evidence with explicit non-claim boundaries.**
   - Rationale: this phase may improve the next prompt, but it does not prove model recovery until a later authorized rerun observes model outputs.
   - Alternative considered: label the phase as recovery. Rejected because no new trained-adapter outputs are generated in this phase.

## Risks / Trade-offs

- [Risk] Stronger prompt wording still may not make the current adapter emit schema-valid objects. -> Mitigation: report the phase as local readiness only and require a later authorized A100 rerun for model-output evidence.
- [Risk] Examples leak too much gold-contract structure into prediction prompts. -> Mitigation: use a generic canonical one-shot and route ontology examples, never row-specific gold targets.
- [Risk] Evidence wording overclaims. -> Mitigation: include non-claim boundaries in JSON/Markdown/Human Brief and run leak/overclaim-oriented tests where available.
- [Risk] Prompt gets longer. -> Mitigation: keep additions concise and focused on the known route/domain failure slice.
