#!/usr/bin/env python3
"""agent-start.py - start coding agents for runs that never ask questions.

Run without arguments to see the help. Standard library only, no venv,
works on macOS, Linux and Windows (tmux or psmux optional).

Why this script exists: an autonomous run fails at every question nobody
answers and at every session that dies on logout. This script knows, for each
agent, the mode in which it does NOT ask, and puts the run either into a
tmux/psmux session (to watch and attach) or into a detached background process
with a log file (headless).
"""

import json
import os
import shlex
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

PREFIX = "hx-"                        # session prefix in the multiplexer
RUNS_DIR = Path(".harness") / "runs"  # logs, prompts, pid files (gitignored)
IS_WINDOWS = os.name == "nt"

# Order = default when --agent is omitted: the first installed one wins.
AGENTS = ["claude", "codex", "gemini", "opencode", "cursor", "hermes"]
BINARIES = {
    "claude": "claude",
    "codex": "codex",
    "gemini": "gemini",
    "opencode": "opencode",
    "cursor": "cursor-agent",
    "hermes": "hermes",
}


# ---------------------------------------------------------------------------
# Command lines per agent (as of 2026-08). If an agent changes its flags,
# THIS table is the only place that needs to change.
# ---------------------------------------------------------------------------
def build_command(agent, prompt, model, headless):
    """Return the command list. headless=True: no TUI, output goes to a log
    file. headless=False: interactive session (for tmux/psmux)."""
    m = ["--model", model] if model else []

    if agent == "claude":
        # dontAsk: silently refuses what is not allowed instead of asking - never hangs.
        base = ["claude", "--permission-mode", "dontAsk"] + m
        if headless:
            return base + ["-p", prompt]
        return base + ([prompt] if prompt else [])

    if agent == "codex":
        # -a never: never ask for approval; the sandbox allows writes in the workspace.
        if headless:
            return ["codex", "exec"] + m + ["-a", "never", "-s", "workspace-write", prompt]
        base = ["codex"] + m + ["-a", "never", "-s", "workspace-write"]
        return base + ([prompt] if prompt else [])

    if agent == "gemini":
        base = ["gemini", "--yolo"] + m
        if headless:
            return base + ["-p", prompt]
        return base + (["-i", prompt] if prompt else [])

    if agent == "opencode":
        if headless:
            return ["opencode", "run"] + m + [prompt]
        # --auto: approves everything that opencode.json does not explicitly deny.
        base = ["opencode", "--auto"] + m
        return base + (["--prompt", prompt] if prompt else [])

    if agent == "cursor":
        base = ["cursor-agent", "--force", "--trust"] + m
        if headless:
            return base + ["-p", prompt]
        return base + ([prompt] if prompt else [])

    if agent == "hermes":
        base = ["hermes", "chat", "--yolo"] + m
        return base + (["-q", prompt] if prompt else [])

    raise SystemExit(f"Abort: unknown agent '{agent}'. Allowed: {', '.join(AGENTS)}")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def multiplexer():
    """Name of the installed terminal multiplexer, or None."""
    for name in (["psmux", "tmux"] if IS_WINDOWS else ["tmux"]):
        if shutil.which(name):
            return name
    return None


def installed_agents():
    return [a for a in AGENTS if shutil.which(BINARIES[a])]


def session_name(name):
    return name if name.startswith(PREFIX) else PREFIX + name


def default_name(directory):
    return f"{Path(directory).resolve().name}-{datetime.now():%m%d-%H%M}"


def mux_sessions(mux):
    """List of (name, path, attached) for sessions with our prefix."""
    try:
        out = subprocess.run(
            [mux, "list-sessions", "-F", "#{session_name}|#{session_path}|#{?session_attached,yes,no}"],
            capture_output=True, text=True,
        ).stdout
    except OSError:
        return []
    rows = []
    for line in out.splitlines():
        parts = line.split("|")
        if len(parts) == 3 and parts[0].startswith(PREFIX):
            rows.append(tuple(parts))
    return rows


def pid_alive(pid):
    if IS_WINDOWS:
        out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}"], capture_output=True, text=True).stdout
        return str(pid) in out
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def headless_runs():
    """List of (name, pid, alive, logpath) for headless runs."""
    rows = []
    if not RUNS_DIR.is_dir():
        return rows
    for pidfile in sorted(RUNS_DIR.glob("*.pid")):
        try:
            pid = int(pidfile.read_text().strip())
        except ValueError:
            continue
        name = pidfile.stem
        rows.append((name, pid, pid_alive(pid), RUNS_DIR / f"{name}.log"))
    return rows


