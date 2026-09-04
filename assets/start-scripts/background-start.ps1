# {{AGENT}}-background-start.ps1 - start {{LABEL}} in the background, no questions asked.
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
# The flags live in tools\agent-start.py (one table for all agents) - fix them THERE
# if {{LABEL}} changes its CLI, then regenerate or edit this header.
#
# Usage:
#   tools\{{AGENT}}-background-start.ps1 "task text" [--name NAME] [--model M] [--attach] [--dry-run] [--no-trust]
#   tools\{{AGENT}}-background-start.ps1 -f task.md   [--name NAME] [--model M] [--attach] [--dry-run] [--no-trust]
# Afterwards:  tools\{{AGENT}}-attach.ps1 [NAME]     (watch, steer, or list the runs)
Set-Location (Join-Path $PSScriptRoot "..")

# Usage errors exit 2 (printed to stderr) before $ErrorActionPreference = "Stop" would turn
# them into exit 1.
if ($args.Count -eq 0) {
    # The header is the contiguous comment block at the top; stop at the first other line.
    foreach ($line in Get-Content $PSCommandPath) {
        if ($line -notmatch '^#') { break }
        $line -replace '^# ?', ''
    }
    exit 2
}
if (-not (Get-Command psmux -ErrorAction SilentlyContinue)) {
    [Console]::Error.WriteLine("psmux is not installed - the run would have no session to attach to. Install psmux ({{INSTALL_HINT}}) or start headless: python tools\agent-start.py start --agent {{AGENT}} --headless --prompt '...'")
    exit 2
}

# Split off the task argument; the rest is passed through. The last valid index of $args
# is Count-1, and a range past it is an error - hence the guards.
$pass = @()
$rest = @()
if ($args[0] -eq "-f") {
    if ($args.Count -lt 2) { [Console]::Error.WriteLine("-f needs a file"); exit 2 }
    $pass = @("--prompt-file", $args[1])
    if ($args.Count -gt 2) { $rest = $args[2..($args.Count - 1)] }
} elseif ($args[0] -notlike "-*") {
    $pass = @("--prompt", $args[0])
    if ($args.Count -gt 1) { $rest = $args[1..($args.Count - 1)] }
} else {
    $rest = $args
}
$ErrorActionPreference = "Stop"
& python tools\agent-start.py start --agent {{AGENT}} @pass @rest
exit $LASTEXITCODE
