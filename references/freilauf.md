# freilauf: letting agents run and monitoring them
**Core:** The harness this skill builds is the in-repo layer (rules, subagents, scripts, wiki). freilauf is the superstructure above it: a self-hosted web interface that runs a standing team of coding agents on schedules and monitors them from outside. (Context: harness skill | As of: 2026-08-30 | Source: https://github.com/hwalde/freilauf)

## What freilauf does
- **Runs without supervision:** every run gets its own Git worktree and its own tmux session; runs do not disturb each other, you can attach at any time and read the whole screen.
- **Schedules:** "Every night at 2, look at the open issues." An *agent* is a saved run definition (coding agent, model, reasoning effort, prompt, repo, branch rule) plus a name and a schedule; a *single run* is the same without a schedule.
- **Observation from outside:** tmux state, logs, transcripts, hooks, provider pulse – rate limits and outages are detected even when the agent itself can no longer report anything.
- **Done means on `main`:** optionally the hub merges itself, checks the agent's claim before believing it (finish gate), and sends the still-living agent back to catch up on what is missing.
- **Budget gates:** scheduled starts wait when subscription quota or credit is running low.
- **Reports** from the agent (`cc-report done|failed|help|progress|branch|pr`), **Telegram notifications**, **no-code flows** (what happens after a run: follow-up runs, messages to running agents, extraction from reports, branching).
- **Coding agents and model providers as plugins:** Claude Code, opencode, hermes, cursor-agent, and others; more via plugin package. The interface in English, German, and Chinese.
- **Skills for the agent that operates it:** freilauf ships user-level skills (`freilauf-agents`, `freilauf-runs`, `freilauf-flows`, `freilauf-repos`, `freilauf-models`, `freilauf-plugins`, `freilauf-stats`), so a coding agent can set the hub up and read it from the shell instead of the browser. `freilauf-agent-flow-builder` is the builder among them (see below).
- Contains the start/attach scripts (`cc-start`, `cc-attach`, `cc-kill`, `cc-report`), of which `tools/agent-start.py` in the built harness is the project-local small edition.

## Installing it – read the source, not this file
freilauf changes faster than this document. Before you describe, recommend or install it, fetch its current README (<https://raw.githubusercontent.com/hwalde/freilauf/refs/heads/main/README.md>): features, prerequisites (as of this writing: Linux with systemd user units, Node.js 22+, tmux, git, jq, curl) and the shipped `freilauf-*` skills are listed there. It runs on **Linux only**; on macOS or Windows the local edition (`tools/agent-start.py` plus tmux/psmux) stays. If the user wants it installed, fetch <https://github.com/hwalde/freilauf/blob/main/SETUP_WITH_AGENT.md> – written for coding agents – and follow it to the end, including its verification steps; do not improvise from memory and do not write its secrets (tokens, VPN keys) into the project. Step F of `SKILL.md` is the procedure; this document supplies the concept and the traps below.

## When it pays off
- As soon as runs are to happen regularly **unattended** or **on a schedule** (night runs, recurring maintenance, working through issues).
- As soon as several agents or several repos run in parallel and you want to know when something went wrong – without constantly looking yourself.
- As soon as the result of a run should land reliably on the main branch, with a check before the merge.

## Interplay with the built harness
| Level | Responsible |
|---|---|
| In the repo: rules (`AGENTS.md`), subagents (evaluator, librarian), skills, scripts, wiki | built by this skill into the repo |
| Above the repo: starting on schedule, worktrees, monitoring, budget, merge, notification | freilauf |

A project whose harness this skill built runs in freilauf without further adaptation: the rules and subagents take hold in every run, the evaluator pass is the natural partner of the finish gate. Mind freilauf's security model (VPN as the access layer; the hub controls tmux, which is shell access).

Setup: `README` and `SETUP_WITH_AGENT.md` in the freilauf repository – the latter is written for coding agents ("Read SETUP_WITH_AGENT.md and set this up for me").

### Concepts made of agents and flows (`freilauf-agent-flow-builder`)
Delivered at user level together with the other `freilauf-*` skills, this one is the builder: it sets a whole ready-made concept – agents plus the flows around them – up in a project. Triggers are "the project should work through its tasks by itself" and "set up the swarm". The first concept is the **task swarm**: a watchdog flow (cron, no LLM) counts the open tasks and wakes a short-lived dispatcher agent, which starts worker agents repeatedly and staggered in time according to the backlog – GLM-5.3-Flash as the workhorse, DeepSeek for the trivial, the strong lane (Claude Code / fable) while subscription quota is free and Gemini otherwise; a third failed attempt on a task goes to the PO automatically, and a PO agent presents the questions that are waiting. Where the tasks come from is a contract with adapters (finding register, GitHub issues, or one of your own), and the engine is copied into the project as a template – at runtime nothing is called out of the skill folder.

## Registering a project (procedure, not a contract)
**This is a dated snapshot – freilauf evolves, and its UI, field names and defaults change with it. Verify against the running version before you follow it; if it no longer matches, follow the current UI and update this section.** Observed 2026-08-31 against commit `584e562`; the UI language was German.

- **Find the hub first:** `freilauf status` reports the port, the systemd unit and the deployed sha. An older installation may still carry the pre-rename "cc-hub" naming (`~/.config/cc-hub/env`, `~/.local/share/cc-hub/cc-hub.db`, `cchub.service`); the `freilauf` CLI reads both.
- **There is no CLI or JSON API for repositories.** `POST /repos/edit` from the HTML form is the only write path, so a browser (Playwright MCP) is the tool. Writing to the SQLite database directly skips the server's validation – avoid it, and if it is ever unavoidable, back the database up with `sqlite3 -readonly … ".backup '<path>'"`, never `cp` (WAL mode).
- **Fields that matter:** name · path to the main checkout · base branch · repo prompt (what a run must know and cannot see) · **worktree extras** · integration mode · max parallel runs.
- **Editing an existing repo: resubmit the *whole* form.** The save handler issues one full
  `UPDATE` over every column, not a patch. A POST carrying only the fields you meant to change
  silently blanks the repo prompt and resets worktree extras to `[]`. Read the current values
  first, change the ones you mean, submit everything.
- **Read the result back** from `/repos` or the database instead of trusting the form – a validation failure renders a problem page rather than saving. Read text columns with a real sqlite binding, not the `sqlite3` CLI: prompts stored with CRLF come back lossy, and rebuilding a prompt from such a dump corrupts it.

### Worktree extras – the field that makes nested checkouts work
Every run gets its own git worktree, unconditionally, and a worktree contains only **tracked** files. So anything gitignored or untracked that a run needs – `node_modules`, a local config, or, in the mother/child layout, the gitignored subfolder holding the actual artifact – is invisible unless it is listed here. Format: a JSON array of `{"path": "<relative>", "mode": "copy"|"link"}`.

- `link` – one shared real directory. Survives worktree cleanup, and the finish gate does not see it as dirty. The price: **all runs share it**, so they can corrupt each other.
- `copy` – real isolation per run, but worktree cleanup **deletes the copy** and everything committed inside it. Only safe if the run pushes before finishing.
- The UI's "find worktree extras" button *replaces* the list with its own suggestion. It cannot know which ignored entry is the point of the project – do not press it on a configured repo.

### Two traps worth knowing before you rely on them
- **`max_parallel` caps only *scheduled* starts.** Manually started runs are never blocked. If you set it to 1 to protect a shared `link` extra, that protection does not cover manual runs.
- **A per-run worktree defeats path-keyed machine-local state.** Anything an agent trusts,
  registers or caches *by absolute path* outside the repo gets a new entry on every run,
  because every run has a new worktree path. hermes's project-skill trust list in
  `~/.hermes/config.yaml` is the known case: it grows without bound with paths that no longer
  exist. Harmless so far, but check for this whenever a bootstrap step keys on a path.
- **A merge check over a `link` extra inspects live, shared state.** The extras are applied
  to the integration worktree too, so the link still points at the one real checkout. A merge
  check that examines it is therefore reading whatever any other run - or the human at the
  keyboard - has left there right now: an unrelated dirty file fails this run's merge, and a
  run can equally be credited with commits it never made. Accept it as a smoke alarm rather
  than a proof, and keep `max_parallel` low.
- **Hub merging pushes.** With integration set to hub, freilauf merges the run branch into the base branch and does `git push origin base:base`. Decide deliberately whether that remote is one an unattended run may write to – and note that in a mother/child layout it can only ever push the *mother*: the child is a separate repository that git's merge machinery never sees, so committing and pushing it stays the run's own duty. Say that in the repo prompt, or runs will assume the hub handled it.
