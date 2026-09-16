# Syntopica public-onboarding stranger test

Tested 2026-09-16 from fresh HTTPS GitHub clones. **Neither published onboarding path reaches its promised completion literally with `brain,clips,atrium`.** The README stops at `init`; the agent procedure stops at Step 5. Bypassing that stop produces an index, but the documented link syntax produces a disconnected graph. A corrected, brain-only quickstart was executed successfully; its exact text is below.

## Scope, evidence, and limitations

The hub README and AGENTS were read fully before inspecting implementation. The selected components were `brain,clips,atrium`. The data directory example `~/wiki` was replaced with `agent-path/` under this audit directory. No private wiki was read. No client-registration command, model request, conversation export of real data, deployment, or remote Git write was performed. The sole data-repository commit contains synthetic pages and stays local. Public engine source trees remain unchanged.

The environment actually resolved `uv 0.12.15`, Python `3.14.7`, Node `v26.8.2`, pnpm `12.4.2`, and Git `2.55.0`; uv selected an already-installed Python `3.14.3`. The agents checkout selected pnpm `11.15.0`. These are measured results, not certification of the advertised minimum versions or Node 24. Node 24 was not at the usual Homebrew `node@24` path.

**Containment exception:** the first two `pnpm install` runs ignored `npm_config_store_dir` and reused the existing store under `the user's pnpm store`. Their output reports zero downloads, but absence of metadata writes outside this directory cannot be certified. This violates the intended containment assurance. No outside cleanup was attempted. All subsequent recorded commands ran through an OS sandbox denying filesystem writes outside this directory. `HOME` was never reassigned. uv tool directories, uv caches, temporary files, XDG paths, Python bytecode and later package-store writes were confined here. See [containment note](evidence/containment-note.md).

The real `claude` and `codex` binaries were shadowed with exit-127 shims during doctor runs, because `mcp list` can interact with existing servers. Consequently, their `INFO ... mcp` lines are not real registration tests. The pre-existing `INFO claude skill: installed` line is also not evidence that this setup installed a skill. Client findings below are explicitly based on source inspection and official documentation.

| Public repository | Tested commit |
| --- | --- |
| syntopica/syntopica | `a4881df880dba7349eb1a9a86865a05fd31398f3` |
| syntopica/brain | `efd721f1ceb1d1ac2f2a9f751c2c6f1595ab11ef` |
| syntopica/clips | `2f633486c407d8490c395ef5f10f1432dbead33b` |
| syntopica/atrium | `b3b5b200c6a8b8c7d8ed41117a6da00800f1d551` |
| syntopica/agents | `cac49b1de4feb4dcadd0f7cd7cf64676762e65b9` |
| syntopica/test-data | `6bb75d7764dbd6643579e7649bc788787b2fcfb3` |

The [complete timeline](evidence/timeline.md) records every instrumented command, its exact working directory, start time, duration, exit code, and a link to complete combined stdout/stderr. The underlying records are [commands.jsonl](evidence/commands.jsonl). Investigation commands that guessed nonexistent filenames remain in the log; those errors are not treated as product defects. Fixture creation is preserved in the local scripts and files.

## 1. Timeline

Times below are elapsed minutes from the first clone at 02:05:37 UTC. Runs overlapped where independent; these are observed audit timings, not a benchmark for an unfamiliar human or an uncached machine. Full installation output and exact absolute paths are in the linked command timeline.

