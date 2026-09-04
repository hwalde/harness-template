# Knowledge storage: LLM wiki, alternatives, rules
**Core:** Working with coding agents is to a large extent knowledge management. Only what is not in the source code belongs in the store; every piece of information belongs to exactly one context; whoever runs a store buys a maintenance duty. (Context: harness skill | As of: 2026-08-30)

## Six ways to give an agent knowledge (freely combinable)
| Way | Description | When |
|---|---|---|
| 1. Link documents from `AGENTS.md` | "Before you start work in this project, check the `docs` folder for a document touching your topic, and read it." Reverse direction: store newly worked-out results there – with an instruction on what is worth storing and what not | small to medium projects, few documents, the team maintains docs anyway |
| 2. Rule files in subfolders | module-specific knowledge lives with the module and is loaded situationally | domain-cut folder tree + an agent that supports it ([rule-files.md](rule-files.md)) |
| 3. rules files | path-bound rules (only for `tests/**`, only for `src/ui/**`) | the agent supports rules; rules attach to file types/areas |
| 4. Skills | knowledge is loaded only when it is needed | guideline catalogs, evolution knowledge, how-tos ([skills-and-commands.md](skills-and-commands.md)) |
| 5. LLM wiki with librarian | a structured store with a subagent as the only access | knowledge across many systems/repos, decisions with rationale, operational knowledge, domain knowledge; long-lived projects |
| 6. MCP server / scripts as knowledge source | a Confluence MCP, a script that delivers docs | when the source lies outside; Confluence content is written for humans and often a garbage dump – agents fail on it just the same |

Prerequisite for all of them: **the model must learn about it** – one sentence in `AGENTS.md`. No RAG/embedding chunking: findability via folder tree + index files works better.

## What belongs in a knowledge store – and what does not
**In:**
- Knowledge that is **not evident from the source files**: decisions with their rationale (the why), pitfalls that cannot be seen in the code, operations/access/infrastructure knowledge, domain and business knowledge, conventions, pointers to the source of truth.
- Your own expert knowledge in areas where models are still thin.

**Out:**
- What is in the source code anyway: "Whoever writes down what is in the source code has two truths – and they drift apart." Codebase-derivable detail (inventories, field lists, endpoint catalogs, counts) drifts and becomes wrong → at most a pointer.
- What the model knows anyway.
- Transient runtime knowledge: a question just answered, progress/status notes, log output, intermediate states, trivia.
- Secrets – only the reference to where they live.

Guiding question: **"Will a future session need this?"** When in doubt, do not ingest. The smarter the model, the fewer knowledge documents it needs; with small/local models they are all the more valuable.

## The LLM wiki (Karpathy pattern) as the skill builds it
```
.my-memory/
├── raw/    immutable originals (append-only)
└── wiki/   condensed, cross-linked pages; index.md per folder (one sentence per entry); log.md
```
- Navigation top-down: always the `index.md` first, then proceed deliberately; cross-references as in an encyclopedia. Two quality rules: index descriptions terse and precise (signpost, not a changelog); nothing the model knows anyway.
- The **librarian** (`.claude/agents/librarian.md`) is the only gate: it fetches knowledge (QUERY) and stores it (INGEST), filters as gatekeeper (library vs. runtime knowledge), enforces context scoping, and returns only the essence – the main agent reads no wiki files and does not have to ponder what goes where. Two attitude rules: it never argues against decisions, and it flags old knowledge as possibly outdated.
- Rules in `AGENTS.md` (compact, justified): ask at the start of work, before the user is asked; ingest the lasting at the end; never read or write `.my-memory/` directly. If the agent ignores the librarian, have the model rephrase the rule itself – compact, justified, without arguing against the system prompt.
- **Context scoping:** every piece of information belongs to a context (project, subsystem, target audience, customer, tool) – modeled as a folder subtree; otherwise the agent links the unrelated.
- **Curation** (a standing duty): knowledge ages and then works against you. Periodically, deliberately triggered (MAINTENANCE mode; for large wikis a dedicated curation skill): merge redundancy, convert drifting detail into pointers, mark the outdated, straighten index descriptions, remove dead links. Never in passing, never without approval for deletions.
- Balance from practice: very proven across projects (a network of several repos/systems); for a single, strongly code-centric project a `docs` folder can suffice.

## Decision aid during setup
| Question | Yes → | No → |
|---|---|---|
| Is there knowledge that lives in no repo (operations, access, domain, decisions), and will the project live longer than a few weeks? | LLM wiki with librarian | `docs` folder + link from `AGENTS.md` |
| Is the folder tree domain-cut and does the agent load subfolder rule files? | module-specific knowledge in subfolder `AGENTS.md` | in `docs/` or the wiki |
| Do rules attach to file types/areas and does the agent support rules? | rules files | subfolder rule file or an `AGENTS.md` section |
| Is there a large guideline/how-to catalog? | skill | a short section in `AGENTS.md` |

If the wiki is not used: remove `.my-memory/`, the librarian, and the wiki rules in `AGENTS.md` (half installations confuse the agent more than they help).
