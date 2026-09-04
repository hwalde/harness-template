---
name: harness
description: >-
  Builds, sets up, explains, extends and updates a coding-agent harness in a project: rule
  files (AGENTS.md/CLAUDE.md, subfolders, rules), the subagents evaluator and librarian, an
  LLM wiki as project memory, skills, MCP servers (when MCP, when a script), agent-friendly
  scripts, autonomous no-questions runs (permission modes, tmux/psmux, usage, self-monitoring),
  workflow and evaluator chains, coding-agent compatibility (Claude Code, Codex, Gemini CLI,
  Cursor, opencode, Copilot, hermes), and freilauf – the self-hosted hub for scheduled,
  unattended runs – including its installation. Use when a user wants a harness created in a
  new or existing project, wants to set up, review, improve or update an existing one (also
  against a newer skill version), asks anything about this harness or a harness concept, wants
  a harness building block (script, subagent, skill, MCP configuration, rule file) created or
  changed, wants freilauf installed or connected, or works on this skill itself.
license: CC-BY-4.0. See LICENSE in this folder.
compatibility: >-
  Designed for Claude Code; the built harness also serves opencode, Codex, Gemini CLI, Cursor,
  Copilot and hermes. Needs git and python3. freilauf (optional) runs on Linux only.
metadata:
  author: Herbert Walde
  version: "1.2.0"
  homepage: https://github.com/hwalde/harness-skill
---

# Harness – the procedure

This skill **builds** a harness into a project and documents how a harness works. It is not a
template you copy: everything a project receives lies under `assets/project/` and is carried
over by `scripts/build.py`, so the project never has to be detached from anything and this
skill stays a plain git clone that `git pull` keeps current. The documentation is a small
LLM wiki under `references/` (`index.md` is the catalog); the state of a *particular* harness
lives in that project's `HARNESS.md`, not here.

Work through the steps below in order. Step 1 decides the route; step F is the conditional
freilauf branch; step Z closes every route that changed a file.

## Step 0 – Always first

1. **Where are you?** If the current directory is this skill's checkout (a `SKILL.md` with
   `name: harness` next to `assets/` and `references/`), the user is working ON the skill →
   route G, unless they name a project folder. Otherwise the current directory is a project.
2. **Read the project's `HARNESS.md`** if it exists. It says what actually exists there (skill
   version it was built with, setup status, coding agents in use, sync duties, decisions with
   reasons, deviations from the templates, open points). Without it you build a second thing
   next to an existing one, or undo a deliberate deviation. No `HARNESS.md` → no harness yet.
3. Read `references/index.md` – one sentence per document, so you can pick the right ones.
4. **Rule of two places**, valid on every route: a rule the running agent must always obey goes
   into the project's `AGENTS.md`; state, decisions and their reasons go into `HARNESS.md`.
   Never both, never the wrong one – `AGENTS.md` is loaded on every request and must stay short.
5. Never write into `assets/` or `references/` on behalf of a project; those are the skill.
   Project-specific knowledge belongs in the project (`AGENTS.md`, `HARNESS.md`, its wiki).
6. **Whenever you create or edit a script** – for a project or for this skill – you need
   `references/scripts.md` first: the ten binding principles, and the rule that shipped and
   templated scripts are drafts you write, test for real and improve, never copy as they are.

## The working style – a guided process, never a finished harness out of nowhere

Unless the user explicitly asks for a fully automatic run, every route that changes the
harness is a **conversation about decisions**, not a build you present at the end. The user
owns the decisions (which agents, which knowledge store, which access, which red lines, which
scripts); you own the advice. For every decision:

1. **Explain in plain language what it is about** – one or two sentences a person who has
   never heard the term can follow; no jargon without a gloss.
2. **Present the options side by side**: what each one is, how they differ, and what each
   one costs and brings – context, effort, maintenance, risk, what becomes possible, what
   becomes impossible. A table or a short list, never a wall of prose.
3. **Give one reasoned recommendation** and say why it fits *this* project, and when the
   other option would be the better one.
4. **Then let the user choose** (question tool if your agent has one, otherwise as text) and
   wait. Do not decide for them, do not batch five decisions into one question, do not carry
   on "provisionally". Record the choice immediately (rule of two places, step 0).

To advise well you must know the project: **before the first recommendation, look at an
existing project** – repository layout, build and test system, languages, existing rule
files and docs, CI, what runs where (setup step 1 lists what to look for). For a project that
does not exist yet, the cold-start questions in `references/setup.md` ("Before you begin")
gather what the recommendations depend on; ask them first, in one round, then advise.

