# MCP servers and tools: when MCP, when not
**Core:** MCP servers give the agent tools (browser, desktop, external systems); they cost context and run with your permissions. The competitor to the MCP server is the script. (Context: harness skill | As of: 2026-08-30)

## What MCP is (in three sentences)
- Model Context Protocol: a client-server protocol (not REST). The coding agent is the client, the server a running program that offers functions as "tools".
- At start the agent reads its configuration, connects, collects the tool list, and appends it to its own tools. When the model calls an MCP tool, the agent forwards the call to the server; the result comes back as text.
- Configuration = command + arguments + environment variables, at user or project level (file name per agent, see [agent-compatibility.md](agent-compatibility.md)). MCP servers can **not** be put into a skill; they are distributable via plugins.

## What they cost
| Cost type | Fact |
|---|---|
| Context window | Without lazy loading, all tool descriptions are sent along with **every** request: five servers ≈ 50k tokens, with a browser server quickly 100k. Claude Code now loads tool descriptions lazily (tool search): ≈ 90 tokens per actually used tool plus ≈ 3 lines per server. Other agents (e.g., GitHub Copilot) send them along permanently (computer-use server ≈ 12k, Playwright ≈ 4k). Check with `/context` or the agent's context command. |
| Unused servers | still cost on every request → switch off servers for platforms not currently in use. |
| Memory | standard construction: one server instance per agent instance. Many open agents = a lot of RAM; extreme case 12 GB for one server. |
| Security | An MCP server runs **with your permissions** and is practically unauditable (a complete application, from scratch on every update). A server that uploads source code to the net is detected by no virus scanner. Unknown origin → do not install. Secrets sometimes end up in the MCP configuration – never commit it to the repo. |
| Mass installation | Directories list thousands of servers. Every additional server (like every skill, every subagent) lowers model performance and raises costs. What gets installed is what the project needs – nothing "in stock". |

## Decision rule: MCP server or CLI/script?
The preliminary question before every extension: **is the task algorithmically decidable?** Then a script (deterministic, an error is a fixable bug). If it needs domain judgment or weighing, it stays with the model. Only then the question MCP or CLI:

| Criterion | → MCP server | → CLI tool / script |
|---|---|---|
| State | stateful: open browser tabs, a session, a window that lives as long as the server | stateless: "is the server running, is the port free, what is in the log", small reused algorithms |
| Remoteness | the function runs on another machine; your own application should be usable from outside | address the REST API directly or build a script over the API |
| Usage frequency | needed constantly (browser control daily) | needed situationally |
| Visibility | the tool should be omnipresent in the model's view | one sentence in `AGENTS.md` in the right place suffices |
| Existing CLI | – | if a command-line tool exists (`gh`, vendor CLIs, `kubectl`, `aws`, `psql` …), an MCP server is superfluous – the agent often knows these tools better than the developer |
| Auditability | barely auditable, full permissions | readable, auditable, versioned in the repo |
| Model strength | small/local models forget scripts → MCP | strong models remember a hint |
| Packaging | user/project level only, not in a skill; secrets in the configuration | the script lives in the repo or skill folder |

Rule of thumb: **state, remoteness, or daily use → MCP. Everything else → script** ([scripts.md](scripts.md)). An MCP server that recreates an existing CLI command is a mistake.

## Providing is not using
An installed tool is not used automatically. If it is to be used, that is stated explicitly in `AGENTS.md`: "For X ALWAYS use tool Y" – if needed with the counterpart "NOT Z". Examples: "If a web page cannot be read (fetch blocked), use the Playwright MCP to read it." · "Computer use may be employed to debug the desktop app."

## Recommended enablement per application type
The goal of enablement: the agent obtains information itself, tests, and looks at things itself – every loop of "human clicks through and writes a prompt that something does not work" costs time.

| Application | Recommendation |
|---|---|
| Command line / library | no browser/desktop control needed; tests and scripts suffice |
| Web application | **Playwright MCP** (or a Selenium/Puppeteer equivalent): open the page, click through, fill forms, take screenshots, read the browser console and network. Headless on servers. Setups: its own empty browser (no logins, safe) · a row of tabs in the real browser (logins present, a lot of access – weigh it) · hybrid with locked pages. **Replaces no tests** – it is for trying out and looking at things during the work; at the end an E2E test runs. |
| Desktop application | **cua-computer-use** (open-source computer-use MCP): the same for desktop apps, the application may run in the background. The agent uses it as a debugging tool only if `AGENTS.md` explicitly allows it. |
| Layout/design work | multimodal models see screenshots anyway; a vision server (positions, distances) only on concrete need |
| Generating images | an image-generation server only if the project needs images |
| Email | **read-only** (list/read, no send function) – e.g., to check confirmation emails/newsletter sign-ups. Red line: no sending without human approval. |
| Ticket/wiki/pipeline systems (Jira, Confluence, CI) | check whether a CLI exists; Confluence content is written for humans and often a garbage dump – an agent-friendly wiki ([knowledge-storage.md](knowledge-storage.md)) is usually the better source |

## Configuration locations (short version)
Project-local, so that every clone has the same tools; secrets via environment variables, never in the repo. File names per agent in [agent-compatibility.md](agent-compatibility.md). Check the context consumption before and after adding.

## Pitfalls
- An MCP server just because it is listed in a directory – without a use case. First the use case, then the server.
- A GitHub/GitLab MCP installed although `gh`/`glab` are there.
- Vendor CLIs bring MCP servers along unasked → check the context view.
- Browser control misunderstood as a substitute for tests.
- A row of tabs in the real browser: the agent must then never close the browser or touch other tabs – belongs as a rule in `AGENTS.md` if this setup is chosen.
- Computer use without explicit permission is not used as a debugging tool.
