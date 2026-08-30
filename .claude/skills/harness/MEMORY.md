# Harness state – what is the case in THIS project
**Core:** State documentation of this harness, beyond `AGENTS.md`. `AGENTS.md` carries the rules for working WITH the harness (99 % of the time); this file carries the state needed for working ON it – so that a later rebuild or improvement knows what is actually there. Read it whenever this skill is loaded; update it after every change to the harness. (Context: harness template | As of: 2026-08-30)

The other documents of this skill describe how a harness works in general – this one describes the harness at hand. State and decisions belong here, rules do not: a rule the running agent must always obey belongs in `AGENTS.md`. Entries are terse; whatever records a decision or an event carries its date (`YYYY-MM-DD`), a standing duty or fact does not. Delete what has become wrong instead of stacking it up.

## Setup status
_Which steps of `einrichtung.md` are done, which were skipped, when._

- 2026-08-30: Template as delivered – setup not yet done.

## Coding agents in use and what they support
_One sentence per agent: which features it supports (subagents, skills, slash commands, rule files in subfolders, rules, project-local MCP configuration) and where its files live. Mark the unverified as "(unconfirmed)"._

- Not settled with the user yet (step 2). The template ships configured for Claude Code (`.claude/`) and opencode (`.opencode/agent/`, generated).

## Sync duties
_What must be regenerated or mirrored after which change, or it silently goes stale._

- After a change in `.claude/agents/`: `python3 tools/sync-agents.py` – generates the subagent definitions for the other agents (e.g. `.opencode/agent/`).

## Decisions (with reasons)
_One line per settled harness decision plus the why – knowledge storage, MCP servers, evaluators, workflow, autonomous runs, security. The why is what cannot be reconstructed later._

_(none yet)_

## Deviations from the template
_Where this harness deliberately differs from the documents of this skill – removed building blocks, own scripts, own evaluators, changed conventions._

_(none yet)_

## Open points
_What is still missing or unsettled, including the steps the user skipped._

_(none yet)_
