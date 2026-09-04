# {{AGENT}}-background-start.ps1 - attach to a running {{LABEL}} session, or list the runs.
#
# Usage:
#   tools\{{AGENT}}-background-start.ps1                 list the runs in progress
#   tools\{{AGENT}}-background-start.ps1 NAME            attach to the run (detach again: Ctrl+b, then d)
#   tools\{{AGENT}}-background-start.ps1 NAME "text"     type text into the run, submit it, then attach
# Runs are started with tools\{{AGENT}}-background-start.ps1; ended with: python tools\agent-start.py kill NAME
Set-Location (Join-Path $PSScriptRoot "..")
if ($args.Count -gt 2) { [Console]::Error.WriteLine("Usage: tools\{{AGENT}}-background-start.ps1 [NAME ['text']]"); exit 2 }
$ErrorActionPreference = "Stop"   # a missing python must fail loudly, not exit 0

switch ($args.Count) {
    0 { & python tools\agent-start.py list; exit $LASTEXITCODE }
    1 { & python tools\agent-start.py attach $args[0]; exit $LASTEXITCODE }
    2 { & python tools\agent-start.py send $args[0] $args[1]
         if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
         & python tools\agent-start.py attach $args[0]; exit $LASTEXITCODE }
}
