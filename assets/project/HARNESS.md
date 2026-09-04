# Harness state – what is the case in THIS project
**Core:** State documentation of this harness, beyond `AGENTS.md`. `AGENTS.md` carries the rules for working WITH the harness (99 % of the time); this file carries the state needed for working ON it – so that a later rebuild, update or improvement knows what is actually there. It is read whenever the `harness` skill is loaded in this project and updated after every change to the harness. (Context: built by the harness skill | As of: 2026-09-04)

The documents of the `harness` skill describe how a harness works in general – this one describes the harness at hand. State and decisions belong here, rules do not: a rule the running agent must always obey belongs in `AGENTS.md`. Entries are terse; whatever records a decision or an event carries its date (`YYYY-MM-DD`), a standing duty or fact does not. Delete what has become wrong instead of stacking it up.

## Skill version
_Which version of the `harness` skill built or last updated this harness (from `metadata.version` in its `SKILL.md`). Route E of the skill compares against it._

- Built with harness skill 1.0.0 – setup not yet done.

## Setup status
_Which steps of the skill's `references/setup.md` are done, which were skipped, when._

- Harness files built – setup not yet done.

## Coding agents in use and what they support
_One sentence per agent: which features it supports (subagents, skills, slash commands, rule files in subfolders, rules, project-local MCP configuration) and where its files live. Mark the unverified as "(unconfirmed)"._

- Not settled with the user yet (step 2). The skill builds the files for Claude Code (`.claude/`) and generates the opencode variants (`.opencode/agent/`).

## Sync duties
_What must be regenerated or mirrored after which change, or it silently goes stale._

- After a change in `.claude/agents/`: `python3 tools/sync-agents.py` – generates the subagent definitions for the other agents (e.g. `.opencode/agent/`).

## Decisions (with reasons)
_One line per settled harness decision plus the why – knowledge storage, MCP servers, evaluators, workflow, autonomous runs, security. The why is what cannot be reconstructed later._

_(none yet)_

## Deviations from the skill's templates
_Where this harness deliberately differs from what the skill builds – removed building blocks, own scripts, own evaluators, changed conventions. Route E (update) keeps every file listed here._

_(none yet)_

## Open points
_What is still missing or unsettled, including the steps the user skipped._

_(none yet)_
