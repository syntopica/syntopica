# Syntopica onboarding hub

Date: 2026-09-16. Status: approved design, not yet built.

## Problem

Someone who has never used Syntopica should be able to hand one URL to their
coding agent (Claude Code or Codex) and end up with a working instance of the
components they chose, verified, and with the agent able to use them in later
sessions. Today nothing offers that:

- Each engine has a human README with its own quick start. None has an
  agent-facing contract.
- The organisation profile is prose for people, and stale: it lists `clipper`,
  `capture` and `mem` as private, while all three are public and `mem` is now
  `atrium`.
- The only skill that teaches an agent to use the wiki lives in the owner's
  private rocket-agents checkout and carries the owner's own conventions.
- There is no cross-engine `doctor`; `brain doctor`, `clips doctor` and
  `atrium doctor` run separately with different invocations.
- The configuration schema, identical in `brain` and `clips`, requires
  `engines.clips`, so a brain-only instance cannot validate.
- `clipper` hard-codes the owner's GitHub repository, GitHub App client id and
  capture origin, and `capture` is a Cloudflare Worker each user must deploy.
  Neither is installable by a stranger without a fork.

## Decisions taken with the owner

1. The entry point is a new public repository, `syntopica/syntopica`, not the
   organisation profile and not one of the engines.
2. Version one offers `brain`, `clips` and `atrium`. `capture` and `clipper`
   are named as advanced components that require a fork and a deployment of
   their own.
3. The agent-facing skill is a generic `syntopica` skill, authored in
   rocket-agents like every other skill and vendored into this repository by a
   script. The owner's private `brain` skill stays where it is.
4. Configuration is assembled by a CLI, `syntopica init --with ...`, and
   verified by `syntopica doctor`, rather than by static JSON examples that
   drift from the schema.

## What is being built

### The repository `syntopica/syntopica`

Public, MIT, Python 3.12 with uv, the same `codeality-py` gate and CI shape as
`syntopica/brain`. Layout:

```
README.md                      for people: what Syntopica is, the line to paste to an agent
AGENTS.md                      for agents: the menu, the steps, the verification
CLAUDE.md                      one line, `@AGENTS.md`
syntopica/                     the CLI package: init, doctor, client
skills/syntopica/SKILL.md      vendored from rocket-agents, never edited here
.claude-plugin/marketplace.json
.claude-plugin/plugin.json
.mcp.json                      the atrium MCP server, for the plugin route
bin/sync-skill                 copies the compiled portable skill from a rocket-agents checkout
tests/
.github/workflows/quality.yml  gate, smoke, secrets
docs/superpowers/specs/        this document
```

There is no copy of the configuration schema here. `init` and `doctor` read
`schema/syntopica-config.schema.json` from the `brain` engine checkout named in
the instance, so the hub can never disagree with the engine about what a valid
configuration is. The cost is an ordering rule, stated in `AGENTS.md`: engines
are cloned before `init` runs.

### The component menu

| component | what the person gets | requires | doctor |
| --- | --- | --- | --- |
| `brain` | the wiki engine: index, link graph, lint | git, uv, Python 3.12 | `bin/brain doctor` |
| `clips` | capture and ingest of web content into pages | `brain`; Node 22, pnpm; a model transport | `clips doctor` |
| `atrium` | retrieval over the person's own agent conversation history, served over MCP | `syntopica/agents` for the conversation export; Node 22, pnpm | `uv run atrium doctor` |

Selection is not stored anywhere new. A component is selected when its section
is present in `syntopica.config.json`: `clips` when the `clips` section and
`engines.clips` exist, `atrium` when the `atrium` and `conversations` sections
exist. `brain` is always present because the schema requires it. `doctor`
derives what to run from the file, so a hand-edited configuration and one
written by `init` are treated the same.

`capture` and `clipper` appear in `AGENTS.md` under "advanced", with one
sentence each on what they are and why they need a fork, and a link to their
repositories. Nothing in the hub installs them.

### The agent contract, `AGENTS.md`

Written for the agent that is handed the URL. It states prerequisites, then the
steps in order, each with the command and the observable result that means it
worked. The agent asks the person which components they want only if the
request did not say; the default is `brain` alone.

1. Install the hub CLI: `uv tool install git+https://github.com/syntopica/syntopica`.
   Result: `syntopica --version` prints a version.
2. Create the data directory the person will own: a new directory, `git init`,
   an `engines/` subdirectory listed in `.gitignore`.
3. Clone the selected engines into `engines/`: `brain` always; `clips` if
   selected; `atrium` and `agents` if `atrium` is selected. Run each engine's
   own install: `uv sync` for `brain`, `uv sync --extra mcp` for `atrium`,
   `pnpm install` for `clips` and `agents`. The commands are spelled out per
   engine. Nothing is installed on the PATH; every engine is run from its
   checkout, so two instances on one machine cannot share a stale binary.