## Step 1 – Classify the assignment and pick the route

| If the user … | then route |
|---|---|
| wants a harness in a project that has none (no `HARNESS.md`), or the offer below accepted | **A – Build and set up** |
| has a built harness whose setup is not finished (`HARNESS.md` says so, or the setup paragraph is still in `AGENTS.md`) | **A** from step 3 on, resuming `references/setup.md` at the first step that `HARNESS.md` ("Setup status") does not record as done |
| wants a project's harness brought up to the current skill version | **E – Update** |
| wants a single building block created or changed (script, subagent/evaluator, skill, MCP entry, rule file, wiki/librarian, permission/run setup) | **C – One building block** |
| wants the harness as a whole reviewed, improved, extended or restructured | **D – Review and extend** |
| wants freilauf installed, connected, or agents that fetch their own work | **F** |
| asks something – about the harness, a concept, a decision made there | **B – Question** |
| works on this skill itself (its documents, templates, scripts, READMEs) | **G – Improve the skill** |

**No harness yet but the user asked for something else?** Offer route A first, in one
sentence; if they decline, take the matching route and say that the building block is built
on assumptions nobody has settled. If the assignment mixes routes, start with the question and
switch to the change route when the first file is to be written.

## Route A – Build and set up a harness

1. **Settle the target folder – ask when it is not obvious.** Obvious: the current directory
   is a git repository that is not this skill. Not obvious: you are inside the skill, the
   directory is not a repository, or the user mentions another project. Then ask (question
   tool if your agent has one): which folder, does it exist, is it a git repository. Never
   guess a path, never build into the skill's own folder – `build.py` refuses that anyway.
2. **Build:** `python3 <skill>/scripts/build.py <target>`. It copies every template under
   `assets/project/`, generates `CLAUDE.md` (`@AGENTS.md`), never overwrites what exists, and
   prints what it created and what differs. Then, in the project: `python3 tools/sync-agents.py`
   (generates the opencode subagents). Read its output; an existing `AGENTS.md`/`CLAUDE.md`
   in a project that already had rule files is merged in setup step 1, not overwritten.
3. Read **all** documents of this skill in the order of `references/index.md`. Half-knowledge
   is dangerous: the decisions in the setup presuppose the connections between the documents.
4. Follow `references/setup.md` from step 0 to step 10, **one step at a time**: present the
   options with a reasoned recommendation, wait for the answer, record the result immediately
   – one sentence per note, in the right place (step 0 above). Never install anything on spec,
   never write secrets into files. Steps the user skips go under "Open points" in `HARNESS.md`.
5. If setup step 6 ends with freilauf wanted or installed, continue with step F right there.
   If freilauf is not used, setup step 6 item 7 offers the named start/attach scripts per
   agent and OS – explain their purpose and the difference to freilauf first, then write
   them yourself from the templates in `assets/start-scripts/` (its README has the
   placeholders and the procedure), adapt them to the project, and test each one with a
   real run before recording it.
6. Step 10 of `references/setup.md` **is** step Z for this route – it already contains the
   evaluator pass, the `HARNESS.md` update, the sync commands, the librarian ingest and the
   commit. Do not run step Z a second time on top of it.

## Route B – Question

1. From `references/index.md` pick the documents that touch the topic and read them **in
   full** – not by grep. The documents are condensed; a fragment out of context misleads.
2. If the question is about THIS project's harness (what is configured, why, which agents),
   the project's `HARNESS.md` is authoritative; a reference describes how it could be,
   `HARNESS.md` how it is.
3. If the question concerns what a coding agent supports (files, flags, folders): do not
   answer from memory. `references/agent-compatibility.md` explains how to investigate; the
   table there is a dated snapshot, not the truth.
4. If no document covers it: say so plainly, do not invent. If the answer is worth keeping,
   offer to add it to the affected reference (→ route G).
5. An answer without a file change produces no diff – nothing for the evaluator, nothing for
   `HARNESS.md`. Done.

## Route C – One building block

