#!/usr/bin/env bash
# {{AGENT}}-background-start - attach to a running {{LABEL}} session, or list the runs.
#
# Usage:
#   tools/{{AGENT}}-background-start                 list the runs in progress
#   tools/{{AGENT}}-background-start NAME            attach to the run (detach again: Ctrl+b, then d)
#   tools/{{AGENT}}-background-start NAME "text"     type text into the run, submit it, then attach
# Runs are started with tools/{{AGENT}}-background-start; ended with: python3 tools/agent-start.py kill NAME
set -euo pipefail
cd "$(dirname "$0")/.."

case $# in
    0) exec python3 tools/agent-start.py list ;;
    1) exec python3 tools/agent-start.py attach "$1" ;;
    2) python3 tools/agent-start.py send "$1" "$2"
       exec python3 tools/agent-start.py attach "$1" ;;
    *) echo "Usage: tools/{{AGENT}}-background-start [NAME ["text"]]" >&2; exit 2 ;;
esac