def trust_workdir(agent, directory, disabled):
    """Claude Code asks 'Do you trust this folder?' on the first start in a directory and
    waits for Enter - an unattended run hangs there forever (found by a real test, not by
    reading docs). Pre-confirm it the way freilauf's fl-start does: set
    projects[<dir>].hasTrustDialogAccepted in ~/.claude.json. Fails soft: on any problem the
    run still starts and the message says what to do. Other agents: nothing to do (cursor
    gets --trust in its command line)."""
    if agent != "claude" or disabled:
        return
    cfg = Path.home() / ".claude.json"
    if not cfg.is_file():
        return
    try:
        data = json.loads(cfg.read_text(encoding="utf-8"))
        proj = data.setdefault("projects", {}).setdefault(str(directory), {})
        if proj.get("hasTrustDialogAccepted"):
            return
        proj["hasTrustDialogAccepted"] = True
        backup = cfg.with_name(".claude.json.bak-agent-start")
        shutil.copy2(cfg, backup)
        tmp = cfg.with_name(".claude.json.tmp-agent-start")
        tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
        tmp.replace(cfg)
        print(f"Trust dialog pre-confirmed for {directory} (~/.claude.json, backup {backup.name}).")
    except (OSError, ValueError) as exc:
        print(f"Note: could not pre-confirm the trust dialog ({exc}). If the run stays on "
              f"'Do you trust this folder?', attach once and press Enter.")


def read_prompt(args):
    if args.get("prompt") and args.get("prompt_file"):
        raise SystemExit("Abort: --prompt and --prompt-file are mutually exclusive. Drop one of them.")
    if args.get("prompt_file"):
        p = Path(args["prompt_file"])
        if not p.is_file():
            raise SystemExit(f"Abort: prompt file not found: {p}\nCheck the path or use --prompt \"text\".")
        return p.read_text(encoding="utf-8").strip()
    return (args.get("prompt") or "").strip()


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------
def cmd_doctor():
    print("Installed coding agents:")
    found = installed_agents()
    for a in AGENTS:
        mark = "yes" if a in found else "no "
        print(f"  {a:<9} {mark}   ({BINARIES[a]})")
    mux = multiplexer()
    if mux:
        print(f"\nTerminal multiplexer: {mux} found -> runs start as a session by default.")
    else:
        hint = "psmux (Windows)" if IS_WINDOWS else "tmux"
        print("\nNo terminal multiplexer found -> runs start headless with a log file.")
        print(f"Install {hint} to get sessions you can attach to.")
    if not found:
        print("\nNo agent on the PATH. Install at least one (e.g. claude, codex, gemini, opencode).")
    else:
        print(f"\nDefault without --agent: {found[0]}")
    print("\nNext step: agent-start.py start --prompt \"...\"   (or: agent-start.py start --help)")


