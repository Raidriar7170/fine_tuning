## 1. Prompt Policy Coverage

- [x] 1.1 Add focused RED tests proving compact-query exact-match prompt policy visibility and gold-target exclusion in prediction prompts.
- [ ] 1.2 Add focused RED tests for the public-safe local policy hardening evidence pack.

## 2. Local Hardening Implementation

- [x] 2.1 Harden the shared SFT/prediction prompt policy so `normalized_command` and `slots.query` share the same compact query phrase and reject extra-particle/decomposed-slot variants.
- [x] 2.2 Expose machine-readable prompt constraint booleans for compact-query exact-match policy visibility.
- [x] 2.3 Generate the local policy hardening evidence JSON, Markdown report, manifest, leak scans, and Chinese Human Brief.

## 3. Validation, Review, Archive, and Integration

- [x] 3.1 Run focused tests, full `PYTHONPATH=src pytest -q`, `uv run ruff check .`, `uv run mypy src`, public data validation, DPO pair check, leak scan, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`, and `git diff --check`.
- [ ] 3.2 Run Reviewer diff review, fix any in-scope Must Fix items, and rerun required validation.
- [ ] 3.3 Archive the OpenSpec change, rerun post-archive validation and final leak scans, then apply guarded local auto integration if safe.
