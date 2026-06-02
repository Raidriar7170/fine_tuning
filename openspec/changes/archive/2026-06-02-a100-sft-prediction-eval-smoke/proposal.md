## Why

The A100 public-sample SFT smoke proved that the real Transformers + PEFT + TRL training path can execute once, but the public evidence still has no sanitized predictions from the trained adapter. This change adds a bounded prediction/evaluation smoke so reviewers can see and score trained-path public-sample prediction rows without publishing checkpoints, adapters, raw remote logs, or private infrastructure details.

## What Changes

- Add an explicit, public-safe prediction export workflow for the completed A100 public-sample SFT adapter path.
- Add sanitized public-sample prediction artifacts that contain only row identifiers, prediction values, and evaluation-safe metadata.
- Run contract ladder metrics and controlled execution smoke against the trained-path public predictions.
- Publish a machine-readable manifest and human-readable report under `reports/public-sample/` with release status, claim boundaries, leak-scan status, metrics links, and controlled smoke status.
- Add validation and leak-scan coverage so evidence rejects raw private rows, local absolute paths, private IPs, SSH details, secrets/tokens, raw logs, checkpoints, adapters, caches, and oversized generated corpora.
- Non-goals: generic chat fine-tuning, Hermes-style skill routing, GUI action policy learning, first-phase GRPO/rule reward training, publishing the full local/private corpus, publishing model checkpoints/adapters, or claiming live-browser benchmark improvement before controlled evidence exists.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `supervised-contract-tuning`: require a bounded, explicit trained-adapter public-sample prediction export path after the A100 SFT smoke.
- `contract-evaluation`: require a public-safe prediction evidence pack with trained-path contract metrics, controlled smoke status, and leak-scan validation.

## Impact

- Affects SFT prediction/export code, evaluation/report CLI surfaces, public evidence manifests, report templates, README/runbook wording, and tests around trained-path evidence validation.
- Uses the existing Transformers + PEFT + TRL stack and the previously completed private A100 smoke artifacts; dependency expansion should be avoided unless the prediction path exposes a concrete missing dependency.
- Requires A100-side execution only for the private adapter prediction step. All generated remote files must stay under the approved private A100 project root, and only sanitized predictions, metrics, manifests, and summary reports may be copied into the repo.
