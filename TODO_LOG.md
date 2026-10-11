# Closed work

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
