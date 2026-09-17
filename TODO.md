# TODO

## Onboarding

- [ ] `clips` publication readiness is reported but never guided. `clips doctor`
  now says `ingest: publication not configured yet`, and the contract says the
  destination is the owner's decision; nothing tells them how to make it. Smallest
  next step: one section in the clips README naming the two repositories, what
  `origin` must point at, and the first commit.
- [ ] The stranger test's remaining findings, ranked in
  `docs/stranger-test-2026-09-16.md`: F3 (the schema's documented link syntax is
  discarded for bare `[[page]]` targets), F6 (the configured runner is not the one
  execution selects, and model names are hardcoded), F7 (the author/verifier
  separation is bypassed by pinned graders), F12 (engine READMEs assume data the
  installation does not create) and F14 (unresolved references in packaged
  guidance). All live in the engines, not here.
