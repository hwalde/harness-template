# Autonomous runs: without follow-up questions, without stopping, without supervision
**Core:** An autonomous run fails on every question that nobody answers, on every session that dies at logout, and on every limit that silently chokes it. The harness removes all three. (Context: harness skill | As of: 2026-08-30)

## Building blocks at a glance
| Building block | What for | Where in the built harness |
|---|---|---|
| No-questions permission mode | the agent never halts to ask | `tools/agent-start.py` knows the mode per agent |
| Terminal multiplexer (tmux / psmux on Windows) | the run survives logging out; you can attach and watch | `tools/agent-start.py start/attach/send` |
| Goal hierarchy + checkable acceptance checklist in the prompt | the agent knows what has priority and when it is done | [workflow.md](workflow.md), below |
| Something that keeps it from stopping before the work is done | the `/goal` command (Claude Code) or a loop | below |
| Usage tracking | stop before the quota limit instead of dying | usage script, see below |
| Self-monitoring | detect hanging scripts and lost agents | the agent's cron/loop + a check script |
| Evaluator | a second one checks the acceptance | [evaluators.md](evaluators.md) |
| Sandbox | security via the boundary of the environment, not via deny lists | below |
| Superstructure for schedules and monitoring from outside | when runs happen regularly unattended | [freilauf.md](freilauf.md) |

## Permission modes (using Claude Code as the example; other agents' counterparts in [agent-compatibility.md](agent-compatibility.md))
| Mode | Behavior |
|---|---|
| manual | asks about every little thing, may not even write to files |
| acceptEdits | writes files in the project folder without asking; asks for commands unless they are approved (it remembers permanently allowed commands) |
| plan | planning only, focused on a technical plan |
| auto | executes where it is sure the command is safe; when unsure (e.g., a delete command with variables) it asks |
| bypassPermissions | does not ask for shell commands; for a few things (its own configuration files) it still does. Unpopular in companies – `auto` usually does just as well |
| **dontAsk** | **the key to autonomy:** never asks; what is not allowed is silently refused and reported to the model, which finds another way. Blocks all interactive question tools (including `AskUserQuestion`). Subagents run like this anyway. Needs an allow list of permitted commands in the settings, otherwise it refuses too much. |

Alternative: `acceptEdits` plus pre-approved commands. For every other agent, look for the counterpart – without a mode in which it *cannot* ask anymore, it does not really run autonomously.

## Security: a sandbox instead of stripping permissions
Whoever lets an agent run for days wants neither it getting stuck nor it being unable to edit its own skills. That speaks against "allow as little as possible". The right concept: **allow everything, but inside a sandbox** (e.g., a micro-VM like the Docker sandbox for coding agents, or a container/worktree with limited network). Inside the boundary the agent may do everything; the security comes from the boundary of the environment, not from the length of the deny list. Without a sandbox you are playing with fire – then at least a worktree, Git as a safety net, and no production access.

### Two things a deny list cannot do
- **A deny scopes an access path, not a capability.** Denying *reading* a key does not stop a
  tool from *using* it; denying one command spelling does not stop an equivalent one. Before
  you rely on a deny, ask what the guarded capability actually requires, and gate it where it
  is exercised - a confirmation flag inside the tool that performs the irreversible act beats
  a pattern match on a command line.
- **A guard that can only be satisfied by evading it is worse than none.** If a rule forbids
  exactly what the workflow requires, the run will find the spelling that slips past - and you
  have taught evasion while believing you built a barrier. When a deny collides with a
  documented workflow, one of the two is wrong; fix that, do not add an exception.

