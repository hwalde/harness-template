---
name: harness
description: >-
  Documentation and step-by-step procedure for this project's harness: rule files
  (AGENTS.md/CLAUDE.md, subfolders, rules), the subagents evaluator and librarian, LLM wiki
  and knowledge storage, skills, MCP servers (when MCP, when a script), scripts for agents,
  autonomous runs (no-questions modes, tmux/psmux, usage, self-monitoring), workflow and
  evaluator chains, coding-agent compatibility, freilauf. Load when the user asks
  anything about this harness, wants to set it up, extend, improve or update it (also
  against a newer template version), or when a harness building block (script, subagent,
  skill, MCP configuration, rule file) is to be created or changed.
---

# Harness – the procedure

This skill is the documentation of the harness in this project, structured like a small
LLM wiki: `index.md` is the catalog, the documents lie flat next to it, `MEMORY.md` records
the state of THIS harness. Work through the steps below in order; the branch in step 1
decides which route you take, step F is the conditional freilauf branch, step Z applies to
every route that changes a file (route A carries its own closing in `einrichtung.md` step 10).

## Step 0 – Always first, before anything else

1. Read `MEMORY.md`. It says what actually exists here (setup status, coding agents in use,
   sync duties, decisions with reasons, deviations from the template, open points). Without
   it you build a second thing next to an existing one, or undo a deliberate deviation.
2. Read `index.md` – one sentence per document, so you can pick the right ones in step 1.
3. Rule of two places, valid on every route: a rule the running agent must always obey goes
   into `AGENTS.md`; state, decisions and their reasons go into `MEMORY.md`. Never both,
   never the wrong one – `AGENTS.md` is loaded on every request and must stay short.

## Step 1 – Classify the assignment and pick the route

First the state of the project, then the assignment.

**Not yet set up?** (`AGENTS.md` still contains the paragraph "Setting up the harness", or
`MEMORY.md` says setup not yet done.) Then **offer** route A to the user before anything
else – `AGENTS.md` says suggest, not start. If the user wants the setup, take route A. If the
user declines or only wants the one thing they asked for, take the matching route below and
note under "Open points" in `MEMORY.md` that the setup is still pending – otherwise the
building block you touch is built on assumptions nobody has settled.

Then classify the assignment; check in this order, the first match wins.

| If the user … | then route |
|---|---|
| wants the harness set up (fresh copy of the template, or the offer above accepted) | **A – Setup** |
| wants to adopt a newer version of the template into this project | **E – Template update** |
| wants a single building block created or changed (script, subagent/evaluator, skill, MCP entry, rule file, wiki/librarian, permission/run setup) | **C – One building block** |
| wants the harness as a whole reviewed, improved, extended or restructured | **D – Review and extend** |
| asks something – about the harness, a concept, a decision made here | **B – Question** |

If the assignment mixes routes (e.g. a question that turns into a change), start with the
question route and switch to C when the first file is to be written.

## Route A – Setup (fresh copy of the template)

1. Read **all** documents of this skill, in the order of `index.md`. Half-knowledge is
   dangerous: the decisions in the setup presuppose the connections between the documents.
2. Follow `einrichtung.md` from step 0 to step 10, **one step at a time**: present the
   options with a reasoned recommendation (question tool if your agent has one), wait for
   the answer, record the result immediately – one sentence per note, in the right place
   (step 0 above). Never install anything on spec, never write secrets into files.
3. Steps the user skips: note them under "Open points" in `MEMORY.md`, keep going.
4. If step 6 ends with freilauf installed, offer step F right there – unattended and
   scheduled runs are what the hub is for, and the builder skill is the tested way in.
5. Step 10 of `einrichtung.md` **is** step Z for this route – it already contains the
   evaluator pass against its checklist, the `MEMORY.md` update, the sync commands, the
   librarian ingest and the commit. Do not run step Z a second time on top of it.

## Route B – Question

1. From `index.md` pick the documents that touch the topic and read them **in full** – not
   by grep. The documents are condensed; a fragment out of context gives a wrong answer.
2. If the question is about THIS project's harness (what is configured, why, which agents),
   `MEMORY.md` is authoritative; a general document describes how it could be, `MEMORY.md`
   describes how it is.
3. If the question concerns what a coding agent supports (files, flags, folders): do not
   answer from memory. `agenten-kompatibilitaet.md` explains how to investigate (docs,
   `--help`, probe); the table there is a dated snapshot, not the truth.
4. If no document covers it: say so plainly, do not invent. If the answer would be worth
   keeping, offer to add it to the affected document (→ route C, skill as building block).
5. An answer without a file change produces no diff and no evidence – so there is nothing
   for the evaluator to judge and nothing for `MEMORY.md` to record. Done.

## Route C – One building block

1. Read the document that owns the building block **in full** before you write anything
   (`index.md` names them); its rules apply here without asking. In particular:
   - Script → the ten principles in `skripte.md` are binding; help without arguments,
     human-readable output, exits fast, error messages as instructions to act.
   - MCP server → first the decision rule in `mcp-und-werkzeuge.md`: algorithmically
     decidable → script; state, remoteness or daily use → MCP; an existing CLI → no MCP.
   - Subagent/evaluator → `evaluatoren.md`; every concern has exactly one owner, the
     out-of-scope section is written together with the prompt.
   - Skill/slash command → `skills-und-commands.md`; the description is the trigger, test it.
   - Rule file, rules, subfolder `AGENTS.md` → `regeldateien.md`; `CLAUDE.md` = `@AGENTS.md`.
   - Wiki, librarian, `docs/` alternative → `wissensablage.md`; a half-installed store
     (wiki removed but rules kept, or the reverse) confuses the agent more than none.
   - A coding agent added or its capabilities in doubt → `agenten-kompatibilitaet.md`.
   - Permissions, no-questions runs, monitoring → `autonome-laeufe.md`; schedules,
     worktrees, hub → `freilauf.md`; agents that fetch their own work, flows → step F;
     the standard workflow itself → `workflow.md`.
