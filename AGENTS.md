# AGENTS.md – Rules for coding agents in this project

This project was created from the harness template (https://github.com/hwalde/harness-template). All project knowledge for agents lives here; `CLAUDE.md` contains only `@AGENTS.md`.

## Setting up the harness (delete this paragraph after setup)

Suggest to the user that you set up this harness together with them. To do so, load the skill `harness` (if it cannot be loaded, read `.claude/skills/harness/SKILL.md`), read ALL documents cataloged there, and then follow `einrichtung.md`. As soon as setup is complete, delete this paragraph from AGENTS.md so the user is not offered the setup again.

## Harness knowledge

If the user asks you anything about this harness or wants to improve or set it up, load the skill `harness`; if the skill cannot be loaded, read `.claude/skills/harness/SKILL.md` and the `index.md` linked there instead. Half-knowledge is dangerous: read the documents that touch your topic in full. The state of this harness (which coding agents work here, sync duties, decisions, deviations, open points) is not in this file but in `.claude/skills/harness/MEMORY.md` – this file is for working WITH the harness, that one for working ON it.

## Rule files

In every folder where an `AGENTS.md` is created, a `CLAUDE.md` must be created next to it containing exactly one line: `@AGENTS.md`. No content of its own is ever written into a `CLAUDE.md`. When you edit this file or a skill, you are writing for yourself: compact, technical terms, every rule with a rationale, nothing obvious.

## Project

<!-- Fill in during setup: one sentence on what this is about; rough structure (deliberately incomplete); language for answers, documentation, and comments. -->

## Project memory (`.my-memory/`) – librarian

This project has a persistent wiki memory in `.my-memory/` (LLM-wiki pattern: `wiki/` = dense knowledge pages with an index per folder, `raw/` = immutable originals). It is served exclusively by the **librarian** subagent. Reason: it filters, finds, and ingests so that your context stays lean and knowledge survives the session.

1. **Start of work:** If the task needs prior knowledge (project facts, earlier decisions, relationships), consult the librarian FIRST (QUERY mode) and tell it your intention – it delivers the distillate and the topics useful for it. Only when it reports `NOT IN WIKI` do you ask the user. If the task needs no prior knowledge, the consultation is skipped. For any planning, the consultation is mandatory.
2. **End of work / end of a section:** Via the librarian (INGEST mode), store only what has lasting, cross-session value: decisions with their rationale, stable insights and patterns, hard-won pitfalls, operations/access/domain knowledge, changed project facts. Do NOT store: a question just answered, progress/status notes, detail recoverable from the code via `grep`, log output, stack traces, trivia. Guiding question: "Will a future session need this?" When in doubt, no. Provide the context (which project/subsystem/topic); if it reports `CONTEXT UNCLEAR`, clarify the attribution (with the user if necessary) and re-issue the task.
3. **Never read or write `.my-memory/` directly** – not even from subagents. Every access goes through the librarian. No exceptions.
4. **Efficiency:** If knowledge to be stored already exists as a file, give the librarian the path instead of copying the content; for source documents it places the original in `raw/`.
5. **Curation:** The wiki is cleaned up periodically and deliberately triggered (MAINTENANCE mode) – never in passing, deletions only with the user's approval.

## Quality assurance – evaluator

This project works by the generator→evaluator pattern. The **evaluator** subagent is a skeptical second reviewer without write permissions: it reads specification, diff, and evidence in its own fresh context and answers `PASS` or `NEEDS_WORK` plus concrete findings. Reason: the builder never grades its own work – a second pair of eyes finds different mistakes.

1. **After every completed task or subtask** ALWAYS run the evaluator BEFORE the result is reported or accepted as done. "Looks good" or "should work" is no substitute for a check.
2. **Produce real, observable evidence first** (test logs, build output, screenshots) and give the evaluator context: the task or acceptance criteria, changed files, paths to the evidence. It trusts no claims.
3. **If it reports `NEEDS_WORK`, comply:** work through all findings – no debate, no explaining away, no weakened tests or loosened acceptance criteria.
4. **Have every rework re-checked.** The loop runs until it reports `PASS`. Only then does the task count as complete.
5. **Focus areas:** The evaluator can be called with a focus (security, performance, clean code, coding guidelines, architecture). <!-- Decide during setup which focus areas run at which scope of change and whether dedicated focus evaluators are created. -->

## Context-window discipline

Be frugal with your context window. Delegate large reading, search, and research tasks to subagents whose result comes back as a terse distillate (e.g., per file: path + one sentence + at most three sentences of rationale) instead of reading files in full on suspicion. Phrase assignments to subagents as a letter to an equally capable instance – with context and goal, not as a list of commands. On long runs you are the orchestrator: you plan, delegate, check; subagents implement.

## Standard workflow

<!-- Define during setup and tailor to the project. Suggestion: -->
1. Gather prior knowledge (librarian; read linked documents that touch the topic).
2. For non-trivial tasks, plan briefly; write acceptance criteria in checkable form.
3. Implement; deterministic checks via script (linters, tests, build).
4. Evaluator loop until `PASS`.
5. Update documentation and wiki (lasting knowledge only); add to `AGENTS.md` when a sentence was needed for the umpteenth time.

## Tools and scripts

- `python3 tools/agent-start.py` – start, list, attach to, and kill coding agents for no-questions runs (tmux/psmux optional). Without arguments: help.
- `python3 tools/bootstrap.py` – one-time local setup that does not survive a `git clone` (agent configuration living outside the repo). Idempotent and silent when nothing is missing. Run it once in a fresh checkout; agents with hooks can run it automatically.
- New scripts for this harness are built following the principles in `.claude/skills/harness/skripte.md` and recorded here with one sentence each.
<!-- During setup: MCP servers (e.g., Playwright for web apps, cua-computer-use for desktop apps) and the rule when they are ALWAYS to be used; further project-specific scripts. -->

## Architecture and coding guidelines

<!-- Fill in during setup: the most important rules in about 20 lines (Pareto). The full catalog belongs in a skill (e.g., `.claude/skills/coding-guidelines/`), mentioned here with one sentence. -->

## Pitfalls

<!-- Only what hurts when missing: "After changing X, Y must happen, or else Z." One sentence per entry. -->