## The launch sequence (proven order)
1. **Write the prompt** – short, by hand, precise. The substantive core is a **goal hierarchy**: goal 1, goal 2, plus an explicit sentence on the order ("when goal 1 is reached, continue with goal 2"). Phrase the goals so that it pursues them rigorously, but keep them attainable.
2. **Cut** what the agent does anyway or what plays no role for this run ("keep documents up to date", "note learnings" – that lives in the harness). What remains is the core: goals, framework conditions (usage, costs), enablements.
3. **Prescribe capability, not the deployment plan:** "use subagents" stays; "start one per bug" gets cut. A prescription about the approach is only justified if your own observation stands behind it (e.g., "first one complete pass, then fix the collected errors", because restarts measurably cost money). The line lies where prescription becomes supervision.
4. **Keep meta-levels clean:** if the project itself works with agents, there are agents *in* the project and agents *of* the coding agent – keep the wording in the prompt unambiguous. Choose a smarter model for such runs.
5. **Have it formatted** in an empty chat: "Format this text as Markdown, do not rewrite anything" – frame the text in XML tags so that data and instruction stay separate.
6. **Have an acceptance checklist generated:** "Write the requirements in checkable form, ordered by goal 1 and goal 2." Check every phrase for second readings ("mandatory dependency" ≠ "mandatory to use") – during the run nobody asks follow-up questions anymore.
7. **Start** via script in a named session: `python3 tools/agent-start.py start --prompt-file lauf.md --name nachtlauf`. The first assignment for a new instance when there are several scripts: call up the scripts' help and understand them.
8. **Question round first, then goal:** "Ask relevant questions within the next ten minutes; after that, work fully autonomously." Answer them. **Only then** set the goal – an active goal keeps the agent from halting for a follow-up question. Name the question tool explicitly (demand or forbid it).
9. **Set the goal:** summary + checklist + working mode ("fully autonomous, no questions, do not wait for answers"). Roughly check the token length; type the command fresh in the target window (copied commands like to pick up one space too many).
10. **Let go.** Close the window, the session keeps running. Do not look in constantly – watching is the hard part.

## Not stopping before the work is done
- Claude Code: `/goal` – conditions in checkable form; the agent does not abort before they are met (it still does not run endlessly).
- Alternatively a loop that restarts the agent with the same task until a check script reports "done" (careful: loops without an abort criterion and without a usage check are dangerous).
- Large goals: describe them at length in the normal chat, put only the conditions to be met into the goal.

