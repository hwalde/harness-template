# Workflow: from assignment to accepted work
**Core:** A standard workflow in `AGENTS.md` fixes the order: gather prior knowledge → plan (as much as needed) → implement with deterministic checks → evaluator loop → update documentation and wiki. The counterpole to a lot of planning is a terse goal with a check criterion. (Context: harness skill | As of: 2026-08-30)

## The standard workflow (a suggestion for `AGENTS.md`, tailor during setup)
1. **Prior knowledge:** librarian QUERY with the intention; read linked documents that touch the topic (subfolder rule files the agent loads situationally).
2. **Plan as much as needed** (levels below). Write acceptance criteria in checkable form – they are the evaluator's yardstick.
3. **Implement.** The deterministic via script: formatting, linters, static analysis, tests, build. For web/desktop apps look for yourself in between (browser/desktop control), at the end run repeatable tests.
4. **Acceptance:** evaluator with criteria, diff, and evidence; on `NEEDS_WORK` rework and re-check until `PASS`. Focus evaluators by scope of change ([evaluators.md](evaluators.md)).
5. **Follow-up:** update documentation/specification; ingest the lasting via the librarian (only what a future session needs); one sentence in `AGENTS.md` when it was needed for the umpteenth time; release/deploy only via the script designated for it.

That is the order, not a form: a one-line fix needs no plan, but every change needs the acceptance.

## How much planning a task needs
| Level | When | Approach |
|---|---|---|
| 1 – just let it do | not complicated (recolor a button, a small fix) | implement straight from the chat; covers most cases today |
| 1+ – let it plan | a bit more structure desired | the agent's planning mode → technical plan → implement |
| 2 – plan in a file | level 1 does not carry; the context should be fresh | have the plan written to a file, then **2–4 correction loops** ("go through the transcript once more – is anything missing for the implementation?") – on the first follow-up something essential always surfaces; implementation in a new chat with only the plan |
| 3 – requirements document | genuinely large; a technical plan becomes dead weight (fine at ~800 lines, bad at 4000) | domain requirements with key numbers (what, not in which file) + implementation packages (every requirement assigned to at least one package – correction loop) + **testing requirements per package** + with a weak harness testing information (usable tools, API docs, MCP servers). Two extra requirements per package: after implementation, reread the document and check off; add terse implementation notes for subsequent packages. One chat or subagent per package |

From this the cycle **read document → work → update document**: the requirements or plan document remains the continuously updated knowledge source for the next chat or subagent.

**Counterpole (preferred where possible):** goal + check criterion instead of a process plan. "The pipeline must cost under 10 dollars; check that via the cost query at X." The prompt work does not disappear, it moves from the procedure into the goal and the criterion ([autonomous-runs.md](autonomous-runs.md)). Frameworks that elicit requirements (Spec-Kit-like) are training wheels – useful as long as you are unpracticed.

**Pre-workflow:** ticket + braindump (everything the agent cannot know: meetings, direction, concerns, your own questions) → 3–8 subagents in parallel as information gatherers ("how did we build X, would a refactoring be needed?") → have the agent propose solution paths, the human decides. The chat is then "a garbage dump with pearls"; from level 2 on, only the pearls are passed on.

## Testing in the workflow
- The test pyramid stays. Tests are more valuable with AI than before, because the agent validates its own result with them; E2E tests at the end, happily written already at the start; for parser-like tasks provide input/output pairs ("build yourself unit tests from these").
- Do not hand over a manual test playbook to be played through – have repeatable E2E tests generated from it (clicking through depends on the day's form).
- Browser/desktop control is for looking in between, not for testing; deterministic state checks (server running? port? health? log?) are scripts.
- Prepare test results for the agent (script: repeat failed tests individually, browser log/network/server log per test, age of the entries) – agents have no sense of time.
- After restructurings: "Straighten the tests; if you find a bug, do not paper over it, write it down."
- Human final acceptance remains where human-visual judgment matters (the sensibleness of user interfaces, special software, video). Place it at the end and do not have the agent check every edge case by screenshot along the way.

## Phrasing assignments (short version)
- Crystal clear, factual; include the **why** and the quality level (a prototype for a demo vs. a production system).
- Context: write it in, have it fetched (and say where), or – harness – have it fetch it itself.
- Examples sparingly with top models (the source code is the example: "like the user service"); plentifully with small models.
- Prescribe the approach only when your own observation stands behind it; otherwise name the capability ("use subagents") and leave the deployment to it.
- Behavior for the unforeseen: boundaries and abort conditions ([autonomous-runs.md](autonomous-runs.md)).
- Name tools explicitly (demand or forbid); limit outward actions ("fill in, do not submit").
- Frame third-party text in XML tags; "format, do not rewrite"; "write one to one into a file".
- Assignments to other instances/subagents as a **letter**, not a list of commands: "Consider that the instance is the same model as you and will fully engage with this – leave it room to think."
- Three control questions: "Restate in your own words what I said." · "Are there open, **relevant** questions?" · after overplanning: "Are there contradictions?"
- Numbers instead of adjectives for scope; text volume is measured by a script.

## Follow-up-question policy
Decide during setup: interactive (follow-up questions allowed, preferably bundled and with the agent's question tool) or fully autonomous (no follow-up questions except on demand; make the best justified assumption, document it, keep working; a question round only before the start). For unattended runs, the latter always applies.

## Dynamic workflows and evaluator chains
- Normal: the main agent starts a subagent → reads the report → thinks → the next one. A **dynamic workflow** (Claude Code: workflow script) saves the in-between: the main agent writes a script of subagent calls (each with model, type, prompt, output schema), executes it, gets a report at the end; results flow as text into the next prompt. Advantage: no thinking between the steps; disadvantage: exactly that is missing. Only with the user's explicit consent – many agents, many tokens.
- Several evaluators in sequence can be modeled this way as a chain (one's findings in the next one's prompt) or simply called sequentially by the main agent.
- The main agent as manager: on long runs it only orchestrates; subagents implement. Swarms with roles and communication rules have not proven themselves.

## The harness grows on the side
Every sentence you type for the second time becomes a rule; every piece of manual work that is algorithmic becomes a script; every recurring check an evaluator; every successful procedure a skill ("Are there parts we should reuse as a skill?").