1. Read the reference that owns the building block **in full** before you write anything
   (`references/index.md` names them); its rules apply without asking. In particular:
   - Script → the ten principles in `scripts.md` are binding; help without arguments,
     human-readable output, exits fast, error messages as instructions to act.
   - MCP server → first the decision rule in `mcp-and-tools.md`: algorithmically decidable →
     script; state, remoteness or daily use → MCP; an existing CLI → no MCP.
   - Subagent/evaluator → `evaluators.md`; every concern has exactly one owner, the
     out-of-scope section is written together with the prompt.
   - Skill/slash command → `skills-and-commands.md`; the description is the trigger, test it.
   - Rule file, rules, subfolder `AGENTS.md` → `rule-files.md`; `CLAUDE.md` = `@AGENTS.md`.
   - Wiki, librarian, `docs/` alternative → `knowledge-storage.md`; a half-installed store
     confuses the agent more than none.
   - A coding agent added or its capabilities in doubt → `agent-compatibility.md`.
   - Permissions, no-questions runs, monitoring, named start/attach scripts per agent and OS
     (templates in `assets/start-scripts/`) → `autonomous-runs.md`; schedules, worktrees,
     hub → `freilauf.md`; agents that fetch their own work, flows → step F; the standard
     workflow itself → `workflow.md`.
2. Check `HARNESS.md` for a deviation or decision that touches this building block. If the
   change would reverse a recorded decision, say so and let the user decide – do not silently
   overwrite a documented why.
3. If the building block must exist for several coding agents (subagent, skill): source of
   truth is `.claude/`, the other formats are generated – see the sync duties in `HARNESS.md`.
4. Build, then test it yourself (run the script, load the skill, call the subagent) – the
   evaluator in step Z trusts no claim. A script the skill ships or generates is a draft:
   the agent it drives may have changed its CLI since the template was written, so run a
   real short task through it in the project, fix what does not fit, and only then record it.
5. Step Z.

## Route D – Review and extend an existing harness

1. Read all references (as in route A) – restructuring needs the connections.
2. Take stock: the checklist in `fundamentals.md` against what `HARNESS.md` and the repository
   actually contain (`AGENTS.md`, `.claude/agents/`, `.claude/skills/`, `tools/`, MCP
   configuration, `.my-memory/`). Look for drift: rules in `AGENTS.md` naming a guard or
   script that does not exist, outdated rules, `HARNESS.md` entries no longer true, sync
   duties not carried out. Run `python3 <skill>/scripts/build.py <project> --check` – it lists
   what differs from the skill's templates. If freilauf is in use: is the agent/flow concept
   still current against the builder skill (step F, "check or update")?
3. Report the gaps as a list with a recommendation and a cost (context, effort); let the user
   pick. A harness is never finished, but every building block costs context – nothing "in
   stock".
4. Implement each chosen item as route C; step Z once at the end (or per item if the items
   are independent and the user wants to commit in between).

## Route E – Update a project's harness to the current skill

The project holds built files; the skill holds the current templates. An update is a
deliberate, file-by-file transfer – `HARNESS.md` decides what stays.

1. Bring the skill itself up to date if the user wants: `git -C <skill> pull`. Read
   `CHANGELOG.md` from the version noted in the project's `HARNESS.md` ("Skill version") to
   the current one – it names what changed and why, and which changes need a hand.
2. `python3 <skill>/scripts/build.py <project> --check`: missing files and files that differ.
3. For every difference decide with `HARNESS.md` in hand: listed under "Deviations from the
   skill's templates" → keep the project's version (or merge by hand, keeping the deviation);
   otherwise take the skill's version (`--force <file>`). Never overwrite `HARNESS.md`, the
   project content of `AGENTS.md`, or the wiki; template changes to `AGENTS.md` are merged by
   hand – the changelog says which sentences moved.
4. If a transferred file changes behavior (new script flags, changed subagent prompt, new sync
   duty), note it in `HARNESS.md` with the date; update the "Skill version" line.
5. Run the sync duties (`python3 tools/sync-agents.py`, `python3 tools/agent-start.py doctor`,
   `python3 tools/bootstrap.py`), then step Z.

## Step F – freilauf: install, connect, agents and flows

Applies on routes A, C, D and on its own, as soon as unattended or scheduled runs, several
repos, or agents that fetch their own work (tasks, issues, a swarm, flows around them) come up.

1. **Know the current state of freilauf before you say anything about it.** Fetch
   <https://raw.githubusercontent.com/hwalde/freilauf/refs/heads/main/README.md> and read it –
   features, prerequisites and the shipped `freilauf-*` skills change between versions;
   `references/freilauf.md` explains the concept and the traps, not the current feature list.
2. **Is it installed?** `freilauf status`, or the `freilauf`/`cc-start` binaries on `PATH`.
   `HARNESS.md` records the decision from setup step 6.