| Minute | Step / working directory | Command | Result |
| ---: | --- | --- | --- |
| 0.00 | Public hub | `git clone https://github.com/syntopica/syntopica.git hub` | Exit 0; 2.0 s. |
| 0.11 | Read onboarding, `hub/` | `cat README.md AGENTS.md` | Both read fully. |
| 0.18 | Agent Step 1 | `uv tool install git+https://github.com/syntopica/syntopica` | Exit 0; installed `syntopica==0.1.0`, 3.83 s. |
| 0.37 | Version | `syntopica --version` | Exit 0; `syntopica 0.1.0`. |
| 0.37–0.53 | Agent Step 3, `agent-path/` | `git clone https://github.com/syntopica/brain.git engines/brain`; likewise `clips`, `atrium`, `agents` with their own HTTPS URLs | All four exit 0; about 2–2.6 s each. |
| 0.46 | Second fresh directory, `cli-path/` | `uv tool install git+https://github.com/syntopica/syntopica` | Exit 0; shared isolated tool installation reused. Data directory was fresh. |
| 0.49 | README CLI path | `syntopica init --with brain,clips,atrium` | Exit 1; four `init: missing checkout engines/...; run: git clone ...` messages. Literal path stops here. |
| 0.49 | README's next command, diagnostic continuation | `syntopica doctor` | Exit 1; `doctor: no syntopica.config.json found walking upward from .../cli-path`. |
| 0.76 | `agent-path/engines/brain/` | `uv sync` | Exit 0; installed 45 packages, 1.075 s. |
| 0.78 | `agent-path/engines/clips/` | `pnpm install` | Exit 0; 412 packages, 2.747 s; home-store containment caveat above. |
| 0.82 | `agent-path/engines/atrium/` | `uv sync --extra mcp` | Exit 0; 44 packages including MCP, 0.940 s. |
| 0.84 | `agent-path/engines/agents/` | `pnpm install` | Exit 0; 275 packages; installed checkout-local Git hooks, 7.166 s. |
| 1.25 | Agent Step 4, `agent-path/` | `syntopica init --with brain,clips,atrium` | Exit 0; config written and repository initialized. |
| 1.26 | Agent Step 5 | `syntopica doctor` | Exit 1; brain/clips PASS, Atrium archive/refresh FAIL. Literal agent instructions require stopping before first page. |
| 1.61 | Explicit audit continuation | `python3 ../seed_pages.py` | Created three synthetic pages using the schema's bare `[[page-name]]` links. |
| 1.61 | First index | `engines/brain/bin/brain index` | Exit 0; `index.md: 3 pages`. |
| 1.62 | First graph | `engines/brain/bin/brain graph` | Exit 0; `pages 3  links 0  orphans 3  dangling 0  unindexed 0`; wrote `graph.html`. |
| 1.64 | First lint | `engines/brain/bin/brain lint` | Exit 0; `lint: 3 pages, 0 issues`. |
| 1.64 | Brain health | `engines/brain/bin/brain doctor` | Exit 0; all checks PASS. |
| 2.05 | Link workaround | `python3 ../qualify_links.py` then `engines/brain/bin/brain graph` | Original artifacts preserved; qualifying links as `[[pages/name]]` gives `pages 3  links 6  orphans 0  dangling 0  unindexed 0`. |
| 2.07 | Workaround verification | `engines/brain/bin/brain lint`; `engines/brain/bin/brain index --check` | Both exit 0. |
| 2.10 | Installed-skill command | `engines/clips/clips.sh status` | Exit 1; config search starts inside `engines/clips`, not data root. |
| 2.27 | Obvious instance-selection workaround | `engines/clips/clips.sh --data "$PWD" status` | Exit 0; `0 clips, 0 inconsistent, 0 unreadable`. |
| 2.29 | Advertised dry run | `engines/clips/clips.sh --data "$PWD" ingest --dry-run` | Exit 1; `fatal: ambiguous argument 'HEAD'`. |
| 2.31 | Atrium notes-only workaround | `uv run --project engines/atrium atrium ingest-notes pages --exclude sources` | Exit 0; `3 notes -> 6 records written` in the instance's `atrium/index.sqlite3`. |
| 2.31 | Retrieval | `uv run --project engines/atrium atrium search onboarding --words` | Exit 0; six matching records returned. This does not repair conversation archive health. |
| 2.39 | Separate brain-only fixture | `syntopica init --with brain --data lint-probe --engines ../agent-path/engines`; then `syntopica doctor` inside it | Both exit 0; no clips engine configured. |
| 2.60 | Malformed-page probe, `lint-probe/` | `../agent-path/engines/brain/bin/brain index`; then `.../brain lint` | Both exit 0 for `Bad_Name.md` with no frontmatter/summary and `[[missing-page]]`; lint says `0 issues`. |
| 2.61 | Minimal prerequisite PATH | `PATH="$PWD/../runtime/minimal-bin:/usr/bin:/bin" ../agent-path/engines/brain/bin/brain doctor` | Exit 1; `FAIL executables: 2 missing` (Node and pnpm). |
| 2.61 | Checkout-only Atrium PATH | `PATH="$PWD/../runtime/minimal-bin:/usr/bin:/bin" uv run --project engines/atrium atrium doctor` | Exit 1; adds `atrium is not on PATH a login shell would use`. |
| 2.89 | Dry-run workaround, synthetic data only | `git add .config .gitignore syntopica.config.json pages index.md graph.html`; local commit with existing author name and command-scoped personal email | Exit 0; initial commit `5cb391d`. No remote configured or pushed. Exact commit command is in the transcript. |
| 2.89 | Retry without model selection | `engines/clips/clips.sh --data "$PWD" ingest --dry-run --manual` | Exit 1; `git fetch --prune origin exited 128: fatal: 'origin' does not appear to be a git repository`. Stop investigating that path after this workaround. |
| 3.05–3.20 | README recovery, `cli-path/` | Execute the four HTTPS clone commands printed by `init`; retry `syntopica init --with brain,clips,atrium` | All exit 0. |
| 3.20 | README recovery doctor | `syntopica doctor` | Exit 1; same Atrium archive/refresh failures. On this pnpm version, doctor also auto-installed Clips dependencies; uv created Atrium's environment. |
| 4.04 | Safe selector probe, `runners-probe/` | `node ../runner_probe.mjs` | Exit 0; configured `codex`, actual selector fallback; same-author pinned grader accepted. No transports invoked. |
| 4.77 | Public-link check | `python3 check_public_links.py` | Repository destinations and uv documentation reachable. One fragment-bearing duplicate timed out on the repeat check; no confirmed dead public repository link. |
| 5.28 | Tested replacement, `demo-path/` | `sh ../demo_quickstart.sh` | Exit 0 in 6.084 s with warm caches; two pages, two links, zero orphans, zero lint issues, brain doctor PASS. |
| 5.74 | Post-workaround doctor checks | `engines/clips/clips.sh --data "$PWD" doctor`; `uv run --project engines/atrium atrium doctor` | Clips still PASS despite unusable ingest; Atrium still FAIL despite successful notes retrieval. |
| 5.77 | README-recovery MCP dependency probe | `uv run python -c "import importlib.util; print(\"mcp SDK installed:\", importlib.util.find_spec(\"mcp\") is not None)"` in `cli-path/engines/atrium` | Exit 0; `mcp SDK installed: False`, despite entrypoints reporting MCP declared. |

