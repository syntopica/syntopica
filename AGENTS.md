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
is `brain` alone.

Two optional pieces live outside this menu because they are not engines:

- **clipper**, a Chrome extension that commits pages to a GitHub inbox
  repository the person owns. No fork needed: clone
  https://github.com/syntopica/clipper, `pnpm install && pnpm build`, load
  `dist/` unpacked, then fill its options page with the inbox repository, and
  the client id of a GitHub App the person registers and installs on that
  repository alone. Its capture-service fields stay empty unless they deploy
  the next one.
- **capture**, a phone URL inbox on Cloudflare Workers
  (https://github.com/syntopica/capture). This one is a deployment of their
  own; point the clipper at its origin afterwards.

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
uv tool install "git+https://github.com/syntopica/atrium#egg=atrium[mcp]"
```

Result: each command exits 0. brain and clips install nothing on the PATH and
run from their checkouts. atrium is the exception: its own doctor requires the
`atrium` command to be reachable from a plain login shell, because the agent
guidance and the Claude Code plugin both call it by name, and an instance whose
CLI existed only inside a checkout's virtualenv answered `command not found` to
every session that followed the guidance.

### 4. Write the configuration

```bash
syntopica init --with brain            # or: brain,clips  /  brain,atrium  /  brain,clips,atrium
```

Result: `wrote .../syntopica.config.json for ...` and `next: syntopica doctor`.
`init` validates the file against the engine's schema before writing, creates
the page and state directories, and makes the directory a Git repository if
it was not one.

### 5. First page

Read `engines/brain/SCHEMA.md`, write one page under `pages/`, then:

```bash
engines/brain/bin/brain index
engines/brain/bin/brain lint
```

Result: `index.md` lists the page and lint reports `0 issues`. The person now
has a working wiki. This comes before the service checks because it is the
part that has to work; everything below is optional wiring.

### 6. Fill the conversation index, with `atrium`

Atrium indexes a canonical archive that the `agents` engine exports; it never
reads a provider's transcripts itself. Export, then index:

```bash
data="$PWD"
(cd engines/agents && pnpm conversations:export --output "$data/conversations/archive.jsonl" --source claude-code)
uv run --project engines/atrium atrium ingest "$data/conversations/archive.jsonl"
```

Result: the export prints `"ok": true` with a record count, and the ingest
prints how many conversations became records. The ingest also records the
refresh the doctor asks about, so both of its staleness checks turn green.
`--source` takes any supported client (`claude-code`, `codex`, `cursor`, ...)
and may be repeated; `pnpm conversations:export --help` lists them. Until this
runs, atrium's doctor reports the archive and the refresh as absent, which is
honest: there is nothing to retrieve yet.

### 7. Verify

```bash
syntopica doctor
```

Result: a `PASS` line for every selected engine under `== summary ==` and exit
code 0. A `FAIL` line means stop: quote it to the person verbatim.

One state is not a failure and must not be reported as one:

- **A new clips instance** reports `ingest: publication not configured yet`,
  because ingestion ends in a fast-forward push and the hub creates neither a
  commit nor a remote. Capture, `clips status` and `clips ingest --dry-run`
  work without one; configure the private destinations deliberately, later.

### 8. Connect the agent

This step is optional and writes **outside** the wiki, so say what it does
before running it:

- Claude receives `~/.claude/skills/syntopica` and a user-scoped atrium entry in
  `~/.claude.json`, available from every project.
- Codex receives `~/.codex/skills/syntopica` and an atrium entry in its own
  configuration, normally `~/.codex/config.toml`.
- Both entries store absolute paths to this wiki and its atrium checkout.
- An existing skill directory that the hub did not write is refused; one it did
  write is replaced in full, local edits included. Back those up first.

```bash
syntopica client claude     # or: syntopica client codex
```

Result: `installed skill at ...`, and with `atrium`, `registered mcp server
atrium`, printed only after the hub reads the registration back and finds this
wiki's path in it. An atrium server registered for another instance is refused
with a message rather than overwritten. Then tell the person to restart their
agent session: a running session does not see new skills or servers.

Claude Code alternative for the skill alone: `/plugin marketplace add
syntopica/syntopica` then `/plugin install syntopica@syntopica`. The plugin
ships the skill and no MCP server: a plugin server has no way to name the data
directory, so it would resolve the instance from the session's working
directory and answer from nothing in every project that is not the wiki
itself. Register the server with `syntopica client claude`, which writes this
wiki's absolute path into the entry.

With atrium and Claude Code, also register the session recorder: it makes the
session write its own memory record when enough work has accumulated, on the
account the person already pays for, so no batch synthesis lane is needed. Add
to `hooks.Stop` in `~/.claude/settings.json` (paths absolute; `SYNTOPICA_DATA`
is the data directory from step 2):

```json
{"matcher": "*", "hooks": [{"type": "command", "timeout": 30,
  "command": "SYNTOPICA_DATA=/abs/path/to/data sh /abs/path/to/engines/atrium/hooks/claude-code/stop-record-episode.sh"}]}
```

Result: after a long turn Claude Code refuses to stop once and asks the model
to run `atrium record-session --checkpoint <id>`; the record lands in
`<data>/atrium/synthesis/records/`. How it decides and what it refuses:
`engines/atrium/docs/designs/session-producer.md`.

## Later

- Update: `git pull` in each `engines/*` checkout, then `uv tool upgrade syntopica`.
- Health: `syntopica doctor` at any time.
- The `syntopica` skill you installed tells a session how to query, write,
  ingest and maintain the wiki.
