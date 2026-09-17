# Syntopica

A personal wiki that an agent maintains and a person owns: synthesized,
cross-linked Markdown pages that people can read and edit, and agents use as
context. The engines are public; your data stays in a directory you control.

- **brain** builds the index and link graph, lints pages, and diagnoses the instance.
- **clips** captures web pages and newsletters and turns them into cited pages.
- **atrium** serves retrieval over your own agent conversation history **and over
  the wiki's pages**, over MCP. It is also where semantic search comes from: brain
  holds no embeddings, so a brain-only instance searches by words (`brain find`)
  and will not find a paraphrase. `brain doctor` says which of the two you have.

## Set it up with your agent

Paste this to Claude Code or Codex:

> Set up Syntopica for me by following https://github.com/syntopica/syntopica/blob/main/AGENTS.md

It will ask which components you want, install them, verify every engine with
`syntopica doctor`, and connect itself. `AGENTS.md` is the whole procedure; you
can follow it by hand too. With atrium and Claude Code it also registers the
session recorder, the hook that makes each session write its own memory
record on your existing subscription: no second account, no batch job.

## The hub CLI

Start with brain alone: a local Markdown wiki, an index, an offline link graph
and keyword search over the pages, in one directory you own -- semantic search
arrives with atrium, not before. You need Git, uv and Python 3.12 or newer.
Installing the hub does not clone the engines; `init` expects them under
`engines/` and tells you which one is missing.

```bash
uv tool install git+https://github.com/syntopica/syntopica
mkdir -p wiki/engines && cd wiki
git clone https://github.com/syntopica/brain.git engines/brain
(cd engines/brain && uv sync)
syntopica init --with brain          # write syntopica.config.json, create the paths, git init
cat > pages/start.md <<'PAGE'
---
title: Start
type: concept
updated: 2026-09-16
summary: 'The starting point for this wiki.'
sources: []
---

Decisions live in [[pages/decisions]].
PAGE
cat > pages/decisions.md <<'PAGE'
---
title: Decisions
type: concept
updated: 2026-09-16
summary: 'Decisions recorded as linked pages.'
sources: []
---

Back to [[pages/start]].
PAGE
engines/brain/bin/brain index        # index.md from the pages
engines/brain/bin/brain graph        # graph.html, orphans, dangling links
engines/brain/bin/brain lint         # frontmatter, filenames, summaries, links
syntopica doctor                     # every selected engine's doctor
```

Expect `index.md: 2 pages`, `pages 2  links 2  orphans 0`, `lint: 2 pages, 0
issues` and `PASS brain doctor`. Links carry the page directory, as in
`[[pages/decisions]]`.

Add clips and atrium afterwards by cloning them under `engines/` and following
`AGENTS.md`; each needs more than a clone (clips a publishable Git remote,
atrium an exported conversation archive), and `syntopica doctor` says so.
`syntopica client claude` (or `codex`) is optional and writes outside the wiki:
it installs the skill under `~/.claude/skills/syntopica` (or
`~/.codex/skills/syntopica`) and registers the atrium MCP server in that
client's user configuration, with absolute paths to this wiki and its atrium
checkout, so the server is offered in every project. A skill directory the hub
did not write is refused; one it did write is replaced in full, local edits
included. The success line is printed only after the hub reads the registration
back, and an atrium server already registered for another instance stops the
command instead of being overwritten.

## Repositories

[brain](https://github.com/syntopica/brain) ·
[clips](https://github.com/syntopica/clips) ·
[atrium](https://github.com/syntopica/atrium) ·
[agents](https://github.com/syntopica/agents) ·
[test-data](https://github.com/syntopica/test-data)

MIT. See `LICENSE`.
