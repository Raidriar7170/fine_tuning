## Context

The archived `evaluate-a100-public-heldout-contract-generalization` evidence showed strict public held-out failure: both `dev` and `test` had `json_valid_rate=1.0`, `contract_exact_match=0.0`, and `slot_f1=0.0`. The residuals are not schema-format failures. They are contract-policy failures for task families that were underrepresented in the public train split: navigation canonical URL/command, ambiguous clarify, confirmation-required form fill, and unsafe payment blocking.

The current public train split mainly covers search/weather and extract-price rows. Training directly on the existing `dev`/`test` rows would invalidate held-out interpretation, so this phase adds distinct public-safe train repair exemplars for the same contract families while preserving the original public `dev`/`test` rows as evaluation rows.

## Goals / Non-Goals

**Goals:**

- Add a small number of public-safe train repair seed traces for navigate, clarify, form-fill confirmation, and unsafe payment blocking.
- Add task-family-specific prompt policy so SFT training text and prediction prompts expose the expected contract shapes without row-specific gold targets.
- Add dedicated DPO hard negatives and validation rules for the observed held-out drifts.
- Regenerate public sample artifacts and run an A100 SFT rerun on the expanded train split.
- Evaluate the rerun on public `dev` and `test` and publish split-specific, public-safe evidence.

**Non-Goals:**

- Do not train on the existing public `dev`/`test` target rows.
- Do not relax, normalize, repair, replace, or re-score predictions.
- Do not run private full-corpus evaluation.
- Do not claim private-corpus generalization, production readiness, checkpoint release, adapter release, public full-corpus release, or live-browser benchmark improvement.
- Do not introduce generic chat fine-tuning, skill routing, GUI action policy learning, or first-phase GRPO.

## Decisions

1. Add train repair exemplars instead of moving held-out rows into train.

   This preserves the original held-out rows as evaluation evidence. The new train rows should be same-family but not duplicate the exact held-out inputs, normalized commands, or slot values.

2. Use prompt-policy visibility plus data/DPO reinforcement.

   Prior phases fixed individual task families with explicit policy wording and hard negatives. The same pattern is appropriate here because the failures are schema-valid but contract-wrong.

3. Keep A100 execution SFT-only for this small phase unless local evidence requires DPO.

   The immediate evidence question is whether expanded train coverage plus prompt policy recovers public `dev`/`test` strict behavior. DPO categories are still generated and validated so a later preference phase can use them without reworking data semantics.

4. Preserve split-specific reporting.

   The final report must keep train, dev, and test metrics separate. A train recovery is useful only as a sanity check; dev/test metrics remain the primary evidence for this phase.

## Risks / Trade-offs

- Public dataset remains very small -> Mitigation: report row counts and avoid broad generalization claims.
- Added train exemplars may overfit to a narrow synthetic public sample -> Mitigation: evaluate only as public-sample evidence and keep private-corpus claims false.
- Prompt policy may leak too much if it includes row-specific gold targets -> Mitigation: tests must prove prediction prompts include policy examples only, not held-out gold contracts or exact train repair target strings except allowed generic examples.
- A100 run may fail or GPUs may be busy -> Mitigation: inspect occupancy, select one idle GPU with `CUDA_VISIBLE_DEVICES`, keep all remote writes under the approved private root, and stop if safe placement is unclear.
