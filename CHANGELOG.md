# Changelog

Everything worth knowing that changed in the `harness` skill, newest first.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) —
the categories **Added**, **Changed**, **Deprecated**, **Removed**, **Fixed**
and **Security**, in that order, and an entry says what changed for someone who
builds or operates a harness with the skill, not which function was renamed.

**The unit of this changelog is the day**, not a release. The skill is
developed from `main`: a change lands together with the entry that describes
it, so there is no release date to hang a section on. One section per day on
which something changed, headed by its
[ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) date (`YYYY-MM-DD`), newest
day at the top — the same shape a Keep-a-Changelog release section has, with
the date doing the work the version number does elsewhere. A day without a
section is a day on which nothing changed.

The skill does keep a version — `metadata.version` in `SKILL.md`, semver —
because a project records in its `HARNESS.md` the version it was built with,
and route E updates a project from there. An entry therefore names the version
it belongs to (**v1.2.0**, …) when the change moved it. A **Migration** line
says what a project built with an older version needs done by hand; everything
else route E (`scripts/build.py --check`) carries over.

The rule that keeps this file up to date — after every change to the skill, in
the same commit as the change — lives in the `AGENTS.md` of this repository's
harness project, the private mother repository
[`hwalde/harness-skill-harness`](https://github.com/hwalde/harness-skill-harness),
which carries this repository as its child.

## 2026-09-05

### Changed

- **This changelog is day-based now** (the format described above) instead of
  version-based. A section is a day, an entry lands in the same commit as the
  change it describes, and today's section is created when the day's first
  change lands. The skill version in `metadata.version` of `SKILL.md` still
  moves with every change (semver) and is named in the entry — the two do not
  collide: the day says *when* something changed, the version says *what a
  project was built with*. Convention 3 in `SKILL.md` ("Every change is a
  version") says the same and points at the mother project for the maintenance
  rule (**v1.2.1**).
- **The skill repository has a harness project of its own.** The private
  repository `hwalde/harness-skill-harness` is the mother project that keeps
  this repository working: it carries the rules (`AGENTS.md`, loaded through
  `CLAUDE.md`) — among them the maintenance rule for this changelog — and
  carries this repository as a git submodule in `harness-skill/`, so a
  `git clone --recurse-submodules` of the mother brings the skill with it. The
  skill repository itself stays flat and unchanged; nothing about installing or
  using the skill changes.

## 2026-09-04

### Added

- **v1.2.0** — `SKILL.md` "The working style": the harness is built in a guided
  conversation, never delivered finished – every decision is explained in plain
  language, options are presented side by side with differences and
  consequences, one reasoned recommendation is given, then the user chooses;
  fully automatic only when the user asks for it.
- **v1.2.0** — `references/setup.md` "Before you begin": look at an existing
  project before advising; eight cold-start questions for a new project, asked
  in one round, each mapped to the setup steps whose recommendations depend on
  it.
- **v1.1.0** — `assets/start-scripts/` – templates (with README: placeholders
  and procedure) from which the agent writes named start/attach scripts per
  coding agent and OS into a project's `tools/` (`claude-background-start`,
  `claude-attach`, …; bash + tmux for Linux/macOS, PowerShell + psmux for
  Windows) as thin wrappers around `tools/agent-start.py`; each header states
  the exact command line, the purpose (long-running tasks without permission
  prompts, in the background) and the difference to freilauf. Deliberately no
  generator: scripts are written, tested and improved by the agent.
- **v1.1.0** — Setup step 6 item 7: when freilauf is not used, the scripts are
  offered after the purpose was explained; OS and agents are asked; every
  script is tested with a real run before it is recorded.
- **v1.1.0** — `tools/agent-start.py`: pre-confirms Claude Code's "Do you trust
  this folder?" dialog in `~/.claude.json` (the way freilauf's `fl-start` does)
  – the first real test of the generated scripts hung there; `--no-trust`
  switches it off.
- **v1.1.0** — Rule in `scripts.md`, `autonomous-runs.md` and `SKILL.md`
  step 0: whoever creates or edits a script reads `references/scripts.md`
  first; shipped scripts and templates are drafts – written by the agent,
  tested for real against the installed agent, improved, then recorded.
- **v1.0.0 — first release as a skill.** Until now this repository was
  `harness-template`: a project starter you copied, detached from its origin
  and then could not update. It is now a skill that *builds* the harness into a
  project and stays a plain git clone, so `git pull` keeps it current.
  `SKILL.md` per the [Agent Skills specification](https://agentskills.io/specification.md):
  routes for build and setup (A), question (B), one building block (C), review
  and extend (D), update against the current skill (E), freilauf (F), improving
  the skill itself (G), closing sequence (Z).
- **v1.0.0** — `scripts/build.py` – copies `assets/project/` into a target
  project, generates `CLAUDE.md`, never overwrites, `--check` reports drift,
  `--force` takes the skill's version of named files.
- **v1.0.0** — `assets/project/` – everything a project receives: `AGENTS.md`,
  `HARNESS.md`, `.gitignore`, `.claude/agents/` (evaluator, librarian),
  `.claude/settings.json`, `.my-memory/` skeleton, `tools/` (agent-start,
  bootstrap, sync-agents).
- **v1.0.0** — Step F: freilauf is installed by reading its current README and
  following its `SETUP_WITH_AGENT.md`; Linux-only stated explicitly.
- **v1.0.0** — `CHANGELOG.md`; version and homepage in the skill metadata.

### Changed

- **v1.0.0** — Documents moved to `references/` and renamed to English file
  names (`einrichtung.md` → `setup.md`, `grundlagen.md` → `fundamentals.md`,
  `regeldateien.md` → `rule-files.md`, `agenten-kompatibilitaet.md` →
  `agent-compatibility.md`, `wissensablage.md` → `knowledge-storage.md`,
  `evaluatoren.md` → `evaluators.md`, `skills-und-commands.md` →
  `skills-and-commands.md`, `mcp-und-werkzeuge.md` → `mcp-and-tools.md`,
  `skripte.md` → `scripts.md`, `autonome-laeufe.md` → `autonomous-runs.md`).
- **v1.0.0** — The state file of a harness is `HARNESS.md` in the project root
  (was `.claude/skills/harness/MEMORY.md`); it now records the skill version it
  was built with.
- **v1.0.0** — Setup step 0 no longer detaches a template copy; it settles the
  repository, where the skill is installed for colleagues, and the language.
  Setup step 10 no longer removes template READMEs.
- **v1.0.0** — `AGENTS.md` template: the fallback for a missing skill is its
  one-line install (`git clone … ~/.claude/skills/harness`) instead of a
  project-local path.
- **v1.0.0** — The generated `.opencode/agent/` files are no longer shipped;
  `tools/sync-agents.py` generates them after the build.

### Fixed

- **v1.1.0** (before release, found by the evaluator) — Windows templates:
  argument slicing past the last index, usage errors exiting 1 instead of 2,
  header print running into implementation comments, attach script exiting 0
  when `python` is missing. POSIX template: empty argument array on bash 3.2.

### Migration

- **v1.1.0** — Take the new `tools/agent-start.py` (`build.py --check`, then
  `--force tools/agent-start.py` unless the project changed it). Existing
  projects without freilauf: offer the start/attach scripts (setup step 6
  item 7).
- **v1.0.0** — A project created from `harness-template`: move
  `.claude/skills/harness/MEMORY.md` to `HARNESS.md` in the project root and
  add the "Skill version" section; delete `.claude/skills/harness/` (the skill
  is installed at user level now, or copied as a whole per setup step 0);
  replace the two skill sentences in `AGENTS.md` with the ones from
  `assets/project/AGENTS.md`; then `scripts/build.py <project> --check`.