def cmd_start(args):
    prompt = read_prompt(args)
    directory = Path(args.get("dir") or ".").resolve()
    if not directory.is_dir():
        raise SystemExit(f"Abort: working directory does not exist: {directory}")

    agent = args.get("agent")
    found = installed_agents()
    if not agent:
        if not found:
            raise SystemExit("Abort: no coding agent found on the PATH. Run 'agent-start.py doctor' first.")
        agent = found[0]
    if agent not in AGENTS:
        raise SystemExit(f"Abort: unknown agent '{agent}'. Allowed: {', '.join(AGENTS)}")
    if agent not in found and not args.get("dry_run"):
        raise SystemExit(f"Abort: '{BINARIES[agent]}' is not on the PATH. Install it or pick another --agent ('doctor' lists them).")

    mux = multiplexer()
    use_mux = mux is not None and not args.get("headless")
    if not use_mux and not prompt:
        raise SystemExit("Abort: without a multiplexer (or with --headless) a prompt is required (--prompt / --prompt-file), "
                         "because there is no session to type into.")

    name = args.get("name") or default_name(directory)
    cmd = build_command(agent, prompt, args.get("model"), headless=not use_mux)

    if args.get("dry_run"):
        print("Dry run - nothing is started.")
        print(f"  Agent:      {agent}")
        print(f"  Directory:  {directory}")
        mode = f"session {mux} ({session_name(name)})" if use_mux else f"headless, log in {RUNS_DIR / (name + '.log')}"
        print(f"  Mode:       {mode}")
        print(f"  Command:    {' '.join(shlex.quote(c) for c in cmd)}")
        return

    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    trust_workdir(agent, directory, args.get("no_trust"))
    if prompt:
        (RUNS_DIR / f"{name}.prompt.md").write_text(prompt + "\n", encoding="utf-8")

    if use_mux:
        sess = session_name(name)
        if sess in [s for s, _, _ in mux_sessions(mux)]:
            raise SystemExit(f"Abort: session '{sess}' is already running. Choose another --name, "
                             f"attach with: agent-start.py attach {name}   or end it: agent-start.py kill {name}")
        subprocess.run([mux, "new-session", "-d", "-s", sess, "-c", str(directory), "--"] + cmd, check=True)
        print(f"Started: {agent} in session '{sess}' ({directory})")
        if prompt:
            print(f"Prompt saved to {RUNS_DIR / (name + '.prompt.md')} ({len(prompt)} characters).")
        print(f"\nWatch:   agent-start.py attach {name}     (detach: Ctrl+b, then d)")
        print(f"Send:    agent-start.py send {name} \"text\"")
        print(f"End:     agent-start.py kill {name}")
        if args.get("attach"):
            cmd_attach(name)
        return

    log = RUNS_DIR / f"{name}.log"
    popen_kwargs = dict(cwd=str(directory), stdin=subprocess.DEVNULL,
                        stdout=open(log, "w", encoding="utf-8"), stderr=subprocess.STDOUT)
    if IS_WINDOWS:
        popen_kwargs["creationflags"] = 0x00000008 | 0x00000200  # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
    else:
        popen_kwargs["start_new_session"] = True
    proc = subprocess.Popen(cmd, **popen_kwargs)
    (RUNS_DIR / f"{name}.pid").write_text(str(proc.pid))
    print(f"Started (headless): {agent}, PID {proc.pid}, log: {log}")
    print(f"\nStatus:  agent-start.py list\nLog:     tail -n 40 {log}\nEnd:     agent-start.py kill {name}")


def cmd_list():
    mux = multiplexer()
    sessions = mux_sessions(mux) if mux else []
    runs = headless_runs()
    if not sessions and not runs:
        print("No runs in progress.\nStart one with: agent-start.py start --prompt \"...\"")
        return
    if sessions:
        print(f"Sessions ({mux}):")
        for s, path, attached in sessions:
            print(f"  {s[len(PREFIX):]:<28} {path}   {'(attached)' if attached == 'yes' else ''}")
    if runs:
        print("Headless runs:")
        for name, pid, alive, log in runs:
            state = "running" if alive else "ended"
            print(f"  {name:<28} PID {pid:<7} {state:<8} log: {log}")
    print("\nAttach: agent-start.py attach NAME   -   End: agent-start.py kill NAME")


def cmd_attach(name):
    mux = multiplexer()
    if not mux:
        raise SystemExit("Abort: no multiplexer installed - headless runs have no session. See the log: agent-start.py list")
    sess = session_name(name)
    if sess not in [s for s, _, _ in mux_sessions(mux)]:
        raise SystemExit(f"Abort: session '{sess}' not found. Running sessions: agent-start.py list")
    if os.environ.get("TMUX"):
        os.execvp(mux, [mux, "switch-client", "-t", "=" + sess])
    os.execvp(mux, [mux, "attach-session", "-t", "=" + sess])


def cmd_send(name, text):
    mux = multiplexer()
    if not mux:
        raise SystemExit("Abort: no multiplexer installed - nothing can be typed into a headless run.")
    sess = session_name(name)
    if sess not in [s for s, _, _ in mux_sessions(mux)]:
        raise SystemExit(f"Abort: session '{sess}' not found. Running sessions: agent-start.py list")
    if not text.strip():
        raise SystemExit("Abort: empty text.")
    # Bracketed paste: deliver multi-line text as ONE input, Enter only afterwards -
    # otherwise the TUI swallows the Enter or submits line by line.
    subprocess.run([mux, "send-keys", "-t", sess + ":", "-l", "--", "\x1b[200~" + text + "\x1b[201~"], check=True)
    time.sleep(0.3)
    subprocess.run([mux, "send-keys", "-t", sess + ":", "Enter"], check=True)
    print(f"Sent to '{sess}' ({len(text)} characters). Watch: agent-start.py attach {name}")


