# Setting up the harness – guided, step by step
**Core:** You (the coding agent) set up the harness together with the user, right after `scripts/build.py` placed the files. Each step settles a decision only the user can make and files its result in one of two places: the rule the running agent always needs goes into `AGENTS.md`, the state of the harness with the reason for it into `HARNESS.md` (project root). Nothing is guessed, nothing installed on spec. (Context: harness skill | As of: 2026-09-04)

## Before you begin
- You have read **all** documents of this skill (`references/index.md` → every file). Half-knowledge is dangerous: the decisions below presuppose the connections.
- **Guided, not automatic** (the working style in `SKILL.md`): every step is a decision the user takes after you explained, in plain language, what it is about, what the options are with their differences and consequences, and which one you recommend and why. Present options clearly (table or short list), one decision at a time, then wait for the choice.
- **Know the project before you advise.** Existing project: look around first (step 1 says what). New or empty project – **cold-start questions**, asked in one round before any recommendation, because most recommendations below hang on the answers:
  1. What is the project, in one sentence, and what kind of application (CLI, library, web app, desktop app, service/API, data pipeline, mixed)? → MCP servers (step 4), test strategy.
  2. Who works on it – one person or a team, in-house or with outsiders – and which coding agents do they use? → compatibility (step 2), where the skill is installed (step 0), wiki vs. docs (step 3).
  3. Where does the code live or should it live (platform, public/private), and is the repository the deliverable itself? → remote (step 0), repository layout (step 1).
  4. Which languages, frameworks, build and test tools are set or preferred? → scripts (step 5), guidelines (step 7).
  5. Should agents run unattended, on a schedule, or overnight – and on which operating systems? → autonomous runs, freilauf or start scripts (step 6).
  6. What must an agent never touch without approval (production, customer data, payments, sending mail, deployments)? → red lines and security (step 6).
  7. Is there knowledge outside the code an agent will need (operations, access, domain rules, past decisions)? → knowledge store (step 3).
  8. What has hurt in similar projects before, or what worries the user about letting agents work? → pitfalls, evaluator focus (step 8).
  Answers you already have from looking at an existing project are not asked again – confirm them in one sentence instead.
