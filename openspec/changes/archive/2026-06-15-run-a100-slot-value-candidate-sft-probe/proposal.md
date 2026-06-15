# Run A100 slot value candidate SFT probe

## Why

The previous phase proved that the candidate-only manifest selects the 12
reviewed slot value SFT rows and refreshed A100 preflight evidence. It could not
launch real SFT because the default remote Python environment was missing
`trl` and `datasets`.

To determine whether the candidate rows are learnable before merging them into
the formal public sample, we need one bounded A100 execution phase that prepares
a private training environment under the approved A100 project root and attempts
the 7B candidate-only SFT probe.

## What Changes

- Prepare a private remote execution workspace under the approved A100 project root.
- Install or locate train dependencies without writing project files, caches, or
  outputs outside the approved root.
- Run the candidate-only 7B SFT probe when GPU placement and dependencies are
  safe.
- If training succeeds, optionally run train-split candidate prediction using
  the produced private adapter.
- Import only sanitized metadata/evidence into git.
- Record blocked/failed status honestly if dependency installation, GPU
  placement, model loading, training, or prediction cannot complete.

## Non-Goals

- No merge of candidate rows into `seed_traces.jsonl` or the formal public
  sample.
- No DPO/GRPO.
- No held-out dev/test claim.
- No evaluator relaxation or promotion of soft slot F1 / semantic equivalence.
- No checkpoint, adapter, raw log, model cache, private override, host detail,
  SSH detail, token, or private path committed to git.

## Success Criteria

- A public-safe evidence pack records one of:
  - real candidate-only SFT completed on A100 and, if available, train-split
    prediction status; or
  - a precise blocked/failed status with sanitized reason.
- All committed paths and specs pass leak scan and `openspec validate --all
  --strict`.
- The Human Brief states whether this is learnability evidence, blocked
  evidence, or failure evidence, and explicitly avoids held-out/generalization
  claims.
