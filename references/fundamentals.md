# Fundamentals: what a harness is and what a good one needs
**Core:** Everything except the LLM is the harness – the environment the agent runs in: rules, knowledge, tools, scripts, reviewers, autonomy building blocks. The goal is always the same question: how can the agent do this itself, autonomously? (Context: harness skill | As of: 2026-08-30)

## The term
- The coding agent itself is already a harness (system prompt, tools, permission modes). The project-specific harness is everything built around it so that runs end well without intervention: rule files, subagents, skills, MCP servers, scripts, knowledge store, launch and monitoring machinery.
- Harness engineering is the third phase of working with coding agents: after "prompting" and "planning processes per task" comes the environment that enables and checks the agent – and the countermovement of largely leaving the approach to it: a hard goal + check criterion, let it run.
- A harness is never finished. It grows on the side: every sentence you type for the umpteenth time moves into the rule file; every piece of manual work that is algorithmic becomes a script; every recurring check an evaluator.

## All building blocks serve the same goal
Rule files, subagents, skills, MCP servers, and scripts control **which information and capabilities sit in the context window when** – neither overtaxing nor undertaxing the model. Two extension paths: natural language (rule files, skills, subagents) and algorithms (scripts, MCP). Everything that sits permanently in the context (descriptions of subagents, skills, MCP tools, rule files) costs on every request – "what do I really want to hold in the model's face all the time?"

## Checklist: what a good harness needs (a selection, not a mandatory list)
| Building block | Purpose | Built by the skill |
|---|---|---|
| Written-down requirements and rules | core rules (architecture, workflow, pitfalls) in `AGENTS.md`, the rest linked | `AGENTS.md`, [rule-files.md](rule-files.md) |
| Evaluator | one agent checks another; qualitatively and functionally | `evaluator`, [evaluators.md](evaluators.md) |
| Knowledge management | the most critical point: requirements, plans, "how does what work", access | librarian + `.my-memory/`, [knowledge-storage.md](knowledge-storage.md) |
| Enablement | the agent obtains information itself, tests and debugs itself: browser/desktop control, access, scripts, tests | [mcp-and-tools.md](mcp-and-tools.md), [scripts.md](scripts.md) |
| Scripts | deterministic support; output as a prompt | `tools/`, [scripts.md](scripts.md) |
| Not stopping before the work is done | goal command or loop | [autonomous-runs.md](autonomous-runs.md) |
| No-questions mode + multiplexer | the run never halts and survives logging out | `tools/agent-start.py` |
| Usage tracking | stop before the quota limit (only with subscription limits) | [autonomous-runs.md](autonomous-runs.md) |
| Self-monitoring | detect hanging scripts and lost agents (cron/loop) | [autonomous-runs.md](autonomous-runs.md) |
| Self-improvement (optional) | the agent updates skills/docs – with limits | [skills-and-commands.md](skills-and-commands.md) |
| Security | sandbox instead of a deny list | [autonomous-runs.md](autonomous-runs.md) |
| Workflow | read docs → plan → work → check → update docs/wiki | [workflow.md](workflow.md) |
| Superstructure | schedules, worktrees, monitoring from outside, merge | [freilauf.md](freilauf.md) |

Self-monitoring is the hardest to do without: an agent that had a question five minutes after being left alone has thrown away two days. The evaluator is the cheapest to build in and yields the most.

## Enablement: your own red line
Everything the agent cannot do itself needs the human. Hence: browser control for web apps, desktop control for desktop apps, access (e.g., a read-only mailbox to check confirmation emails), scripts, tests as self-validation. And deliberately draw a red line – say: no emails without human approval, no access to production systems without approval.

## Order as an architectural requirement
A clear, domain-cut folder tree, unambiguous terms (one word per concept), and fixed places for scripts, documents, and configuration are harness building blocks: like humans, the AI needs structure to find information quickly and to miss nothing – and subfolder rule files only work with a domain-oriented cut.

## Spec-driven as a complement
The path described here (goal + criteria + harness) does not rule out specification documents: for larger endeavors, a requirements document with implementation packages and testing requirements supplies the check criteria; with a weak harness the agent at least gets the access and hints there for the task at hand ([workflow.md](workflow.md)).