The first index appeared after approximately **1.63 minutes**, and the connected graph after **2.08 minutes**, but only with explicit deviations from the published procedure. The HTML's embedded graph data was inspected; no browser rendering or interaction is claimed. The two unmodified procedures do not earn that payoff.

## Questions left unanswered by the first read

The overview explains the intended wiki and the three components. It does not answer these operational questions before asking the stranger to install:

- Does `init` install engines, or only configure existing checkouts? Where should the command run?
- Is the first payoff Markdown, a website, or a local app? Which file should I open?
- Which tools does a brain-only installation actually require?
- Where does the conversation archive come from, and what creates a successful refresh stamp?
- Which model/transport will run, how is it authenticated, and can it incur cost without a runner being selected in the config?
- Which files under my home directory will registration change? Will it affect other projects or replace an existing skill?
- Can I use this without a remote repository? Does ingest publish or push anything?
- What should a first page's `type` be, and what exact link syntax works?
- What is tracked versus ignored, and how do I back up conversation data that Git intentionally ignores?

## 2. Ranked findings and proposed fixes

### F1 — BLOCKER: the README's entire CLI path omits mandatory engine preparation

**Location:** hub `README.md:21–28`; `syntopica/run_init.py`.

**Exact trigger:** `syntopica init --with brain,clips,atrium` in a fresh directory after installing the hub.

**Observed:** exit 1; `init: missing checkout engines/brain; run: git clone ...`, repeated for clips, atrium and agents. `syntopica doctor` then cannot find a configuration. There is also no preceding data-directory creation. `init` neither clones nor installs anything. Following its printed clone suggestions gets to F2, not completion.

**Exact documentation replacement:** replace the current “The hub CLI” section with the runnable “Replacement quickstart” section below. The replacement starts with a complete brain-only payoff and explicitly moves optional components to a later stage. If keeping all three in the first example, insert every clone/install command from AGENTS Step 3 and solve F2 before presenting the sequence as complete.

**Acceptance:** a fresh directory can run the published block through index, graph, lint and doctor. Verified for the replacement with `python3 run.py demo-path 'sh ../demo_quickstart.sh'` (exit 0).

### F2 — BLOCKER: the agent procedure requires pre-existing Atrium operational state it never creates

**Location:** hub `AGENTS.md:75–96`; Atrium `atrium/doctor/archive_freshness.py`, `refresh_health.py`, `entry_point_health.py`, `login_search_path.py`.

**Exact trigger:** AGENTS Step 5, `syntopica doctor`, after every earlier install and init succeeds.

**Exact relevant output:**

```text
  FAIL archive          the canonical archive does not exist
  FAIL refresh          no refresh has ever recorded a completion
== summary ==
PASS brain doctor
PASS clips doctor
FAIL atrium doctor
PASS agents checkout present
```

AGENTS explicitly says to stop and not continue, so its first-page Step 7 is unreachable. Cloning the conversation-export engine does not export an archive; no command in the procedure records a refresh. Atrium's exposed CLI has no `refresh` subcommand. Importing the three synthetic notes enables lexical retrieval but leaves these failures unchanged.

There is a second deterministic mismatch on a stranger's PATH: the doctor deliberately removes the environment's script directory before checking for an `atrium` binary. With only the documented checkout installation it reports `atrium is not on PATH a login shell would use`, even though the current `uv run --project ... atrium doctor` invocation works. The host's pre-existing global Atrium masked this until the minimal-PATH probe.

**Exact replacement for Step 5's result paragraph, and move Step 7 before Step 5:**

```text
Create and inspect the first pages before optional service checks. Run engines/brain/bin/brain doctor to verify the wiki itself. Then run syntopica doctor and report each component separately. A new Atrium installation reports that its conversation archive and refresh history are absent until conversation capture and indexing have been configured; these failures do not prevent brain index, graph, or lint. Do not describe Atrium as ready for conversation retrieval until an archive has been imported and a context query returns the expected evidence. Client registration is optional and comes after the file-write disclosure below.
```

This is an honest interim route to a working wiki, not a completed Atrium setup. The permanent fix needs a documented capture/import/refresh lifecycle, with actual paths and verification. Do not manufacture an empty archive or touch a refresh stamp to silence doctor. Adjust `entry_point_health.py` to recognize the supported checkout invocation, or explicitly add a separate PATH installation requirement; the current “nothing is installed on PATH” contract and health requirement conflict.

### F3 — MAJOR: the schema's documented link syntax is silently discarded

