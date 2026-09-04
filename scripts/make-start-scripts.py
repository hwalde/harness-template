#!/usr/bin/env python3
"""make-start-scripts.py - generate named start/attach scripts per coding agent and OS.

For projects that do NOT use freilauf: a human (or an agent) needs one command that starts
a coding agent for a LONG-RUNNING task so that it never stops at a permission prompt and
keeps running in the background (tmux on Linux/macOS, psmux on Windows), plus one command to
attach to that run and watch or steer it. For ordinary interactive work the agent is started
normally - these scripts exist for the runs nobody sits in front of.

The scripts are thin wrappers around tools/agent-start.py in the project, which owns the
per-agent no-questions flags (one table, one place to fix when an agent changes its CLI).
The wrapper's header states the exact command line at generation time, so the reader sees
which mode the agent runs in without opening the table.

    python3 scripts/make-start-scripts.py <project> --agents claude,opencode --os linux,macos
    python3 scripts/make-start-scripts.py <project> --agents claude --os windows
    python3 scripts/make-start-scripts.py <project> --agents claude --os linux --force

Agents: claude | codex | gemini | opencode | cursor | hermes (the table in agent-start.py).
OS: linux | macos | windows. linux and macos share one POSIX script (bash + tmux); windows
gets PowerShell scripts (psmux). Existing files are never overwritten unless --force.
Result per agent: tools/<agent>-background-start[.ps1] and tools/<agent>-attach[.ps1].
Exit codes: 0 done, 1 a file could not be written, 2 wrong usage.
"""

import argparse
import importlib.util
import pathlib
import shlex
import stat
import sys

AGENT_LABEL = {
    "claude": "Claude Code",
    "codex": "Codex CLI",
    "gemini": "Gemini CLI",
    "opencode": "opencode",
    "cursor": "Cursor CLI (cursor-agent)",
    "hermes": "hermes",
}

PURPOSE = """\
Purpose: start {label} for a LONG-RUNNING task in the background, without a single
permission prompt. An unattended run dies at the first question nobody answers and at
the first terminal that closes - so this script starts the agent in its no-questions
mode inside a {mux} session that survives logout. For ordinary interactive work start
{label} normally; this script is for the runs nobody sits in front of.

Not freilauf: freilauf is the hub ABOVE the projects - schedules, a fresh git worktree
per run, budget gates, a finish gate, merge into main, notifications. This script is
the local edition inside ONE project: one run, in the current checkout, started by hand.
When runs should happen on a schedule, across repos, or be merged and gated by the
machine, install freilauf (https://github.com/hwalde/freilauf) instead."""

POSIX_START = """\
#!/usr/bin/env bash
# {name} - start {label} in the background, no questions asked.
#
{purpose}
#
# Launches (as of {today}): {command}
# The flags live in tools/agent-start.py (one table for all agents) - fix them THERE
# if {label} changes its CLI, then regenerate or edit this header.
#
# Usage:
#   tools/{name} "task text" [--name NAME] [--model M] [--attach] [--dry-run] [--no-trust]
#   tools/{name} -f task.md   [--name NAME] [--model M] [--attach] [--dry-run] [--no-trust]
# Afterwards:  tools/{attach} [NAME]     (watch, steer, or list the runs)
set -euo pipefail
cd "$(dirname "$0")/.."

if [ $# -eq 0 ]; then
    sed -n '2,/^set -euo/p' "$0" | grep '^#' | sed 's/^# \\{{0,1\\}}//'
    exit 2
fi
if ! command -v {mux} >/dev/null 2>&1; then
    echo "{mux} is not installed - the run would have no session to attach to." >&2
    echo "Install {mux} ({install_hint}) or start headless with a log:" >&2
    echo "  python3 tools/agent-start.py start --agent {agent} --headless --prompt \\"...\\"" >&2
    exit 2
fi

args=()
case "$1" in
    -f) [ $# -ge 2 ] || {{ echo "-f needs a file" >&2; exit 2; }}
        args+=(--prompt-file "$2"); shift 2 ;;
    -*) ;;
    *)  args+=(--prompt "$1"); shift ;;
esac
# ${{args[@]+...}}: an empty array under 'set -u' is an error on bash 3.2 (stock macOS).
exec python3 tools/agent-start.py start --agent {agent} ${{args[@]+"${{args[@]}}"}} "$@"
"""

