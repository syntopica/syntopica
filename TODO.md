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
