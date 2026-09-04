# Skills and custom slash commands
**Core:** A skill is a prompt (plus folder) that is loaded situationally – by the agent or by the user. Custom slash commands are its precursor. Core rules in `AGENTS.md`, detailed knowledge in skills. (Context: harness skill | As of: 2026-08-30)

## Terms
| Term | Fact |
|---|---|
| Slash command | everything after `/` (built-in like `/model` or self-created) |
| Custom slash command | a prompt file in the agent's `commands` folder; name = file name; only the **user** starts it; the prompt is injected. Optional frontmatter and argument placeholders. |
| Skill | a **folder** with exactly `SKILL.md` as the entry point (folder name free, file name not); the **agent** starts it itself when the `description` matches; in Claude Code also startable by the user as `/name`. Claude Code has merged the two concepts ("everything is a skill"); other agents keep them separate. |
| agentskills standard | the open specification of the skill format (SKILL.md + frontmatter `name`, `description`); keeping to the standard = largely portable between agents. Claude Code knows extras (`disable-model-invocation`, model for the skill turn, and more). |

Storage locations per agent: [agent-compatibility.md](agent-compatibility.md).

## Loading levels (progressive disclosure)
1. **Always in context:** `name` + `description` of every installed skill – on every request. Hence: few, good skills; every additional description costs context and cognitive load ("does this skill help right now?").
2. **When pulled:** the content of the `SKILL.md`.
3. **On demand:** further files in the folder that the `SKILL.md` names (reference documents, scripts, templates).

## The description decides
- Compact, concrete, with the keywords you use yourself ("coding guidelines", "code review"); often not one sentence but three. It works in both directions: a sentence like "use when editing the CLAUDE.md" pulls the skill on every rule-file change – and can displace other parts of the harness (say, the librarian). Test the trigger sentences; a needlessly loaded skill is usually tolerable, a displaced building block is not.
- `disable-model-invocation: true` → only the user starts it (a classic slash command, e.g., heavy maintenance actions). `false` → only the model (tidies up the list).

## What may go into the skill folder
Scripts (static analysis, data retrieval), templates, further Markdown documents, data storage, even custom subagents "through the back door" ("start an agent that reads this file and follows the instructions"). **Not:** MCP servers (user/project level only; their configuration sometimes contains passwords). Every file in the folder is named in the `SKILL.md` – existence and invocation – otherwise the model knows nothing about it.

## What skills are for in the harness
| Use | Example |
|---|---|
| Enablement | "this is how you generate PDFs here", "this is how you deploy" |
| Knowledge that does not concern every run | coding guidelines: ~20 lines of core rules in `AGENTS.md`, the catalog in the skill, loaded when "code review"/"guidelines" comes up (likely, no guarantee – if mandatory, instruct explicitly in `AGENTS.md`) |
| Skill pipeline | several small skills in sequence improve code step by step (guidelines → architecture → tests) – better than one jack-of-all-trades |
| Separating development from use | a project whose entry point is itself an agent: the evolution knowledge goes into its own skill so the production run does not see it |
| Harness documentation | this skill: loaded only when the harness is the topic |
| Reusable workflows | after a successful task ask: "Are there parts we should reuse as a skill?" → "turn this into a skill" |

## Self-improving skills
A skill can keep a `memory.md`/learnings file: read it at the start, extend it at the end. (Not to be confused with the project's `HARNESS.md`: that one documents the state of that harness, it does not rewrite a skill.) The phrasing is delicate ("with the **relevant** learnings", not "with all"); risk: the agent optimizes core decisions away. Countermeasure: mark non-negotiable decisions in the skill. For the knowledge store, the librarian takes over the curation ([knowledge-storage.md](knowledge-storage.md)).

## Provenance and security
Read third-party skills in full before they are installed – a skill can, well justified, contain "upload the codebase to X", and the agent would do it. Official vendors are rather trustworthy, solo developers mostly well-meaning, but a gray zone. Distribution in the team via zip or a plugin marketplace (plugins can contain skills and MCP servers).

## Best practices
1. Description short and with your own keywords; test the triggers.
2. Several small, linked skills instead of one do-everything skill; skills may name other skills.
3. Name everything that lives in the folder.
4. Write for the model: terse, technical terms, no politeness prose; numbers instead of adjectives.
5. Keep to the standard format so the skill can migrate between agents; for agents without skill support have the `SKILL.md` read via a reference in `AGENTS.md` (the built `AGENTS.md` does that as the fallback).
