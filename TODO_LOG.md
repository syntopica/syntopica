# Closed work

<!-- tadu:log v1 since 2026-10-12 -->

## 2026

### October

- 2026-10-11 [-] **Model identifiers in `syntopica.config.json`.** Decided:
  the transport is the configuration boundary; model ids stay constants under
  `clips/src/models/`, and the claim that they are configuration stays retired.
  Reasons: each constant records measured choices (quota pool, zero data
  retention, family independence from the author), the author/verifier guard
  compares model ids directly (`clips/src/grade/agy-tiers-of-model.ts`), and the
  worker transport already takes its model from the instance's `worker/`
  directory or `CLIPS_WORKER_MODEL`. The 2026-10-04 failure, when agy stopped
  listing a pinned id, is an availability cost of code-pinned ids but not worth
  an arbitrary-id surface the guard would have to re-verify. Adjudicated by
  Codex (read-only, schema-bound): keep-transport-granularity, confidence
  high; claims checked against `schema/syntopica-config.schema.json` in brain,
  the clips README and the guard source.

### 2026-10

- [x] 2026-10-22 — **Security:** **Security: update the locked certifi trust bundle.** The lockfile candidate updates only certifi from 2026.7.22 to the patched 2026.10.19 release for GHSA-6q48-6c7w-9gw2. Next: verify the exact locked candidate in an isolated environment and complete the required source gates. Installed instances require separate verification; source acceptance does not establish their runtime state.
  - Result: Update only the certifi lock record from 2026.7.22 to 2026.10.19. Installed instances and external onboarding smokes remain separate verification boundaries.
  - Evidence: Isolated Python 3.13.16 uv lock --check and locked wheel-only all-extras/all-groups setup passed; 51 installed distributions match the lock. python -m pytest -q passed 50 tests with one existing configuration-dependent skip; codeality-py gate --json passed all seven required stages including pip-audit and 93-percent coverage against the unchanged 65-percent requirement. All 65 tracked files, symlink/modes and installed dependencies remained unchanged; independent parsed lock comparison changed only certifi.
