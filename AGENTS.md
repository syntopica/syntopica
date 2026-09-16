# Setting up Syntopica for the person you are helping

You are an agent that has been given this repository's URL. Follow the steps
below in order. Each step names the command and the result that means it
worked; if the result does not appear, stop, show the person the exact output,
and do not continue.

## What Syntopica is

A personal wiki that an agent maintains and a person owns: synthesized,
cross-linked Markdown pages in a data directory the person controls. The
engines are public; the data stays in that directory and is never sent
anywhere by this setup.

## Components

| component | what the person gets | needs |
| --- | --- | --- |
| `brain` | the wiki engine: index, link graph, lint, doctor | git, uv, Python 3.12+ |
| `clips` | capture web pages and newsletters and turn them into cited wiki pages | `brain`; Node 22+, pnpm; a model transport the person configures later |
| `atrium` | retrieval over the person's own agent conversation history, served to you over MCP | Node 22+, pnpm (for the conversation export) |

If the person did not say which components they want, ask once. The default
is `brain` alone. Advanced components not covered here: `clipper` (a Chrome
extension that commits pages to a GitHub inbox) and `capture` (a phone URL
inbox on Cloudflare Workers); both need a fork and a deployment of their own.
See https://github.com/syntopica/clipper and https://github.com/syntopica/capture.

## Steps

### 1. Install the hub CLI

```bash
uv tool install git+https://github.com/syntopica/syntopica
syntopica --version
```

Result: `syntopica 0.x.y`. If `uv` is missing, install it first:
https://docs.astral.sh/uv/getting-started/installation/.

### 2. Create the data directory

Pick a directory the person will own, for example `~/wiki`. Do not put it
inside another Git repository.

```bash
mkdir -p ~/wiki/engines && cd ~/wiki
```

### 3. Clone and install the engines the components need

Always:

```bash
git clone https://github.com/syntopica/brain.git engines/brain
(cd engines/brain && uv sync)
```

With `clips`:

```bash
git clone https://github.com/syntopica/clips.git engines/clips
(cd engines/clips && pnpm install)
```

With `atrium`:

```bash
git clone https://github.com/syntopica/atrium.git engines/atrium
(cd engines/atrium && uv sync --extra mcp)
git clone https://github.com/syntopica/agents.git engines/agents
(cd engines/agents && pnpm install)
```

Result: each command exits 0. Nothing is installed on the PATH; every engine
runs from its checkout.

### 4. Write the configuration

```bash
syntopica init --with brain            # or: brain,clips  /  brain,atrium  /  brain,clips,atrium
```

Result: `wrote .../syntopica.config.json for ...` and `next: syntopica doctor`.
`init` validates the file against the engine's schema before writing, creates
the page and state directories, and makes the directory a Git repository if
it was not one.

### 5. Verify

```bash
syntopica doctor
```

Result: a `PASS` line for every selected engine under `== summary ==` and exit
code 0. A `FAIL` line means stop: quote it to the person verbatim.

### 6. Connect the agent

```bash
syntopica client claude     # or: syntopica client codex
```

Result: `installed skill at ...`, and with `atrium`, `registered mcp server
atrium`. Then tell the person to restart their agent session: a running
session does not see new skills or servers.

Claude Code alternative, no CLI needed for this step: `/plugin marketplace add
syntopica/syntopica` then `/plugin install syntopica@syntopica`. That route
starts atrium as `atrium-mcp` from the PATH, so it needs
`uv tool install "git+https://github.com/syntopica/atrium#egg=atrium[mcp]"`
as well, and resolves the instance from `SYNTOPICA_DATA` or the working
directory.

### 7. First page

Read `engines/brain/SCHEMA.md`, write one page under `pages/`, then:

```bash
engines/brain/bin/brain index
```

Result: `index.md` lists the page. The person now has a working wiki.

## Later

- Update: `git pull` in each `engines/*` checkout, then `uv tool upgrade syntopica`.
- Health: `syntopica doctor` at any time.
- The `syntopica` skill you installed tells a session how to query, write,
  ingest and maintain the wiki.