## Usage tracking (only relevant with subscription quotas)
- A session window (e.g., 5 hours) plus weekly and model limits. At 100% the run is effectively dead: subagents die or hang; the only way out would be additional, expensive extra quota.
- Solution: a **usage script** that returns the percentage and the reset time (the data source differs per agent – for Claude Code e.g. the status-line/quota data in the configuration folder; otherwise the agent's quota command or the provider API). Output human-readable, plus a byte-stable final line for wrappers.
- Instructions in the prompt: use the script; shorten the check interval the closer the value gets to 90%; above 90% wait until the reset; **subagents pause and check their usage themselves with the same script** – a subagent that knows nothing about the limit burns the main agent's budget unchecked.
- **Track costs separately** (API costs ≠ quota).

## Self-monitoring
- Long-running scripts sometimes hang; agents get lost. Someone is needed who looks in from time to time when nobody sits in front of the screen.
- The agent sets up the monitoring for itself: in Claude Code via the `CronCreate` tool or `/loop` ("use your CronCreate tool to create a job that runs `tools/watch.py` every 30 minutes"). Name the tool explicitly so that the cron tool does not become a Chrome tool; test beforehand with a trivial task (a "hello world" every minute), then delete the job again.
- What the job checks: are the processes still running, is there progress, is the disk filling up, is a script hanging, has a subagent stalled without a result. On a finding: intervene or restart the run.
- For monitoring from outside (including rate limits the agent itself can no longer report) and schedules: [freilauf.md](freilauf.md).

## Behavior for the unforeseen: boundaries and abort conditions
Models want to reach their goal and take the shortest path – normally the built-in brake, but under goal pressure ("think out of the box") also the reason for unwanted paths. Whoever runs autonomously therefore hands over behavior for unforeseen situations:
- **Hard boundaries:** "Migrate only the controllers, nothing else." "No changes outside `src/api/`." "No emails, no deployments, no production systems." Otherwise the agent rewrites half the system because "then this and that must change too".
- **Abort condition:** "If you find that you would need to change something outside X, stop and write down what is missing."
- **Given time:** the first cases together, the next alone, on success all of them.
- **Straighten tests without papering over bugs:** "Straighten the tests that break because of the code change; if you find a bug doing so, do not paper over it, write it down." Without that addition, tests turn green and errors vanish.
- Rough goals have edges: "debug the pipeline" needs the sentence "remove fixed bugs from the bug list", otherwise the list grows endlessly.
- Loops (the agent restarted with the same task) only with an abort criterion and a usage check.

## Steering without disturbing
- Hints typed directly into the chat change the context and affect everything that follows – that is how you steer deliberately (steering). Mid-run "use the librarian now", however, is pointless; offered tools are used less in autonomous runs than expected.
- Silent diagnosis: the whole transcript plus one question to a second model (Claude Code: `/by the way`) answers "where is it standing?" without the agent noticing anything. Pattern: diagnose silently → fix the problem outside the run → put only the one needed piece of information into the chat.
- If the main agent gets lost in detail work: "Better start a subagent for that, so you don't get distracted." For long runs, right at the start: "You only orchestrate; subagents implement – that protects your context window."
- Model and reasoning effort are not one-time settings: for interim tasks without thinking demand a smaller model and lower effort; for runs in which meta-levels and tools must be understood, the smartest model.

## Self-improvement (optional)
The agent may extend the skill from which it draws the knowledge for evolving the system with **relevant** learnings. Project-local skills only – never the user-level `harness` clone, which `git pull` keeps current and a local edit would fork; project learnings about the harness go into the project's `HARNESS.md` or wiki. Risk: it optimizes the skill to pieces and throws core decisions overboard. Countermeasure: mark non-negotiable decisions in the skill as such; "with the relevant learnings", not "with all". A remainder stays surrendered control.

## Shifting verification to the end
Some results only a human can accept. Then it pays to place the final acceptance reliably at the end (e.g., a comment function with timestamps whose feedback the agent works through in a targeted way) and not have every little thing checked by screenshot along the way – continuous interim checking is expensive, and edge cases are better left to the human at the end.

## Named start and attach scripts per agent and OS (when freilauf is not used)
`tools/agent-start.py` is generic: agent, mode, multiplexer, all behind flags. A human who wants
to hand a long-running task to an agent should not have to remember them – one command per
agent, with a name that says what it does: `tools/claude-background-start "task"` and
`tools/claude-attach [NAME]`, likewise `opencode-…`, `codex-…`. **The agent writes them**, from
the templates in `assets/start-scripts/` of the skill (its README lists the placeholders and the
procedure): one pair per agent, bash + tmux for Linux/macOS, PowerShell + psmux for Windows.
There is deliberately no generator – a script the agent wrote, ran and fixed is understood,
matches the installed agent version and carries the project's own pre-checks and defaults.
They are thin wrappers around `agent-start.py`, so the no-questions flags stay in one table;
each header states the exact command line, the purpose, and the difference to freilauf.

**Explain the purpose before offering them** – the user must know why they exist: a run that
nobody sits in front of dies at the first permission prompt and at the first closed terminal.
The script starts the agent in its no-questions mode (Claude Code `--permission-mode dontAsk`,
opencode `--auto`, Codex `-a never`, Gemini `--yolo`, cursor `--force --trust`, hermes `--yolo`)
inside a tmux/psmux session that survives logout; the attach script is the way back in. For
ordinary interactive work the agent is started normally. **The difference to freilauf:** these
scripts are the local edition inside one project – one run, in the current checkout, started
by hand, watched by the human. freilauf is the hub above the projects: schedules, a fresh
worktree per run, budget gates, a finish gate, merge, notifications. Whoever needs that
installs freilauf (step F of `SKILL.md`) and does not need these scripts.

**Templates are drafts, never finished goods.** The flags in the table are a dated snapshot;
a coding agent changes its CLI between versions, a fresh checkout raises a dialog the table did
not foresee (Claude Code's "Do you trust this folder?" hung the first real test of these
scripts – `agent-start.py` now pre-confirms it in `~/.claude.json`, the way freilauf's
`fl-start` does). So, for every agent and OS the user wants: write the script from the
template, adapt it to the project (default model, pre-checks, prompt-file convention), check
the mode against the installed version (`<agent> --help`, the docs), run a **real** short
task through it (not only `--dry-run`), attach, read the screen, end the run – and fix the
table or the script when it does not behave. Only a script that passed a real run gets its
sentence in `AGENTS.md`. What cannot be tested on this machine (the Windows scripts on Linux,
an agent that is not installed) is handed over marked as untested in `HARNESS.md`.

## `tools/agent-start.py` in brief
`doctor` (which agents/multiplexers are there) · `start --prompt/--prompt-file [--agent] [--name] [--dir] [--model] [--headless] [--attach] [--dry-run] [--no-trust]` · `list` · `attach NAME` · `send NAME "Text"` · `kill NAME`. With a multiplexer an interactive session `hx-<name>` is created; without one (or with `--headless`) the agent runs in the background with a log under `.harness/runs/`. The flags per agent live in a table at the top of the script – the only place to adjust when flags change.
