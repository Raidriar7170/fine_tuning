## 1. Config And Dry-Run

- [x] 1.1 Add public-safe SFT v3 and dev/test prediction config templates for the current manifest.
- [x] 1.2 Add focused tests proving the configs use placeholders, current manifest id, and no private paths.
- [x] 1.3 Run a local SFT dry-run and record row selection under the readiness evidence directory.

## 2. Readiness Report

- [x] 2.1 Add a report writer/CLI for `form_fill` remediation SFT v3 readiness.
- [x] 2.2 Generate committed JSON/Markdown/manifest readiness evidence.
- [x] 2.3 Add focused tests for report boundaries, committed evidence, and leak safety.

## 3. Project Context

- [x] 3.1 Add a concise Chinese Human Brief under `docs/human-briefs/`.
- [x] 3.2 Refresh `CONTEXT.md` and `reports/final_status.md` so the next step is SFT v3 execution only if readiness is clean.

## 4. Validation And Archive

- [x] 4.1 Run focused tests for the new readiness evidence.
- [x] 4.2 Run full tests, ruff, OpenSpec strict validation, leak scan, and `git diff --check`.
- [x] 4.3 Archive the OpenSpec change if validation passes.