**Location:** brain `SCHEMA.md`, “Links”; `tools/graph/scan_pages.py:34–38`.

**Exact text:** `` `[[page-name]]` links a page by its filename without the extension. ``

**Observed:** the three pages contain six such links, yet graph says `links 0  orphans 3`; lint says `0 issues`. The scanner skips every target without `/`. Replacing only the targets with `[[pages/name]]` produces six links and zero orphans. Originals are preserved in [pages-documented-links](evidence/pages-documented-links/) and [graph-documented-links.html](evidence/graph-documented-links.html).

**Exact replacement for the link-format sentence:**

```text
Use a path relative to the data directory, without .md: [[pages/page-name]] for pages/page-name.md, or [[notes/page-name]] for notes/page-name.md. The current graph and lint scanners ignore targets without a slash, so [[page-name]] does not create a page edge or a dangling-link warning. Use the same qualified form in page bodies and generated-index references.
```

Alternatively, implement unique-basename resolution in `scan_pages.py` and report ambiguous/unresolved bare links. The smallest immediate fix is the documentation correction plus the two-page example below.

### F4 — MAJOR: the shipped Clips launcher loses the caller's instance

**Location:** clips `clips.sh:3`; hub packaged `syntopica/skills/syntopica/SKILL.md`, “Ingest”.

**Exact trigger:** `engines/clips/clips.sh status`, as instructed by the installed skill, from the data root.

**Observed:** `No syntopica.config.json found from .../agent-path/engines/clips`, exit 1. `pnpm --dir` changes the subprocess directory; instance discovery stops at that checkout's `.git`. Hub doctor hides this because it sets `SYNTOPICA_DATA` explicitly.

**Verified workaround:** `engines/clips/clips.sh --data "$PWD" status` exits 0 with `0 clips, 0 inconsistent, 0 unreadable`.

**Exact replacement for the skill's status example:**

```bash
<engines.clips.path>/clips.sh --data "$PWD" status
```

Precede all skill examples with: `Run these commands from the data directory. Pass its absolute path with --data when calling Clips.` Apply the same flag to its dry-run and ingest examples, while retaining the F5 warning that ingestion needs further Git setup.

**Smallest launcher fix:** make `clips.sh` execute Node against its absolute `src/main.ts` path without changing the caller's working directory, analogous to brain's launcher. Preserve explicit `--data` and environment selection.

### F5 — MAJOR: “local wiki” onboarding cannot run even the advertised Clips dry run

**Location:** clips `src/commands/ingest.ts`, `run-ingest-preflight-checks.ts`, `src/preflight/preflight-repository.ts`; hub `write_instance.py` / `ensure_repository.py`.

**Exact trigger:** `engines/clips/clips.sh --data "$PWD" ingest --dry-run`.

**Observed:** `git rev-parse --abbrev-ref HEAD exited 128: fatal: ambiguous argument 'HEAD'`. `init` creates a repository but no commit. The obvious workaround, committing the synthetic files, exposes the next failure:

```text
git fetch --prune origin exited 128: fatal: 'origin' does not appear to be a git repository
```

The source requires both the wiki and archive repositories to be on `main`, fetch `origin`, and equal `origin/main`, even before the dry-run branch. Meanwhile `init` creates an ordinary `clips/` directory and no remotes. Clips doctor still prints PASS. A dry run also performs a fetch, contradicting its help text's literal “change nothing”.

**Exact interim text before any ingest example:**

```text
Ingestion is not ready immediately after syntopica init. Its current preflight requires an existing commit on main and an origin/main matching main after a fetch, for both the wiki and the resolved clip archive repository. Even ingest --dry-run performs that fetch. The hub creates neither commits nor remotes. Index, graph, lint, and an empty Clips status work locally; do not interpret a passing Clips doctor as proof that ingestion is ready. Configure private repository destinations deliberately before enabling publication.
```

**Smallest code change for a real first-use dry run:** in `ingest.ts`, handle `options.dryRun` before publication-only Git preflight, using read-only archive validation. Keep publication's commit/remote checks for a real run. Add explicit ingest-readiness checks and remediation to Clips doctor; do not auto-create or push a remote during onboarding.

### F6 — MAJOR: configured runners are not the runners execution selects; model names are hardcoded

**Location:** clips README “Models are configuration”; `src/config/with-syntopica-config.ts`; `src/cli/select-synthesizer.ts:29`; `src/commands/grade.ts`; `src/harvest/run-harvest.ts`; `src/models/`.

**Exact claims:** “No model is hardcoded.” and “`runners` in the instance configuration names which transport runs each stage”.

**Measured safe probe:** `node ../runner_probe.mjs` in `runners-probe/` loads a local override with synthesis `codex` and returns:

```json
{"configured":{"synthesis":"codex","grade":"agy-fine","triage":null,"triageRefiner":null},"environmentSynthesis":null,"actualSynthesisIsFallback":true,"sameAuthorPinnedGraderAccepted":true}
```

