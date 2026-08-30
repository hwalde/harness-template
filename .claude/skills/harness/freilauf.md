# freilauf: letting agents run and monitoring them
**Core:** This template is the project starter (what lives in the repo). freilauf is the superstructure above it: a self-hosted web interface that runs a standing team of coding agents on schedules and monitors them from outside. (Context: harness template | As of: 2026-08-30 | Source: https://github.com/hwalde/freilauf)

## What freilauf does
- **Runs without supervision:** every run gets its own Git worktree and its own tmux session; runs do not disturb each other, you can attach at any time and read the whole screen.
- **Schedules:** "Every night at 2, look at the open issues." An *agent* is a saved run definition (coding agent, model, reasoning effort, prompt, repo, branch rule) plus a name and a schedule; a *single run* is the same without a schedule.
- **Observation from outside:** tmux state, logs, transcripts, hooks, provider pulse – rate limits and outages are detected even when the agent itself can no longer report anything.
- **Done means on `main`:** optionally the hub merges itself, checks the agent's claim before believing it (finish gate), and sends the still-living agent back to catch up on what is missing.
- **Budget gates:** scheduled starts wait when subscription quota or credit is running low.
- **Reports** from the agent (`cc-report done|failed|help|progress|branch|pr`), **Telegram notifications**, **no-code flows** (what happens after a run: follow-up runs, messages to running agents, extraction from reports, branching).
- **Coding agents and model providers as plugins:** Claude Code, opencode, hermes, cursor-agent, and others; more via plugin package. The interface in English, German, and Chinese.
- Contains the start/attach scripts (`cc-start`, `cc-attach`, `cc-kill`, `cc-report`), of which `tools/agent-start.py` in this template is the project-local small edition.

## When it pays off
- As soon as runs are to happen regularly **unattended** or **on a schedule** (night runs, recurring maintenance, working through issues).
- As soon as several agents or several repos run in parallel and you want to know when something went wrong – without constantly looking yourself.
- As soon as the result of a run should land reliably on the main branch, with a check before the merge.

## Interplay with this template
| Level | Responsible |
|---|---|
| In the repo: rules (`AGENTS.md`), subagents (evaluator, librarian), skills, scripts, wiki | this template |
| Above the repo: starting on schedule, worktrees, monitoring, budget, merge, notification | freilauf |

A project set up with this template runs in freilauf without further adaptation: the rules and subagents take hold in every run, the evaluator pass is the natural partner of the finish gate. Mind freilauf's security model (VPN as the access layer; the hub controls tmux, which is shell access).

Setup: `README` and `SETUP_WITH_AGENT.md` in the freilauf repository – the latter is written for coding agents ("Read SETUP_WITH_AGENT.md and set this up for me").
