# Setting up the harness – guided, step by step
**Core:** You (the coding agent) set up the harness together with the user. Each step settles a decision only the user can make and files its result in one of two places: the rule the running agent always needs goes into `AGENTS.md`, the state of the harness with the reason for it into `MEMORY.md`. Nothing is guessed, nothing installed on spec. (Context: harness template | As of: 2026-08-30)

## Before you begin
- You have read **all** documents of this skill (`index.md` → every file). Half-knowledge is dangerous: the decisions below presuppose the connections.
- Working style: step by step, per step present the options with a reasoned recommendation (with your agent's question tool, otherwise as text), await the answer, record the result immediately – **one sentence per note**, technical terms, with a rationale where a rule would otherwise be unintelligible. You replace placeholder comments in `AGENTS.md` with content or remove them.
- **Two places, no duplication:** `AGENTS.md` is for regular operation – 99 % of the time the agent works WITH the harness, not ON it: project facts, librarian rules, evaluator rules, workflow, operating tools, pitfalls. Everything harness-internal goes into [MEMORY.md](MEMORY.md): setup status, the coding agents in use and what they support, sync duties, decisions with their reasons, deviations from the template, open points. `MEMORY.md` is loaded only when someone works on the harness – that keeps `AGENTS.md` short. If the project gets a wiki (step 3), `MEMORY.md` remains the authoritative place for the harness state; the same decisions go into the wiki on top, so that a session which never loads this skill still finds them through the librarian.
- Install nothing the user has not confirmed; write no secrets into files; machine-specific values belong in `CLAUDE.local.md` (gitignored) or environment variables.
- The user may skip steps. You note skipped steps under "Open points" in `MEMORY.md` and name them to the user at the end.
- Keep order: a new harness building block (script, subagent, skill, MCP entry) gets its sentence in `AGENTS.md` immediately – a building block that is unknown does not exist for the agent.

## Step 0 – Language
The harness files (`AGENTS.md`, subagents, this skill, wiki skeleton) are written in English – agents read them regardless of the project language; only the template's READMEs are trilingual, because humans read those.
- Ask in which language the user works with the agent and in which language the project's documentation and comments are kept; note that under "Project".
- If the user wants the harness files in their own language, translate them now, once, in place (keep structure, paths, commands and protocol tokens such as `NOT IN WIKI`/`PASS`/`NEEDS_WORK` consistent), then run `python3 tools/sync-agents.py`. There is deliberately only ONE edition – no language mirrors, no sync effort.
- The scripts in `tools/` speak English (source-code language) – that stays.

## Step 1 – Getting to know the project
Look around (repo structure, build system, existing rule files, `docs/`, tests, CI) and ask about what you cannot see:
- What is it about (one sentence)? Application type: command line, library, web application, desktop application, service/API, data pipeline – this decides step 4.
- How is it built, tested, started, released? Is there one single correct way (→ later an ALWAYS/NOT rule)?
- Is the folder tree cut by domain (modules) or by technology (layers)? (→ step 3)
- What regularly hurts (pitfalls)?
Enter "Project" and "Pitfalls" in `AGENTS.md`. If the template was copied into an existing project: work existing `CLAUDE.md`/`AGENTS.md` content into the new `AGENTS.md` (only what always applies, see [regeldateien.md](regeldateien.md)), reduce `CLAUDE.md` to `@AGENTS.md`.

## Step 2 – Coding agents and their capabilities
1. Ask which coding agents work in this project (Claude Code, Codex, Gemini CLI, Cursor, opencode, Copilot, hermes, others) – including the colleagues' ones.
2. Investigate **each named agent, afresh**, per [agenten-kompatibilitaet.md](agenten-kompatibilitaet.md): rule file and includes, subfolder rule files, rules, custom subagents, skills, slash commands, project-local MCP configuration, hooks/cron, no-questions mode, headless start. Official docs plus `--help` on this machine; when in doubt, a probe.
3. Implement:
   - Subagents: the source is `.claude/agents/`; generate the format for every additional agent (extend `tools/sync-agents.py` if a target format is missing).
   - Skills: does the harness skill under `.claude/skills/harness/` live where the agent looks? Otherwise copy/link it to its skill folder (stay inside the project, not at user level). If an agent knows no skills, the sentence in `AGENTS.md` to read the `SKILL.md` directly stays – otherwise it can be shortened to "load the skill `harness`".
   - Rule files: confirm the rule `CLAUDE.md` = `@AGENTS.md` (one sentence is already in `AGENTS.md`); for agents with their own file name (e.g., `GEMINI.md`) the same include solution or the configuration that reads `AGENTS.md`.
   - `tools/agent-start.py`: check the flags in the table at the top of the script against the installed versions (`doctor`, `--dry-run`).
4. Per agent **one sentence** under "Coding agents in use and what they support" in [MEMORY.md](MEMORY.md), plus every sync duty that arises (e.g. "after a change in `.claude/agents/`: `python3 tools/sync-agents.py`"). Into `AGENTS.md` goes only what regular operation needs – if step 2 produced no such rule, nothing goes there.

## Step 3 – Knowledge storage
Read [wissensablage.md](wissensablage.md) for this and decide with the user:
1. **LLM wiki with librarian – yes or no?** Yes if there is knowledge that lives in no repo (operations, access, domain, decisions) and the project is alive. No → remove `.my-memory/`, `.claude/agents/librarian.md` (and generated variants) as well as the wiki section in `AGENTS.md`; instead a `docs/` folder with the sentence "Before you start work in this project, check the `docs` folder for a document touching your topic, and read it" plus one line on what is stored there and what not.
2. **Sharpen the rules:** What concretely belongs in the wiki (or in `docs/`) in this project, what does not? Name examples from the project (e.g., "deploy order and its why: in; endpoint list: out – it is in the code"). Put the sharpened examples as half-sentences into the wiki section of `AGENTS.md`.
3. **Check alternatives and combine if useful:**
   - Rule files in subfolders: only if the folder tree is domain-cut **and** the agents in use load them situationally (step 2). Then create `AGENTS.md` + `CLAUDE.md` (`@AGENTS.md`) per domain module – only with what goes beyond normal use.
   - Link documents from `AGENTS.md` (one sentence suffices, see above).
   - rules files: explain what they are (path-bound rules, loaded only when matching files are touched), check whether the agents support them, and create them if needed (e.g., test rules only for `tests/**`).
4. Record the operating rules as sentences in `AGENTS.md`, the decision itself with its reason (wiki or alternative, and why) in `MEMORY.md`; with a wiki: ingest this session's setup decisions via the librarian at the end (context: "this project's harness").

## Step 4 – Enablement: MCP servers and access
Read [mcp-und-werkzeuge.md](mcp-und-werkzeuge.md). Goal: the agent obtains information itself, can test itself, and can look at things itself.
1. **Web application → recommend the Playwright MCP:** the agent can operate the application through the browser, try things out, take screenshots, read the console and network. Give the note: this replaces no unit/E2E tests. Discuss the setup (fresh browser vs. its own row of tabs; headless on servers).
2. **Desktop application → recommend cua-computer-use:** the same for desktop apps. A rule in `AGENTS.md` that computer use is allowed for debugging – otherwise it will not use it.
3. **Further servers only with a use case:** ticket/CI/wiki systems (first check whether a CLI suffices), read-only mailbox, databases, vision, image generation. For each candidate apply the decision rule MCP vs. script and state the context price.
4. **Access and red lines:** What may the agent read, what execute, what never without approval (sending email, deployments, production systems, payments)?
5. Implement: project-local MCP configuration (file name per agent from step 2), secrets via environment variables, the rule "for X ALWAYS tool Y" in `AGENTS.md`, check context consumption before/after.

## Step 5 – Scripts that support the agent
Read [skripte.md](skripte.md). Ask: which manual work regularly comes up here that is algorithmic? Typical candidates: starting/stopping servers with pre-checks and restart protection, log analysis with navigation, test runners with diagnosis preparation, build/release via exactly one path, database migrations, status checks (is the service running, is the port free, does the health endpoint report errors), counting/measuring.
- For each desired candidate: build it following the ten principles (Python preferred, no venv, help without arguments, human-readable output, exit quickly, error message as an instruction to act) under `tools/`, test it, record it with one sentence each in `AGENTS.md` – including "replaces X, NOT Y anymore" where an old path exists.
- Check whether the project's existing scripts are agent-friendly (data dumps, JSON blobs, long-runners) and propose conversions.

## Step 6 – Autonomous runs, monitoring, security
Read [autonome-laeufe.md](autonome-laeufe.md) and [freilauf.md](freilauf.md).
1. **No-questions runs:** show `python3 tools/agent-start.py doctor` and a `--dry-run`; set up the agent's permission mode and allow list for the mode without follow-up questions (for Claude Code `dontAsk` plus `permissions.allow` in `.claude/settings.json`). Recommend tmux (macOS/Linux) or psmux (Windows) if runs should keep running in the background and be observable. The entry in "Tools and scripts" exists – extend it project-specifically if needed (e.g., default agent, default model).
2. **Usage tracking:** only relevant with subscription quotas – but there practically mandatory for long runs, because at 100 % the subagents die or hang and the run is dead. If yes: clarify the data source (quota command, status data, API) and build a usage script per [skripte.md](skripte.md); the rules (shorten the interval, wait from 90%, subagents check themselves) into `AGENTS.md` or into the prompt template for runs. Costs separately.
3. **Self-monitoring:** does the project need someone who periodically looks for hanging scripts and lost agents? If yes: a check script (`tools/watch.py` or similar) and the instruction to check every N minutes via the agent's cron/loop tool (e.g., `CronCreate`, `/loop`); name the tool explicitly; test beforehand with a trivial task.
4. **Not stopping:** the agent's goal command or loop (clarified in step 2); the order "question round first, then goal" as a rule for runs.
5. **Security:** sandbox (micro-VM/container) or at least worktree + Git + no production access. Split as always: the red line the running agent must obey ("no production access without approval") into `AGENTS.md`, the decision itself with its reason (why sandbox, why only worktree) into `MEMORY.md`.
6. **Superstructure:** if runs are to happen regularly unattended or on a schedule, introduce freilauf (schedules, worktrees, monitoring from outside, budget gates, merge, notification; `SETUP_WITH_AGENT.md` there) – and point out that a project set up with this template runs in it without adaptation.

## Step 7 – Architecture and coding guidelines
This is the most important content step. Read [regeldateien.md](regeldateien.md) and [skills-und-commands.md](skills-und-commands.md).
1. Ask about architecture (style, layers/modules, dependency direction, persistence, error handling, logging) and coding guidelines (language/version, formatting, naming, tests, reviews). Are there documents? Read them.
2. **Core rules (Pareto, about 20 lines)** under "Architecture and coding guidelines" in `AGENTS.md` – only what always applies and what a model does not know anyway.
3. **Create the catalog as a skill** (`.claude/skills/coding-guidelines/SKILL.md`, with reference files if needed), description with the team's keywords ("code review", "guidelines"); in `AGENTS.md` one sentence on when to load it (if mandatory: ALWAYS before acceptance). Optionally a second skill for the architecture documentation. Deterministic rules (formatting, linters) belong in scripts/configuration, not in prose.
4. If desired: `evaluator-guidelines` and `evaluator-architecture` as dedicated subagents following the template in [evaluatoren.md](evaluatoren.md) – or the standard evaluator with a focus.

## Step 8 – Subagents and evaluators
Read [evaluatoren.md](evaluatoren.md).
1. evaluator and librarian are there (librarian only with a wiki). Check whether their `description` and their `model` fit the project (model choice per agent from step 2).
2. **Focus evaluators:** security, performance, clean code, coding guidelines, architecture – which does the project need, as a focus of the standard evaluator or as dedicated files? For each: at which scope of change does it run (security always for auth/inputs/file access; architecture for new modules; performance for hot paths/data access)? Order: deterministic checks → functional acceptance → focus areas. As sentences into the "Quality assurance" section.
3. **Further subagents** only with a clear role and regular need (docs updater before commits, expert for the production environment); otherwise the linking pattern (prompt file + three-liner). Every subagent description costs context permanently.
4. Evaluator from outside (hook, CI) desired? Then set it up if the agent knows hooks (step 2).
5. Afterwards `python3 tools/sync-agents.py`.

## Step 9 – The workflow
Read [workflow.md](workflow.md). Agree the standard workflow with the user and write it as a numbered list into `AGENTS.md`:
- Order: read docs/wiki → plan (which level when) → work → deterministic checks → evaluator loop (which evaluators) → update docs/wiki → release/deploy via which script.
- Testing requirements: which tests must exist and be green for which change? Does a manual test playbook become an E2E test?
- Follow-up-question policy: interactive or fully autonomous; for unattended runs always fully autonomous.
- Git conventions (branch, commit format, when to commit, worktrees) – one sentence per convention.
- When a dynamic workflow or multiple instances would make sense (optional).

## Step 10 – Wrap-up
1. Clean up `AGENTS.md`: all placeholder comments replaced with content or removed; **delete the "Setting up the harness" paragraph**; adapt the sentence about the harness skill to the result of step 2 (fallback only if an agent knows no skills); check the length – core rules short, details linked; every rule with a rationale, no novels.
2. Bring `MEMORY.md` up to date: setup status (which steps done, which skipped, with the date), the coding agents in use and what they support, sync duties, every decision with its reason, deviations from the template, open points. This is where a later rebuild learns what is actually there and why.
3. Replace the template's READMEs (`README.md`, `README.de.md`, `README.zh-CN.md`) with the project's README or delete them; remove the template's `LICENSE` or – if the project is published – carry the attribution from it over into your own license file/README (CC BY 4.0).
4. `python3 tools/sync-agents.py`, `python3 tools/agent-start.py doctor`, check the agent's context view (rule files loaded? unexpected costs?).
5. Update this skill if the setup produced something project-specific about the harness (new scripts, own evaluators): affected document + `index.md`.
6. Call the **evaluator**: task "harness setup", criteria = checklist below, evidence = `AGENTS.md`, `MEMORY.md`, created files, script outputs. Until `PASS`.
7. With a wiki: ingest the decisions with their rationale via the librarian as well. Name open points to the user as a list. Commit if the user wishes.

## Checklist (criteria for the evaluator)
- [ ] Language settled (harness files translated once if wished); template READMEs replaced or removed
- [ ] `AGENTS.md`: project, language, pitfalls, knowledge-storage rules, operating tools/scripts, architecture core rules, quality assurance (evaluators + when), standard workflow – no placeholders left, setup paragraph deleted, nothing harness-internal
- [ ] `CLAUDE.md` = `@AGENTS.md`; the rule for subfolders is in place; subfolder rule files (if chosen) have both files
- [ ] Subagents in all needed formats (`sync-agents.py` run); unneeded subagents removed
- [ ] Harness skill (and guideline skill, if created) where every agent in use finds it – or fallback in `AGENTS.md`
- [ ] Wiki decision implemented (skeleton + librarian, or removed + `docs/` sentence)
- [ ] MCP servers only with a use case, configured project-locally, rule "ALWAYS for X"; secrets not in the repo
- [ ] Scripts per the ten principles, tested, recorded
- [ ] `agent-start.py doctor` and `--dry-run` run; permission mode/allow list set up if autonomous runs are desired
- [ ] Security settled: red lines in `AGENTS.md`, the decision with its reason in `MEMORY.md`
- [ ] `MEMORY.md` reflects the setup: setup status, agents in use, sync duties, decisions with reasons, deviations, open points
- [ ] Open points listed