Config is loaded into async-local context, but execution selectors read `process.env.CLIPS_*_RUNNER`; setting the configuration does not populate those variables. The default selector chooses the agy fallback even with null runners. Checked-in constants include `claude-opus-4-6-thinking` and `gemini-3.1-pro-high`. The initially empty config passed doctor and the dry run printed `synthesizer: agy` on this host. No model request was executed in this audit.

**Exact replacement for the first paragraph of that README section:**

```text
Execution currently selects transports from CLIPS_SYNTHESIS_RUNNER, CLIPS_GRADE_RUNNER, and CLIPS_TRIAGE_RUNNER. The runners fields in syntopica.config.json are loaded and checked by doctor but are not yet wired into the execution selectors. Unset variables select built-in fallback transports; model identifiers are currently constants under src/models/. A passing doctor does not prove that a model transport is configured or authenticated. Use ingest --manual to select the interactive synthesizer; it does not by itself configure grading or remove Git preflight requirements.
```

**Code fix:** pass resolved `config.runners` into the synthesis, grade and triage selectors; preserve environment override precedence in the existing config loader. Null should produce an explicit unconfigured/manual state rather than selecting a remote transport implicitly. Model identifiers need configuration support before restoring the “no model is hardcoded” claim.

### F7 — MAJOR: the advertised author/verifier separation is bypassed by pinned graders

**Location:** clips README “Models are configuration”; `src/grade/select-grade-runner.ts:29–36`; `grade-with-fallback.ts`.

**Exact claim:** “the model that wrote a page may not grade it”.

**Observed:** the same safe selector probe reports `sameAuthorPinnedGraderAccepted: true`: `selectGradeRunner('agy-fine', AGY_FINE_MODEL)` returns the agy-fine grader despite an identical author. The pinned branches do not inspect `author`. The default path's primary Codex attempt also occurs before the fallback-specific separation checks. This is selector-level evidence, not a live graded-page test.

**Exact interim replacement:**

```text
Some fallback grading paths check the author's model before switching transports. This is not yet a universal guard: explicitly pinned graders bypass that check, and a standalone grade command may not know the author. Select a distinct author and grader yourself until every execution path validates both identities.
```

**Code fix:** put author/grader identity validation before any grader execution, including pinned and primary transports. Preserve the guard when choosing fallbacks. The advertised invariant cannot be repaired with onboarding prose alone.

### F8 — MAJOR: client registration can report success without registering anything

**Source-only finding; the registration commands were not run.**

**Location:** hub `syntopica/run_client_command.py:6–11`, `run_client.py:35–44`, `mcp_server_listed.py:6–9`.

**Trigger:** `syntopica client claude` or `syntopica client codex` when the client is missing, returns a nonzero status, or an unrelated/stale Atrium entry already exists.

`run_client_command` discards return codes and stderr and converts missing binaries to an empty string. `run_client` prints `registered mcp server atrium ...` and returns 0 unconditionally after calling it. The existing-registration test only checks whether any line starts with `atrium`; it neither compares the configured data directory nor proves server health. A differently named `atrium-...` entry can also satisfy that prefix check.

**Smallest code fix:** return a structured process result or raise on registration failure; show stderr and return nonzero. Re-read the registered server's structured configuration and compare its exact name, command, arguments and `SYNTOPICA_DATA` before declaring success. Existing entries pointing elsewhere need an explicit conflict message. The skill should not be described as a verified connection merely because its directory exists.

**Exact replacement for AGENTS Step 6's result text until fixed:**

```text
The current success message does not verify registration: the hub does not propagate the client's failure status. Inspect the client's Atrium configuration and verify its absolute checkout path and SYNTOPICA_DATA value. Restart the session and confirm the server exposes atrium_context before reporting that the connection works.
```

### F9 — MAJOR: the setup omits its user-wide write and replacement behavior

**Location:** hub README CLI block; `client_skill_directory.py`, `install_skill.py:10–19`, `mcp_add_command.py`.

**Inspected behavior, not executed:**

| Command | Hub's direct filesystem write | Delegated registration |
| --- | --- | --- |
| `syntopica client claude` | `~/.claude/skills/syntopica/`, including `.syntopica-hub` | `claude mcp add --scope user --env SYNTOPICA_DATA=<absolute-data> atrium -- uv run --project <absolute-atrium-checkout> atrium-mcp` |
| `syntopica client codex` | `~/.codex/skills/syntopica/`, including `.syntopica-hub` | `codex mcp add atrium --env SYNTOPICA_DATA=<absolute-data> -- uv run --project <absolute-atrium-checkout> atrium-mcp` |

Claude's user-scoped registration goes into `~/.claude.json` and applies across projects ([official scope documentation](https://code.claude.com/docs/en/mcp)). Codex MCP configuration defaults to `~/.codex/config.toml`; its CLI, app and IDE integration share that configuration ([official MCP documentation](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)). These are default locations; the delegated client controls any supported configuration-location overrides. The hub's skill destination itself uses `HOME`, not those client-specific overrides.

If a skill directory already exists without the hub marker, the hub refuses it. If the marker exists, it recursively deletes and recopies the whole directory, without backing up local edits. These effects are not disclosed before the command. No deletion was performed in this audit.