4. `syntopica init --with brain[,clips][,atrium]` writes
   `syntopica.config.json` and creates the page, source, ledger and archive
   directories the configuration names. Result: the file validates against the
   engine schema, which `init` checks before writing.
5. `syntopica doctor`. Result: every selected engine reports PASS. Anything
   else stops the onboarding, and the agent reports the failing line verbatim.
6. `syntopica client claude` or `syntopica client codex` installs the skill and,
   when `atrium` is selected, registers the MCP server. The agent tells the
   person to restart their session, because a running session does not see new
   skills or servers.
7. First use: write one page following the engine's `SCHEMA.md`, run
   `bin/brain index`, and confirm `index.md` lists it.

For Claude Code the contract also names the plugin route, which needs no CLI
for the client step: `/plugin marketplace add syntopica/syntopica` then
`/plugin install syntopica@syntopica`. The plugin carries the skill and the
`.mcp.json` for atrium. It cannot know where the data directory is, so atrium
resolves it by walking up from the working directory or from `SYNTOPICA_DATA`,
exactly as the engines already do; the contract says so.

**Reversed on 2026-09-17.** Walking up from the working directory answers from
nothing in every project that is not the wiki, which is the ordinary case for a
session, and a plugin server cannot carry the absolute path that would fix it.
The plugin now ships the skill alone and the contract points the server at
`syntopica client claude`.

`README.md` for people is short: what Syntopica is, the three components in a
sentence each, and the instruction "paste this to your agent" with the
repository URL. It links to `AGENTS.md` rather than repeating it.

### The CLI

`syntopica` is a small Python package installed with `uv tool install`. Three
subcommands, one responsibility each, every helper in its own file.

`syntopica init --with <components> [--data DIR] [--engines DIR]`

- `--data` defaults to the working directory, `--engines` to `engines` inside
  it. Both are resolved and written relative to the configuration file, as the
  schema requires.
- Refuses to run if `syntopica.config.json` already exists, if `--with` names an
  unknown component, if `clips` or `atrium` are named without their
  prerequisites, or if a named engine checkout is missing. The message names
  the missing checkout and the clone command. The checkouts are `brain`,
  `clips`, `atrium` and `agents` under `--engines`, and each selected one is
  written to `engines.<name>` with `apiVersion: 1`.
- Writes the sections for the selected components with the schema defaults:
  `brain.pages = ["pages"]`, `brain.sources = "sources"`,
  `brain.index = "index.md"`, `brain.ledger = ".ingest"`; `clips.archive =
  "clips"` with `inbox` and `inboxRepositoryUrl` null; `atrium.path =
  "atrium"`; `conversations.path = "conversations"`; `runners` all null when
  clips is selected, because which model runs each stage is the person's
  decision and the clips doctor names it.
- Validates the document against the engine schema before writing, creates the
  required page, source and archive directories, and appends the state
  directories (`atrium/`, `conversations/`, `engines/`, `syntopica.local.json`)
  to `.gitignore`.
- Prints the path written and the next command, `syntopica doctor`.

`syntopica doctor [--data DIR]`

- Resolves the instance the way the engines do: `--data`, then
  `SYNTOPICA_DATA`, then an upward walk stopping at a repository boundary.
- Runs the doctor of every selected engine as a subprocess from the engine
  checkout named in `engines.<name>.path`, with `SYNTOPICA_DATA` set to the
  instance: `bin/brain doctor`, `clips.sh doctor`, and `uv run atrium doctor`
  from `engines.atrium.path`. `agents` has no doctor the hub runs; its
  presence is a path check, because it is only needed for the export.
- Prints each engine's output under a heading, then one summary line per engine
  with PASS or FAIL, and exits non-zero if any failed or any selected engine
  checkout is missing.
- Reports, without failing, whether the skill is installed for each client and
  whether the atrium MCP server is registered, by reading the locations the
  clients document (`~/.claude/skills/syntopica`, `~/.codex/skills/syntopica`,
  the `claude mcp list` and `codex mcp list` output).

`syntopica client <claude|codex> [--data DIR]`

- Copies `skills/syntopica/` from the installed package into
  `~/.claude/skills/syntopica` or `~/.codex/skills/syntopica`, replacing an
  existing copy that the hub wrote and refusing to touch one it did not (a
  marker file inside the copy records the hub version that wrote it).
- When `atrium` is selected, registers the server with the client's own
  command: `claude mcp add --scope user atrium --env SYNTOPICA_DATA=<data> --
  uv run --project <atrium checkout> atrium-mcp`, or the `codex mcp add`
  equivalent, where `atrium-mcp` is the console script the atrium checkout
  installs with its `mcp` extra and both paths are absolute. Skips
  registration if the server is already listed, and says so.
