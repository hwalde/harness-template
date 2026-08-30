# harness-template

**English** · [中文](README.zh-CN.md) · [Deutsch](README.de.md)

**A project starter for working with coding agents.** Rules that always apply. A sceptical second reviewer that signs off every piece of work. A librarian that keeps the project memory. Scripts that do the legwork for the agent, and a start script for runs that never ask questions. Plus the documentation of all of it as a skill – and a setup guide your agent walks through *with* you.

> ### 🤖 Setting it up? Let your agent do it.
> Copy the template into your project and start your coding agent (Claude Code, Codex, Gemini CLI, Cursor, opencode …). It reads `AGENTS.md`, proposes the setup and guides you through the decisions only you can make. If it does not do so on its own:
> *"Load the `harness` skill and set up the harness with me."*

## What a harness is

Everything except the language model: the environment the agent runs in. Rule files, subagents, skills, MCP servers, scripts, a knowledge store, start and monitoring mechanics. A good harness enables the agent to fetch information itself and to verify its own work – and it never leaves a run stuck at a question nobody answers. This template is the foundation for that, and it fits any project.

## What's in the box

```
AGENTS.md                  All rules for coding agents – the whole knowledge lives here
CLAUDE.md                  Contains only "@AGENTS.md"
.claude/agents/            evaluator (sign-off) and librarian (wiki) – source of truth
.claude/skills/harness/    Harness documentation as an LLM wiki + einrichtung.md (setup)
.opencode/agent/           Generated subagent variants for opencode
.my-memory/                Empty LLM wiki – accessed only through the librarian
tools/agent-start.py       Start, attach to and end runs that never ask (tmux/psmux)
tools/sync-agents.py       Translate subagent definitions into other formats
```

**evaluator** – checks with a fresh context and no write access against specification, diff and evidence; answers `PASS` or `NEEDS_WORK`. Optionally with a focus (security, performance, clean code, guidelines, architecture).
**librarian** – the only door to the project memory; filters what stays (decisions with their reasons, pitfalls, operational knowledge) and rejects noise.
**Harness skill** – twelve short documents: the guided setup, what a harness needs, rule files, knowledge storage and its alternatives, evaluators, skills, when MCP and when a script, the ten principles for agent-friendly scripts, autonomous runs, workflow, agent compatibility, freilauf. Next to them `MEMORY.md`, which records the state of your harness: setup status, agents in use, decisions with their reasons, open points.

## Quick start

1. **Get the template:** "Use this template" on GitHub, or clone it, or copy the files into an existing project.
2. **Start your agent** in the project directory.
3. **Let it set things up.** The setup settles, in order: language · project · which coding agents work here and what they support (the agent investigates this at setup time) · knowledge storage (LLM wiki or alternatives) · MCP servers and access (Playwright for web apps, computer use for desktop apps) · scripts · autonomous runs, monitoring, security · architecture and coding guidelines · evaluators · workflow. In the end everything is in `AGENTS.md`, and the setup paragraph disappears.

It works without an agent, too: `.claude/skills/harness/index.md` reads just as well for humans.

## Supported coding agents

Claude Code works out of the box. For opencode the subagents are generated. All others (Codex, Gemini CLI, Cursor, Copilot, hermes …) are wired up during setup: the agent investigates what each of them currently supports – rule files and includes, subdirectory rules, rules files, subagents, skills, slash commands, project-local MCP configuration, hooks, a no-questions mode – and puts the files where that agent looks for them. This investigation deliberately happens at setup time, not in the template: that is what keeps it current.

## Languages

Only what humans read is trilingual: these READMEs (EN/ZH/DE). Everything technical – `AGENTS.md`, the subagents, the skill, the wiki skeleton and the scripts in `tools/` – is monolingual English: coding agents read it regardless of your language, and a single edition means no translation sync. If you would rather have the harness files in your own language: step 0 of the setup lets your agent translate them once, in place.

## freilauf: the superstructure

This template is the starter *inside* the project. [freilauf](https://github.com/hwalde/freilauf) is its counterpart *above* the projects: a self-hosted web UI that runs a standing team of coding agents on a schedule – its own worktree and tmux session per run, budget gates, observation from the outside, a finish gate, integration into `main`, notifications. A project set up with this template runs there without further changes.

## Contributing

Pull requests are welcome – improvements to documents and subagents, further target formats for `sync-agents.py`, translations. Ground rules:

- The three READMEs are maintained **together**.
- Every directory with an `AGENTS.md` has a `CLAUDE.md` next to it containing only `@AGENTS.md`.
- Scripts follow `.claude/skills/harness/skripte.md`; the source-code language is English.
- Nothing machine-specific and no secrets in the repository.

## License

[CC BY 4.0](LICENSE) – use it, change it, ship it commercially; name the author (**Herbert Walde**), link to <https://github.com/hwalde/harness-template>, link the license, and say if you changed something.
