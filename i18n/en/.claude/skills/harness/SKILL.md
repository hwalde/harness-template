---
name: harness
description: >-
  Documentation and setup guide for this project's harness: rule files
  (AGENTS.md/CLAUDE.md, subfolders, rules), the subagents evaluator and librarian, LLM wiki
  and knowledge storage, skills, MCP servers (when MCP, when a script), scripts for agents,
  autonomous runs (no-questions modes, tmux/psmux, usage, self-monitoring), workflow and
  evaluator chains, coding-agent compatibility, freilauf. Load when the user asks
  anything about this harness, wants to set it up, extend or improve it, or when
  a harness building block (script, subagent, skill, MCP configuration, rule file) is to be
  created or changed.
---

# Harness knowledge

This skill is the documentation of the harness in this project – structured like a small
LLM wiki: `index.md` is the catalog, the documents lie flat next to it. The contents are
condensed extracts from experience with coding agents, written for you as the reader.

## Procedure

1. Read `index.md` in this folder and pick the documents that touch your topic.
2. **Half-knowledge is dangerous.** For setup, restructuring, or extension of the harness,
   read ALL documents, not just `einrichtung.md`. For a single question, the relevant ones.
3. **Setup:** `einrichtung.md` walks the user step by step through the
   decisions; results land as terse sentences in `AGENTS.md`. At the end, the
   setup paragraph is deleted from `AGENTS.md`.
4. **Scripts** for this harness are ALWAYS built following the principles in `skripte.md` –
   without asking, they apply here.
5. **MCP servers** only per the decision rule in `mcp-und-werkzeuge.md`.
6. Changes to the harness go through the evaluator like any other work, and the affected
   document here (plus `index.md`) is updated – this keeps the documentation the truth.

## Files in this folder

| File | Content |
|---|---|
| `index.md` | catalog of all documents with a one-sentence description |
| `einrichtung.md` | guided setup of the harness with the user |
| `grundlagen.md` | what a harness is, checklist of a good harness |
| `regeldateien.md` | AGENTS.md/CLAUDE.md, subfolder rule files, rules, writing style |
| `agenten-kompatibilitaet.md` | which coding agent supports what and where files live |
| `wissensablage.md` | LLM wiki with librarian, what belongs in it, alternatives |
| `evaluatoren.md` | evaluator pattern, multiple/specialized evaluators, template |
| `skills-und-commands.md` | skills, slash commands, guideline skills |
| `mcp-und-werkzeuge.md` | when MCP, when a script; Playwright, cua, further servers |
| `skripte.md` | the ten principles for scripts that support agents |
| `autonome-laeufe.md` | permission modes, sandbox, tmux/psmux, usage, self-monitoring, `tools/agent-start.py` |
| `workflow.md` | standard workflow, planning levels, testing, evaluator chains |
| `freilauf.md` | the superstructure for letting agents run and monitoring them |