**Exact text to insert before either client example:**

```text
Client connection is optional and changes your user configuration outside the wiki. Claude receives ~/.claude/skills/syntopica and a user-scoped Atrium entry in ~/.claude.json. Codex receives ~/.codex/skills/syntopica and an Atrium entry in its configuration, normally ~/.codex/config.toml. The server stores absolute paths to this wiki and its Atrium checkout and may be available from other projects. An existing skill without the hub marker is refused; a hub-marked skill directory is replaced in full, including local edits. Back up any edits before rerunning this command. Skip this step to keep using index, graph, lint and retrieval from the CLI.
```

Add a preview/dry-run mode and backup-before-replace if repeated client installation is intended to be safe.

### F10 — MAJOR: lint does not enforce the conventions its README and skill promise

**Location:** brain README “What it does”; SCHEMA “What the engine checks”; hub packaged skill “Write” / “Maintain”; brain `tools/index/brain_lint.py:10–27`.

**Exact claim:** lint checks “frontmatter, filenames, links that resolve, summaries that exist”; the skill additionally says an orphan is reported by lint.

**Probe:** `lint-probe/pages/Bad_Name.md` contains no frontmatter, no summary, and a bare `[[missing-page]]`. After index generation:

```text
no summary: pages/Bad_Name
lint: 1 pages, 0 issues
```

Exit code is 0. Implementation checks only index freshness and recognized qualified dangling targets. Missing summaries are stderr warnings emitted while rendering the comparison index; malformed filenames, frontmatter and orphans never become lint issues.

**Exact replacement in all three documentation locations:**

```text
brain lint checks whether the generated index is current and whether recognized, directory-qualified page links resolve. It does not currently reject missing frontmatter, invalid filenames, missing summaries, or orphan pages. Missing summaries produce warnings without a failing exit status. Use brain graph to inspect orphans and disconnected components.
```

The alternative code fix is to add those promised validation results to `brain_lint.py` and fail on them. Do not present `lint: 0 issues` as validation of the full schema before doing so.

### F11 — MAJOR: brain-only requires undeclared tools, and the error hides their names

**Location:** hub AGENTS component table; brain README “Requirements”; brain `tools/index/doctor_executables.py` and Clips' corresponding doctor.

**Declared needs:** Git, uv, Python 3.12+. **Actual check:** the unconditional set is `git`, `uv`, `node`, `pnpm`.

With the declared three tools and system utilities available, a brain-only doctor's entire remediation is:

```text
FAIL executables: 2 missing
```

The same function reduces missing executables to a count instead of naming them. Node/pnpm are not needed for the successful brain index/graph operations, but they block the mandated doctor gate.

**Smallest code fix:** require Node/pnpm only for components or operations that use them, and print each missing executable with a concrete install/documentation pointer. Until then, replace the requirements sentence with:

```text
Install Git, uv, Python 3.12 or newer, Node and pnpm before running the current doctor, including for a brain-only instance. Index, graph and lint themselves do not require Node or pnpm; this extra requirement comes from the current doctor's shared executable check.
```

### F12 — MAJOR: engine READMEs assume shell commands and data that installation does not provide

**Clips:** README lists `clips doctor`, `clips status`, etc., but `package.json` has a `clips` script and no executable `bin` mapping; the hub explicitly installs no engine command on PATH. `pnpm install` alone does not create a global `clips`. Also, its requirements block starts at `pnpm install` without a clone/cd or instance-creation step. Add this exact text:

```text
These examples use “clips” as shorthand. From an instance created by the hub, run engines/clips/clips.sh --data "$PWD" <command>. Installing dependencies does not put a clips executable on PATH. Start with the hub onboarding procedure to create syntopica.config.json, then run engines/clips/clips.sh --data "$PWD" status. See the ingestion prerequisites before running ingest.
```

**Atrium:** the first Usage block starts with bare `atrium ingest ...` without an installation section. `~/p/wiki` is the author's directory convention, not a location created by public onboarding; it was not read. `rocket-agents` in the layer table is not linked, and no capture/import/refresh chain connects the hub's agents checkout to the archive doctor expects.

Replace the beginning of Usage with this tested notes-only entry point:

```text
First create an instance with the hub's brain and atrium components and install the Atrium checkout with its MCP extra. From that instance directory, the following commands index only your wiki pages and perform lexical retrieval; no conversation export or embedding-model download is required. Replace “pages” only if your configuration uses another page directory. These commands do not establish a conversation archive or a scheduled refresh, so the conversation-health doctor can still fail.
```

```bash
uv run --project engines/atrium atrium ingest-notes pages --exclude sources
uv run --project engines/atrium atrium search onboarding --words
```

These exact commands were run against the three synthetic pages. Link `rocket-agents` to `https://github.com/syntopica/agents` and document a separate, consented archive-export procedure; a placeholder archive path is not that procedure. Prefer the checkout command form throughout unless a separate tool installation is documented.

**Brain:** README says the configuration “requires” a sibling Clips checkout even before clipping. The tested `syntopica init --with brain` configuration has only a brain engine and passes doctor on the full tool PATH. Replace that paragraph with:

```text
For a new instance, use the hub's brain-only quickstart. A Clips checkout is needed when selecting the clips component, not for building an index or graph. Keep data separate from engine source: the hub places engine checkouts under the data directory's ignored engines/ directory, while this README's manual layout uses sibling checkouts.
```

### F13 — MINOR: the generated index advertises an inbox and schema link that do not exist

**Location:** brain `tools/index/rendered.py`, constants `HEADER` and `FOOTER`.

The new index contains `See [[SCHEMA]]` although the hub only has `engines/brain/SCHEMA.md`, and always contains:

```text
**Inbox:** `inbox/` is empty. Drop files there to ingest.
```

No `inbox/` was created, no input was inspected, and there is no brain ingestion command. This invents a next action and an empty-state assertion. The user should not have to debug generated onboarding advice.

**Smallest code fix:** remove the unconditional inbox footer from `rendered.py`; render capture instructions only when an actual configured and supported inbox exists. Replace the header sentence with this exact text unless a real local schema link is generated:

```text
Root map of the knowledge base. Page format documentation lives in SCHEMA.md in the configured brain engine checkout.
```

### F14 — MINOR: packaged guidance and examples contain unresolved references

The installed skill ends with `@rules/core/agent-discipline.mdc`, `@rules/core/security-baseline.mdc`, and `@rules/core/text-hygiene.mdc`. Those files are not in the packaged skill or public hub checkout. A stranger cannot follow those references, and another agent runtime does not acquire a rule loader merely by reading them. Remove that Rules Index from the standalone distributed skill, or vendor and link the actual public rules with relative paths.

The linked `syntopica/test-data` README uses `~/p/brain/bin/brain` and bare `clips doctor`; it contains schema stubs, not installed engines or a usable conversation archive. Exact replacement for its command introduction:

```text
This repository is a synthetic fixture, not an installed engine bundle or a conversation archive. Replace /absolute/path/to/brain and /absolute/path/to/clips with your real engine checkouts; do not execute the stub directories. Pass this fixture's absolute directory with --data to those engines.
```

The hub claims `init` creates “page and state directories”. It creates pages, sources, ledger, Clips archive and `.config` files, but does not create `atrium/` or `conversations/`. Replace that phrase with `creates the page and support directories; Atrium and conversation state directories are created later by their owning operations`.

## Doctor output: does every FAIL explain the repair?

**No.** The observed failures and their practical meaning are:

| Output | What is missing from the message |
| --- | --- |
| `FAIL archive ... the canonical archive does not exist` | Expected archive path in the human output, how to export it, and distinction between a new notes-only install and a broken populated archive. |
| `FAIL refresh ... no refresh has ever recorded a completion` | Supported command or scheduler that produces the stamp, and whether refresh is configured at all. |
| `FAIL entrypoints ... atrium is not on PATH a login shell would use` | A remedy compatible with the hub's documented checkout-only installation. |
| `FAIL executables: 2 missing` | The two executable names and why brain needs them. |
| `FAIL atrium doctor` in hub summary | Adds no next action to the engine messages. |
| `doctor: no syntopica.config.json found ...` | A direct pointer to clone/setup/init instructions; the reported search path itself is useful. |

Also distinguish PASS from readiness: `PASS clips doctor` does not mean ingestion works or model selection matches config; `PASS agents checkout present` checks only for `.git`, not dependencies or a usable export. The README-recovery doctor said `atrium-mcp is declared, not started` with the MCP SDK absent. This statement is technically qualified, but it cannot establish MCP readiness. On the observed pnpm version, doctor also installed dependencies and executed install lifecycle scripts; `uv run` created Atrium's venv. It is not a reliably read-only health probe.

## Replacement quickstart — exact proposed README text

Replace the existing “The hub CLI” section with the following introduction, command block and result paragraph. The command block is the contents of [demo_quickstart.sh](demo_quickstart.sh), executed in a fresh directory under this audit. For the public README, users choose their own parent directory; this audit redirected tool/cache writes through its local harness.

```text
Start with a local Markdown wiki and an offline graph. Choose a parent directory outside an existing Git repository. You need Git, uv and Python 3.12 or newer; the current doctor also checks for Node and pnpm even when only brain is selected. Installing the hub does not clone its engines. This example creates a wiki/ data directory, clones brain into wiki/engines/brain, and initializes a local Git repository. It does not configure a remote or connect an agent client.
```

```bash
set -eu
uv tool install git+https://github.com/syntopica/syntopica
mkdir -p wiki/engines
cd wiki
git clone https://github.com/syntopica/brain.git engines/brain
(cd engines/brain && uv sync)
syntopica init --with brain
cat > pages/start.md <<'PAGE'
---
title: Start
type: concept
updated: 2026-09-16
summary: 'The starting point for this local wiki.'
sources: []
---

This wiki keeps [[pages/decisions]] beside their evidence.
PAGE
cat > pages/decisions.md <<'PAGE'
---
title: Decisions
type: concept
updated: 2026-09-16
summary: 'Decisions recorded as linked Markdown pages.'
sources: []
---

Return to [[pages/start]] for the overview.
PAGE
engines/brain/bin/brain index
engines/brain/bin/brain graph
engines/brain/bin/brain lint
syntopica doctor
```

