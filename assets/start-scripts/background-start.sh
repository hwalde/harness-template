#!/usr/bin/env bash
# {{AGENT}}-background-start - start {{LABEL}} in the background, no questions asked.
#
# Purpose: start {{LABEL}} for a LONG-RUNNING task in the background, without a single
# permission prompt. An unattended run dies at the first question nobody answers and at
# the first terminal that closes - so this script starts the agent in its no-questions
# mode inside a {{MUX}} session that survives logout. For ordinary interactive work start
# {{LABEL}} normally; this script is for the runs nobody sits in front of.
#
# Not freilauf: freilauf is the hub ABOVE the projects - schedules, a fresh git worktree
# per run, budget gates, a finish gate, merge into main, notifications. This script is
# the local edition inside ONE project: one run, in the current checkout, started by hand.
# When runs should happen on a schedule, across repos, or be merged and gated by the
# machine, install freilauf (https://github.com/hwalde/freilauf) instead.
#
# Launches (as of {{DATE}}): {{COMMAND}}
# The flags live in tools/agent-start.py (one table for all agents) - fix them THERE
# if {{LABEL}} changes its CLI, then regenerate or edit this header.
#
# Usage:
#   tools/{{AGENT}}-background-start "task text" [--name NAME] [--model M] [--attach] [--dry-run] [--no-trust]
#   tools/{{AGENT}}-background-start -f task.md   [--name NAME] [--model M] [--attach] [--dry-run] [--no-trust]
# Afterwards:  tools/{{AGENT}}-attach [NAME]     (watch, steer, or list the runs)
set -euo pipefail
cd "$(dirname "$0")/.."

if [ $# -eq 0 ]; then
    sed -n '2,/^set -euo/p' "$0" | grep '^#' | sed 's/^# \{0,1\}//'
    exit 2
fi
if ! command -v {{MUX}} >/dev/null 2>&1; then
    echo "{{MUX}} is not installed - the run would have no session to attach to." >&2
    echo "Install {{MUX}} ({{INSTALL_HINT}}) or start headless with a log:" >&2
    echo "  python3 tools/agent-start.py start --agent {{AGENT}} --headless --prompt \"...\"" >&2
    exit 2
fi

args=()
case "$1" in
    -f) [ $# -ge 2 ] || { echo "-f needs a file" >&2; exit 2; }
        args+=(--prompt-file "$2"); shift 2 ;;
    -*) ;;
    *)  args+=(--prompt "$1"); shift ;;
esac
# ${args[@]+...}: an empty array under 'set -u' is an error on bash 3.2 (stock macOS).
exec python3 tools/agent-start.py start --agent {{AGENT}} ${args[@]+"${args[@]}"} "$@"
