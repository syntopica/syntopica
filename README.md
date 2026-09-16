# Syntopica

A personal wiki that an agent maintains and a person owns: synthesized,
cross-linked Markdown pages that people can read and edit, and agents use as
context. The engines are public; your data stays in a directory you control.

- **brain** builds the index and link graph, lints pages, and diagnoses the instance.
- **clips** captures web pages and newsletters and turns them into cited pages.
- **atrium** serves retrieval over your own agent conversation history, over MCP.

## Set it up with your agent

Paste this to Claude Code or Codex:

> Set up Syntopica for me by following https://github.com/syntopica/syntopica/blob/main/AGENTS.md

It will ask which components you want, install them, verify every engine with
`syntopica doctor`, and connect itself. `AGENTS.md` is the whole procedure; you
can follow it by hand too.

## The hub CLI

```bash
uv tool install git+https://github.com/syntopica/syntopica
syntopica init --with brain,clips,atrium   # write syntopica.config.json for the chosen components
syntopica doctor                            # run every selected engine's doctor
syntopica client claude                     # install the skill, register atrium (also: codex)
```

## Repositories

[brain](https://github.com/syntopica/brain) ·
[clips](https://github.com/syntopica/clips) ·
[atrium](https://github.com/syntopica/atrium) ·
[agents](https://github.com/syntopica/agents) ·
[test-data](https://github.com/syntopica/test-data)

MIT. See `LICENSE`.