3. **Not installed and the user wants it:** say plainly that freilauf currently runs on
   **Linux only** (systemd user units; see the README for the exact prerequisites – Node,
   tmux, git, jq, curl), then fetch
   <https://github.com/hwalde/freilauf/blob/main/SETUP_WITH_AGENT.md> – it is written for
   coding agents – and follow it to the end. Do not improvise the installation from memory,
   do not skip its verification steps, do not write secrets into the project. On macOS or
   Windows: `tools/agent-start.py` plus tmux/psmux is the local edition; note freilauf as an
   open point.
4. **Connect the project:** register it in the hub as `references/freilauf.md` describes
   (worktree extras for anything untracked a run needs, `max_parallel`, merge mode), and record
   the resulting configuration in `HARNESS.md` as a dated snapshot – UI and field names change
   between versions.
5. **Agents and flows:** if the skill `freilauf-agent-flow-builder` is in your skill list (it
   ships with freilauf's `freilauf-*` skills), load it and follow it; it owns the concept.
   Missing → install or update freilauf first, do not rebuild the engine from memory. Then
   record the concept in `HARNESS.md` and go to step Z.

## Route G – Improve this skill

You are in the skill's checkout. Conventions, each with its reason:

1. **Layout is the spec:** `SKILL.md` (frontmatter per agentskills.io: `name` = folder name,
   `description` ≤ 1024 chars, `metadata.version`), `references/` (documents, `index.md` is
   the catalog), `assets/project/` (everything a project receives, at its target path),
   `scripts/build.py` (the one generator: it places the harness files), `assets/start-scripts/`
   (script templates the agent writes project scripts from – deliberately no generator, a
   script the agent wrote and ran is understood and fits the installed agent).
   No `AGENTS.md`/`CLAUDE.md` at the root – they would be loaded as rule
   files while the skill is edited; `CLAUDE.md` is not even stored as a template but generated.
2. **Templates and documents move together.** A changed subagent, script or `AGENTS.md`
   sentence in `assets/project/` needs the matching sentence in the reference that describes
   it, and the reverse. `HARNESS.md` in `assets/project/` is the empty state file; keep its
   section names – route E and the setup refer to them.
3. **Every change is a version.** Add a `CHANGELOG.md` entry (Keep a Changelog: Added,
   Changed, Fixed, and a "Migration" line when a project's built files need a hand), bump
   `metadata.version` (semver: templates or procedure changed incompatibly → major; new
   building block or document → minor; wording → patch).
4. **Language:** everything English except the three READMEs (`README.md`, `README.de.md`,
   `README.zh-CN.md`), which are maintained **together** – a change to one is a change to all.
5. **Test the build:** `python3 scripts/build.py <scratch dir>` into an empty temporary
   directory, then `python3 tools/sync-agents.py` and `python3 tools/agent-start.py doctor`
   there; `build.py --check` must report a clean match. A changed script template is
   tested with a **real** run: write a script from it as the procedure says, start an
   installed agent through it, attach, end it – a dry run did not catch the trust dialog
   that hung the first real one. Validate the frontmatter if
   `skills-ref` is installed (`skills-ref validate .`). Then step Z (evaluator, commit).

## Step Z – Closing sequence for every change

Every route that wrote a file ends here; skipping a point is how a harness silently rots.

1. **Evidence, then evaluator.** Produce observable evidence (script output, a loaded skill, a
   subagent's answer, `git diff`) and call the `evaluator` with task, criteria and paths; on
   `NEEDS_WORK` fix and re-check until `PASS`. Changes to the harness are not exempt.
2. **Make it known.** A new script, subagent, skill or MCP entry gets its one sentence in the
   project's `AGENTS.md` (name, when, what it replaces – "NOT z anymore"). A building block
   that is unknown does not exist for the agent.
3. **Sync duties.** Carry out what `HARNESS.md` lists (after `.claude/agents/`:
   `python3 tools/sync-agents.py`; after configuration living outside the repo: extend
   `tools/bootstrap.py`). Agents load their configuration at start – tell the user to restart.
4. **Documentation is the truth.** In the project: `HARNESS.md` – the decision with its
   reason and date, or the deviation, or the closed open point; delete what became wrong
   instead of stacking. In the skill (route G): the affected reference, `index.md` if a
   document was added, `CHANGELOG.md`, version.
5. **With a wiki:** ingest the decision via the librarian too (context: "this project's
   harness"), so a session that never loads this skill still finds it.
6. **Commit** with a message that names the building block; push if a remote exists and the
   user's workflow allows it.
