# Changelog

All notable changes to the `harness` skill. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [Semantic Versioning](https://semver.org/): templates or procedure changed incompatibly → major, new building block or document → minor, wording → patch. The version lives in `metadata.version` of `SKILL.md`; a project records the version it was built with in its `HARNESS.md`. A **Migration** line says what a project built with an older version needs by hand – everything else route E (`scripts/build.py --check`) carries over.

## [1.2.0] – 2026-09-04

### Added
- `SKILL.md` "The working style": the harness is built in a guided conversation, never delivered finished – every decision is explained in plain language, options are presented side by side with differences and consequences, one reasoned recommendation is given, then the user chooses; fully automatic only when the user asks for it.
- `references/setup.md` "Before you begin": look at an existing project before advising; eight cold-start questions for a new project, asked in one round, each mapped to the setup steps whose recommendations depend on it.

## [1.1.0] – 2026-09-04

### Added
- `assets/start-scripts/` – templates (with README: placeholders and procedure) from which the agent writes named start/attach scripts per coding agent and OS into a project's `tools/` (`claude-background-start`, `claude-attach`, …; bash + tmux for Linux/macOS, PowerShell + psmux for Windows) as thin wrappers around `tools/agent-start.py`; each header states the exact command line, the purpose (long-running tasks without permission prompts, in the background) and the difference to freilauf. Deliberately no generator: scripts are written, tested and improved by the agent.
- Setup step 6 item 7: when freilauf is not used, the scripts are offered after the purpose was explained; OS and agents are asked; every script is tested with a real run before it is recorded.
- `tools/agent-start.py`: pre-confirms Claude Code's "Do you trust this folder?" dialog in `~/.claude.json` (the way freilauf's `fl-start` does) – the first real test of the generated scripts hung there; `--no-trust` switches it off.
- Rule in `scripts.md`, `autonomous-runs.md` and `SKILL.md` step 0: whoever creates or edits a script reads `references/scripts.md` first; shipped scripts and templates are drafts – written by the agent, tested for real against the installed agent, improved, then recorded.

### Fixed (before release, found by the evaluator)
- Windows templates: argument slicing past the last index, usage errors exiting 1 instead of 2, header print running into implementation comments, attach script exiting 0 when `python` is missing. POSIX template: empty argument array on bash 3.2.

### Migration
Take the new `tools/agent-start.py` (`build.py --check`, then `--force tools/agent-start.py` unless the project changed it). Existing projects without freilauf: offer the start/attach scripts (setup step 6 item 7).

## [1.0.0] – 2026-09-04

First release as a skill. Until now this repository was `harness-template`: a project starter you copied, detached from its origin and then could not update. It is now a skill that *builds* the harness into a project and stays a plain git clone, so `git pull` keeps it current.

### Added
- `SKILL.md` per the [Agent Skills specification](https://agentskills.io/specification.md): routes for build and setup (A), question (B), one building block (C), review and extend (D), update against the current skill (E), freilauf (F), improving the skill itself (G), closing sequence (Z).
- `scripts/build.py` – copies `assets/project/` into a target project, generates `CLAUDE.md`, never overwrites, `--check` reports drift, `--force` takes the skill's version of named files.
- `assets/project/` – everything a project receives: `AGENTS.md`, `HARNESS.md`, `.gitignore`, `.claude/agents/` (evaluator, librarian), `.claude/settings.json`, `.my-memory/` skeleton, `tools/` (agent-start, bootstrap, sync-agents).
- Step F: freilauf is installed by reading its current README and following its `SETUP_WITH_AGENT.md`; Linux-only stated explicitly.
- `CHANGELOG.md`; version and homepage in the skill metadata.

### Changed
- Documents moved to `references/` and renamed to English file names (`einrichtung.md` → `setup.md`, `grundlagen.md` → `fundamentals.md`, `regeldateien.md` → `rule-files.md`, `agenten-kompatibilitaet.md` → `agent-compatibility.md`, `wissensablage.md` → `knowledge-storage.md`, `evaluatoren.md` → `evaluators.md`, `skills-und-commands.md` → `skills-and-commands.md`, `mcp-und-werkzeuge.md` → `mcp-and-tools.md`, `skripte.md` → `scripts.md`, `autonome-laeufe.md` → `autonomous-runs.md`).
- The state file of a harness is `HARNESS.md` in the project root (was `.claude/skills/harness/MEMORY.md`); it now records the skill version it was built with.
- Setup step 0 no longer detaches a template copy; it settles the repository, where the skill is installed for colleagues, and the language. Setup step 10 no longer removes template READMEs.
- `AGENTS.md` template: the fallback for a missing skill is its one-line install (`git clone … ~/.claude/skills/harness`) instead of a project-local path.
- The generated `.opencode/agent/` files are no longer shipped; `tools/sync-agents.py` generates them after the build.

### Migration
A project created from `harness-template`: move `.claude/skills/harness/MEMORY.md` to `HARNESS.md` in the project root and add the "Skill version" section; delete `.claude/skills/harness/` (the skill is installed at user level now, or copied as a whole per setup step 0); replace the two skill sentences in `AGENTS.md` with the ones from `assets/project/AGENTS.md`; then `scripts/build.py <project> --check`.