- Working style: step by step, per step present the options with a reasoned recommendation (with your agent's question tool, otherwise as text), await the answer, record the result immediately – **one sentence per note**, technical terms, with a rationale where a rule would otherwise be unintelligible. You replace placeholder comments in `AGENTS.md` with content or remove them.
- **Two places, no duplication:** `AGENTS.md` is for regular operation – 99 % of the time the agent works WITH the harness, not ON it: project facts, librarian rules, evaluator rules, workflow, operating tools, pitfalls. Everything harness-internal goes into the project's `HARNESS.md`: skill version, setup status, the coding agents in use and what they support, sync duties, decisions with their reasons, deviations from the skill's templates, open points. `HARNESS.md` is loaded only when someone works on the harness – that keeps `AGENTS.md` short. If the project gets a wiki (step 3), `HARNESS.md` remains the authoritative place for the harness state; the same decisions go into the wiki on top, so that a session which never loads this skill still finds them through the librarian.
- Install nothing the user has not confirmed; write no secrets into files; machine-specific values belong in `CLAUDE.local.md` (gitignored) or environment variables.
- The user may skip steps. You note skipped steps under "Open points" in `HARNESS.md` and name them to the user at the end.
- Keep order: a new harness building block (script, subagent, skill, MCP entry) gets its sentence in `AGENTS.md` immediately – a building block that is unknown does not exist for the agent.

## Step 0 – Where the harness lives, then the language

The harness files were just built into the project by `scripts/build.py` (route A of
`SKILL.md`). Nothing has to be detached from anything: the project has no link to this skill's
repository, and this skill stays a git clone that is updated with `git pull`.

1. **Repository.** If the project is not a git repository yet (`git status` fails), settle it
   with the user – ask, do not assume:
   - **Where does it live?** GitHub, GitLab, Bitbucket, an internal Gitea or Azure DevOps, or
     nowhere at all for now. Many teams and most companies are not on GitHub, and plenty of
     people want no remote at all at first.
   - **Public or private?** Default to **private** and say why: this repository will accumulate
     a knowledge store, internal notes, and rules that reveal how the team works. If it is ever
     to become public, that content must be reviewed *before* the switch – a public git history
     cannot be un-published.
   - Only then `git init`, create the remote and wire it up. If the user is undecided, leave
     the repo without a remote and note it under "Open points" – that costs nothing.
2. **Where this skill is found.** Colleagues and unattended runs must be able to load the
   `harness` skill too, otherwise "load the skill `harness`" in `AGENTS.md` dead-ends for them.
   Two ways, pick with the user and record it in `HARNESS.md`:
   - **User level (default):** every developer clones the skill once into their agent's skill
     folder (`git clone https://github.com/hwalde/harness-skill ~/.claude/skills/harness` for
     Claude Code; other agents per [agent-compatibility.md](agent-compatibility.md)). One
     clone serves all projects and `git pull` updates it. The "Harness knowledge" section of
     `AGENTS.md` carries the one-line install instruction as the fallback – keep it there.
   - **Project copy:** a team that cannot rely on user-level installs gets a full copy of this
     checkout inside the project (`.claude/skills/harness/`, everything except `.git`;
     `build.py` then runs from there). Note the copied version in `HARNESS.md` – it does not
     update itself: refresh it by re-copying from an updated clone, then run route E.

Then the language question.

The harness files (`AGENTS.md`, subagents, wiki skeleton) are written in English – agents read
them regardless of the project language; this skill's own documents stay English in any case.
- Ask in which language the user works with the agent and in which language the project's
  documentation and comments are kept; note that under "Project".
- If the user wants the built files in their own language, translate them now, once, in place
  in the project (keep structure, paths, commands and protocol tokens such as
  `NOT IN WIKI`/`PASS`/`NEEDS_WORK` consistent), then run `python3 tools/sync-agents.py`, and
  record the translation as a deviation in `HARNESS.md` – route E must not overwrite it. There
  is deliberately only ONE edition per project – no language mirrors, no sync effort.
- The scripts in `tools/` speak English (source-code language) – that stays.

## Step 1 – Getting to know the project
Look around (repo structure, build system, existing rule files, `docs/`, tests, CI) and ask about what you cannot see:
- What is it about (one sentence)? Application type: command line, library, web application, desktop application, service/API, data pipeline – this decides step 4.
- How is it built, tested, started, released? Is there one single correct way (→ later an ALWAYS/NOT rule)?
- Is the folder tree cut by domain (modules) or by technology (layers)? (→ step 3)
- What regularly hurts (pitfalls)?
**Settle the layout, because everything else hangs off it.** Two patterns work; pick
deliberately and record the choice with its reason in `HARNESS.md`:

| | **One repository** – harness and project together | **Mother and child** – the harness is its own repo, the artifact sits in a gitignored subfolder |
|---|---|---|
| Fits when | the release is built and shipped elsewhere, so it does not matter that harness files travel along – most company projects | the repository *is* the deliverable and must contain nothing else: a published library, an open-source project, anything where a stranger clones the artifact |
| Cost | harness material is in every clone of the project | two repos to keep straight; the agent must know which one it is touching, and CI/merge tooling usually only sees one of them |
| Bonus | nothing to coordinate | the harness can be swapped, versioned and improved independently of the project |

With the mother/child pattern, be explicit about the consequences: gitignore the child in the
mother, state the split as a rule in `AGENTS.md` ("nothing lands in `<child>/` that does not
belong in a release"), and enforce it mechanically in a check script rather than by good
intentions. Anything that merges, gates or schedules from outside will see only the mother, so
committing and pushing the child stays the agent's own duty – say so, or it will be forgotten.

Enter "Project" and "Pitfalls" in `AGENTS.md`. If the harness was built into an existing project: work existing `CLAUDE.md`/`AGENTS.md` content into the new `AGENTS.md` (only what always applies, see [rule-files.md](rule-files.md)), reduce `CLAUDE.md` to `@AGENTS.md`.

## Step 2 – Coding agents and their capabilities
1. Ask which coding agents work in this project (Claude Code, Codex, Gemini CLI, Cursor, opencode, Copilot, hermes, others) – including the colleagues' ones.
2. Investigate **each named agent, afresh**, per [agent-compatibility.md](agent-compatibility.md): rule file and includes, subfolder rule files, rules, custom subagents, skills, slash commands, project-local MCP configuration, hooks/cron, no-questions mode, headless start. Official docs plus `--help` on this machine; when in doubt, a probe.
3. Implement:
   - Subagents: the source is `.claude/agents/`; generate the format for every additional agent (extend `tools/sync-agents.py` if a target format is missing).
   - Skills: can every agent in use load the `harness` skill from where it is installed (step 0)? Otherwise link or copy it to that agent's skill folder. If an agent knows no skills at all, add to `AGENTS.md` the path of the installed skill's `SKILL.md` so that agent reads it directly.
   - Rule files: confirm the rule `CLAUDE.md` = `@AGENTS.md` (one sentence is already in `AGENTS.md`); for agents with their own file name (e.g., `GEMINI.md`) the same include solution or the configuration that reads `AGENTS.md`.
   - `tools/agent-start.py`: check the flags in the table at the top of the script against the installed versions (`doctor`, `--dry-run`).
4. Per agent **one sentence** under "Coding agents in use and what they support" in `HARNESS.md`, plus every sync duty that arises (e.g. "after a change in `.claude/agents/`: `python3 tools/sync-agents.py`"). Into `AGENTS.md` goes only what regular operation needs – if step 2 produced no such rule, nothing goes there.

## Step 3 – Knowledge storage
Read [knowledge-storage.md](knowledge-storage.md) for this and decide with the user:
1. **LLM wiki with librarian – yes or no?** Yes if there is knowledge that lives in no repo (operations, access, domain, decisions) and the project is alive. No → remove `.my-memory/`, `.claude/agents/librarian.md` (and generated variants) as well as the wiki section in `AGENTS.md`; instead a `docs/` folder with the sentence "Before you start work in this project, check the `docs` folder for a document touching your topic, and read it" plus one line on what is stored there and what not.
2. **Sharpen the rules:** What concretely belongs in the wiki (or in `docs/`) in this project, what does not? Name examples from the project (e.g., "deploy order and its why: in; endpoint list: out – it is in the code"). Put the sharpened examples as half-sentences into the wiki section of `AGENTS.md`.
3. **Check alternatives and combine if useful:**
   - Rule files in subfolders: only if the folder tree is domain-cut **and** the agents in use load them situationally (step 2). Then create `AGENTS.md` + `CLAUDE.md` (`@AGENTS.md`) per domain module – only with what goes beyond normal use.
   - Link documents from `AGENTS.md` (one sentence suffices, see above).
   - rules files: explain what they are (path-bound rules, loaded only when matching files are touched), check whether the agents support them, and create them if needed (e.g., test rules only for `tests/**`).
4. Record the operating rules as sentences in `AGENTS.md`, the decision itself with its reason (wiki or alternative, and why) in `HARNESS.md`; with a wiki: ingest this session's setup decisions via the librarian at the end (context: "this project's harness").

## Step 4 – Enablement: MCP servers and access
Read [mcp-and-tools.md](mcp-and-tools.md). Goal: the agent obtains information itself, can test itself, and can look at things itself.
1. **Web application → recommend the Playwright MCP:** the agent can operate the application through the browser, try things out, take screenshots, read the console and network. Give the note: this replaces no unit/E2E tests. Discuss the setup (fresh browser vs. its own row of tabs; headless on servers).
2. **Desktop application → recommend cua-computer-use:** the same for desktop apps. A rule in `AGENTS.md` that computer use is allowed for debugging – otherwise it will not use it.
3. **Further servers only with a use case:** ticket/CI/wiki systems (first check whether a CLI suffices), read-only mailbox, databases, vision, image generation. For each candidate apply the decision rule MCP vs. script and state the context price.
4. **Access and red lines:** What may the agent read, what execute, what never without approval (sending email, deployments, production systems, payments)?
5. Implement: project-local MCP configuration (file name per agent from step 2), secrets via environment variables, the rule "for X ALWAYS tool Y" in `AGENTS.md`, check context consumption before/after.

## Step 5 – Scripts that support the agent
Read [scripts.md](scripts.md). Ask: which manual work regularly comes up here that is algorithmic? Typical candidates: starting/stopping servers with pre-checks and restart protection, log analysis with navigation, test runners with diagnosis preparation, build/release via exactly one path, database migrations, status checks (is the service running, is the port free, does the health endpoint report errors), counting/measuring.
**Before building anything, ask whether a script is the right answer at all.** Three questions
settle it, and the third is the one people skip:
1. *Is the task algorithmically decidable?* If it needs judgement, it stays with the model. A
   script that guesses is worse than no script.
2. *Can a script actually carry it end to end?* Some tasks depend on things a script cannot
   supply – a credential, a key, a human decision, a system that may be down. That is not a
   reason to abandon the script; it is a reason to **split it into stages** so a failure leaves
   a comprehensible state instead of a half-finished one, and to have it *report* what it
   cannot do rather than fail obscurely. A release script is the classic case.
3. *What happens when it aborts?* Write the failure output as an instruction to act. If the
   honest answer is "an agent has to debug this", then the script is the wrong shape - simplify
   it until its failure modes are few and each one names its own remedy.

**Link scripts and subagents deliberately - they cover different ground.** A script decides the
mechanical questions; a subagent judges the rest. The join is the script's output, which lands
in the context as a prompt: have a `dry-run`/`preflight` stage end by naming the evaluator that
must run next and what only that evaluator can judge. That way the mechanical gate cannot be
mistaken for an acceptance, and the agent is told - in the moment it matters - that a green
script is not a green review. Conversely, keep out of the evaluators anything the script
already decides: a model re-deciding a settled mechanical question only produces noise and
duplicate findings.

- For each desired candidate: build it following the ten principles (Python preferred, no venv, help without arguments, human-readable output, exit quickly, error message as an instruction to act) under `tools/`, test it, record it with one sentence each in `AGENTS.md` – including "replaces X, NOT Y anymore" where an old path exists.
- Check whether the project's existing scripts are agent-friendly (data dumps, JSON blobs, long-runners) and propose conversions.

## Step 6 – Autonomous runs, monitoring, security
Read [autonomous-runs.md](autonomous-runs.md) and [freilauf.md](freilauf.md).
1. **No-questions runs:** show `python3 tools/agent-start.py doctor` and a `--dry-run`; set up the agent's permission mode and allow list for the mode without follow-up questions (for Claude Code `dontAsk` plus `permissions.allow` in `.claude/settings.json` – the skill builds a minimal one with the read-only git commands, the harness scripts, and the `SessionStart` hook that runs `tools/bootstrap.py`; extend it project-specifically). Note that some agents refuse to let a running agent widen its own permissions – if an edit to that file is blocked, that is by design: hand the change to the user rather than routing around it. Read the two deny-list limits in [autonomous-runs.md](autonomous-runs.md) before relying on a deny for anything irreversible. Recommend tmux (macOS/Linux) or psmux (Windows) if runs should keep running in the background and be observable. The entry in "Tools and scripts" exists – extend it project-specifically if needed (e.g., default agent, default model).
2. **Usage tracking:** only relevant with subscription quotas – but there practically mandatory for long runs, because at 100 % the subagents die or hang and the run is dead. If yes: clarify the data source (quota command, status data, API) and build a usage script per [scripts.md](scripts.md); the rules (shorten the interval, wait from 90%, subagents check themselves) into `AGENTS.md` or into the prompt template for runs. Costs separately.
3. **Self-monitoring:** does the project need someone who periodically looks for hanging scripts and lost agents? If yes: a check script (`tools/watch.py` or similar) and the instruction to check every N minutes via the agent's cron/loop tool (e.g., `CronCreate`, `/loop`); name the tool explicitly; test beforehand with a trivial task.
4. **Not stopping:** the agent's goal command or loop (clarified in step 2); the order "question round first, then goal" as a rule for runs.
5. **Security:** sandbox (micro-VM/container) or at least worktree + Git + no production access. Split as always: the red line the running agent must obey ("no production access without approval") into `AGENTS.md`, the decision itself with its reason (why sandbox, why only worktree) into `HARNESS.md`.
6. **Superstructure – offer freilauf explicitly.** As soon as runs should happen unattended,
   on a schedule, or across several repos, ask the user whether they want
   [freilauf](https://github.com/hwalde/freilauf): a self-hosted hub that starts runs on a
   schedule, gives each its own worktree and tmux session, watches them from outside, gates on
   budget, merges the result back and notifies. A project with this harness runs in it without
   adaptation.
   - **Step F of `SKILL.md` owns the details:** read freilauf's current README first, check
     whether it is already installed, say that it runs on Linux only, and install it – if the
     user wants it – by following its `SETUP_WITH_AGENT.md` to the end. Do not improvise an
     installation from memory.
   - **Say plainly that freilauf brings its own system**, because it changes assumptions this
     harness otherwise leaves open: every run gets a fresh **git worktree**, so anything
     untracked or gitignored that a run needs must be declared as a worktree extra; scheduling,
     merging and pushing move out of the agent's hands and into the hub; and "done" becomes
     whatever the hub's finish gate says it is. Read [freilauf.md](freilauf.md) before
     configuring it, and record the resulting configuration in `HARNESS.md` – its UI
     and field names change between versions, so what you write down is a dated snapshot, not
     a contract.
   - If the user does **not** want freilauf (or cannot run it – Linux only), continue with
     item 7.
7. **Named start/attach scripts per agent and OS – offer them whenever freilauf is not used.**
   First explain the purpose in the user's words (section "Named start and attach scripts" in
   [autonomous-runs.md](autonomous-runs.md)): one command that starts an agent for a
   long-running task without a single permission prompt, in the background where tmux/psmux
   exists, and one command to attach to it; ordinary work starts the agent normally; freilauf
   would be the hub above the projects, these scripts are the local edition inside this one.
   Then ask two things: which operating systems must the scripts support (Linux, macOS,
   Windows), and which coding agents (from step 2). Then **write the scripts yourself** from
   the templates in `assets/start-scripts/` of the skill – its README names the placeholders
   and the procedure – and adapt each one to the project (default model, pre-checks, prompt
   files). Then **test every script for real**: check the mode against the installed agent
   (`<agent> --help`), start a short real task through the script, attach, read the screen,
   end the run; fix `tools/agent-start.py`'s table or the script where it does not behave.
   Templates are drafts – never hand a script over untested. One sentence per script pair in
   `AGENTS.md` under "Tools and scripts" (purpose, "NOT for scheduled or multi-repo runs –
   freilauf"); what could not be tested on this machine is noted as untested in `HARNESS.md`.

## Step 7 – Architecture and coding guidelines
This is the most important content step. Read [rule-files.md](rule-files.md) and [skills-and-commands.md](skills-and-commands.md).
1. Ask about architecture (style, layers/modules, dependency direction, persistence, error handling, logging) and coding guidelines (language/version, formatting, naming, tests, reviews). Are there documents? Read them.
2. **Core rules (Pareto, about 20 lines)** under "Architecture and coding guidelines" in `AGENTS.md` – only what always applies and what a model does not know anyway.
3. **Create the catalog as a skill** (`.claude/skills/coding-guidelines/SKILL.md`, with reference files if needed), description with the team's keywords ("code review", "guidelines"); in `AGENTS.md` one sentence on when to load it (if mandatory: ALWAYS before acceptance). Optionally a second skill for the architecture documentation. Deterministic rules (formatting, linters) belong in scripts/configuration, not in prose.
4. If desired: `evaluator-guidelines` and `evaluator-architecture` as dedicated subagents following the template in [evaluators.md](evaluators.md) – or the standard evaluator with a focus.

## Step 8 – Subagents and evaluators
Read [evaluators.md](evaluators.md).
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
1. Clean up `AGENTS.md`: all placeholder comments replaced with content or removed; **delete the "Setting up the harness" paragraph**; adapt the "Harness knowledge" sentence to the result of step 2 (keep the install fallback; for an agent that knows no skills add the absolute path of the installed `SKILL.md`); check the length – core rules short, details linked; every rule with a rationale, no novels.
2. Bring `HARNESS.md` up to date: skill version, setup status (which steps done, which skipped, with the date), the coding agents in use and what they support, sync duties, every decision with its reason, deviations from the skill's templates, open points. This is where a later rebuild learns what is actually there and why.
3. `python3 tools/sync-agents.py`, `python3 tools/agent-start.py doctor`, `python3 <skill>/scripts/build.py <project> --check` (every difference it reports must be a recorded deviation in `HARNESS.md`), check the agent's context view (rule files loaded? unexpected costs?).
4. Project-specific harness knowledge (own scripts, own evaluators, the reasons) goes into `HARNESS.md` and the wiki – never into this skill. If the setup revealed a gap in the skill's documents, note it as a suggestion for route G.
5. Call the **evaluator**: task "harness setup", criteria = checklist below, evidence = `AGENTS.md`, `HARNESS.md`, created files, script outputs. Until `PASS`.
6. With a wiki: ingest the decisions with their rationale via the librarian as well. Name open
   points to the user as a list.
7. **Commit, and push if there is a remote.** The setup is only real once it is committed: an
   agent in a fresh session reads files, not this conversation. If step 0 produced a remote,
   push; if it deliberately produced none, say so in the final report so the user is not left
   assuming their harness is backed up somewhere. Check `git status` for anything that should
   have been gitignored rather than committed – a knowledge store belongs in the repo, a
   `.env`, a key or a machine-specific path does not.

## Checklist (criteria for the evaluator)
- [ ] Language settled (built files translated once if wished, recorded as a deviation); skill install location settled and recorded
- [ ] `AGENTS.md`: project, language, pitfalls, knowledge-storage rules, operating tools/scripts, architecture core rules, quality assurance (evaluators + when), standard workflow – no placeholders left, setup paragraph deleted, nothing harness-internal
- [ ] `CLAUDE.md` = `@AGENTS.md`; the rule for subfolders is in place; subfolder rule files (if chosen) have both files
- [ ] Subagents in all needed formats (`sync-agents.py` run); unneeded subagents removed
- [ ] `harness` skill (and guideline skill, if created) loadable by every agent in use – or its path in `AGENTS.md`
- [ ] Wiki decision implemented (skeleton + librarian, or removed + `docs/` sentence)
- [ ] MCP servers only with a use case, configured project-locally, rule "ALWAYS for X"; secrets not in the repo
- [ ] Scripts per the ten principles, tested, recorded
- [ ] `agent-start.py doctor` and `--dry-run` run; permission mode/allow list set up if autonomous runs are desired; without freilauf: named start/attach scripts offered, written by the agent for the chosen OS and agents, tested with a real run, recorded
- [ ] Security settled: red lines in `AGENTS.md`, the decision with its reason in `HARNESS.md`
- [ ] `HARNESS.md` reflects the setup: skill version, setup status, agents in use, sync duties, decisions with reasons, deviations, open points
- [ ] Git repository and remote settled (platform, visibility) or deliberately absent; `build.py --check` clean apart from recorded deviations
- [ ] Repository layout chosen (one repo, or mother/child) and recorded with its reason
- [ ] freilauf offered; if chosen, installed, configured and its configuration recorded as a dated snapshot
- [ ] Everything committed; pushed if a remote exists
- [ ] Open points listed
