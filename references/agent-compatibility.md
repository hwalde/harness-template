# Coding agents: what they support and where files live
**Core:** Which harness building blocks a coding agent reads and where they must live changes constantly. That is why during setup this is **investigated afresh** by the user's agent – the table at the end is only a dated orientation snapshot, not the truth. (Context: harness skill | As of: 2026-08-30)

## What to clarify per agent in use
| # | Question | Why |
|---|---|---|
| 1 | Which **rule file** does it read (`AGENTS.md`, `CLAUDE.md`, its own format)? Does it support `@file` includes? | Without a rule file nothing takes hold. If it cannot do includes, the rule "CLAUDE.md = `@AGENTS.md`" must do nothing for it – or it reads `AGENTS.md` directly |
| 2 | Does it load **rule files in subfolders** situationally (only when working there)? | decides whether module-specific knowledge may live in subfolder `AGENTS.md` ([knowledge-storage.md](knowledge-storage.md)) |
| 3 | Does it know **rules files** with path/glob binding? Where, which frontmatter? | path-bound rules ([rule-files.md](rule-files.md)) |
| 4 | Does it support **custom subagents**? Folder, frontmatter fields (`name`, `description`, `tools`, `model`)? Does it also read `.claude/agents/`? | evaluator and librarian must exist in its format; `tools/sync-agents.py` generates variants |
| 5 | Does it support **skills** (SKILL.md standard)? Which project folder? Does it also read `.claude/skills/`? | the harness skill and guideline skills must live where it looks; otherwise the fallback "read the SKILL.md" in `AGENTS.md` |
| 6 | **Custom slash commands / prompts**: supported, folder? | user-started procedures ([skills-and-commands.md](skills-and-commands.md)) |
| 7 | **Project-local MCP configuration**: file and format? Lazy loading of the tool descriptions? | MCP servers project-wide instead of per user; context costs ([mcp-and-tools.md](mcp-and-tools.md)) |
| 8 | **Hooks** (before/after tool calls, on stop) and **cron/loop** capability? | enforcing the evaluator from outside; self-monitoring |
| 9 | **No-questions permission mode** – exact flags? **Headless start** with a prompt – exact syntax? | `tools/agent-start.py` (table at the top of the script) must be correct |
| 10 | Where does it show its **context consumption** (memory files, tool descriptions)? | check whether rule files are loaded and what MCP/subagents cost |

## How to investigate (not from memory)
1. The agent's **official documentation** (web) – sections on configuration, memory/instructions, subagents, skills, commands, MCP, hooks, CLI flags. Note date/version.
2. **`<agent> --help`** and subcommands on the user's machine – the installed version is authoritative, not the docs.
3. **Probe:** create a test file (e.g., an `AGENTS.md` in a subfolder with a harmless, recognizable instruction), let the agent work there, observe the behavior, check the context view, remove the test file again.
4. For each agent enter **one sentence** in the project's `HARNESS.md` under "Coding agents in use and what they support": what it supports, where the files live, what is generated for it. Mark the uncertain as "(unconfirmed)". This is harness state, not an operating rule – so it does not go into `AGENTS.md`.

## Setup that does not survive a clone
Some agents keep part of their project configuration **outside** the project. Then a fresh checkout on a new machine silently lacks it, and no file in the repository shows that anything is missing – the building block simply does not take hold, without an error.

The known case (hermes 0.20.5, verified 2026-08-31 – like everything about a moving target, re-check it): **hermes loads project skills (`.hermes/skills/`, `.agents/skills/`) only for trusted projects**, and keeps the trust list in `~/.hermes/config.yaml`. Until `hermes skills trust <project root>` has run, the harness skill is invisible to it. The command is idempotent and takes about 0.2 s, which is what makes the fix cheap.

Ask question 11 of every agent you investigate: **does any of its project configuration live outside the project?** If yes, do not write it into a README as a manual step – nobody reads those twice. Put it in a bootstrap script that is idempotent and safe to run repeatedly (`tools/bootstrap.py`, built by the skill), and wire that script to run automatically: a `SessionStart` hook for agents that have hooks, otherwise a line in the rule file. Have it print nothing when everything is already in order, so the automatic run costs neither context nor attention.

## The built harness's rules for multiple agents
- Source of truth for rules: `AGENTS.md`; `CLAUDE.md` = `@AGENTS.md`. Agents without includes read `AGENTS.md` directly anyway.
- Source of truth for subagents: `.claude/agents/`. Other formats are generated (`python3 tools/sync-agents.py`, currently for opencode into `.opencode/agent/`); for further target formats extend the script instead of maintaining copies by hand.
- Skills live in `.claude/skills/<name>/` (Claude Code; read along by some agents). For agents with their own skill folder, copy or link during setup (symlink where the operating system allows it) and keep the fallback in `AGENTS.md` in case an agent knows no skills.
- An agent usually loads its configuration only at start – restart after changes.
- Only as much duplicate structure as necessary: if an agent is not in use, its folder is not created.

## Orientation snapshot (as of 2026-08 – verify during setup)
Noted from a model's memory (knowledge state early 2026), **not verified** – as a starting point for the investigation, not as proof. Every row is checked during setup against docs and installed version; "?" means: unclear, check first.

| Agent | Rule file | Subfolders | rules | Subagents | Skills | Commands | MCP project-local | No-questions · headless |
|---|---|---|---|---|---|---|---|---|
| Claude Code | `CLAUDE.md`, includes with `@file` | yes, situational | `.claude/rules/*.md` with `paths:` | `.claude/agents/*.md` | `.claude/skills/<name>/SKILL.md` | `.claude/commands/*.md` | `.mcp.json` | `--permission-mode dontAsk` · `claude -p` |
| Codex CLI | `AGENTS.md`, hierarchical | yes | ? | ? | `.agents/skills/` ? | `~/.codex/prompts/` (user-wide) | `.codex/config.toml` `[mcp_servers.*]` ? | `-a never -s workspace-write` · `codex exec` |
| Gemini CLI | `GEMINI.md`; `AGENTS.md` via `context.fileName`; imports with `@file` | yes | ? | experimental ? | ? | `.gemini/commands/*.toml` | `.gemini/settings.json` → `mcpServers` | `--yolo` · `gemini -p` |
| Cursor | `AGENTS.md`; also reads `CLAUDE.md`, `.claude/skills/`, `.claude/agents/` | yes ? | `.cursor/rules/*.mdc` (globs, alwaysApply) | `.cursor/agents/` ? | `.claude/skills/` read along | `.cursor/commands/` ? | `.cursor/mcp.json` | `--force --trust` · `cursor-agent -p` |
| opencode | `AGENTS.md` (fallback `CLAUDE.md`) | ? | ? | `.opencode/agent/*.md` | `.opencode/skill/<name>/` (reads `.claude/skills/` ?) | `.opencode/command/*.md` | `opencode.json` → `mcp` | `--auto` or permission config · `opencode run` |
| GitHub Copilot | `AGENTS.md`; `.github/copilot-instructions.md` | ? | `.github/instructions/*.instructions.md` (`applyTo`) | `.github/agents/*.agent.md` | ? | ? | `.vscode/mcp.json` / repo settings | `--allow-all-tools` ? · ? |
| hermes | `~/.hermes/AGENTS.md` (global); project-local ? | ? | ? | ? | `~/.hermes/skills/` (user-wide) | ? | `~/.hermes/config.yaml` (user-wide) | `--yolo` · `hermes chat -q` |

This table goes stale on its own – the setup verifies every needed cell and records the result as one sentence each in the project's `HARNESS.md`.
