## ADDED Requirements

### Requirement: Validate recovered slot analysis inputs
The system SHALL validate that slot mechanism analysis uses only the recovered metric-reproduced step-matched inputs and SHALL fail closed when the boundary is invalid.

#### Scenario: Accepted recovered inputs
- **WHEN** the analyzer is run against `reports/public-sample/step-matched-canonical-slot-ablation/raw-inputs/`
- **THEN** it MUST confirm `projection_inputs_ready=true`, metric reproduction status is accepted, Control/Treatment/Gold sample ids match by split, dev/test boundaries match the latest step-matched experiment, prediction contracts are recovered per-sample contracts, and no superseded adapter outputs are used
- **AND** it MUST continue without reading raw model outputs as analysis authority

#### Scenario: Invalid recovered boundary
- **WHEN** required files are missing, blocked input exists, sample ids diverge, metric reproduction is not accepted, or source provenance is invalid
- **THEN** the analyzer MUST write `blocked.json` with `decision=ANALYSIS_BLOCKED_INVALID_INPUT`
- **AND** it MUST NOT write success summaries, representation decisions, or downstream recommendations

### Requirement: Classify slot-level error mechanisms deterministically
The system SHALL align gold and predicted slots by sample id and stable slot path, then assign deterministic slot error mechanism labels without repairing predictions.

#### Scenario: Slot path alignment
- **WHEN** gold and prediction slot objects contain nested objects, arrays, missing keys, extra keys, or alias-key candidates
- **THEN** the analyzer MUST flatten nested values to stable paths, align identical paths directly, record missing and extra slot keys separately, and record alias-key candidates without converting them into matches

#### Scenario: Error taxonomy assignment
- **WHEN** a gold slot and its aligned prediction value are compared
- **THEN** the analyzer MUST assign one primary mechanism from the bounded taxonomy and MAY attach secondary tags
- **AND** it MUST distinguish exact match, deterministic normalized match, missing key, extra key, alias-key candidate, semantic wrong key, partial span, wrong entity/value, source copy failure, unsupported source value, normalization failure, derived-value failure, clarify ambiguity representation failure, multivalue structure failure, type mismatch, and unclassified failure

#### Scenario: No semantic scoring or ASR speculation
- **WHEN** the analyzer cannot prove a value from source text and deterministic rules
- **THEN** it MUST NOT use an LLM judge, embeddings, broad semantic equivalence, prediction repair, or an ASR corruption label
- **AND** it MUST use bounded source-support labels such as source absent, generation required, or unsupported analysis

### Requirement: Quantify source support and prediction provenance
The system SHALL report gold slot source-copyability and predicted value provenance with deterministic named rules.

#### Scenario: Gold source support profile
- **WHEN** each gold slot value is compared with the input transcript
- **THEN** the analyzer MUST report exact copyable, normalized copyable, typed derivable, generation required, and unsupported rates overall and by split, run role, task type, route, and slot path

#### Scenario: Prediction provenance profile
- **WHEN** each predicted slot value is compared with the input transcript and deterministic typed rules
- **THEN** the analyzer MUST report exact span, normalized span, partial span, deterministic derived, unsupported by source, non-string or complex, and unavailable labels
- **AND** unsupported-by-source MUST NOT be automatically interpreted as hallucination

### Requirement: Compare Control and Treatment slot movement
The system SHALL pair Control and Treatment outcomes on identical sample ids and slot paths to explain persistent, recovered, introduced, and changed slot errors.

#### Scenario: Paired movement labels
- **WHEN** Control and Treatment are compared for the same sample id and slot path
- **THEN** the analyzer MUST label the movement as correct in both, same-mechanism persistent error, different-mechanism persistent error, recovered by Treatment, introduced by Treatment, value changed but still wrong, slot added correctly, slot added incorrectly, slot removed correctly, or slot removed incorrectly

#### Scenario: Movement metrics
- **WHEN** paired movement analysis completes
- **THEN** the analyzer MUST report persistent error count/rate, treatment recovery count, treatment regression count, net slot movement, top persistent mechanisms, top introduced mechanisms, and task-family distribution
- **AND** it MUST state that this explains existing A/B outputs only and does not rejudge canonical treatment success

### Requirement: Recommend slot representation strategy from bounded evidence
The system SHALL aggregate task-family and slot-path profiles and select exactly one final decision label with one primary next bounded change.

#### Scenario: Representation feasibility metrics
- **WHEN** slot-path profiles are generated
- **THEN** each profile MUST include sample count, copyable rates, typed derivable rate, missing/extra key rates, wrong entity rate, partial span rate, unsupported prediction rate, treatment recovery/regression rates, recommended representation, and confidence level
- **AND** confidence level MUST be one of `HIGH`, `MEDIUM`, or `LOW` with thresholds recorded in the report

#### Scenario: Final decision and next change
- **WHEN** the report selects a final recommendation
- **THEN** it MUST choose exactly one of `COPY_OR_NORMALIZE_REPRESENTATION_JUSTIFIED`, `TASK_SLOT_SCHEMA_CONSTRAINTS_FIRST`, `TYPED_NORMALIZATION_FIRST`, `MIXED_SLOT_REPRESENTATION_REQUIRED`, `DATA_DIVERSITY_OR_GENERALIZATION_FIRST`, or `ANALYSIS_BLOCKED_OR_INCONCLUSIVE`
- **AND** it MUST write `recommended-next-change.md` with the decision label, one proposed next change id, top evidence, target slot paths/task families, scope, acceptance criteria, non-goals, metrics to watch, migration risks, and current claim boundaries
- **AND** it MUST NOT automatically execute the next change

### Requirement: Publish compact public-safe slot representation evidence
The system SHALL publish a compact, public-safe evidence bundle and design-only slot representation document without changing training, runtime, schema, evaluator, or source artifacts.

#### Scenario: Evidence bundle surface
- **WHEN** analysis succeeds
- **THEN** `reports/public-sample/slot-error-mechanism-analysis/` MUST contain at most `summary.md`, `summary.json`, `slot-error-taxonomy.md`, `slot-profile.json`, `paired-error-movement.json`, `representation-feasibility.json`, and `recommended-next-change.md`
- **AND** `blocked.json` MUST be absent unless the analysis is blocked

#### Scenario: Design-only slot representation proposal
- **WHEN** `docs/slot-representation.md` is written
- **THEN** it MUST cover current slot bottleneck evidence, taxonomy, source support results, slot-path profiles, representation boundaries, recommended internal representation, V1/ContractCoreV2 compatibility, future training-target implications, migration risk, and non-goals
- **AND** it MUST state that BrowserTaskContract V1, ContractCoreV2, current training targets, and downstream runtime remain unchanged

#### Scenario: Claim and privacy boundaries
- **WHEN** reports, docs, Human Brief HTML, or archive artifacts are prepared for commit
- **THEN** leak-scan validation MUST reject raw private rows, absolute local paths, private remote paths, host details, SSH details, tokens, secrets, raw logs, checkpoints, adapters, and caches
- **AND** the evidence MUST state that no training, prediction rerun, data mutation, evaluator relaxation, schema migration, ContractCoreV2 change, checkpoint release, adapter release, model-improvement claim, executable-quality-improvement claim, safety-readiness claim, production-readiness claim, held-out-recovery claim, or live-browser claim occurred
