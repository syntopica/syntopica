# TODO

## Onboarding

- [ ] `atrium` is not covered by the `smoke` CI job: its doctor needs a
  conversation archive the runner does not have. Smallest next step: have the
  job run `conversations:export` from the `agents` checkout against a fixture
  transcript, then `syntopica doctor` with `--with brain,atrium`.
- [ ] `clipper` and `capture` stay "advanced, fork required": the extension
  hard-codes the owner's repository, GitHub App client id and capture origin.
  Smallest next step: make those three values extension options with no
  default, then add `clipper` to the component menu.
- [ ] The Claude Code plugin route starts atrium as `atrium-mcp` from the PATH
  and cannot know the data directory. Smallest next step: measure whether
  `/plugin install` users actually reach a working `atrium_context` without the
  CLI, and if not, drop `.mcp.json` from the plugin and point the route at
  `syntopica client claude`.
- [ ] **Stranger test of the public onboarding, 2026-09-16** (`docs/stranger-test-2026-09-16.md`,
      Codex from a clean clone). Fixed the same night: the README CLI block now clones brain
      first and is verified brain-only. Still open, ranked there: F2 AGENTS.md stops at
      `syntopica doctor` because a fresh atrium fails `archive` and `refresh` before any page
      exists (move first-page creation ahead, explain the unconfigured state); F4 `clips.sh`
      loses the caller's instance (`pnpm --dir` moves cwd; pass `--data`); F5 `ingest --dry-run`
      needs `origin` and `HEAD`; F8 `syntopica client` reports success without checking the
      client's exit status; F9 the user-wide writes of `client` are undisclosed; F10 lint does
      not enforce frontmatter or filenames; F11 brain-only doctor still demands Node and pnpm;
      F13 the generated index footer names an inbox that does not exist. Brain-side: a
      brain-only instance still needs a `clips/` directory because the schema default archive
      must exist.
