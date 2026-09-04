# Start/attach script templates – drafts the agent turns into project scripts

These four files are **not copied by a script**. The coding agent creates the project's
start/attach scripts from them by hand – one pair per coding agent the user wants, in the
variant(s) for the operating systems the user wants – then adapts them to the project, tests
each one with a real run, and improves what does not fit. Reason: a script that was stamped
out mechanically is nobody's work; a script the agent wrote, ran and fixed is understood,
matches the installed agent version, and carries the project's own pre-checks and defaults.

| Template | Becomes | Needs |
|---|---|---|
| `background-start.sh` | `tools/<agent>-background-start` (executable) | bash, tmux – Linux and macOS |
| `attach.sh` | `tools/<agent>-attach` (executable) | bash, tmux – Linux and macOS |
| `background-start.ps1` | `tools/<agent>-background-start.ps1` | PowerShell, psmux – Windows |
| `attach.ps1` | `tools/<agent>-attach.ps1` | PowerShell, psmux – Windows |

Both wrap `tools/agent-start.py` in the project, which owns the per-agent no-questions flags
(one table – fix flags there, never in the wrapper).

## Placeholders

| Placeholder | Meaning | Example |
|---|---|---|
| `{{AGENT}}` | agent id as `tools/agent-start.py` knows it | `claude`, `codex`, `gemini`, `opencode`, `cursor`, `hermes` |
| `{{LABEL}}` | human name of the agent | `Claude Code`, `Codex CLI`, `Gemini CLI`, `opencode`, `Cursor CLI (cursor-agent)`, `hermes` |
| `{{COMMAND}}` | the exact command line the wrapper will launch, read from the dry run: `python3 tools/agent-start.py start --agent <agent> --prompt "<task>" --dry-run` | `claude --permission-mode dontAsk '<task>'` |
| `{{DATE}}` | date of creation (the command line is a dated snapshot) | `2026-09-04` |
| `{{MUX}}` | the multiplexer: `tmux` in the `.sh` files, `psmux` in the `.ps1` files | `tmux` |
| `{{INSTALL_HINT}}` | how to install the multiplexer on the target OS | `apt install tmux`, `brew install tmux`, `psmux – a tmux clone for Windows, see its README on GitHub` |

## Procedure (setup step 6 item 7 in `references/setup.md`)

1. Explain the purpose and the difference to freilauf to the user first (the header text of
   `background-start.sh` says it in full).
2. Ask which operating systems and which coding agents the scripts must serve.
3. For each agent and OS family: copy the template to its target name, replace every
   placeholder, read the whole file, and adapt it to the project – a default model, a
   pre-check the project needs (a service that must be up, a port that must be free), a
   prompt file convention, the session name. Keep the header honest: it must describe what the
   script actually does.
4. Check the mode against the installed agent (`<agent> --help`); if the table in
   `tools/agent-start.py` is stale, fix the table, then the header's `Launches` line.
5. **Test for real**: start a short task through the script, attach (or
   `tmux capture-pane -p -t hx-<name>:`), confirm the agent answered and no dialog is waiting,
   end the run (`python3 tools/agent-start.py kill <name>`). A dry run does not count – the
   "Do you trust this folder?" dialog of Claude Code only appears in a real start. Fix and
   repeat until it behaves.
6. Only a script that passed gets its sentence in `AGENTS.md` under "Tools and scripts"; what
   could not be tested on this machine (another OS, an agent that is not installed) is handed
   over marked as untested in `HARNESS.md`.
