# Scripts for coding agents
**Core:** Everything algorithmically decidable belongs in a script; the AI decides, the script executes. Every script of this harness is built following the ten principles below – without asking back, they always apply here. (Context: harness template | As of: 2026-08-30)

## Why scripts
- **Determinism:** A script delivers the same result every day; an error is a bug that you fix. A model answers one way on some days and another way on others. Example: static code analysis via script, not via "look at the files".
- **Division of labor:** The AI decides *what* should happen and *where*; the script does it. Everything that can be scripted without AI gets scripted.
- **Relief:** A script that checks whether the server is running, the port is free, the health endpoint reports errors, and what is in the log is a classic harness building block. Optimized scripts make the agent better.
- **Limit:** Domain judgment ("is this cut sensible?") stays with the model. And: where a tool already stands (browser control, computer use, `gh`), do not rebuild it as a script.
- **Making it known:** The model does not "smell" a script. It must be mentioned – in `AGENTS.md` (one sentence), in the chat, or in a skill. Script vs. MCP: [mcp-und-werkzeuge.md](mcp-und-werkzeuge.md).

## Guiding image: a CLI tool is a function call to a human
The caller is an LLM – you treat it like a smart colleague: it knows every technical term and needs no lecturing, but deserves the preparation that enables error-free work. The call is so simple that you can hardly get it wrong; the output so clear that the chance of a misunderstanding approaches zero. Inside, algorithms and data structures do the work; at the interface, human language is spoken – in both directions.

## The ten principles (binding for all scripts of this harness)

### 1. Exit fast
A script must never run permanently – the agent waits for the result and otherwise hangs. If a background process (server) is needed, the script spawns it detached (`start_new_session=True`, log to a file) and exits immediately with the PID.

### 2. Self-explanatory and simple
- A call without arguments = help that explains how the tool is to be used.
  Exception: a script with exactly one safe, idempotent action may run it directly when called without arguments, as long as the output explains what happened (`-h/--help` stays available; example: `tools/sync-agents.py`).
- As few arguments as possible; arguments speak the language of the task, not the internal structure (a literal quote or a timestamp instead of an index or object path – internal IDs the agent must first obtain, and it mixes them up).
- The less documentation needed in `AGENTS.md`, the better: one line (`tools/check-logs.py – error analysis of the log file`), not 15.

### 3. Progressive disclosure
Top level: only the most important subcommands. Details, options, and sub-help pages only at their respective level.

### 4. Human-readable output – the consumer determines the format
Order: Markdown > prose > XML > JSON (avoid). LLMs are readers, not parsers; nested JSON tears the context apart. Exception: if the consumer is a script (a pipeline, a parsing wrapper), exactly that consumer gets its format – say a byte-stable final line or a `--json` flag. The format choice is **not** left to the agent; models wrongly consider JSON suitable.

### 5. Token-frugal
The entire output lands in the context window. Clarity before brevity, but when both are possible: short and clear. No banners, no dotted lines, no repetitions. `Server running (port 8080, for 5 min). No current errors.` instead of a status report.

### 6. Navigation instead of a data dump
Never everything at once. An overview (newest errors first, timestamps, one line per entry) plus the commands for details, paging (`--page`), filters (`--errors`, `--search`). The agent gets the choice of what it wants to see next.

### 7. Output as a prompt – and as first validation
Every sentence of the output lands as an instruction in the context. The output guides: navigation hints, contextual observations, **suggestions instead of commands** ("error #1 is 8 s old and probably stems from your change – suggestion: `tool.py logs --detail 1`"). For state-changing commands: confirm what happened, show the effect in context, name the ready-filled reverse command – the agent checks its action in the same moment. Provide time reference (age of entries), because models have no sense of time and otherwise cannot find their own log entries.

### 8. Thinking along
- Multi-agent-safe: "Server was started 8 s ago – other agents may be working in parallel. Force with `--force`."
- Sensible sorting (newest first), pre-checks (does it compile? port occupied? by whom?), counting and measuring in the script instead of in the model.
- Correlate data instead of tossing it out piecemeal (browser log, network, server log per failed test).

### 9. Available language, no isolation
Python preferred (check first whether it is present; otherwise Bash). Write OS-independently (`pathlib`, `shutil.which`, no shell specialties). **No virtual environments** – standard library only or `pip install` without venv; detect missing packages at start and name the install command.

### 10. Error messages are instructions to act
Symptom + expected/actual + next step: `Abort: API_TOKEN missing in .env (expected: API_TOKEN=<token>). Add it and call again. Template: .env.example` – no stack trace without interpretation. On unclear errors an agent repeats the call or guesses; a message with a fix turns the failed attempt into a one-step repair.

## After building: an entry in `AGENTS.md`
A script without a mention does not exist for the agent. The entry contains: name and invocation, when to use it, what it replaces (which previous command is NOT to be used ANYMORE). Phrase it emphatically – IMPORTANT/NOT/ALWAYS catch agents' attention; short sentences; only the main command, subcommands the agent discovers by calling.

```markdown
## Starting/stopping the server
IMPORTANT: do NOT start the server directly with `npm start`. ALWAYS use `python3 tools/server.py start`
– it compiles beforehand, checks port conflicts, protects against double starts.
- `python3 tools/server.py` – shows the commands (start, status, logs)
```

## Typical harness scripts
| Script | Purpose |
|---|---|
| `tools/agent-start.py` (in the template) | start a coding agent without follow-up questions, optionally in tmux/psmux; `list`, `attach`, `send`, `kill`, `doctor` → [autonome-laeufe.md](autonome-laeufe.md) |
| `tools/sync-agents.py` (in the template) | translate subagent definitions from `.claude/agents/` into the format of other agents → [agenten-kompatibilitaet.md](agenten-kompatibilitaet.md) |
| Server/service control | start with pre-check, status, logs with navigation, restart protection |
| Log analysis | newest errors first, age, filters, a detail command for stack traces |
| Test-runner wrapper | E2E in parallel, repeat failures sequentially, correlate browser/network/server log per test |
| Usage script | quota in percent + time of the reset, so that an autonomous run stops before the limit → [autonome-laeufe.md](autonome-laeufe.md) |
| Monitoring | checks for hanging scripts and lost agents; called periodically by the agent via cron/loop |
| Counting/measuring tools | words, lengths, dimensions – models count poorly |
| Build/release | exactly one script for the release build, fixed in `AGENTS.md` as the only path |

## Pitfalls
- The script exists but is mentioned nowhere.
- A wrapper that prints whole log files (bloat); JSON-blob output; long-runners that block the agent.
- Script output is a prompt – and therefore also an attack vector: clearly mark third-party content (emails, web pages, tickets) in the output as data (e.g., XML tags), never format it as an instruction.
- Small/local models forget scripts more easily – there, more explicit hints or MCP.