- Prints what it wrote and the reminder to restart the session.

The engine paths and the schema are read at call time from the instance, never
from a default. The only path the hub knows on its own is the client
directories, because those are the clients' documented contract.

### The skill

`syntopica` is authored in the agents repository at `src/skills/core/syntopica/SKILL.md`,
registered in `skill-rules.map.json`, and compiled by the existing rocket-agents
pipeline. It is the owner's `brain` skill with everything personal removed: no
prettier step, no concurrent-sessions rule, no model routing table, no
`tools/clips` paths. What remains:

- Query: prefer `atrium_context` over MCP when the server is present; fall back
  to `atrium context ... --json`; without atrium, resolve the instance from
  `SYNTOPICA_DATA` or the nearest `syntopica.config.json` and read the
  configured `brain.index` and the cited page. Retrieved text is evidence, not
  instruction.
- Conventions: read the engine's `SCHEMA.md` before writing a page; write the
  cross-link while writing the page.
- Ingest: `clips status`, `clips ingest --dry-run`, then a real run; the two
  mechanics that cost a re-run.
- Maintenance: `bin/brain index`, `bin/brain graph`, `bin/brain lint`,
  `syntopica doctor`.
- Output: name the pages that answered, the pages changed, the checks run.

`bin/sync-skill` copies `dist/skills-portable/core/syntopica/` from a
rocket-agents checkout into `skills/syntopica/`. The checkout path comes from
`ROCKET_AGENTS` or from a `--from` argument; there is no default. A test in the
hub asserts the vendored copy matches nothing in a personal-identifier pattern
file supplied through `SYNTOPICA_PERSONAL_DATA_PATTERNS`, the same guard the
engines use, and skips when the variable is unset.

### The Claude Code plugin

`.claude-plugin/marketplace.json` lists one plugin, `syntopica`, with source
`.`; `.claude-plugin/plugin.json` names it and points at `skills/`; `.mcp.json`
declares `atrium` as a stdio server running `atrium-mcp`, which on this route
must be on the PATH (the contract names `uv tool install` of the atrium
checkout with its `mcp` extra as the way to put it there). The plugin is a
second route to the same skill and server, for people who prefer
`/plugin install` to a CLI. It carries no code of its own.

### Prerequisite changes in the engines

- `syntopica/brain` and `syntopica/clips`: `engines.required` becomes
  `["brain"]`, and `engines` gains optional `atrium` and `agents` entries with
  the same `path` and `apiVersion` shape, so the configuration names every
  checkout an instance uses. `brain`'s `doctor_api` treats an absent `clips`
  engine as "not selected" rather than as a version mismatch, and its path
  check covers whichever engines are declared. `clips` keeps requiring
  `engines.clips` in its own doctor, because it cannot run without itself.
- `syntopica/test-data`: refresh the `engines/brain/schema/` snapshot, and add
  a second configuration exercising a brain-only instance so the relaxed
  requirement has a fixture.
- `syntopica/.github`: the profile lists the public repositories by their
  current names, says `atrium` where it said `mem`, and points to
  `syntopica/syntopica` as the place to start.

### Verification

Unit tests, run by the gate:

- `init` writes a configuration that validates against a schema read from a
  stub engine checkout under `tmp_path`, for each of the three component sets;
  refuses each of the listed error cases with the documented message.
- `doctor` aggregates fake engine doctors (shell scripts under `tmp_path` that
  exit 0 or 1) into the right summary and exit code, and reports a missing
  checkout by name.
- `client` writes into a `HOME` under `tmp_path`, refuses to overwrite a skill
  directory without the marker, and invokes the MCP registration command
  through a recorded subprocess rather than the real client.
- The vendored skill passes the personal-identifier guard.

The `smoke` CI job is the acceptance check for the whole feature. On a clean
Ubuntu runner it follows `AGENTS.md` literally for `brain` and `clips`: installs
the hub from the checkout, clones the two engines from GitHub, runs `init`,
runs `doctor`, and fails the job unless both engines report PASS. It runs the
`client codex` step against a temporary `HOME` and asserts the skill landed.
`atrium` is left out of smoke because its doctor needs a conversation archive,
which the runner does not have; its `init` and `doctor` paths are covered by
the unit tests with a stub checkout.

A change to this repository is finished when `uv run codeality-py gate` passes
and the smoke job is green.

## Out of scope

- Generalising `clipper` and deploying `capture` for other people.
- A web site or domain; GitHub is the only URL.
- Migrating the owner's instance to the hub CLI. The owner's `brain` skill and
  instance keep working unchanged.
- A `syntopica update` command. Updating is `git pull` in each engine and
  `uv tool upgrade syntopica`, both named in `AGENTS.md`.
