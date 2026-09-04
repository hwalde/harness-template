# harness – a skill that builds the harness for your coding agents

**English** · [中文](README.zh-CN.md) · [Deutsch](README.de.md)

**Let coding agents work on company IT projects autonomously – and safely.** This skill builds a complete harness into any project: rules that always apply, a sceptical second reviewer that signs off every piece of work, a librarian that keeps the project memory, scripts that do the legwork, and a start script for runs that never ask questions. Your agent installs it, builds it, walks you through the setup, and keeps it up to date.

> ### 🤖 One line to start
> ```bash
> git clone https://github.com/hwalde/harness-skill ~/.claude/skills/harness
> ```
> Then, in your project, tell your coding agent: *"Load the `harness` skill and build the harness for this project with me."* (Other agents: clone into their skill folder – the skill tells the agent where.)

## Why a harness

A harness is everything except the language model: the environment the agent runs in. Rule files, subagents, skills, MCP servers, scripts, a knowledge store, start and monitoring mechanics. Without one, an agent works from a blank context, grades its own work, forgets what the last session learned, and stops at the first question nobody answers. With this one:

- **Every result is checked by a second pair of eyes.** The `evaluator` subagent reads specification, diff and evidence in a fresh context, with no write access, and answers `PASS` or `NEEDS_WORK`. The builder never accepts its own work.
- **Knowledge survives the session.** The `librarian` is the only door to an LLM wiki in the repository: decisions with their reasons, pitfalls, operational knowledge – filtered, so the context stays lean.
- **Runs never stall.** Permission modes for no-questions runs, named start and attach scripts per agent and OS (`claude-background-start`, `claude-attach`) for long-running tasks in tmux/psmux sessions, usage tracking, self-monitoring, and the rule "question round first, then the goal".
- **Red lines are written down.** What the agent may read, execute and never touch without approval lives in `AGENTS.md`, and the decision behind it in `HARNESS.md` – so an unattended run in a company project stays inside the corridor you set.
- **It fits every coding agent.** Claude Code out of the box; opencode generated; Codex, Gemini CLI, Cursor, Copilot, hermes wired up at setup time, when the agent investigates what each of them currently supports.

## What the skill builds into your project

```
AGENTS.md                All rules for coding agents – project facts, wiki rules, QA, workflow
CLAUDE.md                Contains only "@AGENTS.md"
HARNESS.md               The state of this harness: skill version, agents in use, decisions, open points
.claude/agents/          evaluator (sign-off) and librarian (wiki) – source of truth
.claude/settings.json    Minimal allow list for no-questions runs, a SessionStart hook for bootstrap
.my-memory/              Empty LLM wiki – accessed only through the librarian
tools/agent-start.py     Start, attach to and end runs that never ask (tmux/psmux)
tools/bootstrap.py       Re-establish local setup that does not survive a clone
tools/sync-agents.py     Translate subagent definitions into other agents' formats
```

Then the guided setup settles, in order: repository · language · project and layout · which coding agents work here and what they support · knowledge storage · MCP servers and access (Playwright for web apps, computer use for desktop apps) · scripts · autonomous runs, monitoring, security · architecture and coding guidelines · evaluators · workflow. Everything ends up in `AGENTS.md`, the reasons in `HARNESS.md`.

## What is in the skill

```
SKILL.md                 The procedure: build, question, building block, review, update, freilauf, improve
references/              Twelve documents – what a harness needs, rule files, knowledge storage,
                         evaluators, skills, MCP vs. script, the ten principles for agent-friendly
                         scripts, autonomous runs, workflow, agent compatibility, freilauf, the setup
assets/project/          Everything a project receives, at its target path
scripts/build.py         Builds (or checks) a project against the templates – idempotent, never overwrites
assets/start-scripts/
                         Templates for named start/attach scripts per agent and OS (projects without freilauf)
CHANGELOG.md             What changed per version, and what a built project needs by hand
```

Because the skill stays a git clone, `git pull` updates it, and route E of the skill carries the changes into your projects file by file – your recorded deviations stay. The documents read just as well for humans: start with `references/index.md`.

## freilauf: the superstructure

The harness is the starter *inside* the project. [freilauf](https://github.com/hwalde/freilauf) is its counterpart *above* the projects: a self-hosted web UI that runs a standing team of coding agents on a schedule – its own git worktree and tmux session per run, budget gates, observation from the outside, a finish gate that checks the agent's claim before believing it, integration into `main`, notifications, no-code flows for what happens after a run. A project with this harness runs there without further changes. The skill installs and connects freilauf for you if you want it (currently Linux only).

## About the author

I am Herbert Walde. I have been developing software since 1999, and I have taught more than 200 developers to raise their productivity with AI drastically – this skill is the distilled form of what works in practice. I offer trainings for companies worldwide, in German and English: <https://entwickler-training.de>.

## Contributing

Pull requests are welcome – improvements to the documents and subagents, further target formats for `sync-agents.py`, translations. Ground rules (route G of `SKILL.md` has the reasons):

- The three READMEs are maintained **together**.
- Everything else is English. Templates live in `assets/project/` at their target path; `CLAUDE.md` is generated, not stored.
- Every change gets a `CHANGELOG.md` entry and a version bump in `SKILL.md`.
- Scripts follow `references/scripts.md`. Nothing machine-specific and no secrets in the repository.

## License

[CC BY 4.0](LICENSE) – use it, change it, ship it commercially; name the author (**Herbert Walde**), link to <https://github.com/hwalde/harness-skill>, link the license, and say if you changed something.
