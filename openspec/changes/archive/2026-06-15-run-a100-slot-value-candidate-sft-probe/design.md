# Design: A100 slot value candidate SFT probe

## Context

The candidate probe manifest and configs are committed:

- `data/public-samples/manifest_slot_value_candidate_probe.json`
- `configs/sft-a100-slot-value-candidate-probe.json`
- `configs/sft-a100-slot-value-candidate-probe-prediction.json`

Current remote preflight shows SSH and approved root are available, GPUs 3-7 are
idle candidates, and the default remote Python environment has `torch`,
`transformers`, `peft`, and `accelerate`, but lacks `trl` and `datasets`.

## Decisions

1. Use a phase-specific remote workspace under the approved private A100 root.
   - Rationale: avoids mutating the existing remote project checkout and keeps
     all writes inside the approved root.
   - Example public-safe label: `<a100_candidate_probe_workspace>`.

2. Use a private remote dependency environment.
   - Rationale: installing `trl` and `datasets` into the default environment may
     affect other work. A venv or equivalent project-local environment keeps the
     change isolated.
   - Pip/cache directories must be under the approved private A100 root.

3. Keep committed configs as templates and generate private overrides only on
   A100.
   - Rationale: committed files must preserve `<a100_project_root>` placeholders.
     Resolved paths are private runtime details.

4. Treat training success as candidate learnability evidence only.
   - Rationale: the run uses 12 train rows from a standalone candidate dataset.
     Even a perfect train-split result does not prove held-out generalization or
     production readiness.

5. Preserve blocked/failed evidence.
   - Rationale: environment, package, model, GPU, or training failures are useful
     evidence if recorded with public-safe reason codes and without raw logs.

## Risks / Trade-offs

- **Risk:** Dependency install writes outside the approved root.
  **Mitigation:** set venv, pip cache, HF/model caches, and temp/cache dirs under
  the approved private A100 root; stop if this cannot be enforced.
- **Risk:** Real training artifacts leak into git.
  **Mitigation:** import only sanitized metadata/report files; never copy adapter
  or checkpoint directories.
- **Risk:** Candidate train-split success is overstated.
  **Mitigation:** reports and Human Briefs state `generalization_claim=false` and
  keep held-out/dev/test claims false.
- **Risk:** GPU placement interferes with other users.
  **Mitigation:** re-run `nvidia-smi`, choose an idle GPU explicitly, and stop if
  safe placement is unclear.

## Validation Plan

1. Add tests for public-safe observed/blocked A100 candidate probe report shape.
2. Run remote preflight immediately before any GPU work.
3. Run focused tests, full pytest, public sample validation, leak scan,
   `openspec validate --all --strict`, and `git diff --check`.
4. Generate a Chinese Human Brief summarizing observed or blocked status.