2. Check `MEMORY.md` for a deviation or decision that touches this building block. If the
   change would reverse a recorded decision, say so and let the user decide – do not
   silently overwrite a documented why.
3. If the building block must exist for several coding agents (subagent, skill): source of
   truth is `.claude/`, the other formats are generated or linked – see the sync duties in
   `MEMORY.md`, do not maintain copies by hand.
4. Build, then test it yourself (run the script, load the skill, call the subagent) – the
   evaluator in step Z trusts no claim.
5. Step Z.

## Route D – Review and extend an existing harness

1. Read all documents (as in route A) – restructuring needs the connections.
2. Take stock: the checklist in `grundlagen.md` against what `MEMORY.md` and the repository
   actually contain (`AGENTS.md`, `.claude/agents/`, `.claude/skills/`, `tools/`, MCP
   configuration, `.my-memory/`). Also look for drift: rules in `AGENTS.md` that name a
   guard or script that does not exist, outdated rules, `MEMORY.md` entries that are no
   longer true, sync duties not carried out. If freilauf is in use: is the agent/flow
   concept still current against the builder skill (step F, "check or update")?
3. Report the gaps to the user as a list with a recommendation and a cost (context, effort);
   let the user pick. A harness is never finished, but every building block costs context –
   nothing "in stock".
4. Implement each chosen item as route C, step Z once at the end (or per item if the items
   are independent and the user wants to commit in between).

## Route E – Adopt a newer template version

The copy is detached from the template (step 0 of `einrichtung.md`), so there is no merge
path – an update is a deliberate, file-by-file transfer.

1. Get the current template into a scratch directory outside the project
   (`git clone https://github.com/hwalde/harness-template <scratch>`), never into the repo.
2. Diff the harness parts only: this skill's documents, `.claude/agents/`, `tools/`,
   `.claude/settings.json`, the template's `AGENTS.md`. Ignore the template's READMEs,
   `LICENSE` and setup paragraph – they belong to the template, not to this project.
3. For every difference decide with `MEMORY.md` in hand: if the file is listed under
   "Deviations from the template", keep the project's version (or merge by hand, keeping
   the deviation); otherwise take the newer version. Never restore the "Setting up the
   harness" paragraph, never overwrite `MEMORY.md` or the project content of `AGENTS.md`.
4. If a transferred file changes behavior (new script flags, changed subagent prompt,
   new sync duty), note it in `MEMORY.md` with the date and the template commit.
5. Run the sync duties (`python3 tools/sync-agents.py`, `python3 tools/agent-start.py
   doctor`, `python3 tools/bootstrap.py`), then step Z.

## Step F – Only if freilauf is in use: agents and flows via the builder skill

Applies on routes A, C and D as soon as the assignment is about agents that fetch their own work
(tasks, issues, bugs worked through by themselves, a swarm, scheduled agents with flows
around them), or such a concept is to be checked, updated or carried into another repo.

1. Is freilauf in use? `MEMORY.md` says so (decision from setup step 6), or
   `freilauf status` answers. If not → offer freilauf as in step 6 of `einrichtung.md`;
   without the hub there is nothing for a swarm to run on, so do not build one.
2. Is the skill `freilauf-agent-flow-builder` available? It ships at user level with
   freilauf's other `freilauf-*` skills, so it is present on a machine where freilauf is
   installed – check your skill list. If it is missing → `freilauf.md` describes the concept
   only; install or update freilauf first (its `SETUP_WITH_AGENT.md`), do not rebuild the
   engine from memory – the skill copies a tested version into the project.
3. Both yes → load `freilauf-agent-flow-builder` and follow it; it owns the concept
   (agents, flows, task adapters, the copied engine). This skill's part stays what it always
   is: read `freilauf.md` for the traps (worktree extras, `max_parallel`, hub pushing),
   record the resulting configuration in `MEMORY.md` as a dated snapshot, then step Z.

## Step Z – Closing sequence for every change to the harness

Every route that wrote a file ends here; skipping a point is how a harness silently rots.

1. **Evidence, then evaluator.** Produce observable evidence (script output, a loaded skill,
   a subagent's answer, `git diff`) and call the `evaluator` with task, criteria and paths;
   on `NEEDS_WORK` fix and re-check until `PASS`. Changes to the harness are not exempt.
2. **Make it known.** A new script, subagent, skill or MCP entry gets its one sentence in
   `AGENTS.md` (name, when, what it replaces – "NOT z anymore"). A building block that is
   unknown does not exist for the agent.
3. **Sync duties.** Carry out what `MEMORY.md` lists (after `.claude/agents/`:
   `python3 tools/sync-agents.py`; after configuration living outside the repo: extend
   `tools/bootstrap.py`). Agents load their configuration at start – tell the user to restart.
4. **Documentation is the truth.** Update the affected document of this skill and, if a
   document was added, `index.md`; then `MEMORY.md`: the decision with its reason and date,
   or the deviation, or the closed open point. Delete what became wrong instead of stacking.
5. **With a wiki:** ingest the decision via the librarian too (context: "this project's
   harness"), so a session that never loads this skill still finds it.
6. **Commit** with a message that names the building block; push if a remote exists.
