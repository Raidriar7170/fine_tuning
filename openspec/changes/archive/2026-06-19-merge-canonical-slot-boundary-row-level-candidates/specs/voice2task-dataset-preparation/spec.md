## ADDED Requirements

### Requirement: Merge canonical slot-boundary candidates into formal public sample
The system SHALL support a guarded formal merge of reviewed canonical
slot-boundary row-level candidate seeds into the committed public sample while
preserving provenance, train-only split labels, derived artifact
synchronization, and comparison-boundary warnings.

#### Scenario: Promote reviewed canonical slot-boundary candidates exactly once
- **WHEN** the merge command runs with the current formal public seed file and
  `data/public-samples/canonical_slot_boundary_seed_candidates.jsonl`
- **THEN** it MUST validate exactly the reviewed seven canonical slot-boundary
  candidate seed rows
- **AND** it MUST reject missing, extra, duplicate, already-formal, unreviewed,
  non-public-safe, or non-standalone candidate rows before rewriting formal
  public sample artifacts
- **AND** each promoted seed MUST use
  `source_mode="canonical_slot_boundary_formal_public_seed"`,
  `candidate_status="formal_public_sample"`, and a source reference to the
  candidate seed artifact
- **AND** each promoted seed MUST preserve `split="train"`.

#### Scenario: Rebuild synchronized canonical formal artifacts
- **WHEN** canonical slot-boundary candidates are promoted into the formal
  public sample
- **THEN** the system MUST rebuild `seed_traces.jsonl`,
  `sft_public_sample.jsonl`, `dpo_public_sample.jsonl`, and
  `manifest_public_sample.json` from the updated formal seed file
- **AND** the rebuilt manifest MUST record canonical slot-boundary candidate
  seed and SFT counts, eligible source class counts, train-only split counts,
  and comparison-boundary warnings
- **AND** the derived artifacts MUST validate through the public dataset
  validator.

#### Scenario: Publish canonical merge evidence
- **WHEN** the canonical slot-boundary formal merge completes
- **THEN** the system MUST publish JSON, Markdown, manifest, and leak-scan
  evidence under `reports/public-sample/canonical-slot-boundary-formal-merge/`
- **AND** the evidence MUST record pre-merge counts, post-merge counts,
  candidate source identity, candidate seed/SFT/DPO contributions,
  validation status, execution scope, claim boundaries, and comparison-boundary
  warnings.

#### Scenario: Preserve comparison and claim boundaries
- **WHEN** merge evidence, reports, manifests, tests, or Human Briefs describe
  the canonical formal merge
- **THEN** they MUST state that the formal public sample boundary changed and
  old metrics are not directly comparable
- **AND** they MUST state that strict `contract_exact_match`, strict
  `slot_f1`, and the contract evaluation ladder remain authoritative
- **AND** they MUST state that `slot_f1_soft` is diagnostic-only
- **AND** they MUST NOT claim held-out recovery, model quality improvement,
  safety improvement, model recovery, checkpoint release, adapter release,
  production readiness, private-corpus generalization, public full-corpus
  release, or live-browser benchmark improvement
- **AND** they MUST state `training_run=false`, `prediction_run=false`,
  `a100_execution=false`, `prompt_change=false`,
  `postprocessor_implementation=false`, and
  `evaluator_metric_change=false`.