def cmd_kill(name):
    mux = multiplexer()
    sess = session_name(name)
    done = False
    if mux and sess in [s for s, _, _ in mux_sessions(mux)]:
        subprocess.run([mux, "kill-session", "-t", "=" + sess], check=True)
        print(f"Session '{sess}' ended.")
        done = True
    for rname, pid, alive, log in headless_runs():
        if rname == name:
            if alive:
                if IS_WINDOWS:
                    subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], capture_output=True)
                else:
                    os.kill(pid, 15)
                print(f"Headless run '{name}' (PID {pid}) ended.")
            else:
                print(f"Headless run '{name}' had already ended.")
            (RUNS_DIR / f"{name}.pid").unlink(missing_ok=True)
            done = True
    if not done:
        raise SystemExit(f"Abort: no run named '{name}'. Runs in progress: agent-start.py list")


# ---------------------------------------------------------------------------
# Help & arguments
# ---------------------------------------------------------------------------
HELP = """agent-start.py - start coding agents for runs that never ask questions

Commands:
  doctor               Which agents and which multiplexer are installed?
  start                Start a run (details: agent-start.py start --help)
  list                 Show runs in progress (sessions and headless)
  attach NAME          Attach to a running session (detach: Ctrl+b, then d)
  send NAME "text"     Type text into a running session and submit it
  kill NAME            End a run

Typical flow:
  agent-start.py doctor
  agent-start.py start --prompt-file task.md --name nightrun
  agent-start.py attach nightrun
"""

START_HELP = """agent-start.py start [options]

  --prompt "text"        The task; the run works without asking questions.
  --prompt-file FILE     Read the task from a file (instead of --prompt).
  --agent NAME           claude | codex | gemini | opencode | cursor | hermes
                         (default: the first installed one, in this order)
  --name NAME            Name of the run (default: <directory>-<MMDD-HHMM>)
  --dir PATH             Working directory (default: current)
  --model M              Pass a model to the agent
  --headless             Do not use tmux/psmux; detached background process with log file
  --attach               Attach right after starting (multiplexer only)
  --dry-run              Only show what would be started
  --no-trust             claude: do not pre-confirm the "trust this folder" dialog

Without a prompt (and with a multiplexer) a normal interactive session starts.
Without a multiplexer a prompt is required; the agent then runs headless.
"""


def parse(argv):
    args = {"_pos": []}
    i = 0
    flags_with_value = {"--prompt", "--prompt-file", "--agent", "--name", "--dir", "--model"}
    while i < len(argv):
        a = argv[i]
        if a in flags_with_value:
            if i + 1 >= len(argv):
                raise SystemExit(f"Abort: {a} needs a value.")
            args[a[2:].replace("-", "_")] = argv[i + 1]
            i += 2
        elif a in ("--headless", "--attach", "--dry-run", "--no-trust"):
            args[a[2:].replace("-", "_")] = True
            i += 1
        elif a in ("-h", "--help"):
            args["help"] = True
            i += 1
        elif a.startswith("-"):
            raise SystemExit(f"Abort: unknown option {a}. Help: agent-start.py start --help")
        else:
            args["_pos"].append(a)
            i += 1
    return args


def main(argv):
    if not argv or argv[0] in ("-h", "--help", "help"):
        print(HELP)
        return 0
    cmd, rest = argv[0], argv[1:]
    if cmd == "doctor":
        cmd_doctor()
    elif cmd == "start":
        args = parse(rest)
        if args.get("help"):
            print(START_HELP)
            return 0
        cmd_start(args)
    elif cmd == "list":
        cmd_list()
    elif cmd == "attach":
        if not rest:
            raise SystemExit("Abort: name missing. Usage: agent-start.py attach NAME   (names: agent-start.py list)")
        cmd_attach(rest[0])
    elif cmd == "send":
        if len(rest) < 2:
            raise SystemExit('Abort: usage: agent-start.py send NAME "text"')
        cmd_send(rest[0], " ".join(rest[1:]))
    elif cmd == "kill":
        if not rest:
            raise SystemExit("Abort: name missing. Usage: agent-start.py kill NAME   (names: agent-start.py list)")
        cmd_kill(rest[0])
    else:
        print(f"Unknown command '{cmd}'.\n")
        print(HELP)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
