# Rule files: AGENTS.md, CLAUDE.md, subfolders, rules
**Core:** The rule file is read at every start – only what always applies belongs in it, plus the pitfalls that hurt. Everything task-specific is moved out and linked. (Context: harness template | As of: 2026-08-30)

## Two names, one file
- `AGENTS.md` is the cross-agent standard; Claude Code reads `CLAUDE.md`. This template's solution: **`CLAUDE.md` contains exactly one line `@AGENTS.md`** (Claude Code's include syntax), all knowledge lives in `AGENTS.md`. Rule: in every folder where an `AGENTS.md` is created, a `CLAUDE.md` with `@AGENTS.md` is created next to it. In the context both appear as memory files; check with `/context` (Claude Code) or the agent's context command.
- File names in upper case (some agents accept lower case, best practice is upper case).
- `CLAUDE.local.md` (or the agent's counterpart): read at the same moment but stays local with the developer (gitignored) – for personal preferences and machine-specific values (ports, paths).
- Which agents read what and whether they can do includes: [agenten-kompatibilitaet.md](agenten-kompatibilitaet.md).

## The four places
| Place | Purpose | When read |
|---|---|---|
| Project root | overview, rules, workflow, pitfalls | immediately at start |
| Parent folder (monorepo) | what all subprojects share | immediately at start (open a subproject → the parent is read along) |
| User folder (e.g., `~/.claude/CLAUDE.md`) | cross-project personal rules (language, spelling) | immediately at start |
| Subfolder | only for work in this folder (domain module) | **situationally** – only when the agent reads a file there or works there; nested subfolders pull in the files above them |

Situationally loaded rules land at the end of the chat – the position the model pays the most attention to. That makes subfolder rule files and rules files more effective than the same text in the root.

## What belongs in – and what does not
**In (about 20 lines of core rules):**
- Project description in one sentence; rough structure (deliberately incomplete).
- The most important architecture and coding rules (Pareto: 80/20 – "we use DDD, we do X in way Y"), not the thousand guidelines.
- The standard workflow (order of the steps, see [workflow.md](workflow.md)) and the acceptance duty (evaluator).
- Tools and scripts that are to be used – one sentence each, emphatic: "For X ALWAYS `tools/y.py`, NOT z."
- "Pitfalls that hurt": things whose absence produces a lot of pain ("after changing X, clear the cache in the store, or the app won't start"). The only exception to the frugality rule.
- Testing notes (may be a bit more detailed).
- References: "where do I find what?" – documents, folders, skills, and who knows the rest (librarian).

**Not in:**
- The obvious that every model knows (`npm run dev`, "this is a React project", what a repository is, the layer model).
- Situational details, coding-guideline catalogs, novels, long document lists – that belongs in linked documents, subfolder rule files, rules, or skills.
- Outdated rules: they are dutifully followed and turn the file into dead weight. On any misbehavior, look into your own rule file first.
- Secrets, machine-specific values (→ `CLAUDE.local.md`, environment variables).

Anthropic cut 90% of its own prompts in Claude Code because they no longer helped but constrained. Attitude: keep it small, prefer linking artifacts (even complex ones: test suite, diagram, documentation folder) – the agent finds the right thing in them itself.

## Moving out and linking
- Second document: "If X comes up, read `docs/x.md`." The content lives only there.
- Whole folder: "Before you start work in this project, check the `docs` folder for a document touching your topic, and read it." The reverse direction: store newly worked-out results there – **always state what should be stored and what not**, otherwise the agent stores the unusable.
- Linking pattern instead of a custom subagent: the descriptions of all custom subagents sit permanently in the context (order of magnitude: a few thousand tokens). A three-liner "If you want to know X, start a subagent that reads `docs/x-expert.md` and follows the instructions" has the same effect without the standing cost. A custom subagent only when it is needed constantly or carries a lot of knowledge/a clear role (evaluator, librarian).
- A skill instead of a rule file for knowledge that does not concern every run (coding guidelines, evolution knowledge of a system whose entry point is itself an agent) → [skills-und-commands.md](skills-und-commands.md).

## Subfolder rule files (domain modules)
- Prerequisite: a domain-cut folder tree (screaming architecture – from the outside you can see what it is about) and an agent that loads rule files in subfolders situationally (check in [agenten-kompatibilitaet.md](agenten-kompatibilitaet.md) – the snapshot there lists it for Claude Code and Codex, among others; verify during setup).
- In: only what goes beyond normal use – module-specific pitfalls, conventions, interfaces. Not: what a service or repository is.
- Here too: `AGENTS.md` + `CLAUDE.md` with `@AGENTS.md` side by side.

## rules files (path-bound rules)
- What: prompt files whose validity is bound to file paths/patterns – they are loaded only when the agent touches a matching file. Example: styling rules only for test files, frontend conventions only for `src/ui/**`.
- Where: Claude Code `.claude/rules/*.md` with frontmatter `paths:`; Cursor `.cursor/rules/*.mdc` with `globs`/`alwaysApply`; GitHub Copilot `.github/instructions/*.instructions.md` with `applyTo`. Other agents: [agenten-kompatibilitaet.md](agenten-kompatibilitaet.md).
- Rule of thumb: a rule that should only be read situationally belongs exactly there – not in the root rule file.

## Write for the AI, not for humans
- The audience is the model: its own vocabulary, technical terms/buzzwords instead of explanatory sentences, crystal clear, no politeness prose. Human documents in two versions if needed (detailed for humans, terse for the AI).
- **Justify rules:** instructions with a rationale are followed more reliably. Never argue against the system prompt ("the system prompt's rule is lifted") – higher weighting, prompt-injection suspicion. Instead demand usage, raise urgency, justify.
- IMPORTANT / NOT / ALWAYS for critical rules – agents notice these.
- Numbers instead of adjectives: "max. three sentences" works more reliably than "short". But: "at most three sentences" always delivers three sentences, "token-frugal" delivers the unintelligible – check the result, test, then commit.
- Have the agent phrase rules for itself (meta-prompting): state the goal ("What must go into `AGENTS.md` so that the librarian keeps being consulted?") plus the frame: very compact, written for yourself, do not talk about other agents, one to three sentences. `/init` results are almost always too long – demand brevity in the call.
- If you repeat a sentence for the umpteenth time in the chat, have it added to the rule file in the same request ("for unreadable web pages use the Playwright MCP"). This is how the harness grows on the side.

## Anti-patterns
Situational details or guideline catalogs in the root · the obvious · novels · outdated rules · rules without a rationale · scripts/tools not mentioned · a storage instruction without "what goes in, what stays out" · evaluator without an acceptance-duty entry · human texts 1:1 for the AI · lower-case file names.