POSIX_ATTACH = """\
#!/usr/bin/env bash
# {name} - attach to a running {label} session, or list the runs.
#
# Usage:
#   tools/{name}                 list the runs in progress
#   tools/{name} NAME            attach to the run (detach again: Ctrl+b, then d)
#   tools/{name} NAME "text"     type text into the run, submit it, then attach
# Runs are started with tools/{start}; ended with: python3 tools/agent-start.py kill NAME
set -euo pipefail
cd "$(dirname "$0")/.."

case $# in
    0) exec python3 tools/agent-start.py list ;;
    1) exec python3 tools/agent-start.py attach "$1" ;;
    2) python3 tools/agent-start.py send "$1" "$2"
       exec python3 tools/agent-start.py attach "$1" ;;
    *) echo "Usage: tools/{name} [NAME ["text"]]" >&2; exit 2 ;;
esac
"""

WIN_START = """\
# {name}.ps1 - start {label} in the background, no questions asked.
#
{purpose}
#
# Launches (as of {today}): {command}
# The flags live in tools\\agent-start.py (one table for all agents) - fix them THERE
# if {label} changes its CLI, then regenerate or edit this header.
#
# Usage:
#   tools\\{name}.ps1 "task text" [--name NAME] [--model M] [--attach] [--dry-run] [--no-trust]
#   tools\\{name}.ps1 -f task.md   [--name NAME] [--model M] [--attach] [--dry-run] [--no-trust]
# Afterwards:  tools\\{attach}.ps1 [NAME]     (watch, steer, or list the runs)
Set-Location (Join-Path $PSScriptRoot "..")

# Usage errors exit 2 (printed to stderr) before $ErrorActionPreference = "Stop" would turn
# them into exit 1.
if ($args.Count -eq 0) {{
    # The header is the contiguous comment block at the top; stop at the first other line.
    foreach ($line in Get-Content $PSCommandPath) {{
        if ($line -notmatch '^#') {{ break }}
        $line -replace '^# ?', ''
    }}
    exit 2
}}
if (-not (Get-Command psmux -ErrorAction SilentlyContinue)) {{
    [Console]::Error.WriteLine("psmux is not installed - the run would have no session to attach to. Install psmux ({install_hint}) or start headless: python tools\\agent-start.py start --agent {agent} --headless --prompt '...'")
    exit 2
}}

# Split off the task argument; the rest is passed through. The last valid index of $args
# is Count-1, and a range past it is an error - hence the guards.
$pass = @()
$rest = @()
if ($args[0] -eq "-f") {{
    if ($args.Count -lt 2) {{ [Console]::Error.WriteLine("-f needs a file"); exit 2 }}
    $pass = @("--prompt-file", $args[1])
    if ($args.Count -gt 2) {{ $rest = $args[2..($args.Count - 1)] }}
}} elseif ($args[0] -notlike "-*") {{
    $pass = @("--prompt", $args[0])
    if ($args.Count -gt 1) {{ $rest = $args[1..($args.Count - 1)] }}
}} else {{
    $rest = $args
}}
$ErrorActionPreference = "Stop"
& python tools\\agent-start.py start --agent {agent} @pass @rest
exit $LASTEXITCODE
"""

WIN_ATTACH = """\
# {name}.ps1 - attach to a running {label} session, or list the runs.
#
# Usage:
#   tools\\{name}.ps1                 list the runs in progress
#   tools\\{name}.ps1 NAME            attach to the run (detach again: Ctrl+b, then d)
#   tools\\{name}.ps1 NAME "text"     type text into the run, submit it, then attach
# Runs are started with tools\\{start}.ps1; ended with: python tools\\agent-start.py kill NAME
Set-Location (Join-Path $PSScriptRoot "..")
if ($args.Count -gt 2) {{ [Console]::Error.WriteLine("Usage: tools\\{name}.ps1 [NAME ['text']]"); exit 2 }}
$ErrorActionPreference = "Stop"   # a missing python must fail loudly, not exit 0

switch ($args.Count) {{
    0 {{ & python tools\\agent-start.py list; exit $LASTEXITCODE }}
    1 {{ & python tools\\agent-start.py attach $args[0]; exit $LASTEXITCODE }}
    2 {{ & python tools\\agent-start.py send $args[0] $args[1]
         if ($LASTEXITCODE -ne 0) {{ exit $LASTEXITCODE }}
         & python tools\\agent-start.py attach $args[0]; exit $LASTEXITCODE }}
}}
"""

INSTALL_HINT = {
    "linux": "apt install tmux / dnf install tmux",
    "macos": "brew install tmux",
    "windows": "a tmux clone for Windows - see its README on GitHub",
}


def load_agent_start(project: pathlib.Path):
    path = project / "tools" / "agent-start.py"
    if not path.is_file():
        raise SystemExit(f"{path} is missing - build the harness first (scripts/build.py {project}).")
    spec = importlib.util.spec_from_file_location("agent_start", path)
    mod = importlib.util.module_from_spec(spec)
    sys.dont_write_bytecode = True   # no tools/__pycache__ in the project from this import
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