```text
The result is wiki/index.md plus wiki/graph.html. Open index.md in your Markdown editor and graph.html in a browser; the graph needs no server. Expect “index.md: 2 pages”, “pages 2 links 2 orphans 0”, zero lint issues, and PASS brain doctor. Edit the pages and rerun index and graph. Their links must include the page directory, as in [[pages/start]].

Add Clips and Atrium after this first check, using AGENTS.md's component-specific clone/install steps. Their operational setup requires more than cloning: Clips ingestion needs Git publication configuration, and Atrium conversation retrieval needs an exported archive and a refresh lifecycle. Client connection is optional and writes user-wide configuration; read its write-location disclosure before running syntopica client.
```

This is a fresh-instance example. `syntopica init` refuses an existing config; do not present it as an “add component” command for the just-created instance. The hub currently has no add-component subcommand. Extending an existing instance needs documented config edits or a dedicated command, preserving pages and local overrides.

## 3. One paragraph for the author

If you fix these **three things** before tonight—replace the incomplete README commands with the tested brain-only quickstart, move first-page creation ahead of optional Atrium health/registration and explain its unconfigured state, and correct the page-link format with a runnable linked-page example—a stranger can reach a working index and connected offline graph within fifteen minutes. Without those changes he stops at the README's second command or AGENTS Step 5; if he improvises past the stop, the documented links make every page appear disconnected. The proposed quickstart ran successfully in this audit, but that does not make Clips ingestion or Atrium conversation retrieval ready: their separate findings still need to be addressed or explicitly scoped out of the initial promise.

## 4. Promise / implementation ledger

| Public promise or implication | Observed implementation |
| --- | --- |
| README's four commands install and connect the system | Mandatory engine preparation omitted; init fails before writing config. |
| AGENTS is the whole procedure and every selected doctor passes | No archive export or refresh lifecycle; Atrium fails before the first page. |
| Engines run only from checkouts | Atrium doctor additionally requires a global/login-PATH executable. |
| `[[page-name]]` forms a page link | Scanner discards targets without `/`. |
| Lint enforces frontmatter, filenames, summaries and orphan conventions | Only index freshness and qualified dangling links fail lint. |
| Models are not hardcoded and runners are instance configuration | Execution reads environment selectors; model constants are in source. |
| The author cannot grade its own page | Pinned selectors accept the author's model; guards are not universal. |
| Successful client output proves registration | Process status/stderr ignored; existing entry compared only by prefix. |
| Setup effects are confined to owned wiki data | Tool installation uses user tool/cache locations by default; client setup writes personal skill/config paths and replaces marked directories. This does not establish that setup uploads wiki contents. |
| `ingest --dry-run` changes nothing | Publication preflight fetches `origin` and needs HEAD before checking the dry-run flag. |
| Passing Clips doctor means usable Clips setup | It passes with null runners, unborn HEAD and no origin. |
| `init` creates state directories | It defers Atrium and conversations directories. |
| Brain needs a Clips checkout | Current brain-only config and doctor work without one, given the full executable PATH. |
| Generated index can direct users to an inbox | Footer hardcodes an absent inbox and an unsupported drop-file workflow. |
| Doctor is just diagnosis | This run auto-installed Clips dependencies and created Atrium's venv. |
| Everything useful requires full onboarding | Brain produces an index/HTML locally, and Atrium notes-only lexical retrieval works without a conversation archive. Neither requires a model request for the tested commands. |

Public repo links for brain, clips, atrium, agents, test-data, clipper and capture resolved; the Clips sandbox-boundary document and Brain schema/eval paths exist. There is **no confirmed dead repository link** in the tested main onboarding documents. The failures are missing procedures, runtime assumptions and incompatible claims, rather than unavailable repositories. The public [link-check results](evidence/public-links.json) retain the one repeated-request timeout. No private instance was inspected to fill the gaps.

## Deliverables and verification

- [Working three-page index](agent-path/index.md) and [connected graph](agent-path/graph.html).
- [Tested replacement demo index](demo-path/wiki/index.md) and [graph](demo-path/wiki/graph.html).
- [Original disconnected graph](evidence/graph-documented-links.html), malformed-page fixture under `lint-probe/`, and safe [runner probe](runner_probe.mjs).
- [Complete command timeline](evidence/timeline.md), [raw command records](evidence/commands.jsonl), and [public revision manifest](evidence/revisions.json).

Verify the report's retained evidence and generated graph/index contents from this directory:

```bash
python3 verify_findings.py
```

Verification executed successfully with exit 0: three graph fixtures matched their expected node/edge/orphan counts, seven public checkouts matched their recorded revisions with unchanged source, and the report structure, local artifact links, replacement script and retained failure transcripts passed. The verification checks recorded failures as expected failures, not as passing product behavior. Registration remains source-reviewed only; browser rendering, actual model transports, personal conversation capture, publication, and minimum-version compatibility remain untested.
