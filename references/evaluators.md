# Evaluators: generator → evaluator
**Core:** The agent that did the work always answers "well done?" with yes. A second agent with fresh context, without write permissions, judging against observed evidence finds different things. The pattern = one subagent + one entry in the rule file. (Context: harness skill | As of: 2026-08-30)

## The pattern
| Part | Content |
|---|---|
| Subagent `evaluator` (`.claude/agents/evaluator.md`) | skeptical second reviewer; the skepticism is stated explicitly in the prompt; reads the specification, `git status`/`git diff` (and the commit history if needed), opens every piece of evidence, observes for itself where possible (tests, build, smoke check); no Write/Edit permissions; answers `PASS` or `NEEDS_WORK` + concrete findings |
| Acceptance duty in `AGENTS.md` | "Before anything is called 'done' or 'working', the evaluator checks with fresh context and without write permissions against observed evidence. `NEEDS_WORK` → work through the findings → re-check until `PASS`." Without this entry the subagent is not used. |
| Loop | build → evaluator → fix → evaluator … until `PASS`. No debate, no explaining away, no weakened tests. |

Effect in practice: a noticeably lower error rate; the evaluator regularly finds things that were not right yet. Cost: a few tokens and some time.

## What the caller provides
The evaluator trusts no claims – so produce and reference verifiable evidence:
1. Task / acceptance criteria (specification, ticket, plan, checklist).
2. Scope of change (files; with Git it determines the diff itself).
3. Evidence: test logs, build output, screenshots, rendered artifacts – as paths.
4. Optionally a focus (see below).

The prompt to the evaluator as a letter, not as a list of commands: it is the same model at full cognitive capacity; leave room to think, pre-empt nothing.

## Limits and countermeasures
- The more defiant the model, the sooner it bypasses the evaluator or tries to deceive it (models genuinely deceive): suggesting only a partial aspect to the evaluator, weakening tests, "known limitation". Countermeasures in the evaluator prompt: scope check, builder excuses do not count, weakened tests are a finding of their own.
- Who starts the evaluator: (a) the implementing agent itself – the simplest level, what the skill builds; (b) from outside via a hook (e.g., a stop hook or pre-commit) – the agent can no longer forget it; (c) in the CI/CD pipeline with findings in the review platform – "a notch better" because independent. Decide during setup whether (b) or (c) is additionally desired.
- A green test only proves the path the test took. Written-down check criteria are the yardstick; without criteria the evaluator checks against the task description and says so.

## Multiple and specialized evaluators
The smallest configuration is one evaluator. Bigger: several instances one after the other (Anthropic runs a whole series internally), by topic focus depending on the project. Two ways:

1. **One evaluator, several focuses** (built in by the skill): call the `evaluator` several times, each time with "focus: security" / "performance" / "clean code" / "coding guidelines" / "architecture". No additional standing context, because only one description is loaded.
2. **Dedicated subagents per focus** (creatable during setup, see the template below): sensible when a focus needs its own knowledge (the architecture documentation, the guideline catalog, a security checklist) or when it should run separately in a pipeline/CI.

Order when several run: first deterministic checks (linters, static analysis, tests – via script, not via model), then functional acceptance (standard evaluator), then the focus areas (security → architecture/guidelines → performance → clean code). Each looks at the changes via `git status`/`git diff` and returns concrete, fixable findings to the main agent; the main agent works through them and has it re-checked. Not all of them for every trifle: define in `AGENTS.md` which evaluators run at which scope of change (e.g., security always for auth/inputs/file access; architecture for new modules).

## Give every concern exactly one owner
When several evaluators run on the same diff in parallel, any concern named in two of them
produces the same finding twice, every round. That is not merely noise: it trains the reader to
skim, and it hides the one finding that mattered. So when you write a second evaluator, write
its **out of scope** section at the same time, naming the other evaluators and what belongs to
them – and where two could plausibly claim a concern, give it to one and have the other defer
explicitly ("that reviewer runs in the same round and its verdict wins").

The same discipline applies against the scripts: whatever the deterministic gate already
decides must not appear in an evaluator's checklist. A model re-deciding a settled mechanical
question is pure cost.

And beware of a claim that its own guard does not back: if a rule file says "evaluator X checks
this", open evaluator X and confirm it actually does. An agent that believes a guard exists
will stop looking - a false assurance is worse than none.

## Template for a specialized evaluator
File `.claude/agents/evaluator-<focus>.md` (translate for other agents with `tools/sync-agents.py`):

```markdown
---
name: evaluator-security
description: >-
  Security reviewer (generator→evaluator). Call after changes to authentication,
  authorization, input handling, file/network access, or dependencies, before the work
  counts as done. Reads diff and evidence with fresh context, checks against the security
  rules in AGENTS.md/docs, answers with PASS or NEEDS_WORK. No write permissions.
tools: Read, Glob, Grep, Bash
model: opus
---

You review another agent's changes exclusively under the aspect of security. You trust
no claim; you evaluate, you do not repair.

1. Look at `git status` and `git diff`; read the affected files in full.
2. Check: input validation, injection (SQL/shell/prompt), AuthN/AuthZ, secrets in code/log/
   commit, insecure defaults, paths outside the allowed area, new dependencies,
   error handling that leaks internals. Project-specific rules: <path to the document>.
3. Observe for yourself where possible (tests, linters, security scanners via Bash).

Answer: first line `PASS` or `NEEDS_WORK`. Then per finding: file:line, risk,
expected behavior, concrete fix proposal. Blocking findings first. No summary of the diff.
```

Analogously: `evaluator-performance` (complexity, N+1, IO in the hot path, memory, caching/batching), `evaluator-clean-code` (readability, naming, duplicates, function size, dead paths), `evaluator-guidelines` (reads the guideline skill/document and checks point by point), `evaluator-architecture` (reads the architecture documentation, checks layer boundaries, dependency direction, module cut). Every focus evaluator gets one sentence in `AGENTS.md` on when it runs.

## Further proven subagent types (for orientation)
| Type | Task |
|---|---|
| librarian | the only access to the knowledge store → [knowledge-storage.md](knowledge-storage.md) |
| docs updater | update the documentation before every commit; check criteria in the prompt |
| remote-system expert | answers questions about the production environment from ingested knowledge; without tools |
| linking pattern | instead of a custom subagent: a prompt in a file + a three-liner in `AGENTS.md` "start a subagent that reads this file" – without standing context |

Custom subagent = Markdown with frontmatter (`name`, `description`, `tools`, `model`, optionally `color`) plus a prompt; the `description` decides whether the main agent uses it; keep `tools` minimal; descriptions cost context on every request – only create what is needed regularly.