def render_purpose(label: str, mux: str, comment: str) -> str:
    return "\n".join(f"{comment} {line}".rstrip() for line in PURPOSE.format(label=label, mux=mux).splitlines())


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("project", nargs="?", help="project folder with a built harness (tools/agent-start.py)")
    ap.add_argument("--agents", default="", help="comma-separated: claude,codex,gemini,opencode,cursor,hermes")
    ap.add_argument("--os", dest="oses", default="", help="comma-separated: linux,macos,windows")
    ap.add_argument("--force", action="store_true", help="overwrite existing scripts")
    a = ap.parse_args()
    if not a.project or not a.agents or not a.oses:
        print(__doc__.strip())
        return 2

    project = pathlib.Path(a.project).expanduser().resolve()
    if not project.is_dir():
        print(f"Project folder does not exist: {project}")
        return 2
    mod = load_agent_start(project)
    agents = [x.strip() for x in a.agents.split(",") if x.strip()]
    oses = [x.strip().lower() for x in a.oses.split(",") if x.strip()]
    bad = [x for x in agents if x not in mod.AGENTS]
    if bad:
        print(f"Unknown agent(s): {', '.join(bad)}. Known (tools/agent-start.py): {', '.join(mod.AGENTS)}")
        return 2
    bad = [x for x in oses if x not in INSTALL_HINT]
    if bad:
        print(f"Unknown OS: {', '.join(bad)}. Allowed: linux, macos, windows")
        return 2

    from datetime import date
    today = date.today().isoformat()
    tools = project / "tools"
    written: list[str] = []
    kept: list[str] = []
    failed: list[str] = []

    def put(rel: str, content: str, executable: bool) -> None:
        dst = tools / rel
        if dst.exists() and not a.force:
            kept.append(rel)
            return
        try:
            dst.write_text(content, encoding="utf-8", newline="\n")
            if executable:
                dst.chmod(dst.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        except OSError as exc:
            failed.append(f"{rel}: {exc}")
            return
        written.append(rel)

    posix = [o for o in oses if o != "windows"]
    for agent in agents:
        label = AGENT_LABEL[agent]
        cmd = " ".join(shlex.quote(c) for c in mod.build_command(agent, "<task>", None, headless=False))
        start, attach = f"{agent}-background-start", f"{agent}-attach"
        if posix:
            hint = " / ".join(INSTALL_HINT[o] for o in posix)
            put(start, POSIX_START.format(name=start, attach=attach, label=label, agent=agent, mux="tmux",
                                          purpose=render_purpose(label, "tmux", "#"), today=today,
                                          command=cmd, install_hint=hint), True)
            put(attach, POSIX_ATTACH.format(name=attach, start=start, label=label), True)
        if "windows" in oses:
            put(start + ".ps1", WIN_START.format(name=start, attach=attach, label=label, agent=agent,
                                                 purpose=render_purpose(label, "psmux", "#"), today=today,
                                                 command=cmd, install_hint=INSTALL_HINT["windows"]), False)
            put(attach + ".ps1", WIN_ATTACH.format(name=attach, start=start, label=label), False)

    print(f"start/attach scripts -> {tools}")
    for title, items in (("written", written), ("kept (exist; --force overwrites)", kept), ("failed", failed)):
        if items:
            print(f"\n{title}:")
            for i in items:
                print(f"  {i}")
    if written:
        print("\nNext:")
        print("  1. Verify the flags against the installed agents: for each one, --help (or its docs) must")
        print("     still know the mode in the 'Launches' line; else fix the table in tools/agent-start.py")
        print("     and rerun with --force.")
        print("  2. Test each script for REAL - a dry run is not enough (the trust dialog only shows in a")
        print("     real start): tools/<agent>-background-start \"Reply with the word OK only.\" --name t1,")
        print("     then tools/<agent>-attach t1 (or read the screen: tmux capture-pane -p -t hx-t1:), check")
        print("     that the agent answered and no dialog is waiting, then: python3 tools/agent-start.py kill t1.")
        print("     Windows: the same with the .ps1 files and psmux. What you cannot test here (an OS or an")
        print("     agent that is not installed) is handed over marked as untested in HARNESS.md.")
        print("  3. Only a script that passed goes into AGENTS.md under 'Tools and scripts', one sentence per pair, e.g.:")
        for agent in agents:
            print(f"     - `tools/{agent}-background-start` / `tools/{agent}-attach` - start {AGENT_LABEL[agent]} for a")
            print(f"       long-running task without permission prompts in a tmux/psmux session, and attach to it;")
            print(f"       ordinary work starts {AGENT_LABEL[agent]} normally. NOT for scheduled or multi-repo runs (freilauf).")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
